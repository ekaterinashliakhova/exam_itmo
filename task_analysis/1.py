import pandas as pd
import math

# Загрузка данных
df = pd.read_parquet('/Users/ekaterinashlyakhova/Documents/GitHub/exam_itmo/transaction_fraud_data.parquet')

# Общее количество транзакций
total_transactions = len(df)

# Количество мошеннических транзакций
fraud_transactions = df['is_fraud'].sum()

# Расчет доли
fraud_ratio = fraud_transactions / total_transactions

# Округление вверх до 1 знака после запятой
fraud_ratio_rounded = math.ceil(fraud_ratio * 10) / 10

# Вывод результатов
print(f"Доля мошеннических транзакций до округления: {fraud_ratio:.4f}")
print(f"Доля мошеннических транзакций после округления вверх: {fraud_ratio_rounded:.1f}")