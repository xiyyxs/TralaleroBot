import logging
import random
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)

from responses import (
    GREETINGS,
    MEMES,
    ROFL_RESPONSES,
    RANDOM_REACTIONS,
    QUIZ_QUESTIONS,
    TRALALA_PHRASES,
    INSULTS,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "ТВОЙ_ТОКЕН_СЮДА")


# ─── /start ────────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    greeting = random.choice(GREETINGS).format(name=user.first_name)
    keyboard = [
        [
            InlineKeyboardButton("🦆 MEME", callback_data="meme"),
            InlineKeyboardButton("💀 ROFL", callback_data="rofl"),
        ],
        [
            InlineKeyboardButton("🎯 QUIZ", callback_data="quiz"),
            InlineKeyboardButton("🎵 TRALALA", callback_data="tralala"),
        ],
        [InlineKeyboardButton("🤬 ОБОССАТЬ МЕНЯ", callback_data="insult")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(greeting, reply_markup=reply_markup)


# ─── /meme ─────────────────────────────────────────────────────────────────────
async def meme_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    meme = random.choice(MEMES)
    await update.message.reply_text(meme)


# ─── /rofl ─────────────────────────────────────────────────────────────────────
async def rofl_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    rofl = random.choice(ROFL_RESPONSES)
    await update.message.reply_text(rofl)


# ─── /tralala ──────────────────────────────────────────────────────────────────
async def tralala_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    phrase = random.choice(TRALALA_PHRASES)
    await update.message.reply_text(phrase)


# ─── /insult ───────────────────────────────────────────────────────────────────
async def insult_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    insult = random.choice(INSULTS).format(name=user.first_name)
    await update.message.reply_text(insult)


# ─── /quiz ─────────────────────────────────────────────────────────────────────
async def quiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question_data = random.choice(QUIZ_QUESTIONS)
    context.user_data["quiz_answer"] = question_data["answer"]

    options = question_data["options"]
    random.shuffle(options)

    keyboard = [[InlineKeyboardButton(opt, callback_data=f"quiz_{opt}")] for opt in options]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"🧠 QUIZ TIME, БЛЯТЬ!\n\n{question_data['question']}\n\nВЫБИРАЙ, ТУПОЙ КРЕТИНО!",
        reply_markup=reply_markup,
    )


# ─── Callback handler ──────────────────────────────────────────────────────────
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "meme":
        await query.edit_message_text(random.choice(MEMES))

    elif data == "rofl":
        await query.edit_message_text(random.choice(ROFL_RESPONSES))

    elif data == "tralala":
        await query.edit_message_text(random.choice(TRALALA_PHRASES))

    elif data == "insult":
        user = query.from_user
        insult = random.choice(INSULTS).format(name=user.first_name)
        await query.edit_message_text(insult)

    elif data == "quiz":
        question_data = random.choice(QUIZ_QUESTIONS)
        context.user_data["quiz_answer"] = question_data["answer"]
        options = question_data["options"][:]
        random.shuffle(options)
        keyboard = [[InlineKeyboardButton(opt, callback_data=f"quiz_{opt}")] for opt in options]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"🧠 QUIZ TIME, БЛЯТЬ!\n\n{question_data['question']}\n\nВЫБИРАЙ, ТУПОЙ КРЕТИНО!",
            reply_markup=reply_markup,
        )

    elif data.startswith("quiz_"):
        chosen = data[5:]
        correct = context.user_data.get("quiz_answer", "")
        if chosen == correct:
            await query.edit_message_text(
                f"✅ ПРАВИЛЬНО, CAZZO! Даже ты смог, BOMBARDIRO CROCODILO гордится тобой! 🐊💥"
            )
        else:
            await query.edit_message_text(
                f"❌ НЕПРАВИЛЬНО, STUPIDO КАЗЁЛ!\nПравильный ответ: {correct}\n\nTRALALERO TRALALA ПЛАЧЕТ ИЗ-ЗА ТЕБЯ 😭🎵"
            )


# ─── Обработка ЛЮБОГО сообщения ────────────────────────────────────────────────
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.lower() if update.message.text else ""

    # Реагируем на ключевые слова
    if any(w in text for w in ["привет", "хай", "hi", "hello", "salve", "ciao"]):
        user = update.effective_user
        response = random.choice(GREETINGS).format(name=user.first_name)
    elif any(w in text for w in ["мем", "мему", "meme"]):
        response = random.choice(MEMES)
    elif any(w in text for w in ["tralala", "тралала", "tralalero"]):
        response = random.choice(TRALALA_PHRASES)
    elif any(w in text for w in ["rofl", "рофл", "lol", "хаха", "haha", "kek", "кек"]):
        response = random.choice(ROFL_RESPONSES)
    elif any(w in text for w in ["бля", "блять", "нах", "хуй", "пиздец", "ёбан"]):
        response = f"О, МАТЫ УСЛЫШАЛ! ДА ТЫ СВОЙ, FRATELLO МОЙ! 🤌\n\n{random.choice(TRALALA_PHRASES)}"
    else:
        # Случайная реакция на любое сообщение
        response = random.choice(RANDOM_REACTIONS)

    await update.message.reply_text(response)


# ─── Запуск ────────────────────────────────────────────────────────────────────
def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("meme", meme_command))
    app.add_handler(CommandHandler("rofl", rofl_command))
    app.add_handler(CommandHandler("tralala", tralala_command))
    app.add_handler(CommandHandler("insult", insult_command))
    app.add_handler(CommandHandler("quiz", quiz_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("🦆 TRALALERO TRALALA BOT ЗАПУЩЕН! BOMBARDIRO CROCODILO ОДОБРЯЕТ!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
