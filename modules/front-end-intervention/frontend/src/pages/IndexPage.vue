<template>
  <q-page class="row fit flex justify-center items-center" style="background-color: #1D1D1D;">
    <div class="col column fit " 
          style="width: 100%; 
                  max-width: 750px;
                  border-left: 1px solid #222;
                  border-right: 1px solid #222;
                  border-bottom: 1px solid #222;
                  border-top: none;
                  border-radius: 5px;
                  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                  padding-left: 20px;
                  padding-right: 20px;
                  padding-top: 8px;
                  margin-top:1px;  background-color: #252525;" >
      <chat-window></chat-window>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import ChatWindow from 'src/components/ChatWindow.vue';
</script>
