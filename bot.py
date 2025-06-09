
import os
from handlers.uno import uno_join, uno_start, uno_play, uno_hand, uno_status
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("⚠️ TOKEN not set in environment variables!")

dispatcher.add_handler(CommandHandler("uno_join", uno_join))
dispatcher.add_handler(CommandHandler("uno_start", uno_start))
dispatcher.add_handler(CommandHandler("play", uno_play))
dispatcher.add_handler(CommandHandler("uno_hand", uno_hand))
dispatcher.add_handler(CommandHandler("uno_status", uno_status))
