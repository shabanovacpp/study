import numpy as np
import re

def parse_file(filename, variant_number):
     

     # Пробуем разные кодировки
    encodings = ['cp1251', 'utf-8', 'cp866', 'latin-1', 'windows-1251', 'koi8-r']
    
    content = None
    used_encoding = None
    
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as f:
                content = f.read()
                used_encoding = encoding
                break
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    if content is None:
        # Последняя попытка - читаем в бинарном режиме и игнорируем ошибки
        try:
            with open(filename, 'rb') as f:
                raw_data = f.read()
                # Пробуем декодировать с заменой ошибок
                content = raw_data.decode('utf-8', errors='ignore')
                used_encoding = 'utf-8 (with ignore)'
        except:
            raise ValueError(f"Не удалось прочитать файл {filename}")
    
    
    # Используем регулярные выражения для поиска варианта
    # Паттерн для поиска блока варианта
    variant_pattern = rf'\*\*\*+\s*Вариант\s+{variant_number}\s*\*\*\*+(.*?)(?=\*\*\*+|\Z)'
    match = re.search(variant_pattern, content, re.DOTALL | re.IGNORECASE)
    
    if not match:
        # Пробуем другой формат
        variant_pattern = rf'Вариант\s+{variant_number}\s*\n(.*?)(?=\n\s*\*\*|\Z)'
        match = re.search(variant_pattern, content, re.DOTALL | re.IGNORECASE)
    
    if not match:
        raise ValueError(f"Вариант {variant_number} не найден")
    
    block = match.group(1)
    
    # Извлекаем все числа из блока
    # Паттерн для поиска чисел (целых и с плавающей точкой)
    number_pattern = r'-?\d+\.?\d*'
    
    # Находим все строки в блоке
    lines = block.strip().split('\n')
    
    # Очищаем строки от лишних символов
    clean_lines = []
    for line in lines:
        # Убираем звёздочки и другие символы в начале строки
        line = re.sub(r'^\s*\*+\s*', '', line)
        if line.strip():
            clean_lines.append(line)
    
    # Если строк меньше 4, пробуем собрать все числа в один список
    if len(clean_lines) < 4:
        all_numbers = []
        for line in clean_lines:
            # Находим все числа в строке
            numbers = re.findall(number_pattern, line)
            for num in numbers:
                try:
                    if '.' in num:
                        all_numbers.append(float(num))
                    else:
                        all_numbers.append(int(num))
                except ValueError:
                    continue
        
        if len(all_numbers) >= 4:
            # Определяем размерность
            n = len(all_numbers) // 4
            if n >= 2:  # Минимальная размерность
                a_data = all_numbers[:n]
                b_data = all_numbers[n:2*n]
                c_data = all_numbers[2*n:3*n]
                d_data = all_numbers[3*n:4*n]
            else:
                raise ValueError(f"Недостаточно данных для варианта {variant_number}")
        else:
            raise ValueError(f"Не удалось извлечь числа для варианта {variant_number}")
    else:
        # Парсим каждую строку отдельно
        def extract_numbers(line):
            # Находим все числа в строке
            numbers = re.findall(number_pattern, line)
            result = []
            for num in numbers:
                try:
                    if '.' in num:
                        result.append(float(num))
                    else:
                        result.append(int(num))
                except ValueError:
                    continue
            return result
        
        a_data = extract_numbers(clean_lines[0])
        b_data = extract_numbers(clean_lines[1])
        c_data = extract_numbers(clean_lines[2])
        d_data = extract_numbers(clean_lines[3])
    
    # Проверяем, что данные не пустые
    if not b_data:
        raise ValueError(f"Не удалось извлечь вектор b для варианта {variant_number}")
    
    # Преобразуем в numpy массивы
    b = np.array(b_data, dtype=float)
    d = np.array(d_data, dtype=float)
    
    n = len(b)
    
    # Обрабатываем a (поддиагональ) - ожидаем n-1 элементов
    if len(a_data) == n:
        # Если дали n элементов, берём со второго (индекс 1)
        a = np.array(a_data[1:], dtype=float)
    elif len(a_data) >= n - 1:
        # Берём первые n-1 элементов
        a = np.array(a_data[:n-1], dtype=float)
    else:
        # Дополняем нулями если нужно
        a = np.zeros(n-1)
        a[:len(a_data)] = a_data[:len(a_data)]
    
    # Обрабатываем c (наддиагональ) - ожидаем n-1 элементов
    if len(c_data) == n:
        # Если дали n элементов, берём без последнего
        c = np.array(c_data[:-1], dtype=float)
    elif len(c_data) >= n - 1:
        # Берём первые n-1 элементов
        c = np.array(c_data[:n-1], dtype=float)
    else:
        # Дополняем нулями если нужно
        c = np.zeros(n-1)
        c[:len(c_data)] = c_data[:len(c_data)]
    
    # Проверяем размерность d
    if len(d) != n:
        d = np.pad(d, (0, n - len(d)), 'constant', constant_values=0)

    return a, b, c, d
    