class Task:
    def __init__(self, description, priority, completed=False):
        self.description = description
        self.priority = priority  # High, Medium, Low
        self.completed = completed
        self.next = None  # للإشارة إلى المهمة التالية في القائمة المتصلة

class TaskLinkedList:
    def __init__(self):
        self.head = None  # رأس القائمة المتصلة

    def add_task(self, description, priority):
        new_task = Task(description, priority)
        if not self.head:
            self.head = new_task
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_task  # إضافة المهمة في نهاية القائمة

    def delete_task(self, description):
        current = self.head
        prev = None
        while current:
            if current.description == description:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next
        return False  # إذا لم يتم العثور على المهمة

    def display_tasks(self):
        tasks = []
        current = self.head
        while current:
            tasks.append((current.description, current.priority, current.completed))
            current = current.next
        return tasks

class TaskHashTable:
    def __init__(self):
        self.table = {}

    def add_task(self, task):
        self.table[task.description] = task  # تخزين المهمة باستخدام الوصف كمفتاح

    def search_task(self, description):
        return self.table.get(description, None)  # البحث عن المهمة

    def delete_task(self, description):
        if description in self.table:
            del self.table[description]
            return True
        return False

class BSTNode:
    def __init__(self, task):
        self.task = task
        self.left = None
        self.right = None

class TaskBST:
    def __init__(self):
        self.root = None

    def insert(self, task):
        if not self.root:
            self.root = BSTNode(task)
        else:
            self._insert(self.root, task)

    def _insert(self, node, task):
        if task.priority < node.task.priority:  # فرز المهام حسب الأولوية
            if node.left is None:
                node.left = BSTNode(task)
            else:
                self._insert(node.left, task)
        else:
            if node.right is None:
                node.right = BSTNode(task)
            else:
                self._insert(node.right, task)

    def inorder_traversal(self):
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, node, result):
        if node:
            self._inorder_traversal(node.left, result)
            result.append((node.task.description, node.task.priority, node.task.completed))
            self._inorder_traversal(node.right, result)

import tkinter as tk
from tkinter import messagebox

class ToDoApp:
    def __init__(self, main_root):
        self.root = main_root
        self.root.title("To-Do List App")

        self.task_list = TaskLinkedList()
        self.task_table = TaskHashTable()
        self.task_tree = TaskBST()

        # إدخال وصف المهمة
        tk.Label(root, text="Task Description:").grid(row=0, column=0)
        self.task_entry = tk.Entry(root)
        self.task_entry.grid(row=0, column=1)

        # إدخال مستوى الأولوية
        tk.Label(root, text="Priority:").grid(row=1, column=0)
        self.priority_var = tk.StringVar()
        self.priority_var.set("Medium")
        tk.OptionMenu(root, self.priority_var, "High", "Medium", "Low").grid(row=1, column=1)

        # زر إضافة المهمة
        tk.Button(root, text="Add Task", command=self.add_task).grid(row=2, column=0, columnspan=2)

        # زر حذف المهمة
        tk.Button(root, text="Delete Task", command=self.delete_task).grid(row=3, column=0, columnspan=2)

        # زر عرض جميع المهام
        tk.Button(root, text="Show Tasks", command=self.display_tasks).grid(row=4, column=0, columnspan=2)

        # قائمة عرض المهام
        self.task_listbox = tk.Listbox(root, width=50)
        self.task_listbox.grid(row=5, column=0, columnspan=2)

    def add_task(self):
        description = self.task_entry.get()
        priority = self.priority_var.get()

        if description:
            new_task = Task(description, priority)
            self.task_list.add_task(description, priority)
            self.task_table.add_task(new_task)
            self.task_tree.insert(new_task)
            self.task_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Task added successfully!")
        else:
            messagebox.showwarning("Input Error", "Please enter a task description.")

    def delete_task(self):
        selected_task = self.task_listbox.get(tk.ACTIVE)
        if selected_task:
            task_description = selected_task.split(" - ")[0]
            if self.task_list.delete_task(task_description):
                self.task_table.delete_task(task_description)
                self.display_tasks()
                messagebox.showinfo("Success", "Task deleted successfully!")
            else:
                messagebox.showerror("Error", "Task not found.")
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def display_tasks(self):
        self.task_listbox.delete(0, tk.END)
        tasks = self.task_list.display_tasks()
        for task in tasks:
            status = " - Completed" if task[2] else ""
            self.task_listbox.insert(tk.END, f"{task[0]} - {task[1]}{status}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()