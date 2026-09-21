import logging
import asyncio
os = __import__('os')
from telethon import TelegramClient
from telethon.sessions import StringSession

# Aapki API Credentials
api_id = 38322948
api_hash = '71abd5e892c8ecd676cd3460fb2289fb'

# Railway ke Environment Variable se String Session uthayega
string_session = os.environ.get('SESSION_STRING', '')

if not string_session:
    print("CRITICAL ERROR: Railway variables mein 'SESSION_STRING' nahi mila ya khali hai!")
    exit(1)

# Channels ki IDs
SOURCE_CHANNEL = -1001624901868
TARGET_CHANNEL = -1004392281798

# Logging setup
logging.basicConfig(level=logging.INFO)

# Client initialize karein
client = TelegramClient(StringSession(string_session), api_id, api_hash)

async def fast_transfer_videos():
    print("Superfast direct transfer shuru ho gaya hai...")
    uploaded_count = 0
    
    async with client:
        # Purane se naye kram mein messages padhenge
        async for message in client.iter_messages(SOURCE_CHANNEL, reverse=True):
            try:
                # Check karein ki message mein video hai ya nahi
                if message.video or (message.document and 'video' in message.document.mime_type):
                    
                    # Direct media object bhejenge bina download kiye
                    await client.send_file(
                        TARGET_CHANNEL, 
                        message.media, 
                        caption=None # Caption bilkul hata diya gaya hai
                    )
                    
                    uploaded_count += 1
                    print(f"Superfast sent count: {uploaded_count}")
                    
                    # Agar 100 videos ho jayein tab 5 minute ka rest lein taaki flood wait na aaye
                    if uploaded_count % 100 == 0:
                        print("100 videos ho chuki hain, 5 minute ka rest liya ja raha hai...")
                        await asyncio.sleep(300)
                    else:
                        # Bina kisi rukawat ke tezi se bhejne ke liye chhota sa gap
                        await asyncio.sleep(0.5)
                        
            except Exception as e:
                print(f"Error aa gaya: {e}")
                continue
                
    print("Sabhi videos successfully transfer ho chuke hain!")

def main():
    with client:
        client.loop.run_until_complete(fast_transfer_videos())

if __name__ == '__main__':
    main()
    
