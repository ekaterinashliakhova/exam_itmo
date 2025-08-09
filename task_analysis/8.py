import pandas as pd
import math

# Загрузка данных
transactions = pd.read_parquet('transaction_fraud_data.parquet')
exchange_rates = pd.read_parquet('historical_currency_exchange.parquet')

# Преобразуем timestamp в дату
transactions['date'] = transactions['timestamp'].dt.date

# Объединяем с курсами валют
merged = pd.merge(transactions, exchange_rates, on='date', how='left')

# Конвертация в USD (исправлено!)
def convert_to_usd(row):
    if row['currency'] == 'USD':
        return row['amount']
    rate = row[row['currency']]
    return row['amount'] / rate if rate != 0 else 0

merged['amount_usd'] = merged.apply(convert_to_usd, axis=1)

# Фильтрация немошеннических операций
legit_transactions = merged[merged['is_fraud'] == False]

# Удаляем нулевые/аномальные значения (если есть)
legit_transactions = legit_transactions[legit_transactions['amount_usd'] > 0]

# Рассчитываем стандартное отклонение
std_dev = legit_transactions['amount_usd'].std()
rounded_std = math.ceil(std_dev)

print(f"Стандартное отклонение (до округления): {std_dev}")
print(f"Результат (округлённый вверх): {rounded_std}")