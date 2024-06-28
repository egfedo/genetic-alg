import tkinter as tk
import GraphDrawer as gd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from MartixCreator import MatrixCreator
from tkinter.messagebox import showerror, showwarning, showinfo


class Gui:
    count_v = 0
    graph_drawer = gd.GraphDrawer()

    def __init__(self):
        self.window = tk.Tk()
        self.window.state('zoomed')
        self.window.title('Нахождение МОД')

        self.frm_input = tk.Frame(self.window, relief="solid", bd=2, bg='silver')
        self.frm_input.grid(row=0, column=0, stick='wens')
        self.frm_matrix = tk.Frame(self.window, relief="solid", bd=2, bg='silver')
        self.frm_matrix.grid(row=1, column=0, stick='wens')
        btn_build_graph = tk.Button(self.window, relief="solid", bd=2, bg='green', command=self.create_graph,
                                         text="Построить граф", font=14)
        btn_build_graph.grid(row=2, column=0, stick='wens')
        self.frm_graph = tk.Frame(self.window, relief="solid", bd=2, bg='#fafafa')
        self.frm_graph.grid(row=3, column=0, stick='wens')
        self.frm_ga = tk.Frame(self.window, relief="solid", bd=2, bg='silver')
        self.frm_ga.grid(row=0, column=1, rowspan=4, stick='wens')

        self.window.grid_rowconfigure(0, minsize=150)
        self.window.grid_rowconfigure(1, minsize=330)
        self.window.grid_rowconfigure(2, minsize=30)
        self.window.grid_rowconfigure(3, minsize=470)
        self.window.grid_columnconfigure(0, minsize=1920 * 0.2)
        self.window.grid_columnconfigure(1, minsize=1920 * 0.8)

        self.matr_creator = MatrixCreator(self.frm_matrix)

        self.fill_fr_input()

    def fill_fr_input(self):
        lbl = tk.Label(self.frm_input, text="Количество вершин в графе: ", bg='silver', font=14)
        entry = tk.Entry(self.frm_input, bg="#fafafa", font=14, width=3, relief="solid", bd=2,
                                          justify='center')
        btn_for_count_v = tk.Button(self.frm_input, text="Ок", bg='green', font=14, relief="solid", bd=2,
                                         command=lambda: self.create_matrix(entry))
        btn_for_file_reading = tk.Button(self.frm_input, text="Ввод из\nфайла", bg='green', font=14, relief="solid", bd=2,
                                         command=lambda: self.create_win_for_path_file())
        lbl.grid(row=0, column=0, padx=5, pady=5)
        entry.grid(row=0, column=1, padx=5, pady=5)
        btn_for_count_v.grid(row=0, column=2, padx=5, pady=5)
        btn_for_file_reading.grid(row=1, column=2, padx=30, pady=20)


    def start(self):
        self.window.mainloop()

    def create_matrix(self, entry):
        if self.count_v != 0:
            self.matr_creator.destroy()
            self.frm_matrix = tk.Frame(self.window, relief="solid", bd=2, bg='silver')
            self.frm_matrix.grid(row=1, column=0, stick='wens')
            self.matr_creator = MatrixCreator(self.frm_matrix)
        str_count_v = entry.get()
        if not str_count_v.isdigit() or int(str_count_v) <= 0 or int(str_count_v) >= 20:
            showerror("Ошибка", "Количество вершин графа задаётся целыми положительными числами от 1 до 15!")
            return
        self.count_v = int(str_count_v)
        self.matr_creator.create_entries_matrix(self.count_v)


    def create_graph(self):
        for widget in self.frm_graph.winfo_children():
            widget.destroy()

        try:
            self.graph_matr = self.matr_creator.create_graph_matrix()

            figure = self.graph_drawer.draw(self.graph_matr)
            canvas = FigureCanvasTkAgg(figure, self.frm_graph)
            canvas.get_tk_widget().pack(fill='both')
            canvas.draw()
        except ValueError as text:
            showerror("Ошибка", text)

    def create_win_for_path_file(self):
        win = tk.Toplevel(self.window)
        win.title('Чтение матрицы смежности из файла')
        tk.Label(win, text="Путь к файлу:", font=14).grid(row=0, column=0, padx=15, pady=15)
        tk.Entry(win, font=14, width=50).grid(row=0, column=1, padx=15, pady=15)
        tk.Button(win, text="Ок", font=14, command=self.create_graph_from_file).grid(row=1, column=1, padx=15, pady=15)

    def create_graph_from_file(self):
        pass


