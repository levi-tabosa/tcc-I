<script setup lang="ts">
// Não precisamos mais importar nenhum componente de página aqui!
// O roteador cuidará disso.
</script>

<template>
  <!-- 
    Pense no <router-view /> como um "espaço reservado" mágico.
    O Vue Router irá automaticamente colocar o componente da rota atual aqui.
    - Se a URL for "/", ele coloca <Home.vue> aqui.
    - Se a URL for "/perfil/204554", ele coloca <Perfil.vue> aqui.
  -->
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
