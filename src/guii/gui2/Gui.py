import tkinter as tk
import networkx as nx
import GrafhDrawer as gd
import ga
from MatrixGetterFromFile import MatrixGetterFromFile
from MatrixGetterFromGui import MatrixGetterFromGui
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Gui:
    generation = 100
    count_steps = 600
    p_c = 0.9
    p_m = 0.1

    def __init__(self):
        self.window = tk.Tk()
        self.window.state('zoomed')
        self.window.title('Генетический алгоритм для поиска МОД')
        self.create_start_widgets()
        self.graph_drawer = gd.GrafhDrawer()
        self.graph = None

    def create_start_widgets(self):
        self.create_menu()
        self.frm_input = tk.Frame(self.window, relief="solid", bd=2, height=300, width=300)
        self.frm_input.grid(row=0, column=0, padx=80, pady=60)

        self.frm_graph = tk.Frame(self.window, relief="solid", bd=2, height=700, width=700)
        self.frm_graph.grid(row=0, column=1, padx=80, pady=60)

        tk.Button(self.window, text="Начать\nалгоритм", bg='silver', font=14, relief="solid", bd=2,
                  command=self.start_ga).grid(row=0, column=2, padx=80, pady=80)

        lbl = tk.Label(self.frm_input, text="Выберите способ задания\nматрицы смежности графа", font=14)
        btn_gui_input = tk.Button(self.frm_input, text="С помощью Gui", bg='silver', font=14, relief="solid", bd=2,
                                  command=lambda: MatrixGetterFromGui(self))
        btn_file_input = tk.Button(self.frm_input, text="Файл", bg='silver', font=14, relief="solid", bd=2,
                                   command=lambda: MatrixGetterFromFile(self))
        lbl.grid(row=0, column=0, padx=5, pady=5)
        btn_gui_input.grid(row=1, column=0, padx=5, pady=5)
        btn_file_input.grid(row=2, column=0, padx=5, pady=5)

    def create_menu(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Рестарт", command=self.restart)
        settings_menu.add_command(label='Настройки', command=self.create_settings_win)
        menubar.add_cascade(label='Файл', menu=settings_menu)

    def start(self):
        self.window.mainloop()

    def create_graph(self, matrix: [[int]]):
        self.graph = nx.Graph()
        for i in range(len(matrix)):
            self.graph.add_node(str(i + 1))
        for i in range(len(matrix)):
            for j in range(i):
                el = matrix[i][j]
                if el:
                    self.graph.add_edge(str(i + 1), str(j + 1), weight=matrix[i][j])

        self.show_graph()

    def show_graph(self):
        for widget in self.frm_graph.winfo_children():
            widget.destroy()

        figure = self.graph_drawer.draw(self.graph)
        canvas = FigureCanvasTkAgg(figure, self.frm_graph)
        canvas.get_tk_widget().pack(fill='both')
        canvas.draw()

    def restart(self):
        self.clear()
        self.create_start_widgets()

    def create_settings_win(self):
        win = tk.Toplevel(self.window)
        win.title('Настройки')

        tk.Label(win, text="Количество шагов", font=14).grid(row=0, column=0, padx=20, pady=20)
        tk.Label(win, text="Вероятность скрещивания", font=14).grid(row=1, column=0, padx=20, pady=20)
        tk.Label(win, text="Вероятность мутации", font=14).grid(row=2, column=0, padx=20, pady=20)
        tk.Label(win, text="Размер популяции", font=14).grid(row=3, column=0, padx=20, pady=20)

        entry_steps = tk.Entry(win, font=14)
        entry_steps.grid(row=0, column=1, padx=20, pady=20)
        entry_steps.insert(0, str(Gui.count_steps))
        entry_p_c = tk.Entry(win, font=14)
        entry_p_c.grid(row=1, column=1, padx=20, pady=20)
        entry_p_c.insert(0, str(Gui.p_c))
        entry_p_m = tk.Entry(win, font=14)
        entry_p_m.grid(row=2, column=1, padx=20, pady=20)
        entry_p_m.insert(0, str(Gui.p_m))
        entry_generation = tk.Entry(win, font=14)
        entry_generation.grid(row=3, column=1, padx=20, pady=20)
        entry_generation.insert(0, str(Gui.generation))

        btn = tk.Button(win, font=14, text="Применить", bg='silver',
                        command=lambda: self.change_settings(entry_steps, entry_p_c, entry_p_m, entry_generation))
        btn.grid(row=4, column=1, padx=20, pady=20)

    def change_settings(self, entry_steps: tk.Entry, entry_p_c: tk.Entry, entry_p_m: tk.Entry,
                        entry_generation: tk.Entry):

        Gui.count_steps = int(entry_steps.get())
        Gui.p_c = float(entry_p_c.get())
        Gui.p_m = float(entry_p_m.get())
        Gui.generation = int(entry_generation.get())

    def clear(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def start_ga(self):
        self.clear()
        self.algorithm = ga.Solver(self.graph)
        self.algorithm.algorithm(Gui.generation, Gui.count_steps, Gui.p_c, Gui.p_m)
        self.create_menu()
