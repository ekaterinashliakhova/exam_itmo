import pandas as pd

# Загрузка данных
df = pd.read_parquet('/Users/ekaterinashlyakhova/Documents/GitHub/exam_itmo/transaction_fraud_data.parquet')

# Фильтруем fast_food транзакции и исключаем Unknown City/NaN
fast_food_transactions = df[
    (df['vendor_type'] == 'fast_food') &
    (df['city'].notna()) &
    (df['city'] != 'Unknown City')
    ]

# Если нет подходящих данных
if fast_food_transactions.empty:
    print("Нет данных о fast_food транзакциях с указанным городом.")
else:
    # Группируем по городу и считаем средний чек
    avg_amount = fast_food_transactions.groupby('city')['amount'].mean()

    # Город с максимальным средним чеком
    city = avg_amount.idxmax()
    max_avg = avg_amount.max()

    print(f"Город с самым высоким средним чеком (fast_food): {city} (${max_avg:.2f})")

    # Дополнительно: топ-5 городов
    print("\nТоп-5 городов по среднему чеку:")
    print(avg_amount.sort_values(ascending=False).head().round(2))