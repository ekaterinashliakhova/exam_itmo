import pandas as pd
import math

# Загрузка данных
df = pd.read_parquet('/Users/ekaterinashlyakhova/Documents/GitHub/exam_itmo/transaction_fraud_data.parquet')

# Фильтруем транзакции высокорисковых продавцов
high_risk_transactions = df[df['is_high_risk_vendor'] == True]

# Считаем общее количество транзакций у высокорисковых продавцов
total_high_risk = len(high_risk_transactions)

# Считаем количество мошеннических транзакций у высокорисковых продавцов
fraud_high_risk = high_risk_transactions['is_fraud'].sum()

# Рассчитываем долю мошенничества
fraud_ratio = fraud_high_risk / total_high_risk if total_high_risk > 0 else 0

# Округляем вверх до 1 знака после запятой
rounded_ratio = math.ceil(fraud_ratio * 10) / 10

# Выводим результаты
print(f"Доля мошенничества до округления: {fraud_ratio:.4f}")
print(f"Доля мошенничества после округления: {rounded_ratio:.1f}")