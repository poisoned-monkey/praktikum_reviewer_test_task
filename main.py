import datetime as dt


# Докстринги в коде отсутствуют.
# Подробнее о докстрингах тут: https://peps.python.org/pep-0257/
class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = ( 
            # Можно вынести манипуляции с датой в отдельный метод.
            # Или просто поместить их в одну строку.
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        # Имеет смысл добавить проверки на невалидность типа и пустую запись.
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Названия переменных следует писать с маленькой буквы.
        for Record in self.records:
            # Данную конструкцию if можно сократить через list comprehensions
            if Record.date == dt.datetime.now().date():
                # Можно использовать конструкцию +=, как сделано в методе ниже.
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Избавиться от бэкслэша. 
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # Необходимо убрать скобки и добавить пробел в соответствии с PEP8.
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.
    # Для названий аргументов функций используются маленькие буквы.
    # А вообще USD_RATE и EURO_RATE уже есть внутри класса.
    # Их необязательно передавать в метод.
    
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Ненужная строка ниже. Можно удалить.
            cash_remained == 1.00
            currency_type = 'руб'
        # Имеет смысл явно прописать случай, если на вход подается неизвестная валюта.
        if cash_remained > 0:
            return (
                # Формат вывода. В коде используются разные форматы вывода.
                # Стоит придерживаться одного формата. 
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # elif можно заменить на else.
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
        
    # Переопределение метода здесь бессмысленно. Можно удалить. 
    def get_week_stats(self):
        super().get_week_stats()
