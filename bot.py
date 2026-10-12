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

# Channels ki IDs (Updated)
SOURCE_CHANNEL = -1003873597935
TARGET_CHANNEL = -1004490293383

# Logging setup
logging.basicConfig(level=logging.INFO)

# Client initialize karein
client = TelegramClient(StringSession(string_session), api_id, api_hash)

async def fast_transfer_videos():
    print("Bypass transfer (Download & Re-upload) shuru ho gaya hai...")
    uploaded_count = 0
    
    async with client:
        # Purane se naye kram mein messages padhenge
        async for message in client.iter_messages(SOURCE_CHANNEL, reverse=True):
            file_path = None
            try:
                # Check karein ki message mein video hai ya nahi
                if message.video or (message.document and 'video' in message.document.mime_type):
                    print(f"📥 Video download ki ja rahi hai (ID: {message.id})...")
                    
                    # Forward restriction bypass karne ke liye pehle media download karein
                    file_path = await message.download_media()
                    
                    if file_path and os.path.exists(file_path):
                        print(f"📤 Target channel par fresh upload ho rahi hai...")
                        
                        # Target channel par re-upload karein (Caption bilkul hata diya gaya hai)
                        await client.send_file(
                            TARGET_CHANNEL, 
                            file_path, 
                            caption=None,
                            supports_streaming=True
                        )
                        
                        uploaded_count += 1
                        print(f"✅ Successfully sent count: {uploaded_count}")
                    else:
                        print(f"⚠️ File download nahi ho saki: {message.id}")
                    
                    # Agar 100 videos ho jayein tab 5 minute ka rest lein taaki flood wait na aaye
                    if uploaded_count % 100 == 0:
                        print("100 videos ho chuki hain, 5 minute ka rest liya ja raha hai...")
                        await asyncio.sleep(300)
                    else:
                        # Bina kisi rukawat ke tezi se bhejne ke liye chhota sa gap
                        await asyncio.sleep(0.5)
                        
            except Exception as e:
                print(f"❌ Error aa gaya: {e}")
                continue
                
            finally:
                # Temporary file ko delete karein taaki Railway disk space full na ho
                if file_path and os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except Exception as del_err:
                        print(f"⚠️ Temp file delete karne mein error: {del_err}")
                
    print("Sabhi videos successfully transfer ho chuke hain!")

def main():
    with client:
        client.loop.run_until_complete(fast_transfer_videos())

if __name__ == '__main__':
    main()
