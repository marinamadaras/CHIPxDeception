<template>
  <q-page class="row fit">
    <div class="col column fit">
      <example-component
        @reloadVisualization="reloadVisualization"
      ></example-component>
    </div>
    <div class="col column">
      <div class="fit" style="background: grey">
        <iframe
          ref="visualizationFrame"
          class="fit"
          src="/kgraph/graphs-visualizations?uri=http:%2F%2Fwww.semanticweb.org%2Faledpro%2Fontologies%2F2024%2F2%2FuserKG%23John_work&embedded"
          title="description"
        ></iframe>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
// import { ref } from 'vue';
// import type { Todo, Meta } from 'components/models';
import ExampleComponent from 'components/ExampleComponent.vue';
import { ref } from 'vue';

function reloadVisualization() {
  visualizationFrame.value?.contentWindow?.location?.reload();
}

const visualizationFrame = ref<HTMLIFrameElement | null>(null);

// const todos = ref<Todo[]>([
//   {
//     id: 1,
//     content: 'ct1'
//   },
//   {
//     id: 2,
//     content: 'ct2'
//   },
//   {
//     id: 3,
//     content: 'ct3'
//   },
//   {
//     id: 4,
//     content: 'ct4'
//   },
//   {
//     id: 5,
//     content: 'ct5'
//   }
// ]);

// const meta = ref<Meta>({
//   totalCount: 1200,
// });
</script>
