import pandas as pd
import math
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def extended_fraud_analysis(file_path):
    df = pd.read_parquet(file_path)

    plt.style.use('seaborn-v0_8')
    sns.set_theme(style="whitegrid")

    # 1. Анализ по категориям
    category_analysis = df.groupby('vendor_category')['is_fraud'].agg(['mean', 'count'])
    category_analysis['mean_rounded'] = category_analysis['mean'].apply(lambda x: math.ceil(x * 100) / 100)

    # Визуализация анализа по категориям
    plt.figure(figsize=(12, 8))
    top_categories = category_analysis.sort_values('mean', ascending=False).head(10)
    sns.barplot(x=top_categories['mean'], y=top_categories.index)
    plt.title('Топ-10 категорий с самым высоким процентом мошенничества')
    plt.xlabel('Доля мошеннических операций')
    plt.ylabel('Категория')
    plt.tight_layout()
    plt.show()

    # 2. Анализ по времени
    df['hour'] = df['timestamp'].dt.hour
    time_analysis = df.groupby('hour')['is_fraud'].mean()

    # Визуализация временных паттернов
    plt.figure(figsize=(12, 6))
    time_analysis.plot(kind='bar', color='skyblue')
    plt.title('Распределение мошеннических операций по часам')
    plt.xlabel('Час дня')
    plt.ylabel('Доля мошеннических операций')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # 3. Анализ по географии
    geo_analysis = df.groupby('country')['is_fraud'].mean().sort_values(ascending=False)

    # Визуализация географического анализа
    plt.figure(figsize=(12, 6))
    geo_analysis.head(10).plot(kind='bar', color='salmon')
    plt.title('Топ-10 стран с самым высоким процентом мошенничества')
    plt.xlabel('Страна')
    plt.ylabel('Доля мошеннических операций')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # 4. Анализ по устройствам
    device_analysis = df.groupby('device')['is_fraud'].mean().sort_values(ascending=False)

    # Визуализация анализа по устройствам
    plt.figure(figsize=(12, 6))
    device_analysis.head(10).plot(kind='bar', color='lightgreen')
    plt.title('Топ-10 устройств с самым высоким процентом мошенничества')
    plt.xlabel('Устройство')
    plt.ylabel('Доля мошеннических операций')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # Вывод текстовых результатов
    print("1. Анализ по категориям:")
    print(category_analysis.sort_values('mean', ascending=False).head(10))

    print("\n2. Временные паттерны (топ-5 самых рискованных часов):")
    print(time_analysis.sort_values(ascending=False).head())

    print("\n3. Географический анализ (топ-5 самых рискованных стран):")
    print(geo_analysis.head())

    print("\n4. Анализ по устройствам (топ-5 самых рискованных):")
    print(device_analysis.head())

    # Сохранение отчёта
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f'fraud_analysis_report_{timestamp}.txt', 'w') as f:
        f.write("Отчёт по анализу мошеннических операций\n\n")
        f.write("1. Анализ по категориям:\n")
        f.write(category_analysis.sort_values('mean', ascending=False).to_string())
        f.write("\n\n2. Временные паттерны:\n")
        f.write(time_analysis.sort_values(ascending=False).to_string())
        f.write("\n\n3. Географический анализ:\n")
        f.write(geo_analysis.to_string())
        f.write("\n\n4. Анализ по устройствам:\n")
        f.write(device_analysis.to_string())

# Начало анализа
extended_fraud_analysis('/Users/ekaterinashlyakhova/Documents/GitHub/exam_itmo/transaction_fraud_data.parquet')
