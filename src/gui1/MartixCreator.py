import random
import tkinter as tk


class MatrixCreator:
    def __init__(self, frame):
        self.frame = frame
        self.count_v = 0

    def create_entries_matrix(self, count_v):
        self.count_v = count_v

        self.entries_for_matr = []

        for i in range(self.count_v):
            self.entries_for_matr.append([None] * self.count_v)

        btn_random = tk.Button(self.frame, bg='green', font=14, relief="solid", bd=2, text='R', command=self.random)
        btn_random.grid(row=0, column=0, stick='wens')

        for i in range(1, self.count_v + 1):
            lbl = tk.Label(self.frame, text=str(i), bg='grey', font=14, relief="solid", bd=2)
            lbl.grid(row=i, column=0, stick='wens')
            self.frame.columnconfigure(i, weight=1)

        for j in range(1, self.count_v + 1):
            lbl = tk.Label(self.frame, text=str(j), bg='grey', font=14, relief="solid", bd=2)
            lbl.grid(row=0, column=j, stick='wens')
            self.frame.rowconfigure(j, weight=1)

        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        for i in range(0, self.count_v):
            for j in range(0, i):
                entry = tk.Entry(self.frame, bg="#fafafa", font=20, width=2, relief="solid", bd=2,
                                 justify='center')
                self.entries_for_matr[i][j] = entry
                entry.grid(row=i+1, column=j+1, stick='wens')

    def destroy(self):
        self.clear()
        self.frame.destroy()

    def create_graph_matrix(self):
        graph_matr = []
        for i in range(self.count_v):
            graph_matr.append([None] * self.count_v)

            lbl = tk.Label(self.frame, bg="gray", font=20, width=2, relief="solid", bd=2,
                           justify='center', text='')
            lbl.grid(row=i + 1, column=i + 1, stick='wens')

            for j in range(i):
                el = self.entries_for_matr[i][j].get()
                if not el.isdigit() or int(el) <= 0:
                    raise ValueError("Веса рёбер задаются целыми положительными числами!")
                if el:
                    graph_matr[i][j] = int(el)
                    graph_matr[j][i] = int(el)
                    lbl = tk.Label(self.frame, bg="gray", font=20, width=2, relief="solid", bd=2,
                                   justify='center', text=int(el))
                    lbl.grid(row=j + 1, column=i + 1, stick='wens')


        return graph_matr

    def fill_matrix(self, graph_matr):
        for i in range(self.count_v):
            lbl = tk.Label(self.frame, bg="gray", font=20, width=2, relief="solid", bd=2,
                           justify='center', text='')
            lbl.grid(row=i + 1, column=i + 1, stick='wens')
            for j in range(i):
                weight = graph_matr[i][j]
                entry = self.entries_for_matr[i][j]
                entry.delete(0, 'end')
                entry.insert(0, weight)
                if weight:
                    weight = str(weight)
                else:
                    weight = ""
                lbl = tk.Label(self.frame, bg="gray", font=20, width=2, relief="solid", bd=2,
                               justify='center', text=weight)
                lbl.grid(row=j + 1, column=i + 1, stick='wens')

    def random(self):
        self.clear()
        self.create_entries_matrix(self.count_v)
        for i in range(self.count_v):
            lbl = tk.Label(self.frame, bg="gray", font=20, width=2, relief="solid", bd=2,
                           justify='center', text='')
            lbl.grid(row=i + 1, column=i + 1, stick='wens')
            for j in range(i):
                entry = self.entries_for_matr[i][j]
                weight = random.randint(1, 100)
                entry.delete(0, 'end')
                entry.insert(0, weight)
                lbl = tk.Label(self.frame, bg="gray", font=20, width=2, relief="solid", bd=2,
                               justify='center', text=weight)
                lbl.grid(row=j + 1, column=i + 1, stick='wens')


    def clear(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

