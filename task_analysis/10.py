import pandas as pd
import math

# Загрузка данных
transactions = pd.read_parquet('/Users/ekaterinashlyakhova/Documents/GitHub/exam_itmo/transaction_fraud_data.parquet')
exchange_rates = pd.read_parquet(
    '/Users/ekaterinashlyakhova/Documents/GitHub/exam_itmo/historical_currency_exchange.parquet')

# Преобразуем timestamp в дату для объединения
transactions['date'] = transactions['timestamp'].dt.date

# Объединяем данные с курсами валют
merged = pd.merge(transactions, exchange_rates, on='date', how='left')


# Функция для конвертации в USD
def convert_to_usd(row):
    if row['currency'] == 'USD':
        return row['amount']
    rate = row[row['currency']]
    return row['amount'] / rate if rate != 0 else 0


# Применяем конвертацию
merged['amount_usd'] = merged.apply(convert_to_usd, axis=1)

# Фильтруем мошеннические операции
fraud_transactions = merged[merged['is_fraud'] == True]

# Проверяем, есть ли данные
if len(fraud_transactions) == 0:
    print("Нет мошеннических операций для анализа")
else:
    # Рассчитываем стандартное отклонение
    std_dev = fraud_transactions['amount_usd'].std()

    # Округляем вверх до целого
    rounded_std = math.ceil(std_dev)

    # Выводим результаты
    print(f"Среднеквадратичное отклонение до округления: {std_dev:.2f}")
    print(f"Среднеквадратичное отклонение после округления вверх: {rounded_std}")

    # Дополнительная информация для проверки
    print(f"\nКоличество мошеннических операций: {len(fraud_transactions)}")
    print("Топ-5 самых крупных мошеннических операций (USD):")
    print(fraud_transactions[['amount_usd', 'currency', 'vendor_type']]
          .sort_values('amount_usd', ascending=False).head().to_string())