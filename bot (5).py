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

# Multiple Source Channels ki List
SOURCE_CHANNELS = [
    -1004321038948,
    -1003863501103,
    -1004296863313
]

# Target Channel jahan saari videos aayengi
TARGET_CHANNEL = -1004490293383

# Duplicate videos rokne ke liye global memory set
processed_hashes = set()

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
                
                # 🛑 Duplicate Check: Agar media ka hash pehle se hai, toh skip kar do
                media_hash = getattr(message.file, 'hash', None)
                if media_hash and media_hash in processed_hashes:
                    continue
                
                # Step 1: Pehle Direct Forward try karein (Instant speed ke liye)
                try:
                    await client.forward_messages(TARGET_CHANNEL, message)
                    
                    if media_hash:
                        processed_hashes.add(media_hash)
                        
                    uploaded_count += 1
                    print(f"⚡ [Direct Forward] Sent count from {source_id}: {uploaded_count}")
                    await asyncio.sleep(0.1) # Bahut hi kam gap taaki speed super fast rahe
                    continue # Direct forward ho gaya toh download ka sawal hi nahi uthta!
                
                except Exception:
                    # Agar forward restrict hai, tabhi download aur re-upload par jayega
                    print(f"🔒 Restricted channel, downloading (ID: {message.id})...")
                
                # Step 2: Sirf restricted content ke liye Download & Re-upload
                file_path = await message.download_media()
                
                if file_path and os.path.exists(file_path):
                    await client.send_file(
                        TARGET_CHANNEL, 
                        file_path, 
                        caption=None,
                        supports_streaming=True
                    )
                    
                    if media_hash:
                        processed_hashes.add(media_hash)
                        
                    uploaded_count += 1
                    print(f"✅ [Bypass Upload] Sent count from {source_id}: {uploaded_count}")
                else:
                    print(f"⚠️ File download nahi ho saki: {message.id}")
                
                await asyncio.sleep(0.3)
                    
        except Exception as e:
            print(f"❌ Error aa gaya: {e}")
            continue
            
        finally:
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as del_err:
                    print(f"⚠️ Temp file delete karne mein error: {del_err}")

async def main_runner():
    async with client:
        print("🤖 Lightning Fast Smart Transfer Bot chalu ho gaya hai...")
        
        for source_id in SOURCE_CHANNELS:
            await transfer_from_channel(source_id)
            
        print("🎉 Sabhi channels ka transfer complete ho chuka hai!")

def main():
    with client:
        client.loop.run_until_complete(main_runner())

if __name__ == '__main__':
    main()
