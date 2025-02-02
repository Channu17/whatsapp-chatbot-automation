from fastapi import FastAPI, Request
import requests
import uvicorn

app = FastAPI()

ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
PHONE_NUMBER_ID = "YOUR_PHONE_NUMBER_ID"

menu = {
    "1": {"name": "Cheeseburger", "price": 8},
    "2": {"name": "Pizza", "price": 10}
}

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    data = await request.json()

    try:
        user_message = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
        sender_number = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
    except KeyError:
        return {"status": "No message received"}

    response = "I didn't understand. Type 'menu' to see options."


    if user_message.lower() == "menu":
        response = "🍽️ Today's Menu:\n1️⃣ Cheeseburger - $8\n2️⃣ Pizza - $10\nReply with the number to order."

    elif user_message in menu:
        item = menu[user_message]
        response = f"✅ You selected {item['name']}.\nPrice: ${item['price']}\nType 'Confirm' to place order."

    send_whatsapp_message(sender_number, response)
    return {"status": "received"}

def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    data = {"messaging_product": "whatsapp", "to": to, "text": {"body": message}}
    requests.post(url, json=data, headers=headers)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
