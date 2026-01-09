import { ref } from 'vue'

type Theme = 'light'

// Estado global do tema (agora fixo em light)
const theme = ref<Theme>('light')

export function useTheme() {
  // Mantemos as funções para evitar quebra de contrato, mas elas não fazem nada
  const applyTheme = () => {
    document.documentElement.classList.remove('dark')
  }

  const toggleTheme = () => {
    // Não faz nada
  }

  const setTheme = () => {
    // Não faz nada
  }

  const initTheme = () => {
    applyTheme()
  }

  return {
    theme,
    toggleTheme,
    setTheme,
    initTheme
  }
}
