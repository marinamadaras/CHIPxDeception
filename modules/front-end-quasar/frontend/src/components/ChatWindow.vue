<template>
  <div
    class="col-11 q-pa-md"
    ref="messagesDiv"
    style="overflow-y: scroll; overflow-x: hidden"
  >
    <q-chat-message
      v-for="item in messageStore.messages"
      :key="item.message"
      :text="[item.message]"
      :sent="item.user?.human"
      :name="item.user?.name"
    />
    <q-chat-message
        :name="botUser?.name"
        :sent="botUser?.human"
        v-if="waiting"
      >
        <q-spinner-dots size="2rem" />
      </q-chat-message>
  </div>

  <q-input
    filled
    bottom-slots
    v-model="text"
    label="Label"
    dense
    @keyup.enter="submit"
    class="col-1 q-mr-md"
  >
    <template v-slot:before>
      <q-avatar icon="account_circle" />
    </template>
    <template v-slot:after>
      <q-btn round dense flat icon="send" @click="submit" />
    </template>
  </q-input>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted, onUnmounted } from 'vue';
import { useMessageStore } from 'src/stores/message-store';
import { useUserStore } from 'src/stores/user-store';

const emit = defineEmits(['reloadVisualization']);

const messageStore = useMessageStore();
const userStore = useUserStore();

// Set user for now, later on I suppose it can come from login/etc
userStore.user = { name: 'John', human: true };
const botUser = { name: 'Bot', human: false };

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
