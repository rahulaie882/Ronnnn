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

# Naya Source Channel aur Target Channel
SOURCE_CHANNEL = -1003855434388
TARGET_CHANNEL = -1004307539975

# File-based tracking taaki restart karne par duplicate videos na jayein
TRACKING_FILE = "sent_hashes.txt"

def load_processed_hashes():
    if os.path.exists(TRACKING_FILE):
        with open(TRACKING_FILE, "r") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_hash(media_hash):
    with open(TRACKING_FILE, "a") as f:
        f.write(f"{media_hash}\n")

processed_hashes = load_processed_hashes()

# Logging setup
logging.basicConfig(level=logging.INFO)

# Client initialize karein
client = TelegramClient(StringSession(string_session), api_id, api_hash)

async def transfer_clean_media():
    print("🤖 Clean Transfer Bot chalu ho gaya hai (-1003855434388 se clean upload)...")
    uploaded_count = 0
    
    async with client:
        # Purane se naye kram mein messages padhenge
        async for message in client.iter_messages(SOURCE_CHANNEL, reverse=True):
            try:
                # Agar message mein media (video/photo) hai
                if message.media:
                    media_hash = getattr(message.file, 'hash', None) if message.file else None
                    
                    # Agar yeh video pehle se bhej di gayi hai, toh skip kar do
                    if media_hash and str(media_hash) in processed_hashes:
                        continue
                    
                    # Fresh send without any forward tag (Clean upload)
                    await client.send_file(
                        TARGET_CHANNEL,
                        message.media,
                        caption=message.text if message.text else None,
                        supports_streaming=True
                    )
                    
                    if media_hash:
                        processed_hashes.add(str(media_hash))
                        save_hash(str(media_hash))
                        
                    uploaded_count += 1
                    print(f"✅ [Fresh Upload & Saved] Sent count: {uploaded_count}")
                    
                elif message.text:
                    # Agar sirf text message hai
                    msg_id_str = f"text_{message.id}"
                    if msg_id_str in processed_hashes:
                        continue
                        
                    await client.send_message(TARGET_CHANNEL, message.text)
                    processed_hashes.add(msg_id_str)
                    save_hash(msg_id_str)
                    
                    uploaded_count += 1
                    print(f"✅ [Text Sent] Sent count: {uploaded_count}")
                
                # Rate limit se bachne ke liye chhota sa gap
                await asyncio.sleep(0.3)
                    
            except Exception as e:
                print(f"❌ Error aa gaya message ID {message.id} par: {e}")
                continue
                
    print("🎉 Sabhi videos bina kisi forward tag ke aur bina duplicate ke transfer ho chuki hain!")

def main():
    with client:
        client.loop.run_until_complete(transfer_clean_media())

if __name__ == '__main__':
    main()
