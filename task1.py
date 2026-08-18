def caching_fibonacci():
    # Створюємо порожній словник для кешування результатів 
    cache = {}

    def fibonacci(n):
        # Базові випадки для ряду Фібоначчі 
        if n <= 0:
            return 0
        if n == 1:
            return 1
        
        # Перевірка, чи результат уже є у кеші 
        if n in cache:
            return cache[n]

        # Рекурсивне обчислення та збереження результату в кеш 
        # Замикання дозволяє внутрішній функції мати доступ до змінної cache 
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        
        return cache[n]

    # Повертаємо внутрішню функцію як об'єкт 
    return fibonacci

# Приклад використання:
fib = caching_fibonacci()

# Обчислення значень
print(fib(10))  # Виведе 55
print(fib(15))  # Виведе 610