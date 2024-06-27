import tkinter as tk
import GrafhDrawer as gd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Gui:
    count_v = 0
    graph_drawer = gd.GrafhDrawer()

    def __init__(self):
        self.window = tk.Tk()
        self.window.state('zoomed')
        self.window.title('Нахождение МОД')


        self.frm_input = tk.Frame(self.window, relief="solid", bd=2, bg='grey')
        self.frm_input.grid(row=0, column=0, stick='wens')
        self.frm_matrix = tk.Frame(self.window, relief="solid", bd=2, bg='grey')
        self.frm_matrix.grid(row=1, column=0, stick='wens')
        self.btn_build_graph = tk.Button(self.window, relief="solid", bd=2, bg='#fafafa', command=self.create_graph, text="Построить граф", font=14)
        self.btn_build_graph.grid(row=2, column=0, stick='wens')
        self.frm_graph = tk.Frame(self.window, relief="solid", bd=2, bg='#fafafa')
        self.frm_graph.grid(row=3, column=0, stick='wens')
        self.frm_ga = tk.Frame(self.window, relief="solid", bd=2, bg='grey')
        self.frm_ga.grid(row=0, column=1, rowspan=4, stick='wens')

        self.window.grid_rowconfigure(0, minsize=150)
        self.window.grid_rowconfigure(1, minsize=300)
        self.window.grid_rowconfigure(2, minsize=30)
        self.window.grid_rowconfigure(3, minsize=500)
        self.window.grid_columnconfigure(0, minsize=1920 * 0.2)
        self.window.grid_columnconfigure(1, minsize=1920 * 0.8)

        self.fill_fr_input()

    def fill_fr_input(self):
        self.lbl_for_count_v = tk.Label(self.frm_input, text="Количество вершин в графе: ", bg='#fafafa', font=14,
                                        relief="solid", bd=2)
        self.entry_for_count_v = tk.Entry(self.frm_input, bg="#fafafa", font=14, width=4, relief="solid", bd=2, justify='center')
        self.btn_for_count_v = tk.Button(self.frm_input, text="Ок", bg='#fafafa', font=14, relief="solid", bd=2,
                                         command=self.create_matrix)
        self.lbl_for_count_v.grid(row=0, column=0, padx=5, pady=5)
        self.entry_for_count_v.grid(row=0, column=1, padx=5, pady=5)
        self.btn_for_count_v.grid(row=0, column=2, padx=5, pady=5)

    def create_matrix(self):
        if self.count_v != 0:
            self.restart_matrix()
        self.count_v = int(self.entry_for_count_v.get())
        self.cells = []

        for i in range(self.count_v + 1):
            self.cells.append([None] * (self.count_v+1))

        self.cells[0][0] = tk.Label(self.frm_matrix, bg='grey', font=14, relief="solid", bd=2)
        for i in range(1, self.count_v + 1):
            self.cells[i][0] = tk.Label(self.frm_matrix, text=str(i), bg='grey', font=14, relief="solid", bd=2)

        for j in range(1, self.count_v + 1):
            self.cells[0][j] = tk.Label(self.frm_matrix, text=str(j), bg='grey', font=14, relief="solid", bd=2)


        for i in range(1, self.count_v+ 1):
            for j in range(1,self.count_v+1):
                func = lambda i=i, j=j: self.add_edge(i, j)
                btn = tk.Entry(self.frm_matrix, bg="#fafafa", font=20, width=2, relief="solid", bd=2, justify='center')
                self.cells[i][j] = btn

        for i in range(self.count_v+1):
            self.frm_matrix.rowconfigure(i, weight=1)
            self.frm_matrix.columnconfigure(i, weight=1)
            for j in range(self.count_v+1):
                self.cells[i][j].grid(row=i, column=j, stick='wens')


    def start(self):
        self.window.mainloop()

    def restart_matrix(self):
        for i in range(self.count_v+1):
            for j in range(self.count_v + 1):
                self.cells[i][j].destroy()
        self.frm_matrix.destroy()
        self.frm_matrix = tk.Frame(self.window, relief="solid", bd=2, bg='grey')
        self.frm_matrix.grid(row=1, column=0, stick='wens')

    def create_graph(self):
        for widget in self.frm_graph.winfo_children():
            widget.destroy()

        self.graph_matr = []
        for i in range(self.count_v):
            self.graph_matr.append([None] * self.count_v)
            for j in range(self.count_v):
                el = self.cells[i+1][j+1].get()
                if el:
                    self.graph_matr[i][j] = int(el)

        figure = self.graph_drawer.draw(self.graph_matr)
        canvas = FigureCanvasTkAgg(figure, self.frm_graph)
        canvas.get_tk_widget().pack(fill='both')
        canvas.draw()




g = Gui()
g.start()
