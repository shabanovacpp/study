import numpy as np
import re

def parse_variant(file_path, variant_number):
    """
    Парсит файл с данными и возвращает две матрицы для указанного варианта
    
    Parameters:
    file_path (str): путь к файлу с данными
    variant_number (int): номер варианта (1-30)
    
    Returns:
    tuple: (A_good, b_good, exact_good, A_bad, b_bad, exact_bad) 
           - хорошо и плохо обусловленные матрицы и их точные решения
           Каждая матрица A имеет размер 4x4, b - размер 4, exact - размер 4
    """
    
    # Пробуем разные кодировки
    encodings = ['cp1251', 'latin-1', 'utf-8', 'cp866']
    content = None
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
            # print(f"Файл успешно прочитан в кодировке: {encoding}")
            break
        except UnicodeDecodeError:
            continue
    
    if content is None:
        raise ValueError("Не удалось прочитать файл ни в одной из пробованных кодировок")
    
    # Разбиваем на варианты
    variants = re.split(r'\*{34}\s+Вариант\s+(\d+)\s+\*{34}', content)[1:]
    
    # Ищем нужный вариант
    found = False
    for i in range(0, len(variants), 2):
        if int(variants[i]) == variant_number:
            variant_text = variants[i + 1]
            found = True
            break
    
    if not found:
        raise ValueError(f"Вариант {variant_number} не найден")
    
    # Разделяем на хорошо и плохо обусловленные матрицы
    parts = variant_text.strip().split('2. Плохо обусловленная матрица')
    
    good_part = parts[0].replace('1. Хорошо обусловленная матрица', '').strip()
    bad_part = parts[1].strip() if len(parts) > 1 else ''
    
    def parse_matrix_section(section):
        """Парсит секцию с матрицей и возвращает A, b и точное решение"""
        lines = section.strip().split('\n')
        A = []
        b = []
        exact = []
        
        for line in lines:
            # Пропускаем пустые строки
            if not line.strip():
                continue
            
            # Ищем все числа в строке
            numbers = re.findall(r'-?\d+\.?\d*', line)
            
            # Ищем точное решение после символа @
            exact_match = re.search(r'@\s*(-?\d+\.?\d*)\s*(?:$|\s+)', line)
            
            if len(numbers) >= 5:
                # Первые 4 числа - коэффициенты матрицы A
                row = [float(num) for num in numbers[:4]]
                # 5-е число - правая часть b
                b_val = float(numbers[4])
                
                A.append(row)
                b.append(b_val)
                
                # Если есть точное решение в этой строке, добавляем его
                if exact_match:
                    exact_val = float(exact_match.group(1))
                    exact.append(exact_val)
        
        # Если точное решение не было найдено в строках (оно может быть в отдельной строке),
        # ищем его отдельно
        if not exact:
            exact_match = re.search(r'@\s*\[?([-?\d+\.?\d*\s*,?\s*]+)\]?', section)
            if exact_match:
                exact_str = exact_match.group(1)
                exact = [float(x) for x in re.findall(r'-?\d+\.?\d*', exact_str)]
        
        return np.array(A), np.array(b), np.array(exact)
    
    # Парсим хорошую матрицу
    A_good, b_good, exact_good = parse_matrix_section(good_part)
    
    # Парсим плохую матрицу
    A_bad, b_bad, exact_bad = None, None, None
    if bad_part:
        A_bad, b_bad, exact_bad = parse_matrix_section(bad_part)
    
    return A_good, b_good, exact_good, A_bad, b_bad, exact_bad