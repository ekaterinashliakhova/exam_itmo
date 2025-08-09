import pandas as pd
import math

# Загрузка данных
transactions = pd.read_parquet('/Users/ekaterinashlyakhova/Documents/GitHub/exam_itmo/transaction_fraud_data.parquet')
exchange_rates = pd.read_parquet('/Users/ekaterinashlyakhova/Documents/GitHub/exam_itmo/historical_currency_exchange.parquet')

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

# Фильтруем немошеннические операции
legit_transactions = merged[merged['is_fraud'] == False]

# Рассчитываем среднее значение и округляем вверх
average_usd = legit_transactions['amount_usd'].mean()
rounded_average = math.ceil(average_usd)

print(rounded_average)