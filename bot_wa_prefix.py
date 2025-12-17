from flask import Flask, request
import requests
import json

app = Flask(__name__)

ACCESS_TOKEN = "ISI_ACCESS_TOKEN_KAMU"
PHONE_NUMBER_ID = "ISI_PHONE_NUMBER_ID"
VERIFY_TOKEN = "VERIFIKASI_TOKEN_KAMU"

# DATA PREFIX
PREFIX = {
    "telkomsel": "0811, 0812, 0813, 0821, 0822, 0823, 0851, 0852, 0853",
    "indosat": "0814, 0815, 0816, 0855, 0856, 0857, 0858",
    "xl": "0817, 0818, 0819, 0859, 0877, 0878",
    "tri": "0895, 0896, 0897, 0898, 0899",
    "axis": "0831, 0832, 0833, 0838",
    "smartfren": "0881, 0882, 0883, 0884, 0885, 0886, 0887, 0888"
}

def send_message(to, text):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }
    requests.post(url, headers=headers, json=data)

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid token"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = message["from"]
        text = message["text"]["body"].lower()

        if text.startswith("prefix"):
            operator = text.replace("prefix", "").strip()
            if operator in PREFIX:
                reply = f"📱 PREFIX {operator.upper()}:\n{PREFIX[operator]}"
            else:
                reply = "❌ Operator tidak ditemukan\n\nContoh:\nprefix telkomsel"
        else:
            reply = (
                "🤖 BOT PREFIX NOMOR\n\n"
                "Perintah:\n"
                "prefix telkomsel\n"
                "prefix indosat\n"
                "prefix xl\n"
                "prefix tri\n"
                "prefix axis\n"
                "prefix smartfren"
            )

        send_message(sender, reply)

    except Exception as e:
        print("Error:", e)

    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000)
