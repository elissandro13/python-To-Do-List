"""
Sistema de Gerenciamento de Tarefas (To-Do List)
Permite criar, listar, marcar como concluída e remover tarefas
"""

from datetime import datetime, timedelta
from enum import Enum
import json

class Priority(Enum):
    """Enum para prioridades das tarefas"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Task:
    """Classe que representa uma tarefa"""
    
    def __init__(self, title, description="", priority=Priority.MEDIUM, due_date=None):
        self.id = None
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = False
        self.created_at = datetime.now()
        self.completed_at = None
    
    def mark_completed(self):
        """Marca a tarefa como concluída"""
        self.completed = True
        self.completed_at = datetime.now()
    
    def is_overdue(self):
        """Verifica se a tarefa está atrasada"""
        if self.due_date and not self.completed:
            return datetime.now() > self.due_date
        return False
    
    def days_until_due(self):
        """Calcula quantos dias restam até o prazo"""
        if self.due_date and not self.completed:
            delta = self.due_date - datetime.now()
            return delta.days
        return None
    
    def to_dict(self):
        """Converte a tarefa para dicionário"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority.value,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class TaskManager:
    """Classe principal para gerenciar tarefas"""
    
    def __init__(self):
        self.tasks = []
        self.next_id = 1
    
    def add_task(self, title, description="", priority=Priority.MEDIUM, due_date=None):
        """Adiciona uma nova tarefa"""
        if not title.strip():
            raise ValueError("Título da tarefa não pode estar vazio")
        
        task = Task(title, description, priority, due_date)
        task.id = self.next_id
        self.tasks.append(task)
        self.next_id += 1
        return task
    
    def get_task_by_id(self, task_id):
        """Busca uma tarefa pelo ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def complete_task(self, task_id):
        """Marca uma tarefa como concluída"""
        task = self.get_task_by_id(task_id)
        if task:
            task.mark_completed()
            return True
        return False
    
    def remove_task(self, task_id):
        """Remove uma tarefa"""
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False
    
    def get_pending_tasks(self):
        """Retorna tarefas pendentes"""
        return [task for task in self.tasks if not task.completed]
    
    def get_completed_tasks(self):
        """Retorna tarefas concluídas"""
        return [task for task in self.tasks if task.completed]
    
    def get_overdue_tasks(self):
        """Retorna tarefas atrasadas"""
        return [task for task in self.tasks if task.is_overdue()]
    
    def get_tasks_by_priority(self, priority):
        """Retorna tarefas por prioridade"""
        return [task for task in self.tasks if task.priority == priority and not task.completed]
    
    def get_task_count(self):
        """Retorna contagem de tarefas"""
        total = len(self.tasks)
        completed = len(self.get_completed_tasks())
        pending = len(self.get_pending_tasks())
        overdue = len(self.get_overdue_tasks())
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'overdue': overdue
        }
    
    def search_tasks(self, query):
        """Busca tarefas por título ou descrição"""
        query = query.lower()
        results = []
        for task in self.tasks:
            if (query in task.title.lower() or 
                query in task.description.lower()):
                results.append(task)
        return results
    
    def export_to_json(self):
        """Exporta tarefas para JSON"""
        data = {
            'tasks': [task.to_dict() for task in self.tasks],
            'export_date': datetime.now().isoformat()
        }
        return json.dumps(data, indent=2)

def main():
    """Função principal para demonstrar o sistema"""
    print("=== Sistema de Gerenciamento de Tarefas ===\n")
    
    # Criar o gerenciador
    manager = TaskManager()
    
    # Adicionar algumas tarefas de exemplo
    manager.add_task(
        "Estudar Python",
        "Revisar conceitos de POO e testes unitarios",
        Priority.HIGH,
        datetime.now() + timedelta(days=3)
    )
    
    manager.add_task(
        "Fazer compras",
        "Comprar ingredientes para o jantar",
        Priority.MEDIUM,
        datetime.now() + timedelta(days=1)
    )
    
    manager.add_task(
        "Exercitar-se",
        "Ir a academia ou fazer uma caminhada",
        Priority.LOW,
        datetime.now() + timedelta(days=2)
    )
    
    # Adicionar uma tarefa atrasada para demonstração
    overdue_task = manager.add_task(
        "Tarefa Atrasada",
        "Esta tarefa esta com prazo vencido",
        Priority.HIGH,
        datetime.now() - timedelta(days=1)
    )
    
    # Completar uma tarefa
    manager.complete_task(2)
    
    # Mostrar estatísticas
    stats = manager.get_task_count()
    print("ESTATISTICAS:")
    print(f"   Total: {stats['total']}")
    print(f"   Pendentes: {stats['pending']}")
    print(f"   Concluidas: {stats['completed']}")
    print(f"   Atrasadas: {stats['overdue']}\n")
    
    # Mostrar tarefas pendentes
    print("TAREFAS PENDENTES:")
    for task in manager.get_pending_tasks():
        status = "ATRASADA" if task.is_overdue() else "No prazo"
        priority_symbol = "[ALTA]" if task.priority == Priority.HIGH else "[MEDIA]" if task.priority == Priority.MEDIUM else "[BAIXA]"
        print(f"   {priority_symbol} [{task.id}] {task.title} - {status}")
        if task.description:
            print(f"      Descricao: {task.description}")
        if task.due_date:
            print(f"      Prazo: {task.due_date.strftime('%d/%m/%Y')}")
        print()
    
    # Mostrar tarefas concluídas
    print("TAREFAS CONCLUIDAS:")
    for task in manager.get_completed_tasks():
        print(f"   [{task.id}] {task.title}")
        if task.completed_at:
            print(f"      Concluida em: {task.completed_at.strftime('%d/%m/%Y %H:%M')}\n")
    
    # Demonstrar busca
    print("BUSCA por 'python':")
    results = manager.search_tasks("python")
    for task in results:
        print(f"   [{task.id}] {task.title}")
    
    print("\nSistema funcionando perfeitamente!")

if __name__ == "__main__":
    main()