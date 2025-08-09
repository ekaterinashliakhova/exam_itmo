import pandas as pd
import numpy as np

# Загрузка данных
df = pd.read_parquet('/Users/ekaterinashlyakhova/Documents/GitHub/exam_itmo/transaction_fraud_data.parquet')

# Извлекаем количество уникальных продавцов за последний час для каждой транзакции
df['unique_merchants'] = df['last_hour_activity'].apply(lambda x: x['unique_merchants'] if pd.notnull(x) else 0)

# Группируем по клиенту и вычисляем медиану уникальных продавцов
client_medians = df.groupby('customer_id')['unique_merchants'].median().reset_index()

# Вычисляем 95-й квантиль по всем медианам
threshold = client_medians['unique_merchants'].quantile(0.95)

# Находим клиентов, чья медиана строго превышает порог
dangerous_clients = client_medians[client_medians['unique_merchants'] > threshold]

# Получаем количество таких клиентов
result = len(dangerous_clients)

print(result)