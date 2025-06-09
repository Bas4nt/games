import os
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv

# ✅ Load environment variables from .env file (local use only)
load_dotenv()

# ✅ Get the token from the environment
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("❌ Telegram bot token not set. Please set the TOKEN environment variable.")

# ✅ Create updater and dispatcher
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# ✅ Import your UNO handlers
from handlers.uno import uno_join, uno_start, uno_play, uno_hand, uno_status

# ✅ Register UNO command handlers
dispatcher.add_handler(CommandHandler("uno_join", uno_join))
dispatcher.add_handler(CommandHandler("uno_start", uno_start))
dispatcher.add_handler(CommandHandler("play", uno_play))
dispatcher.add_handler(CommandHandler("uno_hand", uno_hand))
dispatcher.add_handler(CommandHandler("uno_status", uno_status))

# ✅ Start polling
if __name__ == "__main__":
    print("🤖 UNO Bot is running...")
    updater.start_polling()
    updater.idle()
