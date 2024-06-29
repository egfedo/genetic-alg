import tkinter as tk
from ReaderMatrix import ReaderMatrix
from tkinter.messagebox import showerror


class MatrixGetterFromFile:
    def __init__(self, gui):
        self.main_gui = gui
        self.win = tk.Toplevel(gui.window)
        self.win.title('Чтение матрицы смежности из файла')
        tk.Label(self.win, text="Путь к файлу:", font=14).grid(row=0, column=0, padx=15, pady=15)
        entry = tk.Entry(self.win, font=14, width=50)
        entry.grid(row=0, column=1, padx=15, pady=15)
        tk.Button(self.win, text="Ок", font=14, command=lambda: self.save_matrix(entry), bg='silver').grid(row=1, column=1, padx=15,
                                                                                       pady=15)

    def save_matrix(self, entry):
        try:
            reader = ReaderMatrix(entry.get())
            matrix = reader.read_sim_square_matrix()
            self.main_gui.create_graph(matrix)
            self.win.destroy()
        except FileNotFoundError as text:
            showerror("Ошибка", text)
        except ValueError as text:
            showerror("Ошибка", text)
