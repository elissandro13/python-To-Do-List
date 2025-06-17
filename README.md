# 📋 Sistema de Gerenciamento de Tarefas

Este projeto foi desenvolvido para a **Aula Prática 5 - GitHub Actions**, implementando um sistema completo de gerenciamento de tarefas (To-Do List) com testes em múltiplos sistemas operacionais e versões de linguagem.

## 🎯 Funcionalidades

### 📝 Gerenciamento de Tarefas
- ➕ **Criar tarefas** com título, descrição e prioridade
- ✅ **Marcar como concluída**
- 🗑️ **Remover tarefas**
- 📅 **Definir prazos** (due dates)
- 🔍 **Buscar tarefas** por título ou descrição

### 📊 Organização e Relatórios
- 🎯 **Filtrar por prioridade** (Alta, Média, Baixa)
- ⚠️ **Identificar tarefas atrasadas**
- 📈 **Estatísticas completas** (total, pendentes, concluídas, atrasadas)
- 📤 **Exportar para JSON**

### 🔧 Funcionalidades Avançadas
- 🕒 **Controle de datas** (criação, conclusão, prazo)
- 🎨 **Sistema de prioridades** com enum
- 🔍 **Busca inteligente** por texto
- 📊 **Relatórios detalhados**

## 🧪 Testes Implementados

O projeto inclui **10 testes unitários** abrangentes:

### Testes da Classe Task
1. **test_task_creation**: Criação correta de tarefas
2. **test_mark_completed**: Marcação como concluída
3. **test_is_overdue**: Verificação de tarefas atrasadas

### Testes da Classe TaskManager
4. **test_add_task_valid**: Adição de tarefas válidas
5. **test_add_task_empty_title**: Tratamento de títulos vazios
6. **test_complete_and_remove_task**: Completar e remover tarefas
7. **test_get_tasks_by_status**: Filtros por status
8. **test_search_and_priority_filter**: Busca e filtros
9. **test_task_count_statistics**: Estatísticas de contagem
10. **test_export_to_json**: Exportação para JSON

## 🖥️ Sistemas Operacionais Testados

O GitHub Actions executa os testes em:
- 🐧 **Ubuntu** (ubuntu-latest)
- 🪟 **Windows** (windows-latest)  
- 🍎 **macOS** (macos-latest)

## 🐍 Versões do Python Testadas

Os testes são executados nas seguintes versões:
- **Python 3.9**
- **Python 3.11**

## 🚀 Como Executar Localmente

### Pré-requisitos
- Python 3.9 ou superior

### Executar o programa:
```bash
python task_manager.py
```

### Executar os testes:
```bash
python -m unittest test_task_manager.py -v
```
## 📁 Estrutura do Projeto

```
.
├── .github/
│   └── workflows/
│       └── ci.yml              # Configuração GitHub Actions
├── task_manager.py             # Sistema principal
├── test_task_manager.py        # Testes unitários
├── requirements.txt            # Dependências
└── README.md                   # Documentação
```

## ⚙️ Configuração do GitHub Actions

O workflow `.github/workflows/ci.yml` executa:

1. **Setup** multi-plataforma (Ubuntu, Windows, macOS)
2. **Configuração** Python (versões 3.9 e 3.11)
3. **Instalação** de dependências
4. **Execução** de 10 testes unitários
5. **Execução** do programa principal
6. **Verificação** de sintaxe Python
