"""
Testes unitários para o Sistema de Gerenciamento de Tarefas
"""

import unittest
from datetime import datetime, timedelta
from task_manager import TaskManager, Task, Priority

class TestTask(unittest.TestCase):
    """Testes para a classe Task"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.task = Task("Tarefa Teste", "Descrição teste", Priority.HIGH)
    
    def test_task_creation(self):
        """Teste 1: Criação de tarefa"""
        self.assertEqual(self.task.title, "Tarefa Teste")
        self.assertEqual(self.task.description, "Descrição teste")
        self.assertEqual(self.task.priority, Priority.HIGH)
        self.assertFalse(self.task.completed)
        self.assertIsNone(self.task.completed_at)
        self.assertIsNotNone(self.task.created_at)
    
    def test_mark_completed(self):
        """Teste 2: Marcar tarefa como concluída"""
        self.assertFalse(self.task.completed)
        self.task.mark_completed()
        self.assertTrue(self.task.completed)
        self.assertIsNotNone(self.task.completed_at)
    
    def test_is_overdue(self):
        """Teste 3: Verificar se tarefa está atrasada"""
        # Tarefa sem prazo não pode estar atrasada
        self.assertFalse(self.task.is_overdue())
        
        # Tarefa com prazo futuro não está atrasada
        future_task = Task("Futura", due_date=datetime.now() + timedelta(days=1))
        self.assertFalse(future_task.is_overdue())
        
        # Tarefa com prazo passado está atrasada
        overdue_task = Task("Atrasada", due_date=datetime.now() - timedelta(days=1))
        self.assertTrue(overdue_task.is_overdue())
        
        # Tarefa concluída não está atrasada mesmo com prazo passado
        overdue_task.mark_completed()
        self.assertFalse(overdue_task.is_overdue())

class TestTaskManager(unittest.TestCase):
    """Testes para a classe TaskManager"""
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.manager = TaskManager()
    
    def test_add_task_valid(self):
        """Teste 4: Adicionar tarefa válida"""
        task = self.manager.add_task("Nova Tarefa", "Descrição", Priority.MEDIUM)
        
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(task.title, "Nova Tarefa")
        self.assertEqual(task.id, 1)
        self.assertEqual(self.manager.next_id, 2)
    
    def test_add_task_empty_title(self):
        """Teste 5: Tentar adicionar tarefa com título vazio"""
        with self.assertRaises(ValueError):
            self.manager.add_task("")
        
        with self.assertRaises(ValueError):
            self.manager.add_task("   ")  # Apenas espaços
        
        # Lista deve permanecer vazia
        self.assertEqual(len(self.manager.tasks), 0)
    
    def test_complete_and_remove_task(self):
        """Teste 6: Completar e remover tarefas"""
        # Adicionar tarefas
        task1 = self.manager.add_task("Tarefa 1")
        task2 = self.manager.add_task("Tarefa 2")
        
        # Completar tarefa existente
        self.assertTrue(self.manager.complete_task(task1.id))
        self.assertTrue(task1.completed)
        
        # Tentar completar tarefa inexistente
        self.assertFalse(self.manager.complete_task(999))
        
        # Remover tarefa existente
        self.assertTrue(self.manager.remove_task(task2.id))
        self.assertEqual(len(self.manager.tasks), 1)
        
        # Tentar remover tarefa inexistente
        self.assertFalse(self.manager.remove_task(999))
    
    def test_get_tasks_by_status(self):
        """Teste 7: Obter tarefas por status"""
        # Adicionar tarefas
        task1 = self.manager.add_task("Pendente 1")
        task2 = self.manager.add_task("Pendente 2")
        task3 = self.manager.add_task("Completada", due_date=datetime.now() - timedelta(days=1))
        
        # Completar uma tarefa
        self.manager.complete_task(task3.id)
        
        # Verificar listas
        pending = self.manager.get_pending_tasks()
        completed = self.manager.get_completed_tasks()
        overdue = self.manager.get_overdue_tasks()
        
        self.assertEqual(len(pending), 2)
        self.assertEqual(len(completed), 1)
        self.assertEqual(len(overdue), 0)  # task3 foi completada, não está mais atrasada
        
        # Adicionar tarefa atrasada
        overdue_task = self.manager.add_task("Atrasada", due_date=datetime.now() - timedelta(days=2))
        overdue = self.manager.get_overdue_tasks()
        self.assertEqual(len(overdue), 1)
        self.assertEqual(overdue[0].id, overdue_task.id)
    
    def test_search_and_priority_filter(self):
        """Teste 8: Busca e filtro por prioridade"""
        # Adicionar tarefas variadas
        self.manager.add_task("Estudar Python", "Curso online", Priority.HIGH)
        self.manager.add_task("Comprar Python (livro)", "Livraria", Priority.LOW)
        self.manager.add_task("Fazer exercícios", "Academia", Priority.MEDIUM)
        
        # Testar busca
        results = self.manager.search_tasks("python")
        self.assertEqual(len(results), 2)
        
        results = self.manager.search_tasks("academia")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Fazer exercícios")
        
        # Testar filtro por prioridade
        high_priority = self.manager.get_tasks_by_priority(Priority.HIGH)
        self.assertEqual(len(high_priority), 1)
        self.assertEqual(high_priority[0].title, "Estudar Python")
        
        medium_priority = self.manager.get_tasks_by_priority(Priority.MEDIUM)
        self.assertEqual(len(medium_priority), 1)
    
    def test_task_count_statistics(self):
        """Teste 9: Estatísticas de contagem de tarefas"""
        # Estado inicial
        stats = self.manager.get_task_count()
        self.assertEqual(stats['total'], 0)
        self.assertEqual(stats['completed'], 0)
        self.assertEqual(stats['pending'], 0)
        self.assertEqual(stats['overdue'], 0)
        
        # Adicionar tarefas
        task1 = self.manager.add_task("Normal")
        task2 = self.manager.add_task("Atrasada", due_date=datetime.now() - timedelta(days=1))
        task3 = self.manager.add_task("Futura", due_date=datetime.now() + timedelta(days=1))
        
        # Completar uma tarefa
        self.manager.complete_task(task1.id)
        
        # Verificar estatísticas
        stats = self.manager.get_task_count()
        self.assertEqual(stats['total'], 3)
        self.assertEqual(stats['completed'], 1)
        self.assertEqual(stats['pending'], 2)
        self.assertEqual(stats['overdue'], 1)
    
    def test_export_to_json(self):
        """Teste 10: Exportar tarefas para JSON"""
        # Adicionar algumas tarefas
        self.manager.add_task("Tarefa 1", "Desc 1", Priority.HIGH)
        task2 = self.manager.add_task("Tarefa 2", "Desc 2", Priority.LOW)
        self.manager.complete_task(task2.id)
        
        # Exportar para JSON
        json_data = self.manager.export_to_json()
        
        # Verificar se é um JSON válido
        import json
        data = json.loads(json_data)
        
        self.assertIn('tasks', data)
        self.assertIn('export_date', data)
        self.assertEqual(len(data['tasks']), 2)
        
        # Verificar estrutura da primeira tarefa
        task_data = data['tasks'][0]
        expected_fields = ['id', 'title', 'description', 'priority', 'due_date', 
                          'completed', 'created_at', 'completed_at']
        for field in expected_fields:
            self.assertIn(field, task_data)

if __name__ == '__main__':
    # Executa os testes com verbose para mostrar detalhes
    unittest.main(verbosity=2)