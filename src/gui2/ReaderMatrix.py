class ReaderMatrix:
    f = None
    def __init__(self, filename):
        try:
            self.f = open(filename, "r")
        except FileNotFoundError:
            raise FileNotFoundError("Ошибка открытия файла")


    def read_sim_square_matrix(self):
        matrix = []

        for line in self.f:  # пока есть строчки в файле
            line = line.split()  # делим считаную строку
            row = []
            for item in line:
                if not ((item.isdigit() and int(item) > 0) or item == '-'):
                    raise ValueError("Веса рёбер задаются целыми положительными числами!")
                if item == '-':
                    weight = None
                else:
                    weight = int(item)
                row.append(weight)
            # преобразованую строчку добавляем в матрицу
            matrix.append(row)
        if not self.matr_is_sim_square(matrix):
            raise ValueError("Матрица не является квадратной и симметричной!")
        return matrix

    def matr_is_sim_square(self, matr):
        size = len(matr)
        for i in range(size):
            if len(matr[i]) != size:
                return False
            for j in range(0, i):
                if matr[i][j] != matr[j][i]:
                    return False
        return True

    def __del__(self):
        if self.f:
            self.f.close()


