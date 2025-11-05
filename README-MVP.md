# Transparência BR - MVP

Sistema simples para consulta de dados de deputados federais.

## Sobre o MVP

Este é um **Minimum Viable Product (MVP)** focado na funcionalidade essencial: consultar dados básicos dos deputados federais brasileiros.

### Funcionalidades Core

✅ **Backend API (FastAPI)**
- Endpoints para buscar deputados
- Consulta por ID
- Conexão com PostgreSQL

✅ **Frontend (Vue.js)**
- **Página Inicial**: Busca simples + estatísticas básicas
- **Lista de Deputados**: Busca e listagem simples
- **Perfil Individual**: Dados básicos + gastos
- **Dashboard**: Estatísticas gerais + rankings

### O que foi simplificado para MVP

❌ **Removido**:
- Filtros complexos (partido, estado)
- Ordenação avançada
- Gráficos elaborados
- Comparação entre deputados
- Páginas de metodologia/contato
- Designs complexos com múltiplas animações
- Menu mobile elaborado

✅ **Mantido** (Essencial):
- Busca por nome
- Dados básicos dos deputados
- Gastos e presença
- Interface limpa e responsiva
- API funcional

## Estrutura MVP

```
backend/
├── main.py                 # FastAPI app
├── api/deputados/router.py # Endpoints dos deputados  
└── database/db.py          # Conexão PostgreSQL

frontend/
├── src/
│   ├── views/
│   │   ├── Home.vue        # Página inicial simplificada
│   │   ├── Parlamentares.vue # Lista simples
│   │   ├── Perfil.vue      # Perfil básico
│   │   └── Dashboard.vue   # Stats básicas
│   ├── components/
│   │   └── AppHeader.vue   # Header minimalista
│   └── assets/
│       └── main-mvp.css    # Estilos simples
```

## Executar MVP

### Backend
```bash
cd backend
pip install fastapi uvicorn psycopg2-binary python-dotenv
uvicorn main:app --reload
```

### Frontend  
```bash
cd frontend
npm install
npm run dev
```

## Características MVP

**🎯 Foco**: Transparência parlamentar básica  
**👥 Usuário**: Qualquer pessoa querendo consultar dados de deputados  
**📱 Interface**: Simples, responsiva, sem complexidade desnecessária  
**⚡ Performance**: Rápido e direto ao ponto  
**🔧 Manutenção**: Código simples e fácil de manter  

## Próximos Passos (Pós-MVP)

1. **Filtros avançados** (partido, estado, faixa de gastos)
2. **Gráficos interativos** (ECharts)
3. **Comparação entre deputados**
4. **Exportação de dados**
5. **Sistema de favoritos**
6. **Notificações de novos gastos**

---

**Este MVP valida a ideia core**: permitir que cidadãos consultem dados básicos de deputados de forma simples e acessível.