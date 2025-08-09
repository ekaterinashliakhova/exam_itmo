import pandas as pd

# Загрузка данных
df = pd.read_parquet('/Users/ekaterinashlyakhova/Documents/GitHub/exam_itmo/transaction_fraud_data.parquet')

# Фильтрация мошеннических транзакций и подсчёт по странам
fraud_by_country = df[df['is_fraud']].groupby('country').size().reset_index(name='fraud_count')

# Сортировка и выбор топ-5
top_5_countries = fraud_by_country.sort_values('fraud_count', ascending=False).head(5)['country'].tolist()

# Форматирование ответа
answer = ",".join(top_5_countries)
print(answer)