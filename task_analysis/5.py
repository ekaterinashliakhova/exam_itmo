import pandas as pd

# Загрузка данных
df = pd.read_parquet('/Users/ekaterinashlyakhova/Documents/GitHub/exam_itmo/transaction_fraud_data.parquet')

# Фильтруем, исключая "Unknown City"
df_known = df[df['city'] != 'Unknown City']

# Группируем по городам и считаем среднюю сумму
city_avg = df_known.groupby('city')['amount'].mean()

# Находим город с максимальной средней суммой
max_city = city_avg.idxmax()

print(max_city)