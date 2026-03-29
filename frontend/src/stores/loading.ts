import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLoadingStore = defineStore('loading', () => {
  const isLoading = ref(false)
  const message = ref('Carregando...')

  function setLoading(value: boolean, msg: string = 'Carregando...') {
    isLoading.value = value
    message.value = msg
  }

  function startLoading(msg: string = 'Carregando...') {
    isLoading.value = true
    message.value = msg
  }

  function stopLoading() {
    isLoading.value = false
  }

  return {
    isLoading,
    message,
    setLoading,
    startLoading,
    stopLoading
  }
})
