<template>
  <!-- <div class="col fit"> -->
  <!-- <p>{{ title }}</p>
    <ul>
      <li v-for="todo in todos" :key="todo.id" @click="increment">
        {{ todo.id }} - {{ todo.content }}
      </li>
    </ul>
    <p>Count: {{ todoCount }} / {{ meta.totalCount }}</p>
    <p>Active: {{ active ? 'yes' : 'no' }}</p>
    <p>Clicks on todos: {{ clickCount }}</p> -->

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
  <!-- </div> -->
  <!-- <div style="background: red" class="col-8">dsgag</div>
  <div style="background: green" class="col-4">dsgag</div> -->
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted, onUnmounted } from 'vue';
// import type { ChatMessage } from './models';
import { useMessageStore } from 'src/stores/example-store';
import { useUserStore } from 'src/stores/user-store';

const emit = defineEmits(['reloadVisualization']);

const messageStore = useMessageStore();
const userStore = useUserStore();

// Set user for now, later on I suppose it can come from login/etc
userStore.user = { name: 'John', human: true };
const botUser = { name: 'Bot', human: false };

messageStore.addMessage({ message: 'Hello', user: userStore.user });
messageStore.addMessage({
  message: `Hello, ${userStore.user?.name}`,
  user: botUser,
});

const text = ref('');

async function submit() {
  if (text.value) {
    messageStore.addMessage({ message: text.value, user: userStore.user });

    // Send message to backend
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        patient_name: userStore.user?.name,
        sentence: text.value,
      }),
    };

    text.value = '';
    fetch('/api/submit', requestOptions).then((response) =>
      console.log(response),
    );

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
      });
      scrollToBottom();
      console.log(`Received response: ${data.message}`);
      // do what you want with this data
    },
    false,
  );
});

onUnmounted(() => {
  source?.close();
});

// interface Props {
//   title: string;
//   todos?: Todo[];
//   meta: Meta;
//   active: boolean;
// }

// const props = withDefaults(defineProps<Props>(), {
//   todos: () => [],
// });

// const props = defineProps<{
//   messages: string;
//   bar?: number;
// }>();

// const clickCount = ref(0);
// function increment() {
//   clickCount.value += 1;
//   return clickCount.value;
// }

// const todoCount = computed(() => props.todos.length);
</script>
