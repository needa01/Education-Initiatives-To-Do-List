# Memento Pattern: Create a TaskMemento class to store the state of a task.
class TaskMemento:
    def __init__(self, description, due_date, completed):
        self.description = description
        self.due_date = due_date
        self.completed = completed

# Builder Pattern: Create a TaskBuilder class for constructing tasks.
class TaskBuilder:
    def __init__(self, description):
        self.description = description
        self.due_date = None
        self.completed = False

    def with_due_date(self, due_date):
        self.due_date = due_date
        return self

    def with_completed(self, completed):
        self.completed = completed
        return self

    def build(self):
        return Task(self.description, self.due_date, self.completed)

# Encapsulation: Create a Task class to encapsulate task data and methods.
class Task:
    def __init__(self, description, due_date, completed):
        self.description = description
        self.due_date = due_date
        self.completed = completed

    def mark_completed(self):
        self.completed = True

    def mark_pending(self):
        self.completed = False

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        return f"{self.description} - {status}, Due: {self.due_date}"

# To-Do List Manager
class ToDoListManager:
    def __init__(self):
        self.tasks = []
        self.undo_stack = []
        self.redo_stack = []

    def add_task(self, task):
        self.tasks.append(task)
        self.undo_stack.append(TaskMemento(task.description, task.due_date, task.completed))
        self.redo_stack.clear()

    def mark_completed(self, task_description):
        for task in self.tasks:
            if task.description == task_description:
                task.mark_completed()
                self.undo_stack.append(TaskMemento(task.description, task.due_date, task.completed))
                self.redo_stack.clear()
                return

    def delete_task(self, task_description):
        for task in self.tasks:
            if task.description == task_description:
                self.tasks.remove(task)
                self.undo_stack.append(None)  # Mark for undo
                self.redo_stack.clear()
                return

    def undo(self):
        if self.undo_stack:
            memento = self.undo_stack.pop()
            if memento:
                task = TaskBuilder(memento.description).with_due_date(memento.due_date).with_completed(not(memento.completed)).build()
                self.delete_task(memento.description)
                self.tasks.append(task)
                self.redo_stack.append(TaskMemento(task.description, task.due_date, not(task.completed)))
            else:
                self.tasks.pop()
                self.redo_stack.append(None)

    def redo(self):
        if self.redo_stack:
            memento = self.redo_stack.pop()
            if memento:
                task = TaskBuilder(memento.description).with_due_date(memento.due_date).with_completed(memento.completed).build()
                self.delete_task(memento.description)
                self.tasks.append(task)
                self.undo_stack.append(TaskMemento(task.description, task.due_date, task.completed))
            else:
                self.tasks.pop()
                self.undo_stack.append(None)

    def view_tasks(self, filter_type="all"):
        if filter_type == "completed":
            return [str(task) for task in self.tasks if task.completed]
        elif filter_type == "pending":
            return [str(task) for task in self.tasks if not task.completed]
        else:
            return [str(task) for task in self.tasks]

# Example usage:
if __name__ == "__main__":
    manager = ToDoListManager()

    task1 = TaskBuilder("Buy groceries").with_due_date("2023-09-20").build()
    task2 = TaskBuilder("Finish report").build()
    task3 = TaskBuilder("Call mom").build()

    manager.add_task(task1)
    manager.add_task(task2)
    manager.add_task(task3)

    manager.mark_completed("Buy groceries")

    print("All Tasks:")
    print(manager.view_tasks("all"))

    manager.undo()

    print("\nAfter Undo:")
    print(manager.view_tasks("all"))

    manager.redo()

    print("\nAfter Redo:")
    print(manager.view_tasks("all"))

    manager.delete_task("Call mom")

    print("\nAfter Deleting 'Call mom':")
    print(manager.view_tasks("all"))
