import telebot
import requests
import time

BOT_TOKEN = "8240785502:AAEHjQ0Ul2pEso8vTidrVUxbtV982LrRWAg87ef82debbd5ec8"
API_KEY = "acde250d137c72b8f"

bot = telebot.TeleBot(BOT_TOKEN)

def get_odds():
    url = "https://api.the-odds-api.com/v4/sports/upcoming/odds"
    params = {
        "apiKey": API_KEY,
        "regions": "eu",
        "markets": "h2h,spreads,totals",
    }
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return None
    return r.json()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Bot de Odds Ativado!")

@bot.message_handler(commands=['odds'])
def send_odds(message):
    odds = get_odds()
    if not odds:
        bot.send_message(message.chat.id, "Erro ao buscar odds.")
        return

    for event in odds[:3]:
        text = f"🏆 *{event['sport_title']}*\n\n" \
               f"🆚 {event['home_team']} x {event['away_team']}\n" \
               f"⏰ {event['commence_time']}\n"
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

while True:
    try:
        bot.polling()
    except:
        time.sleep(3)
