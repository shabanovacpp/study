
from tabulate import tabulate

import numpy as np

np.set_printoptions(suppress=True, precision=16)


def print_matrix(*matrices, titles=None, spaces=4):

    n_matrices = len(matrices)
    
    if titles is None:
        titles = [f"Матрица {i+1}" for i in range(n_matrices)]
    elif len(titles) != n_matrices:
        raise ValueError(f"Количество заголовков ({len(titles)}) должно совпадать с количеством матриц ({n_matrices})")
    
    # Форматируем каждую матрицу как строки
    matrices_str = []
    widths = []
    
    for mat in matrices:
        # Преобразуем одномерный массив в двумерный с одной строкой
        if isinstance(mat, (np.ndarray, list)):
            mat = np.array(mat)
            if mat.ndim == 1:
                mat = mat.reshape(1, -1)  # Преобразуем в матрицу 1xN
            elif mat.ndim == 0:
                mat = mat.reshape(1, 1)   # Преобразуем скаляр в матрицу 1x1
        
        # Форматируем с явным указанием, что это таблица
        mat_str = tabulate(mat, tablefmt="fancy_grid", numalign="center").split('\n')
        matrices_str.append(mat_str)
        widths.append(max(len(line) for line in mat_str))
    
    # Выводим заголовки
    header = ""
    for i, title in enumerate(titles):
        header += f"{title:^{widths[i]}}"
        if i < n_matrices - 1:
            header += " " * spaces
    print(header)
    
    # Выводим разделительную линию
    total_width = sum(widths) + spaces * (n_matrices - 1)
    print("─" * total_width)
    
    # Выводим матрицы рядом
    max_rows = max(len(mat_str) for mat_str in matrices_str)
    
    for row in range(max_rows):
        line = ""
        for i in range(n_matrices):
            if row < len(matrices_str[i]):
                line += matrices_str[i][row]
            else:
                line += " " * widths[i]
            
            if i < n_matrices - 1:
                line += " " * spaces
        print(line)


def print_numbers(*numbers, titles=None):

    if titles is None:
        titles = [f"#{i+1}" for i in range(len(numbers))]
    
    # Создаем простую таблицу 1xN
    data = [list(numbers)]
    
    # Добавляем заголовки как отдельную строку
    table = tabulate(data, headers=titles, tablefmt="fancy_grid", numalign="center")
    print(table)
