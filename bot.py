import logging
import asyncio
os = __import__('os')
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# आपकी API Credentials
api_id = 38322948
api_hash = '71abd5e892c8ecd676cd3460fb2289fb'

# Railway के Environment Variable से Session उठाएगा
string_session = os.environ.get('SESSION_STRING', '')

# जो लिंक्स आपने दिए हैं
SOURCE_CHANNEL = 'https://t.me/+jGIqRcawDX4wNjM1'
TARGET_CHANNEL = 'https://t.me/+tDuIpvJe2LM0Y2Yx'

# लॉगिंग सेट अप
logging.basicConfig(level=logging.INFO)

# StringSession का इस्तेमाल करके क्लाइंट इनिशियलाइज करें
client = TelegramClient(StringSession(string_session), api_id, api_hash)

# वीडियो गिनने के लिए काउंटर
uploaded_count = 0

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def download_and_upload_handler(event):
    global uploaded_count
    try:
        # चेक करें कि मैसेज में वीडियो या वीडियो डॉक्यूमेंट है या नहीं
        if event.message.video or (event.message.document and 'video' in event.message.document.mime_type):
            print("नया वीडियो मिल गया, डाउनलोड किया जा रहा है...")
            
            # वीडियो को डाउनलोड करें
            file_path = await event.message.download_media()
            print("डाउनलोड हो गया, 5 सेकंड रुक कर टारगेट चैनल पर अपलोड किया जा रहा है...")
            
            # हर वीडियो के बीच छोटा गैप (5 सेकंड)
            await asyncio.sleep(5)
            
            # बिना फॉरवर्ड टैग के नए वीडियो की तरह अपलोड करें
            await client.send_file(
                TARGET_CHANNEL, 
                file_path, 
                caption=event.message.text
            )
            
            uploaded_count += 1
            print(f"सफलतापूर्वक अपलोड किए गए कुल वीडियो: {uploaded_count}")
            
            # हर 100 वीडियो पूरे होने पर 10 मिनट (600 सेकंड) का ब्रेक
            if uploaded_count % 100 == 0:
                print(f"100 वीडियो पूरे हो चुके हैं! सुरक्षा के लिए अगले 10 मिनट का रेस्ट लिया जा रहा है...")
                await asyncio.sleep(600)  # 600 सेकंड = 10 मिनट
                print("रेस्ट पूरा हुआ, अब आगे के वीडियो अपलोड होंगे।")
                
    except Exception as e:
        print(f"एरर आ गया: {e}")

def main():
    print("यूज़रबॉट Railway पर शुरू हो रहा है...")
    client.start()
    print("यूज़रबॉट लाइव है और वीडियो का इंतज़ार कर रहा है!")
    client.run_until_disconnected()

if __name__ == '__main__':
    main()
  
