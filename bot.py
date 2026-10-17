import logging
import asyncio
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Aapki API Credentials
api_id = 38322948
api_hash = '71abd5e892c8ecd676cd3460fb2289fb'

# Railway ke Environment Variable se String Session
string_session = os.environ.get('SESSION_STRING', '')

if not string_session:
    print("CRITICAL ERROR: Railway variables mein 'SESSION_STRING' nahi mila!")
    exit(1)

# Multiple Source Channels ki List
SOURCE_CHANNELS = [
-1003863501103,
]

# Target Channel jahan saari videos aayengi
TARGET_CHANNEL = -1004483108196

# Duplicate videos rokne ke liye memory set
processed_files = set()

# Logging setup
logging.basicConfig(level=logging.INFO)

# Client initialize karein
client = TelegramClient(StringSession(string_session), api_id, api_hash)

async def process_and_send_video(message):
    try:
        # Check karein ki message mein video hai ya nahi
        if message.video or (message.document and 'video' in message.document.mime_type):
            
            media_obj = message.video or message.document
            media_id = getattr(media_obj, 'id', None)
            
            if media_id and media_id in processed_files:
                return
            
            print(f"🚀 Instant Sending (Message ID: {message.id})...")
            
            # 🛑 NO DOWNLOAD REQUIRED: Direct media object bhej raha hai (Bina Tag ke)
            await client.send_file(
                TARGET_CHANNEL, 
                message.media, 
                caption=message.text if message.text else None,
                supports_streaming=True
            )
            
            if media_id:
                processed_files.add(media_id)
                
            print(f"✅ Successfully Sent (Clean & Fast) ID: {message.id}")
            
    except Exception as e:
        print(f"❌ Error aa gaya: {e}")

async def main_runner():
    print("🤖 Ultra-Fast Direct Media Sender Bot chalu ho gaya hai...")
    
    # 1. Pehle purane messages ko transfer karega
    for source_id in SOURCE_CHANNELS:
        print(f"📥 Scanning old messages in {source_id}...")
        async for message in client.iter_messages(source_id, reverse=True):
            await process_and_send_video(message)
            await asyncio.sleep(0.1)
            
    print("🎉 Sync complete! Ab Live Mode active hai.")

# 2. Live New Messages ke liye Event Listener
@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def live_transfer_handler(event):
    await process_and_send_video(event.message)

def main():
    with client:
        client.loop.run_until_complete(main_runner())
        client.run_until_disconnected()

if __name__ == '__main__':
    main()
    
