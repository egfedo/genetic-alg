import tkinter as tk
import networkx as nx
import GrafhDrawer as gd
from MatrixGetterFromFile import MatrixGetterFromFile
from MatrixGetterFromGui import MatrixGetterFromGui
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Gui:
    graph = None
    graph_drawer = gd.GrafhDrawer()

    def __init__(self):
        self.window = tk.Tk()
        self.window.state('zoomed')
        self.window.title('Генетический алгоритм для поиска МОД')
        self.window.config(bg='silver')
        self.create_start_widgets()


    def create_start_widgets(self):
        self.frm_input = tk.Frame(self.window, relief="solid", bd=2, bg='silver', height=300, width=300)
        self.frm_input.grid(row=0, column=0, padx=80, pady=60)

        self.frm_graph = tk.Frame(self.window, relief="solid", bd=2, bg='silver', height=700, width=700)
        self.frm_graph.grid(row=0, column=1, padx=80, pady=60)

        tk.Button(self.window, text="Начать\nалгоритм", bg='green', font=14, relief="solid", bd=2,
                  command=self.ga).grid(row=0, column=2, padx=80, pady=80)

        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Рестарт", command=self.restart)
        settings_menu.add_command(label='Настройки')
        menubar.add_cascade(label='Файл', menu=settings_menu)

        lbl = tk.Label(self.frm_input, text="Выберите способ задания\nматрицы смежности графа", bg='silver', font=14)
        btn_gui_input = tk.Button(self.frm_input, text="С помощью Gui", bg='green', font=14, relief="solid", bd=2,
                                  command=lambda: MatrixGetterFromGui(self))
        btn_file_input = tk.Button(self.frm_input, text="Файл", bg='green', font=14, relief="solid", bd=2,
                                   command=lambda: MatrixGetterFromFile(self))
        lbl.grid(row=0, column=0, padx=5, pady=5)
        btn_gui_input.grid(row=1, column=0, padx=5, pady=5)
        btn_file_input.grid(row=2, column=0, padx=5, pady=5)


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

    def ga(self):
        pass

    def restart(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        self.create_start_widgets()


