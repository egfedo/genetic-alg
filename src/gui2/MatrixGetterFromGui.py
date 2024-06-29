import tkinter as tk
from tkinter.messagebox import showerror
import random


class MatrixGetterFromGui:
    count_v = 0

    def __init__(self, gui):
        self.main_gui = gui
        self.win = tk.Toplevel(gui.window)
        self.win.title('Чтение матрицы смежности из файла')
        self.win.geometry("700x700")

        self.entries_for_matr = []

        lbl = tk.Label(self.win, text="Количество вершин в графе: ", font=14)
        entry = tk.Entry(self.win, bg="#fafafa", font=14, width=3, relief="solid", bd=2, )
        btn_for_count_v = tk.Button(self.win, text="Построить матрицу для ввода", bg='silver', font=14, relief="solid",
                                    bd=2,
                                    command=lambda: self.check_entry_and_create_new_matrix(entry))
        self.frm_matrix = tk.Frame(self.win, relief="solid", bd=2, width=600, height=600)
        btn_for_save = tk.Button(self.win, text="Задать граф", bg='silver', font=14, relief="solid", bd=2,
                                 command=self.save_matrix)
        btn_for_rand = tk.Button(self.win, text="Случайные веса", bg='silver', font=14, relief="solid", bd=2,
                                 command=self.random_weighs)

        lbl.grid(row=0, column=0, padx=5, pady=5)
        entry.grid(row=0, column=1, padx=5, pady=5)
        btn_for_count_v.grid(row=0, column=2, padx=5, pady=5)
        self.frm_matrix.grid(row=1, column=0, columnspan=8, padx=50, pady=5)
        btn_for_save.grid(row=2, column=7, padx=5, pady=5)
        btn_for_rand.grid(row=2, column=0, padx=5, pady=5)

    def create_new_matrix(self):
        cell_size = int(600 / (self.count_v + 1))

        if self.count_v != 0:
            self.frm_matrix.destroy()
            self.frm_matrix = tk.Frame(self.win, relief="solid", bd=2, width=600, height=600)
            self.frm_matrix.grid(row=1, column=0, columnspan=8, padx=50, pady=5)

        for i in range(self.count_v):
            self.entries_for_matr.append([None] * self.count_v)

        lbl = tk.Label(self.frm_matrix, text='', bg='grey', font=14, relief="solid", bd=2)
        lbl.grid(row=0, column=0, stick='wens')

        for i in range(1, self.count_v + 1):
            lbl = tk.Label(self.frm_matrix, text=str(i), bg='grey', font=14, relief="solid", bd=2)
            lbl.grid(row=i, column=0, stick='wens')
            self.frm_matrix.columnconfigure(i, minsize=cell_size)

        for j in range(1, self.count_v + 1):
            lbl = tk.Label(self.frm_matrix, text=str(j), bg='grey', font=14, relief="solid", bd=2)
            lbl.grid(row=0, column=j, stick='wens')
            self.frm_matrix.rowconfigure(j, minsize=cell_size)

        self.frm_matrix.rowconfigure(0, minsize=cell_size)
        self.frm_matrix.columnconfigure(0, minsize=cell_size)
        for i in range(self.count_v):
            lbl = tk.Label(self.frm_matrix, bg="gray", font=20, width=2, relief="solid", bd=2,
                           justify='center', text='')
            lbl.grid(row=i + 1, column=i + 1, stick='wens')
            for j in range(i):
                entry = tk.Entry(self.frm_matrix, bg="#fafafa", font=20, width=2, relief="solid", bd=2,
                                 justify='center')
                self.entries_for_matr[i][j] = entry
                entry.grid(row=i + 1, column=j + 1, stick='wens')
                lbl = tk.Label(self.frm_matrix, bg="gray", font=20, width=2, relief="solid", bd=2,
                               justify='center', text='')
                lbl.grid(row=j + 1, column=i + 1, stick='wens')

    def check_entry_and_create_new_matrix(self, entry):
        str_count_v = entry.get()
        if not str_count_v.isdigit() or int(str_count_v) <= 0 or int(str_count_v) > 20:
            showerror("Ошибка", "Количество вершин графа задаётся целыми положительными числами от 1 до 20!")
            return
        self.count_v = int(str_count_v)
        self.create_new_matrix()

    def get_matrix(self):
        matrix = []
        for i in range(self.count_v):
            matrix.append([None] * self.count_v)
            for j in range(i):
                el = self.entries_for_matr[i][j].get()
                if not ((el.isdigit() and int(el) > 0) or el == ''):
                    raise ValueError("Веса рёбер задаются целыми положительными числами!")
                if el == '':
                    weight = None
                else:
                    weight = int(el)
                matrix[i][j] = weight
                matrix[j][i] = weight

        return matrix

    def save_matrix(self):
        try:
            self.main_gui.create_graph(self.get_matrix())
            self.win.destroy()
        except ValueError as text:
            showerror("Ошибка", text)

    def random_weighs(self):
        if self.count_v == 0:
            showerror("Ошибка", "Не указано количество вершин")
            return
        self.clear()
        self.create_new_matrix()
        for i in range(self.count_v):

            for j in range(i):
                entry = self.entries_for_matr[i][j]
                weight = random.randint(1, 100)
                entry.delete(0, 'end')
                entry.insert(0, weight)

    def clear(self):
        for widget in self.frm_matrix.winfo_children():
            widget.destroy()
