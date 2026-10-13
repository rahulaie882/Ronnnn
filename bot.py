import logging
import asyncio
os = __import__('os')
from telethon import TelegramClient
from telethon.sessions import StringSession

# Aapki Purani API Credentials
api_id = 38322948
api_hash = '71abd5e892c8ecd676cd3460fb2289fb'

# Railway ke Environment Variable se String Session uthayega
string_session = os.environ.get('SESSION_STRING', '')

if not string_session:
    print("CRITICAL ERROR: Railway variables mein 'SESSION_STRING' nahi mila ya khali hai!")
    exit(1)

# Source aur Target Channel ki IDs (Target ke aage -100 zaroori hai)
SOURCE_CHANNEL = -1004476590137
TARGET_CHANNEL = -100447659013  # Yahan -100 lagana compulsory hai

# Duplicate messages rokne ke liye memory set
processed_ids = set()

# Logging setup
logging.basicConfig(level=logging.INFO)

# Client initialize karein
client = TelegramClient(StringSession(string_session), api_id, api_hash)

async def transfer_everything_smart():
    print("🤖 Smart All-in-One Transfer Bot chalu ho gaya hai...")
    sent_count = 0
    
    async with client:
        async for message in client.iter_messages(SOURCE_CHANNEL, reverse=True):
            if message.id in processed_ids:
                continue
                
            file_path = None
            try:
                # Step 1: Pehle Direct Forward try karein
                try:
                    await client.forward_messages(TARGET_CHANNEL, message)
                    processed_ids.add(message.id)
                    sent_count += 1
                    print(f"⚡ [Direct Forward] Sent count: {sent_count}")
                    await asyncio.sleep(0.3)
                    continue
                except Exception:
                    pass
                
                # Step 2: Agar Forwarding Off hai, toh Media ya Text ko handle karein
                if message.media:
                    file_path = await message.download_media()
                    
                    if file_path and os.path.exists(file_path):
                        await client.send_file(
                            TARGET_CHANNEL, 
                            file_path, 
                            caption=message.text if message.text else None,
                            supports_streaming=True
                        )
                        sent_count += 1
                        print(f"✅ [Bypass Media Upload] Sent count: {sent_count}")
                    else:
                        print(f"⚠️ Media download nahi ho saki: {message.id}")
                
                elif message.text:
                    await client.send_message(TARGET_CHANNEL, message.text)
                    sent_count += 1
                    print(f"✅ [Text Sent] Sent count: {sent_count}")
                
                processed_ids.add(message.id)
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"❌ Error message ID {message.id} par: {e}")
                continue
                
            finally:
                if file_path and os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except Exception as del_err:
                        print(f"⚠️ Temp file delete error: {del_err}")
                
    print("🎉 Sabhi messages successfully transfer ho chuke hain!")

def main():
    with client:
        client.loop.run_until_complete(transfer_everything_smart())

if __name__ == '__main__':
    main()
