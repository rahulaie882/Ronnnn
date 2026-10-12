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

# Multiple Source Channels ki Updated List
SOURCE_CHANNELS = [
    -1004321038948,
    -1003863501103,
    -1004296863313
]

# Ek hi Single Target Channel jahan saari videos upload hongi
TARGET_CHANNEL = -1004490293383

# Logging setup
logging.basicConfig(level=logging.INFO)

# Client initialize karein
client = TelegramClient(StringSession(string_session), api_id, api_hash)

async def transfer_from_channel(source_id):
    print(f"📥 Source channel {source_id} se transfer shuru ho raha hai...")
    uploaded_count = 0
    
    # Purane se naye kram mein messages padhenge
    async for message in client.iter_messages(source_id, reverse=True):
        file_path = None
        try:
            # Check karein ki message mein video hai ya nahi
            if message.video or (message.document and 'video' in message.document.mime_type):
                print(f"📥 Video download ki ja rahi hai (ID: {message.id})...")
                
                # Forward restriction bypass karne ke liye pehle media download karein
                file_path = await message.download_media()
                
                if file_path and os.path.exists(file_path):
                    print(f"📤 Target channel par fresh upload ho rahi hai...")
                    
                    # Target channel par re-upload karein
                    await client.send_file(
                        TARGET_CHANNEL, 
                        file_path, 
                        caption=None,
                        supports_streaming=True
                    )
                    
                    uploaded_count += 1
                    print(f"✅ Successfully sent count from {source_id}: {uploaded_count}")
                else:
                    print(f"⚠️ File download nahi ho saki: {message.id}")
                
                # Flood wait se bachne ke liye chhota sa gap
                await asyncio.sleep(1)
                    
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

async def main_runner():
    async with client:
        print("🤖 Multi-source transfer bot chalu ho gaya hai...")
        
        # Har ek source channel par ek ke baad ek process chalayega
        for source_id in SOURCE_CHANNELS:
            await transfer_from_channel(source_id)
            
        print("🎉 Sabhi source channels ki videos successfully transfer ho chuki hain!")

def main():
    with client:
        client.loop.run_until_complete(main_runner())

if __name__ == '__main__':
    main()
