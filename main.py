import os
from flask import Flask, request
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import Update

TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)
bot_app = ApplicationBuilder().token(TOKEN).build()

# ========== HANDLERS ==========
async def start(update, context):
    await update.message.reply_text("🤖 Bot funcionando via Webhook no Render!")

bot_app.add_handler(CommandHandler("start", start))

# ========== FLASK ==========
@app.route("/")
def home():
    return "Bot ativo com webhook!", 200

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return "OK", 200

# ========== STARTUP ==========
if __name__ == "__main__":
    import asyncio

    async def setup():
        webhook_url = f"https://telegram-odds-bot.onrender.com/webhook/{TOKEN}"
        await bot_app.bot.set_webhook(webhook_url)
        print("Webhook configurado:", webhook_url)

    asyncio.run(setup())

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
