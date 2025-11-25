<script setup lang="ts">
import AppHeader from '@/components/AppHeader.vue'
</script>

<template>
  <AppHeader />
  <router-view />
</template>

<style>
/* 
  É uma boa prática remover o "scoped" do style no App.vue
  para que você possa definir estilos globais para toda a sua aplicação aqui.
*/
body {
  margin: 0;
  font-family: sans-serif;
  background-color: #f8fafc;
}
</style>
