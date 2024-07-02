import tkinter as tk
import networkx as nx

from src.modules import Drawer
from src.modules.MatrixGetterFromFile import MatrixGetterFromFile
from src.modules.MatrixGetterFromGui import MatrixGetterFromGui
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.messagebox import showerror
from src.modules.VisualisatorGA import VisualisatorGA


class Gui:
    def __init__(self):
        self.window = tk.Tk()
        self.window.state('zoomed')
        self.window.title('Генетический алгоритм для поиска МОД')
        self.graph = None

        self.size_generation = 10
        self.count_generations = 100
        self.p_c = 0.9
        self.p_m = 0.1

        self.create_frms()

    def create_frms(self):
        self.create_menu()
        frm_left = tk.Frame(self.window)
        self.frm_mid = tk.Frame(self.window, relief="solid", bd=2, height=800, width=800, bg='white')
        frm_right = tk.Frame(self.window)

        frm_left.pack(side='left', fill='both', expand=True)
        self.frm_mid.pack(side='left', expand=True)
        frm_right.pack(side='left', fill='both', expand=True)

        tk.Button(frm_right, text="Начать\nалгоритм", bg='silver', font='Calibri 14', relief="solid", bd=2,
                  command=self.start_ga).pack(expand=True)

        frm_input = tk.Frame(frm_left, relief="solid", bd=2)
        frm_input.pack(expand=True)
        self.fill_frm_input(frm_input)

        frm_settings = tk.Frame(frm_left, relief="solid", bd=2)
        frm_settings.pack(expand=True)
        self.fill_frm_settings(frm_settings)

    def fill_frm_input(self, frm_input):
        lbl = tk.Label(frm_input, text="Выберите способ задания\nматрицы смежности графа", font='Calibri 14')
        btn_gui_input = tk.Button(frm_input, text="С помощью Gui", bg='silver', font='Calibri 14', relief="solid", bd=2,
                                  command=lambda: MatrixGetterFromGui(self))
        btn_file_input = tk.Button(frm_input, text="Файл", bg='silver', font='Calibri 14', relief="solid", bd=2,
                                   command=lambda: MatrixGetterFromFile(self))
        lbl.pack(pady=10)
        btn_gui_input.pack(pady=10)
        btn_file_input.pack(pady=10)

    def fill_frm_settings(self, frm_settings):
        tk.Label(frm_settings, text="Количество поколений - ", font='Calibri 14', justify='right').grid(row=0, column=0, pady=20, sticky='e')
        tk.Label(frm_settings, text="Вероятность скрещивания - ", font='Calibri 14').grid(row=1, column=0,
                                                                                       pady=20, sticky='e')
        tk.Label(frm_settings, text="Вероятность мутации - ", font='Calibri 14').grid(row=2, column=0, pady=20, sticky='e')
        tk.Label(frm_settings, text="Размер поколения - ", font='Calibri 14').grid(row=3, column=0, pady=20, sticky='e')

        entry_count_gener = tk.Entry(frm_settings, font='Calibri 14', width=6)
        entry_count_gener.grid(row=0, column=1, pady=20, sticky='w')
        entry_count_gener.insert(0, str(self.count_generations))
        entry_p_c = tk.Entry(frm_settings, font='Calibri 14', width=6)
        entry_p_c.grid(row=1, column=1, pady=20, sticky='w')
        entry_p_c.insert(0, str(self.p_c))
        entry_p_m = tk.Entry(frm_settings, font='Calibri 14', width=6)
        entry_p_m.grid(row=2, column=1, pady=20, sticky='w')
        entry_p_m.insert(0, str(self.p_m))
        entry_size_gener = tk.Entry(frm_settings, font='Calibri 14', width=6)
        entry_size_gener.grid(row=3, column=1, pady=20, sticky='w')
        entry_size_gener.insert(0, str(self.size_generation))

        btn = tk.Button(frm_settings, font='Calibri 14', text="Применить", bg='silver',
                        command=lambda: self.change_settings(entry_count_gener, entry_p_c, entry_p_m, entry_size_gener))
        btn.grid(row=4, column=1, padx=20, pady=20)

    def create_menu(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        menubar.add_command(label="Рестарт", command=self.restart)


    def start(self):
        self.window.mainloop()

    def create_graph(self, matrix: [[int]]):
        graph = nx.Graph()
        for i in range(len(matrix)):
            graph.add_node(str(i + 1))
        for i in range(len(matrix)):
            for j in range(i):
                el = matrix[i][j]
                if el:
                    graph.add_edge(str(i + 1), str(j + 1), weight=matrix[i][j])

        if not nx.is_connected(graph):
            showerror("Ошибка", "Необходимо задать связный граф!")
            return

        self.graph = graph
        self.show_graph()

    def show_graph(self):
        for widget in self.frm_mid.winfo_children():
            widget.destroy()

        figure = Drawer.draw_graph(self.graph, (8, 8))
        canvas = FigureCanvasTkAgg(figure, self.frm_mid)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True)

    def restart(self):
        self.clear()
        self.create_frms()
        self.graph = None

    def change_settings(self, entry_count_gener: tk.Entry, entry_p_c: tk.Entry, entry_p_m: tk.Entry,
                        entry_size_gener: tk.Entry):
        try:
            count_generations = int(entry_count_gener.get())
            if count_generations <= 0:
                raise ValueError()
            self.count_generations = count_generations
        except ValueError:
            showerror("Ошибка", "Количество поколений задаётся целыми положительными числами!")
            return

        try:
            size_generation = int(entry_size_gener.get())
            if size_generation <= 0:
                raise ValueError()
            self.size_generation = size_generation
        except ValueError:
            showerror("Ошибка", "Размер поколения задаётся целыми положительными числами!")
            return

        try:
            p_c = float(entry_p_c.get())
            if not 0 < p_c < 1:
                raise ValueError()
            self.p_c = p_c
        except ValueError:
            showerror("Ошибка", "Вероятность скрещивания задаётся вещественным числом от 0 до 1!")
            return

        try:
            p_m = float(entry_p_m.get())
            if not 0 < p_m < 1:
                raise ValueError()
            self.p_m = p_m
        except ValueError:
            showerror("Ошибка", "Вероятность мутации задаётся вещественным числом от 0 до 1!")
            return

    def clear(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def start_ga(self):
        if self.graph is None:
            showerror("Ошибка", "Граф не задан!")
            return
        VisualisatorGA(self.graph, self.size_generation, self.count_generations, self.p_c, self.p_m)
