import psutil
import json
import sys
import math
import re
import os


def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def get_process_info(regex_filter=None):
    processes_info = []
    try:
        for proc in psutil.process_iter(['name', 'pid']):
            if regex_filter:
                if not re.search(regex_filter, proc.info['name']):
                    continue
            info = proc.info
            is_pid_prime = is_prime(info['pid'])
            info['is_prime'] = is_pid_prime
            processes_info.append(proc.info)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
        print(f"Ошибка при доступе к процессу: {e}", file=sys.stderr)
        return None
    return processes_info


def save_to_json(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Данные успешно сохранены в файл '{filename}'")
    except IOError as e:
        print(f"Ошибка записи в файл: {e}", file=sys.stderr)


def check_json_file(filename, regex_filter=None):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Ошибка чтения или декодирования JSON файла: {e}", file=sys.stderr)
        return

    errors_count = 0
    
    for proc in data:
        if regex_filter:
            if not re.search(regex_filter, proc['name']):
                continue

        if 'pid' in proc and 'is_prime' in proc and 'name' in proc:
            is_correct = is_prime(proc['pid'])
            
            if proc['is_prime'] != is_correct:
                errors_count += 1
                
                print(f"Для {proc['name']} процесса найдена ошибка.")
                
                real_type = "простое" if is_correct else "составное"
                file_type = "простое" if proc['is_prime'] else "составное"
                print(f"Число(PID) {proc['pid']} на самом деле {real_type}, а в файле написано {file_type}.")
                
        else:
            print(f"Объект в файле имеет неверный формат: {proc}", file=sys.stderr)

    print("-" * 20)
    print(f"В файле найдены ошибки: {errors_count} штук")


if __name__ == "__main__":
    filter_regex = os.environ.get('PROCESS_FILTER_REGEX', None)
    if filter_regex:
        print(f"Применяю фильтр по регулярному выражению: '{filter_regex}'")

    if len(sys.argv) > 1 and sys.argv[1] == '--check':
        if len(sys.argv) > 2:
            check_json_file(sys.argv[2], filter_regex)
        else:
            print("Пожалуйста, укажите имя файла для проверки. Пример: python main.py --check processes.json")
    else:
        print("Собираю информацию о процессах и проверяю ID на простоту...")
        process_list = get_process_info(filter_regex)
        if process_list:
            output_filename = 'processes.json'
            save_to_json(process_list, output_filename)
            
        print("Программа завершена.")