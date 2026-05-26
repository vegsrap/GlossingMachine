import tkinter as tk
from tkinter import scrolledtext
from main import glossing_machine

def run_analysis():
    glossed = entry_gloss.get("1.0", tk.END).strip()
    tags = entry_tags.get().strip()

    if not glossed or not tags:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Пожалуйста, заполните оба поля.")
        return

    result = glossing_machine(glossed, tags)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)

# Создаём окно
root = tk.Tk()
root.title("Локализация языков по глоссам")
root.geometry("700x600")

# Поле ввода глосс
tk.Label(root, text="Глоссированный текст:", font=("Arial", 11)).pack(pady=(10,0))
entry_gloss = tk.Text(root, height=3, width=80)
entry_gloss.pack(pady=5)

# Поле ввода тегов
tk.Label(root, text="Теги частей речи (через пробел):", font=("Arial", 11)).pack(pady=(10,0))
entry_tags = tk.Entry(root, width=80, font=("Arial", 11))
entry_tags.pack(pady=5)

# Кнопка
btn = tk.Button(root, text="Анализировать", command=run_analysis,
                bg="#4CAF50", fg="white", font=("Arial", 11), padx=20, pady=5)
btn.pack(pady=15)

# Поле вывода результата
tk.Label(root, text="Результат:", font=("Arial", 11)).pack()
output_text = scrolledtext.ScrolledText(root, height=12, width=80, wrap=tk.WORD, font=("Arial", 10))
output_text.pack(pady=10)

root.mainloop()