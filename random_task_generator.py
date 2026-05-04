import random
import json
import os
from tkinter import *
from tkinter import ttk, messagebox

history_file = "tasks_history.json"

default_tasks = [
    {"text": "Прочитать статью по Python", "type": "учёба"},
    {"text": "Сделать зарядку 15 минут", "type": "спорт"},
    {"text": "Закончить отчёт по работе", "type": "работа"},
    {"text": "Изучить новый фреймворк", "type": "учёба"},
    {"text": "Пробежка 5 км", "type": "спорт"},
    {"text": "Позвонить клиенту", "type": "работа"},
    {"text": "Посмотреть вебинар", "type": "учёба"},
    {"text": "Отжимания 30 раз", "type": "спорт"},
    {"text": "Составить план задач", "type": "работа"}
]

def load_history():
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_history():
    try:
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except:
        pass

history = load_history()
if not history:
    for task in random.sample(default_tasks, min(5, len(default_tasks))):
        history.append(task)

current_filter = "все"

def refresh_history_display():
    history_listbox.delete(0, END)
    
    if current_filter != "все":
        filtered_history = [task for task in history if task["type"] == current_filter]
    else:
        filtered_history = history
    
    for i, task in enumerate(reversed(filtered_history), 1):
        history_listbox.insert(END, f"{i}. {task['text']} [{task['type']}]")

def generate_random_task():
    global current_filter
    
    available_tasks = default_tasks.copy()
    user_tasks = [task for task in history if task not in default_tasks]
    available_tasks.extend(user_tasks)
    
    if current_filter != "все":
        filtered_tasks = [task for task in available_tasks if task["type"] == current_filter]
    else:
        filtered_tasks = available_tasks
    
    if not filtered_tasks:
        messagebox.showwarning("Нет задач", f"Нет задач типа '{current_filter}'. Добавьте новые задачи!")
        return
    
    selected_task = random.choice(filtered_tasks)
    history.append(selected_task)
    
    current_task_label.config(text=f"✨ Текущая задача: {selected_task['text']} (Тип: {selected_task['type']})", fg="green")
    
    refresh_history_display()
    save_history()

def apply_filter():
    global current_filter
    current_filter = filter_var.get()
    refresh_history_display()

def add_new_task():
    task_text = new_task_entry.get().strip()
    task_type = task_type_var.get()
    
    if not task_text:
        messagebox.showerror("Ошибка", "Описание задачи не может быть пустым!")
        return
    
    for task in history:
        if task["text"].lower() == task_text.lower() and task["type"] == task_type:
            messagebox.showwarning("Предупреждение", "Такая задача уже существует в истории!")
            return
    
    new_task = {"text": task_text, "type": task_type}
    history.append(new_task)
    new_task_entry.delete(0, END)
    
    refresh_history_display()
    save_history()
    messagebox.showinfo("Успех", f"Задача '{task_text}' добавлена!")

def clear_history():
    if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
        global history
        history = default_tasks.copy()
        random.shuffle(history)
        history = history[:5]
        
        refresh_history_display()
        save_history()
        current_task_label.config(text="История очищена!", fg="gray")

def export_history():
    try:
        export_file = "tasks_export.json"
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Успех", f"История экспортирована в {export_file}")
    except:
        messagebox.showerror("Ошибка", "Не удалось экспортировать")

root = Tk()
root.title("Random Task Generator")
root.geometry("600x550")
root.resizable(True, True)

gen_frame = LabelFrame(root, text="Генерация задачи", padx=10, pady=10)
gen_frame.pack(fill="x", padx=10, pady=5)

generate_btn = Button(gen_frame, text="🎲 Сгенерировать случайную задачу", command=generate_random_task, bg="lightblue", font=("Arial", 12, "bold"))
generate_btn.pack(pady=5)

current_task_label = Label(gen_frame, text="Нажмите кнопку для генерации", font=("Arial", 11), wraplength=550)
current_task_label.pack(pady=5)

filter_frame = LabelFrame(root, text="Фильтрация по типу", padx=10, pady=10)
filter_frame.pack(fill="x", padx=10, pady=5)

filter_var = StringVar(value="все")

filters = [("Все", "все"), ("Учёба", "учёба"), ("Спорт", "спорт"), ("Работа", "работа")]
for text, value in filters:
    Radiobutton(filter_frame, text=text, variable=filter_var, value=value, command=apply_filter).pack(side="left", padx=10)

add_frame = LabelFrame(root, text="Добавить новую задачу", padx=10, pady=10)
add_frame.pack(fill="x", padx=10, pady=5)

Label(add_frame, text="Описание:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
new_task_entry = Entry(add_frame, width=35)
new_task_entry.grid(row=0, column=1, padx=5, pady=5)

Label(add_frame, text="Тип:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
task_type_var = StringVar(value="учёба")
type_menu = ttk.Combobox(add_frame, textvariable=task_type_var, values=["учёба", "спорт", "работа"], width=10, state="readonly")
type_menu.grid(row=0, column=3, padx=5, pady=5)

add_btn = Button(add_frame, text="➕ Добавить", command=add_new_task, bg="lightgreen")
add_btn.grid(row=0, column=4, padx=10, pady=5)

history_frame = LabelFrame(root, text="История задач", padx=10, pady=10)
history_frame.pack(fill="both", expand=True, padx=10, pady=5)

scrollbar = Scrollbar(history_frame)
scrollbar.pack(side="right", fill="y")

history_listbox = Listbox(history_frame, yscrollcommand=scrollbar.set, font=("Arial", 10), height=12)
history_listbox.pack(fill="both", expand=True)
scrollbar.config(command=history_listbox.yview)

control_frame = Frame(root)
control_frame.pack(fill="x", padx=10, pady=10)

clear_btn = Button(control_frame, text="🗑️ Очистить историю", command=clear_history, bg="orange")
clear_btn.pack(side="left", padx=5)

save_btn = Button(control_frame, text="💾 Сохранить историю", command=save_history, bg="lightgray")
save_btn.pack(side="left", padx=5)

export_btn = Button(control_frame, text="📋 Экспорт в JSON", command=export_history, bg="lightgray")
export_btn.pack(side="left", padx=5)

refresh_history_display()

root.mainloop()
