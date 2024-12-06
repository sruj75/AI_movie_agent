from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import ParseMode
from Agentic_workflow.llm_setup import agent
import os

def start(update, context):
    welcome_msg = (
        "*Welcome to your Personal Movie Booking Assistant!*\n"
        "Ask me something like: '_I want to watch Avengers: Endgame tonight at a nearby theater._'"
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=welcome_msg,
        parse_mode=ParseMode.MARKDOWN
    )

def handle_message(update, context):
    user_input = update.message.text.strip()
    if user_input.lower() in ["exit", "quit"]:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Goodbye!")
        return

    # Process the user query through the plan-and-execute agent
    response = agent.run(user_input)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def setup_telegram_bot():
    # Set your Telegram Bot Token as an environment variable or paste it directly here
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")  # or "YOUR_TELEGRAM_BOT_TOKEN_HERE"

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling() 