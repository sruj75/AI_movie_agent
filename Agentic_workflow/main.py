import os
from dotenv import load_dotenv
from Agentic_workflow.telegram_bot import setup_telegram_bot

load_dotenv()

def main():
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
    updater = setup_telegram_bot(TELEGRAM_TOKEN)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main() 