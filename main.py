import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ============================
# CONFIGURAÇÃO DO BOT
# ============================
TOKEN = os.environ.get("BOT_TOKEN", "8240785502:AAEHjQ0Ul2pEso8vTidrVUxbtV982LrRWAg87ef82debbd5ec8")

app_telegram = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot funcionando no Render!")

app_telegram.add_handler(CommandHandler("start", start))


# ============================
# FLASK - NECESSÁRIO PARA O RENDER
# ============================
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Bot rodando no Render!"

@flask_app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, app_telegram.bot)
    app_telegram.process_update(update)
    return "OK", 200


# ============================
# INICIALIZAÇÃO
# ============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    import threading

    # Rodar o Telegram em paralelo
    def run_bot():
        app_telegram.run_polling()

    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    # Rodar Flask
    flask_app.run(host="0.0.0.0", port=port)

