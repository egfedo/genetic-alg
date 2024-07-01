import tkinter as tk
from src.modules.Drawer import Drawer
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.modules.Solver import Solver
import networkx as nx
from tkinter.messagebox import showerror

class VisualisatorGA:
    def __init__(self, drawer: Drawer, graph: nx.Graph, size_gener, count_gener, p_c, p_m):
        self.window = tk.Tk()
        self.window.state('zoomed')
        self.window.title('Генетический алгоритм для поиска МОД')
        self.size_generation = size_gener
        self.count_generations = count_gener
        self.p_c = p_c
        self.p_m = p_m

        self.graph = graph
        (self.best_solutions,
         self.best_weights,
         self.average_weights) = Solver(graph, size_gener, count_gener, p_c, p_m).algorithm()
        # Update generation count after solver is done
        self.count_generations = len(self.best_solutions)

        self.step = 0

        self.drawer = drawer
        self.create_frms()
        self.show_best_solution(0)
        self.show_graphic()

        self.window.mainloop()



    def create_frms(self):
        frm_left = tk.Frame(self.window)
        self.frm_mid = tk.Frame(self.window, relief="solid", bd=2, height=800, width=700, bg='white')
        frm_right = tk.Frame(self.window)

        frm_left.pack(side='left', fill='both', expand=True)
        self.frm_mid.pack(side='left', fill='both', expand=True)
        frm_right.pack(side='left', fill='both', expand=True)

        self.fill_left_frm(frm_left)
        self.fill_right_frm(frm_right)


    def fill_right_frm(self, frm: tk.Frame):
        tk.Label(frm, text='Три лучших остовных дерева\nтекущего поколения:', font='Calibri 14').pack(side='top',
                                                                                                      fill='both',
                                                                                                      expand=True,
                                                                                                      padx=5)
        tk.Button(frm, text='Первое', bg='silver', font='Calibri 14', relief="solid", bd=2, command=lambda: self.show_best_solution(0)).pack(side='top',
                                                                                                 fill='both',
                                                                                                 expand=True, pady=20,
                                                                                                 padx=5)
        tk.Button(frm, text='Второе', bg='silver', font='Calibri 14', relief="solid", bd=2, command=lambda: self.show_best_solution(1)).pack(side='top',
                                                                                                 fill='both',
                                                                                                 expand=True, pady=20,
                                                                                                 padx=5)
        tk.Button(frm, text='Третье', bg='silver', font='Calibri 14', relief="solid", bd=2, command=lambda: self.show_best_solution(2)).pack(side='top',
                                                                                                 fill='both',
                                                                                                 expand=True, pady=20,
                                                                                                 padx=5)

        frm_step = tk.Frame(frm)
        frm_step.pack(side='top', fill='both', expand=True, padx=10, pady=50)
        tk.Label(frm_step, text='Шаг ', font='Calibri 20').pack(expand=True, anchor='e', side='left')
        self.lbl_step = tk.Label(frm_step, text='0', font='Calibri 20')
        self.lbl_step.pack(expand=True, side='left',  anchor='w',)

        tk.Button(frm, text='Назад', bg='silver', font='Calibri 14', relief="solid", bd=2, command=self.prev_step).pack(side='left',
                                                                                                fill='both',
                                                                                                expand=True, pady=10,
                                                                                                padx=10)
        tk.Button(frm, text='Вперёд', bg='silver', font='Calibri 14', relief="solid", bd=2, command=self.next_step).pack(side='left',
                                                                                                 fill='both',
                                                                                                 expand=True, pady=10,
                                                                                                 padx=5)
        tk.Button(frm, text='Пропустить', bg='silver', font='Calibri 14', relief="solid", bd=2, command=self.last_step).pack(side='left',
                                                                                                     fill='both',
                                                                                                     expand=True,
                                                                                                     pady=10, padx=5)

    def fill_left_frm(self, frm):
        text = f"Текущие параметры алгоритма:" \
               f"\nКоличество поколений - {self.count_generations}" \
               f"\nВероятность скрещивания - {self.p_c}" \
               f"\nВероятность мутации - {self.p_m}" \
               f"\nРазмер поколения - {self.size_generation}"
        tk.Label(frm, text=text, font='Calibri 14').pack(side='top', expand=True, padx=10)

        frm_best_weight = tk.Frame(frm)
        frm_best_weight.pack(side='top', expand=True, padx=10)
        tk.Label(frm_best_weight, text=f'Вес лучшего решения - ', font='Calibri 14').pack(side='left', anchor='e', expand=True)
        self.lbl_best_weight = tk.Label(frm_best_weight, text=self.best_weights[0][0], font='Calibri 14')
        self.lbl_best_weight.pack(side='left', anchor='w', expand=True)

        self.frm_graphic = tk.Frame(frm, relief="solid", bd=2, height=500, width=450, bg='#fafafa')
        self.frm_graphic.pack(side='top', expand=True, fill='x')

    def update(self):
        self.lbl_step.config(text=self.step)
        self.lbl_best_weight.config(text=self.best_weights[self.step][0])
        self.show_best_solution(0)
        self.show_graphic()


    def next_step(self):
        if self.step + 1 == self.count_generations:
            return
        self.step += 1
        self.update()

    def prev_step(self):
        if self.step == 0:
            return
        self.step -= 1
        self.update()

    def last_step(self):
        if self.step + 1 == self.count_generations:
            return
        self.step = self.count_generations - 1
        self.update()

    def show_best_solution(self, i_solution):
        if i_solution >= self.size_generation:
            showerror("Ошибка", "Из-за размера поколения данного решения не существует!")
            return

        for widget in self.frm_mid.winfo_children():
            widget.destroy()

        graph = self.graph.edge_subgraph(self.best_solutions[self.step][i_solution])
        if len(graph.nodes) <= 10:
            figure = self.drawer.draw_graph(self.graph, (7, 7), subgraph=graph)
        else:
            figure = self.drawer.draw_graph(graph, (7, 7))
        canvas = FigureCanvasTkAgg(figure, self.frm_mid)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')
        tk.Label(self.frm_mid, text=f'Вес дерева - {self.best_weights[self.step][i_solution]}', font='Calibri 14', bg='white').pack(expand=True)

    def show_graphic(self):
        for widget in self.frm_graphic.winfo_children():
            widget.destroy()
        y = [None] * (self.step + 1)
        for i in range(self.step + 1):
            y[i] = self.best_weights[i][0]
        min_bound = min(map(lambda lst: lst[0], self.best_weights))
        figure = self.drawer.draw_graphic(y, (4, 4),
                                          self.average_weights[:self.step+1],
                                          full_size=self.count_generations,
                                          lower_bound=min_bound)
        canvas = FigureCanvasTkAgg(figure, self.frm_graphic)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')

