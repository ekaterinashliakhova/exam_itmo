import json
import re
from fuzzywuzzy import fuzz

DATA_FILE = "task_49/data/programs.json"

TAG_KEYWORDS = {
    "ml": ["machine learning", "машин", "ml", "нейрон", "нейрос", "deep learning", "глубок"],
    "math": ["матем", "анализ", "линейн", "статист", "probability", "вероятн"],
    "cs": ["программир", "алгоритм", "систем", "software", "архитектур"],
    "nlp": ["обработка естественного", "nlp", "язык", "linguistic", "nlp"],
    "product": ["product", "продукт", "управлен", "product management", "стратегия"],
    "analytics": ["analytics", "аналитик", "data", "анализа", "data science"],
    "vision": ["computer vision", "vision", "изображен"],
    "ethics": ["этика", "правов", "регул"]
}

def load_programs(path=DATA_FILE):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def score_course_for_tags(course_name, tags):
    name = course_name.lower()
    score = 0
    for tag in tags:
        kws = TAG_KEYWORDS.get(tag, [])
        for kw in kws:
            if kw in name:
                score += 10
            else:
                # fuzzy check
                if fuzz.partial_ratio(kw.lower(), name) > 80:
                    score += 6
    return score

def recommend(program_key, programs, user_tags, top_n=7):
    prog = programs.get(program_key, {})
    courses = prog.get("courses", [])
    scored = []
    for c in courses:
        name = c.get("name","")
        s = score_course_for_tags(name, user_tags)
        if s>0:
            scored.append((s, name))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [name for _, name in scored[:top_n]]

if name == "__main__":
    import sys
    progs = load_programs()
    # пример: python recommender.py ai ml product
    if len(sys.argv) < 3:
        print("Usage: recommender.py <program_key> <tag1> [tag2 ...]")
        sys.exit(1)
    program_key = sys.argv[1]
    tags = sys.argv[2:]
    rec = recommend(program_key, progs, tags)
    print("Recommendations:")
    for r in rec:
        print("-", r)