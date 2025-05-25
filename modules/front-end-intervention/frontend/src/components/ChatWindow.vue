<template>
  <!-- <div> -->
  <div
    class="col-11  q-pa-md"
    ref="messagesDiv"
    style="overflow-y: scroll; overflow-x: hidden;  background-color: #FDFCFA;"
  >
    <q-chat-message
      v-for="item in messageStore.messages"
      :key="item.message"
      :sent="item.user?.human"
      :name="item.user?.name"
      :bg-color="item.user?.human ? 'grey-3' : 'light-blue-11'"
      > 
      <template v-slot:name>
        <span class="text-grey-9" style =  "font-family: 'Trebuchet MS'; font-size: 12px">{{ item.user?.name }}</span>
      </template>
      <template v-slot:default >
          <div class="text-blue-grey-10" style="max-width: 450px; width: fit-content; font-family: 'Trebuchet MS'">
            <q-message-text >
              {{ item.message }}
            </q-message-text>
          </div>
      </template>
    </q-chat-message>

   
    
    <q-chat-message
        :name="botUser?.name"
        :sent="botUser?.human"
        v-if="waiting"
        bg-color="light-blue-11"
        class = "text-blue-grey-9"
      >
        <q-spinner-dots size="2rem" />
      </q-chat-message>
  </div>

  <!-- Input -->
  <div class="col-1">
      <q-input
        filled
        bottom-slots
        v-model="text"
        label="Type your message"
        dense
        @keyup.enter="submit"
        dark
        color="light-blue-3"
        bg-color="brown-1"
        style="margin-top: 7px;font-family: 'Trebuchet MS' "
        input-class="text-grey-9"
        input-style="padding-top: 1.5em; padding-bottom:0.5em; font-family: 'Trebuchet MS'"
        label-color="grey-6" 
      >
        <template v-slot:before>
          <q-avatar icon="account_circle" color="light-blue-3" text-color="grey-1" />
        </template>
        <template v-slot:after>
          <q-btn round dense flat icon="send" @click="submit" color="light-blue-5" />
        </template>
      </q-input>
    </div>
  <!-- </div> -->
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted, onUnmounted } from 'vue';
import { useMessageStore } from 'src/stores/message-store';
import { useUserStore } from 'src/stores/user-store';

const emit = defineEmits(['reloadVisualization']);

const messageStore = useMessageStore();
const userStore = useUserStore();

// Set user for now, later on I suppose it can come from login/etc
userStore.user = { name: 'Oscar', human: true };
const botUser = { name: 'Chip', human: false };

const text = ref('');
var waiting = false;

async function submit() {
  if (text.value) {
    var timestamp = new Date().toISOString();
    messageStore.addMessage({ message: text.value, user: userStore.user, timestamp: timestamp });

    // Send message to backend
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        patient_name: userStore.user?.name,
        sentence: text.value,
        timestamp: timestamp
      }),
    };

    text.value = '';
    fetch('/api/submit', requestOptions).then((response) => {
      console.log(response);
    }
    );
    waiting = true;

    scrollToBottom();
    emit('reloadVisualization');
  }
}

async function scrollToBottom() {
  await nextTick();
  if (messagesDiv.value) {
    messagesDiv.value.scrollTop = messagesDiv.value.scrollHeight;
  }
}

const messagesDiv = ref<HTMLDivElement | null>(null);

var source: EventSource;
onMounted(() => {
  source = new EventSource('/api/stream');
  source.addEventListener(
    'response',
    function (event) {
      var data = JSON.parse(event.data);
      messageStore.addMessage({
        message: data.message,
        user: botUser,
        timestamp: new Date().toISOString()
      });
      waiting = false;
      scrollToBottom();
      console.log(`Received response: ${data.message}`);
    },
    false,
  );
});

onUnmounted(() => {
  source?.close();
});
</script>
