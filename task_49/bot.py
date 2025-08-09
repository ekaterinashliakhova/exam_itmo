import os
import json
import logging
import re
from fuzzywuzzy import fuzz
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler

DATA_FILE = "task_49/data/programs.json"
TELEGRAM_TOKEN = os.environ.get("8220942309:AAEXzul2NOGELdIalp3ehyOw7AqA-jAkoKo")  # установите в окружении

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STATE_WAIT_PROFILE = 1

def load_programs():
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)

PROGRAMS = load_programs()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот-помощник по двум магистерским программам:\n"
        "1) AI\n2) AI Product\n\n"
        "Сначала расскажите, пожалуйста, кратко о вашем бэкграунде (например: 'программист, ML, нет бизнес-опыта' или выберите теги: ml, math, cs, product, analytics)."
    )
    return STATE_WAIT_PROFILE

async def profile_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    # Примитивная экстракция тегов
    tags = []
    for tag in ["ml","math","cs","product","analytics","nlp","vision","business","ux"]:
        if tag in text:
            tags.append(tag)
    if not tags:
        # пытаемся найти слова
        if "машин" in text or "нейрон" in text:
            tags.append("ml")
        if "матем" in text:
            tags.append("math")
        if "программ" in text:
            tags.append("cs")
        if "продукт" in text:
            tags.append("product")
    context.user_data["tags"] = tags
    await update.message.reply_text(
        f"Принято. Теги: {tags or 'не распознаны'}.\n"
        "Теперь задайте вопрос по учебным планам (напр., 'Какие элективы по NLP есть в программе AI?')\n"
        "Я буду отвечать только на вопросы, релевантные содержимому этих двух магистратур."
    )
    return ConversationHandler.END

def is_relevant_question(question, programs=PROGRAMS, threshold=70):
    # считаем релевантной, если в вопросе встречается название курса (fuzzy) или ключевое слово совпадающее с курсом
    q = question.lower()
    for prog_key, prog in programs.items():
        for c in prog.get("courses", []):
            name = c.get("name","").lower()
            # direct word intersection
            for token in re.findall(r'\w{3,}', name):
                if token in q:
                    return True
            # fuzzy compare
            if fuzz.partial_ratio(name, q) > threshold or fuzz.partial_ratio(q, name) > threshold:
                return True
    return False

def find_best_matches(question, programs=PROGRAMS, top_n=5):
    q = question.lower()
    matches = []
    for prog_key, prog in programs.items():
        for c in prog.get("courses", []):
            name = c.get("name","")
            score = max(fuzz.partial_ratio(q, name.lower()), fuzz.partial_ratio(name.lower(), q))
            if score > 50:
                matches.append((score, prog_key, name))
    matches.sort(reverse=True)
    return matches[:top_n]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not is_relevant_question(text):
        await update.message.reply_text(
            "Извините, я могу отвечать только на вопросы, связанные с содержимым программ магистратур AI и AI Product (учебные планы, дисциплины, рекомендации по выбору элективов)."
        )
        return

    # если в сессии есть теги — использовать recommender для персонализации
    tags = context.user_data.get("tags", [])
    # примитив: если пользователь просит рекомендации
    if any(w in text.lower() for w in ["рекоменд", "что взять", "посовет", "элект"]):
        # определим про какую программу спрашивает
        program_choice = None
        if "ai product" in text.lower() or "product" in text.lower():
            program_choice = "ai_product"
        elif "ai" in text.lower() and "product" not in text.lower():
            program_choice = "ai"# fallback: если не ясно — предложим оба
        from recommender import recommend
        prog_keys = [program_choice] if program_choice else list(PROGRAMS.keys())
        replies = []
        for pk in prog_keys:
            recs = recommend(pk, PROGRAMS, tags or ["ml","product"])  # дефолт теги если не заданы
            replies.append(f"Рекомендации для {pk}:\n" + ("\n".join(f"- {r}" for r in recs) if recs else "Нет релевантных курсов."))
        await update.message.reply_text("\n\n".join(replies))
        return

    # иначе — возвращаем совпадающие курсы и отрывки
    matches = find_best_matches(text)
    if not matches:
        await update.message.reply_text("Не нашёл ничего релевантного в учебных планах.")
        return
    resp_lines = []
    for score, prog_key, name in matches:
        resp_lines.append(f"[{prog_key}] {name} (score {score})")
    await update.message.reply_text("Найденные дисциплины:\n" + "\n".join(resp_lines))

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start — начать\n/help — помощь\nПример вопросов: 'Какие элективы по NLP есть в AI?', 'Что взять из элективов если я product менеджер?'")

def main():
    if TELEGRAM_TOKEN is None:
        raise RuntimeError("Set TELEGRAM_TOKEN env var.")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={STATE_WAIT_PROFILE: [MessageHandler(filters.TEXT & ~filters.COMMAND, profile_received)]},
        fallbacks=[CommandHandler("help", help_cmd)],
    )

    app.add_handler(conv)
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot started")
    app.run_polling()

if name == "__main__":
    main()