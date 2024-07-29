import tkinter as tk
from tkinter import ttk
import webbrowser


def calculate_resources(version: float, players: int, plugins: int):
    base_cpu_cores = {
        1.8: 2,
        1.9: 2,
        1.10: 2,
        1.11: 2,
        1.12: 2,
        1.13: 2,
        1.14: 2,
        1.15: 2,
        1.16: 2,
        1.17: 2,
        1.18: 2,
        1.19: 2,
        1.20: 2,
        1.21: 2
    }

    base_ram = {
        1.8: 2,
        1.9: 2,
        1.10: 2,
        1.11: 2,
        1.12: 2,
        1.13: 2,
        1.14: 2,
        1.15: 2,
        1.16: 3,
        1.17: 3,
        1.18: 3,
        1.19: 3,
        1.20: 3,
        1.21: 3
    }

    plugin_cpu_factor = 0.01
    plugin_ram_factor = 0.05
    player_cpu_factor = 0.05
    player_ram_factor = 0.2

    cpu_cores = base_cpu_cores.get(version, 6) + plugins * plugin_cpu_factor + players * player_cpu_factor
    ram = base_ram.get(version, 12) + plugins * plugin_ram_factor + players * player_ram_factor

    cpu_cores = int(cpu_cores + 0.5)
    ram = int(ram + 0.5)

    return cpu_cores, ram


def update_resources(event=None):
    try:
        version = float(version_var.get())
        players = int(players_scale.get())
        plugins = int(plugins_scale.get())
        cpu_cores, ram = calculate_resources(version, players, plugins)
        result_label.config(text=f"Необходимо ядер процессора: {cpu_cores}\nНеобходимо ОЗУ (в ГБ): {ram}")
        players_label.config(text=f"Количество игроков: {players}")
        if kernel_var.get() != "Vanilla":
            plugins_label.config(text=f"Количество {plugin_or_mod_label}: {plugins}")
        else:
            plugins_label.config(text="")
    except ValueError:
        result_label.config(text="Ошибка: Неверное значение.")


def open_donation_page():
    webbrowser.open("https://yoomoney.ru/fundraise/13V8SMFA5M4.240713")


def update_kernel_options(event=None):
    global plugin_or_mod_label
    kernel = kernel_var.get()
    if kernel == "Vanilla":
        plugins_scale.pack_forget()
        plugins_label.pack_forget()
        plugin_or_mod_label = ""
    else:
        if kernel == "Forge":
            plugin_or_mod_label = "модов"
        else:
            plugin_or_mod_label = "плагинов"
        plugins_label.config(text=f"Количество {plugin_or_mod_label}: {plugins_scale.get()}")
        plugins_label.pack(pady=10)
        plugins_scale.pack(pady=5)
    update_resources()


# Создание главного окна
root = tk.Tk()
root.title("Server Resources")
root.geometry("600x500")  # Устанавливаем размер окна
root.configure(bg="#2E2E2E")  # Тёмный фон
root.iconbitmap('icon.ico')  # Укажите путь к вашему файлу иконки .ico

# Настройка стилей
style = ttk.Style()
style.configure("TLabel", background="#2E2E2E", foreground="white")
style.configure("TCombobox", fieldbackground="#3E3E3E", background="#3E3E3E", foreground="white")
style.configure("TScale", background="#2E2E2E")
style.configure("TButton", background="#4A4A4A", foreground="white")
style.map("TButton", background=[("active", "#5A5A5A")])

# Настройка выпадающего списка для выбора ядра
kernel_var = tk.StringVar()
kernel_var.set("Paper/Spigot")  # Устанавливаем начальное значение

kernel_label = ttk.Label(root, text="Выберите ядро:")
kernel_label.pack(pady=10)

kernel_menu = ttk.Combobox(
    root,
    textvariable=kernel_var,
    values=["Vanilla", "Paper/Spigot", "Forge"],
    state="readonly"
)
kernel_menu.pack(pady=5)

# Добавление обработчика для изменения параметров в зависимости от выбора ядра
kernel_menu.bind("<<ComboboxSelected>>", update_kernel_options)

# Настройка выпадающего списка для версии игры
version_var = tk.StringVar()
version_var.set("1.8")  # Устанавливаем начальное значение

version_label = ttk.Label(root, text="Выберите версию игры:")
version_label.pack(pady=10)

version_menu = ttk.Combobox(
    root,
    textvariable=version_var,
    values=[
        "1.8", "1.9", "1.10", "1.11", "1.12",
        "1.13", "1.14", "1.15", "1.16", "1.17",
        "1.18", "1.19", "1.20", "1.21"
    ],
    state="readonly"
)
version_menu.pack(pady=5)

# Добавление обработчика для обновления ресурсов при изменении версии
version_menu.bind("<<ComboboxSelected>>", update_resources)

# Ползунок для выбора количества игроков
players_scale = ttk.Scale(root, from_=0, to=100, orient="horizontal", command=lambda _: update_resources())
players_scale.set(0)  # Устанавливаем начальное значение
players_scale.bind("<ButtonRelease-1>", update_resources)

players_label = ttk.Label(root, text="Количество игроков: 0")
players_label.pack(pady=10)
players_scale.pack(pady=5)

# Ползунок для выбора количества плагинов/модов
plugins_scale = ttk.Scale(root, from_=0, to=100, orient="horizontal", command=lambda _: update_resources())
plugins_scale.set(0)  # Устанавливаем начальное значение
plugins_scale.bind("<ButtonRelease-1>", update_resources)

plugins_label = ttk.Label(root, text="Количество плагинов: 0")
plugins_label.pack(pady=10)
plugins_scale.pack(pady=5)

# Метка для отображения результатов
result_label = ttk.Label(root, text="")
result_label.pack(pady=20)

# Нижняя панель с информацией
bottom_frame = tk.Frame(root, bg="#2E2E2E")
bottom_frame.pack(side="bottom", fill="x", pady=10)

version_text = ttk.Label(bottom_frame, text="Версия 1.0", anchor="w")
version_text.pack(side="left", padx=20)

author_text = ttk.Label(bottom_frame, text="made by PlugMan", anchor="e")
author_text.pack(side="right", padx=20)

# Кнопка "Donate"
donate_button = tk.Button(root, text="Donate", command=open_donation_page, bg="red", fg="white",
                          font=("Helvetica", 12, "bold"))
donate_button.pack(side="bottom", pady=20, anchor="center")

# Обновляем результат при старте
plugin_or_mod_label = "плагинов"
update_resources()

root.mainloop()
