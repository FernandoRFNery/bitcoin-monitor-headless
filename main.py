import requests
import time
from urllib.parse import quote

def get_bitcoin_price():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
        data = response.json()
        return data['bitcoin']['usd']
    except Exception as e:
        print(f"Error getting Bitcoin price: {e}")
        return None

def send_whatsapp_message(phone, message, api_key):
    encoded_message = quote(message)
    url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={encoded_message}&apikey={api_key}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Message sent successfully to {phone}")
        else:
            print(f"Failed to send message to {phone}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")

def main():
    API_KEY = "1690058"
    PHONE_NUMBERS = ["555191961507"]  # Add more phone numbers as needed
    CHECK_INTERVAL = 20  # 20 seconds between checks (3 times per minute)
    
    previous_price = None
    
    while True:
        current_price = get_bitcoin_price()
        
        if current_price and previous_price:
            # Only send message if price dropped
            if current_price < previous_price:
                price_drop = previous_price - current_price
                drop_percentage = (price_drop / previous_price) * 100
                
                message = (f"⚠️ Bitcoin Price Drop Alert!\n"
                          f"Previous: ${previous_price:,.2f}\n"
                          f"Current: ${current_price:,.2f}\n"
                          f"Drop: ${price_drop:,.2f} (-{drop_percentage:.2f}%)")
                
                for phone in PHONE_NUMBERS:
                    send_whatsapp_message(phone, message, API_KEY)
        
        previous_price = current_price
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=10000, use_reloader=False)

