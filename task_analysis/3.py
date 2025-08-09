import pandas as pd
import math

# Загрузка данных
df = pd.read_parquet('/Users/ekaterinashlyakhova/Documents/GitHub/exam_itmo/transaction_fraud_data.parquet')

# 1. Преобразуем timestamp в datetime и извлекаем час
df['hour'] = df['timestamp'].dt.floor('H')

# 2. Группируем по клиенту и часу, считаем транзакции
transactions_per_client_hour = df.groupby(['customer_id', 'hour']).size().reset_index(name='tx_count')

# 3. Вычисляем среднее количество транзакций на клиента в час
mean_tx_per_hour = transactions_per_client_hour['tx_count'].mean()

# 4. Округляем вниз до 1 знака после запятой
rounded_mean = math.floor(mean_tx_per_hour * 10) / 10

# Выводим результаты
print(f"Среднее количество транзакций до округления: {mean_tx_per_hour:.2f}")
print(f"Среднее количество транзакций после округления: {rounded_mean:.1f}")