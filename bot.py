import logging
import asyncio
os = __import__('os')
from telethon import TelegramClient
from telethon.sessions import StringSession

# Aapki API Credentials
api_id = 38322948
api_hash = '71abd5e892c8ecd676cd3460fb2289fb'

# Railway ke Environment Variable se String Session
string_session = os.environ.get('SESSION_STRING', '')

# Channels ki IDs
SOURCE_CHANNEL = -1001624901868
TARGET_CHANNEL = -1004392281798

# Logging setup
logging.basicConfig(level=logging.INFO)

# Client initialize karein
client = TelegramClient(StringSession(string_session), api_id, api_hash)

async def forward_old_videos():
    print("Userbot shuru ho gaya hai, purane videos scan kiye ja rahe hain...")
    uploaded_count = 0
    
    async with client:
        async for message in client.iter_messages(SOURCE_CHANNEL, reverse=True):
            try:
                if message.video or (message.document and 'video' in message.document.mime_type):
                    print("Clean video mil gaya, download kiya ja raha hai...")
                    
                    file_path = await message.download_media()
                    print("Download ho gaya, target channel par clean upload ho raha hai...")
                    
                    await client.send_file(
                        TARGET_CHANNEL, 
                        file_path, 
                        caption=None
                    )
                    
                    uploaded_count += 1
                    print(f"Safaltaपूर्वक upload kiye gaye kul clean videos: {uploaded_count}")
                    
                    if uploaded_count % 100 == 0:
                        print(f"100 videos poori ho chuki hain! Ab safety ke liye 5 minute ka rest liya ja raha hai...")
                        await asyncio.sleep(300)
                        
            except Exception as e:
                print(f"Error aa gaya is message par: {e}")
                continue
                
    print("Source channel ke saare videos successfully forward ho chuke hain!")

def main():
    with client:
        client.loop.run_until_complete(forward_old_videos())

if __name__ == '__main__':
    main()
    
