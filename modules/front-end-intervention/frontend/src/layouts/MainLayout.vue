<template>
  <q-layout view="hHh Lpr lFf" class="fullscreen">
    <q-header style="box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2); background-color: #faf9f5; position: absolute; top: 0; left: 0; right: 0; z-index: 10;">
      <q-toolbar>
        <q-toolbar-title class="text-center  text-grey-4 text-h5" 
                         style="font-family: 'Verdana', serif; text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.4); "> 
          <img src="../../src/assets/chip-high-resolution-logo-4.png" alt="CHIP Logo" style="height: 30px; margin-top: 5px;" />
        </q-toolbar-title>
      </q-toolbar>
    </q-header>
    <q-page-container class="fit">
      <router-view />
    </q-page-container>
  </q-layout>
</template>