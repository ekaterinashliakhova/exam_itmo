import requests
from bs4 import BeautifulSoup

urls = {
    'ai': 'https://abit.itmo.ru/program/master/ai',
    'ai_product': 'https://abit.itmo.ru/program/master/ai_product'
}


def fetch_curriculum(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Найдем блок с учебным планом
    curriculum_block = soup.find('div', class_='program__curriculum-table')
    if not curriculum_block:
        return "Учебный план не найден."

    # Обычно там таблица или списки, возьмём текст и отформатируем
    rows = curriculum_block.find_all(['tr', 'div'], recursive=True)
    curriculum_text = ''
    for row in rows:
        text = row.get_text(separator=' ', strip=True)
        if text:
            curriculum_text += text + '\n'

    return curriculum_text.strip()


curriculums = {name: fetch_curriculum(url) for name, url in urls.items()}

for program, curriculum in curriculums.items():
    print(f"Учебный план для программы {program}:\n{curriculum[:1000]}...\n")