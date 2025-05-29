import json
import sys

def sort_json(obj):
    if isinstance(obj, dict):
        return {k: sort_json(v) for k, v in sorted(obj.items())}
    if isinstance(obj, list):
        return [sort_json(x) for x in obj]  # не сортуємо список, лише обробляємо елементи
    return obj

def compare_json(obj1, obj2, path="root", diffs=None):
    if diffs is None:
        diffs = []

    if type(obj1) != type(obj2):
        diffs.append(f"Типи відрізняються у {path}: {type(obj1).__name__} vs {type(obj2).__name__}")
        return diffs

    if isinstance(obj1, dict):
        for key in obj1:
            if key not in obj2:
                diffs.append(f"Ключ '{key}' відсутній у другому файлі в {path}")
            else:
                compare_json(obj1[key], obj2[key], path + f".{key}", diffs)
        for key in obj2:
            if key not in obj1:
                diffs.append(f"Ключ '{key}' відсутній у першому файлі в {path}")
        return diffs

    if isinstance(obj1, list):
        if len(obj1) != len(obj2):
            diffs.append(f"Різна довжина списку у {path}: {len(obj1)} vs {len(obj2)}")
        min_len = min(len(obj1), len(obj2))
        for i in range(min_len):
            compare_json(obj1[i], obj2[i], path + f"[{i}]", diffs)
        return diffs

    if obj1 != obj2:
        diffs.append(f"Відмінність у {path}: {obj1} vs {obj2}")

    return diffs

def main(file1, file2):
    try:
        with open(file1, 'r', encoding='utf-8') as f:
            data1 = json.load(f)
        with open(file2, 'r', encoding='utf-8') as f:
            data2 = json.load(f)
    except Exception as e:
        print(f"Помилка читання файлів: {e}")
        return

    data1_sorted = sort_json(data1)
    data2_sorted = sort_json(data2)

    diffs = compare_json(data1_sorted, data2_sorted)

    if not diffs:
        print("Файли ідентичні!")
    else:
        print("Знайдені відмінності:")
        for diff in diffs:
            print(diff)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Використання: python compare_json.py etalon.json newfile.json")
    else:
        main(sys.argv[1], sys.argv[2])

