import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

app = Flask(__name__)
bot_app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot ativo no Render!")

bot_app.add_handler(CommandHandler("start", start))

@app.route("/")
def home():
    return "Bot rodando com webhook!", 200

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    update = Update.de_json(data, bot_app.bot)
    bot_app.process_update(update)
    return "OK", 200

if __name__ == "__main__":
    import asyncio

    async def main():
        url = f"https://telegram-odds-bot.onrender.com/webhook/{TOKEN}"
        await bot_app.bot.set_webhook(url)
        print(f"Webhook configurado: {url}")

    asyncio.get_event_loop().run_until_complete(main())

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
