import logging
from config import BOT_TOKEN, GROUP_ID
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING_FEEDBACK, FEEDBACK_RECEIVED, FEEDBACK_UNSATISFIED = range(3)

reply_keyboard_feedback = [
    ["Да", "Нет"],
]
markup_level = ReplyKeyboardMarkup(reply_keyboard_feedback, one_time_keyboard=True, resize_keyboard=True)

reply_keyboard_satisfaction = [
    ["Да", "Нет"],
]
markup_satisfaction = ReplyKeyboardMarkup(reply_keyboard_satisfaction, one_time_keyboard=True, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Добро пожаловать в медицинский центр "Решение"! Я - ваш виртуальный помощник, '
        'готовый сделать наш сервис качественнее. Ваша обратная связь помогает нам становиться лучше.',
        reply_markup=markup_level,
    )
    await update.message.reply_text(
        "Вы желаете оставить отзыв?",
        reply_markup=markup_level,
    )
    return CHOOSING_FEEDBACK


async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text
    if user_choice == "Да":
        await update.message.reply_text(
            "Вы удовлетворены качеством услуги оказанной вам?",
            reply_markup=markup_satisfaction,
        )
        return FEEDBACK_RECEIVED
    else:
        return ConversationHandler.END


async def feedback_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text
    if user_choice == "Да":
        await update.message.reply_text("Оставьте, пожалуйста, отзыв о нас")
        await update.message.reply_text(
            "Яндекс. Карты (https://clck.ru/3AWvmm)\n"
            "Google maps (https://cick.ru/3AWvrU)\n"
            "2gis (https://clck.ru/3AWvv4)\n"
            "Продокторов (https://clck.ru/3AWvy3)"
        )
    else:
        await update.message.reply_text("Опишите нам проблему с которой вы столкнулись, постараемся её решить")
        return FEEDBACK_UNSATISFIED


async def feedback_unsatisfied(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_feedback = update.message.text

    await context.bot.send_message(chat_id=GROUP_ID, text=user_feedback)

    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_FEEDBACK: [
                MessageHandler(
                    filters.Regex("^(Да|Нет)$"), feedback
                ),
            ],
            FEEDBACK_RECEIVED: [
                MessageHandler(
                    filters.Regex("^(Да|Нет)$"), feedback_received
                ),
            ],
            FEEDBACK_UNSATISFIED: [
                MessageHandler(
                    filters.Regex("^(.+)"), feedback_unsatisfied
                ),
            ],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
