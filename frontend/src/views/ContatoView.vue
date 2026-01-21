<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

onMounted(() => {
  // Redireciona para a página inicial — contato foi removido
  router.replace('/')
})
</script>
