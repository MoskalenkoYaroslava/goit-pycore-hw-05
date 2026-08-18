import sys
from datetime import datetime


LOG_LEVELS = ("INFO", "DEBUG", "ERROR", "WARNING")


def parse_log_line(line: str) -> dict:
    """Розбирає рядок логу на дату, час, рівень і повідомлення."""
    parts = line.strip().split(maxsplit=3)

    if len(parts) != 4:
        raise ValueError("рядок не відповідає формату логу")

    date, time, level, message = parts
    level = level.upper()

    try:
        datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
    except ValueError as error:
        raise ValueError("некоректні дата або час") from error

    if level not in LOG_LEVELS:
        raise ValueError(f"невідомий рівень логування: {level}")

    return {
        "date": date,
        "time": time,
        "level": level,
        "message": message,
    }


def load_logs(file_path: str) -> list:
    """Завантажує та аналізує записи з лог-файлу."""
    logs = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                logs.append(parse_log_line(line))
            except ValueError as error:
                print(f"Рядок {line_number} пропущено: {error}")

    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    """Повертає записи вказаного рівня логування."""
    level = level.upper()
    return [log for log in logs if log["level"] == level]


def count_logs_by_level(logs: list) -> dict:
    """Підраховує кількість записів кожного рівня."""
    counts = {level: 0 for level in LOG_LEVELS}

    for log in logs:
        counts[log["level"]] += 1

    return counts


def display_log_counts(counts: dict) -> None:
    """Виводить статистику логів у вигляді таблиці."""
    print("Рівень логування | Кількість")
    print("-----------------|----------")

    for level in LOG_LEVELS:
        print(f"{level:<17}| {counts.get(level, 0)}")


def main() -> None:
    if len(sys.argv) not in (2, 3):
        print("Використання: python3 task3.py <шлях> [рівень]")
        return

    file_path = sys.argv[1]
    selected_level = sys.argv[2].upper() if len(sys.argv) == 3 else None

    if selected_level and selected_level not in LOG_LEVELS:
        print(
            f"Невідомий рівень '{selected_level}'. "
            f"Доступні рівні: {', '.join(LOG_LEVELS)}"
        )
        return

    try:
        logs = load_logs(file_path)
    except FileNotFoundError:
        print(f"Файл '{file_path}' не знайдено.")
        return
    except OSError as error:
        print(f"Помилка читання файлу: {error}")
        return

    display_log_counts(count_logs_by_level(logs))

    if selected_level:
        filtered_logs = filter_logs_by_level(logs, selected_level)
        print(f"\nДеталі логів для рівня '{selected_level}':")

        if not filtered_logs:
            print("Записів не знайдено.")

        for log in filtered_logs:
            print(
                f"{log['date']} {log['time']} - "
                f"{log['message']}"
            )


if __name__ == "__main__":
    main()