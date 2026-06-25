import asyncio
from io import BytesIO
import qrcode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ====== CONFIGURATION ======
TOKEN = "8522802558:AAEuL_8BiS2QbJjGBzzAkbedYN0N9-tw4NU"
UPI_ID = "Q691189350@ybl"
ADMIN_ID = "8655565578" 
BANNER_URL = "https://pic-link-bot.lovable.app/i/telegram-1779454035738-e9821961.jpg"
PREMIUM_LINK = "https://t.me/+mH3_WFgKWx81YWQ9"
DEMO_LINK = "https://telegra.ph/New-Collection-2026-06-01"

CATEGORIES = {
    "desi": {"name": "💦 Real Ind!an Dēsi P0rn 🫦", "price": 69, "days": "Lifetime", "count": "50,000+", "videos": ["https://files.catbox.moe/lbqulg.mp4", "https://files.catbox.moe/7sdo4a.mp4", "https://files.catbox.moe/lbqulg.mp4"]},
    "child": {"name": "🌝 ¢𝐡!𝐥𝐝 𝐏𝟎𝐫𝐧 𝐈𝐧𝐝!𝐚𝐧 ⚡️⚡️", "price": 99, "days": "Lifetime", "count": "50,000+", "videos": ["https://files.catbox.moe/1b9zja.mp4", "https://files.catbox.moe/i02d8l.mp4", "https://files.catbox.moe/1b9zja.mp4"]},
    "mom": {"name": "🥶 𝐌0𝐦 & 𝐒0𝐧 𝐕¡𝐝𝐞𝐨𝐬 😱", "price": 149, "days": "Lifetime", "count": "50,000+", "videos": ["https://files.catbox.moe/agntne.mp4", "https://files.catbox.moe/y4q779.mp4", "https://files.catbox.moe/agntne.mp4"]},
    "rape": {"name": "💀 𝐑@𝐩€ 𝐜@𝐬𝐞 𝐢𝐧𝐝¡𝐚𝐧 💢🌚", "price": 199, "days": "Lifetime d", "count": "50,000+", "videos": ["https://files.catbox.moe/lr228r.mp4", "https://files.catbox.moe/ht1t5c.mp4", "https://files.catbox.moe/lr228r.mp4"]}
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🎉 𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 😋\n\n"
        "✨ 𝐆𝐞𝐭 𝐞𝐱𝐜𝐥𝐮𝐬𝐢𝐯𝐞 𝐚𝐜𝐜𝐞𝐬𝐬 𝐭𝐨 𝐩𝐫𝐞𝐦𝐢𝐮𝐦 𝐜𝐨𝐧𝐭𝐞𝐧𝐭\n"
        "💰 𝐀𝐟𝐟𝐨𝐫𝐝𝐚𝐛𝐥𝐞 𝐩𝐥𝐚𝐧𝐬 𝐬𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐚𝐭 𝐣𝐮𝐬𝐭 ₹6𝟗\n\n"
        "🥵 𝐀𝐋𝐋 𝐓𝐘𝐏𝐄 𝐏𝐎𝐑𝐍 𝐕𝐈𝐃𝐄𝐎𝐒 𝐀𝐕𝐀𝐈𝐋𝐀𝐁𝐋𝐄 🥵\n\n"
        "💦 𝐑𝐞𝐚𝐥 𝐈𝐧𝐝!𝐚𝐧 𝐃ē𝐬𝐢 𝐏𝟎𝐫𝐧 🫦 𝟓𝟎𝟎𝟎𝟎+ 𝐕!𝐝𝐞𝐨𝐬\n"
        "🌝 ¢𝐡!𝐥𝐝 𝐏𝟎𝐫𝐧 𝐈𝐧𝐝!𝐚𝐧 ⚡️⚡️   𝟓𝟎𝟎𝟎𝟎+ 𝐕!𝐝𝐞𝐨𝐬💥\n"
        "🥶 𝐌0𝐦 & 𝐒0𝐧 𝐕¡𝐝𝐞𝐨𝐬 😱    𝟓𝟎𝟎𝟎𝟎+ 𝐕!𝐝𝐞𝐨𝐬\n"
        "💀 𝐑@𝐩€ 𝐜@𝐬𝐞 𝐢𝐧𝐝¡𝐚𝐧 💢🌚   𝟓𝟎𝟎𝟎𝟎+ 𝐕!𝐝𝐞𝐨𝐬\n\n"
        "🚀 𝐓𝐨𝐭𝐚𝐥 𝟏𝟎𝟎𝟎𝟎𝟎𝟎 𝐕!𝐝𝐞𝐨𝐬 𝐒𝐭0𝐜𝐤 ✅\n"
        "🚀 𝐕𝐚𝐥𝐢𝐝𝐢𝐭𝐲 :- 𝐋𝐢𝐟𝐞𝐭𝐢𝐦𝐞 ✅\n\n"
        f"🔗 𝐃𝐄𝐌𝐎 👇 {DEMO_LINK}\n\n"
        "👇 𝐂𝐇𝐎𝐎𝐒𝐄 𝐀 𝐏𝐋𝐀𝐍 👇"
    )
    keyboard = [
        [InlineKeyboardButton(f"{CATEGORIES['desi']['name']} — ₹{CATEGORIES['desi']['price']} / {CATEGORIES['desi']['days']}", callback_data="buy_desi")],
        [InlineKeyboardButton(f"{CATEGORIES['child']['name']} — ₹{CATEGORIES['child']['price']} / {CATEGORIES['child']['days']}", callback_data="buy_child")],
        [InlineKeyboardButton(f"{CATEGORIES['mom']['name']} — ₹{CATEGORIES['mom']['price']} / {CATEGORIES['mom']['days']}", callback_data="buy_mom")],
        [InlineKeyboardButton(f"{CATEGORIES['rape']['name']} — ₹{CATEGORIES['rape']['price']} / {CATEGORIES['rape']['days']}", callback_data="buy_rape")],
        [InlineKeyboardButton("📖 How to Use", callback_data="how_to"), InlineKeyboardButton("🚨 Report Issue", callback_data="report")]
    ]
    await update.message.reply_photo(photo=BANNER_URL, caption=welcome_text, reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("buy_"):
        key = query.data.split("_")[1]
        data = CATEGORIES[key]
        for v in data['videos']:
            await context.bot.send_video(query.message.chat_id, video=v)
            await asyncio.sleep(0.5)
            
        qr = qrcode.make(f"upi://pay?pa={UPI_ID}&am={data['price']}&cu=INR")
        bio = BytesIO()
        qr.save(bio, "PNG")
        bio.seek(0)
        
        caption = (
            f"💳 **PAYMENT BILL**\n\n"
            f"📂 Category: {data['name']}\n"
            f"📊 Video Count: {data['count']}\n"
            f"⏳ Validity: {data['days']}\n"
            f"💰 Payable Amount: ₹{data['price']}\n\n"
            "✅ Pay karke 'I Have Paid' dabayein."
        )
        await context.bot.send_photo(query.message.chat_id, photo=bio, caption=caption, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ I Have Paid", callback_data="ask_proof")]]))

    elif query.data == "report":
        await query.message.reply_text("🚨 Report an Issue\n\nPlease describe your issue or send a screenshot. We'll get back to you as soon as possible.")
    elif query.data == "how_to":
        await query.message.reply_text("📖 How to use\n\n1. Select category.\n2. Scan QR & pay.\n3. Click 'I Have Paid' & send screenshot.")
    elif query.data == "ask_proof":
        await query.message.reply_text("📸 Please send your payment screenshot.")
        context.user_data['waiting_for_proof'] = True
    elif query.data.startswith(("approve_", "reject_")):
        action, user_id = query.data.split("_")
        await context.bot.send_message(user_id, f"Payment {action.capitalize()}ed! Link: {PREMIUM_LINK}" if action == "approve" else "Payment Rejected.")
        await query.edit_message_caption(caption=f"✅ {action.capitalize()}ed")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('waiting_for_proof'):
        user = update.message.from_user
        keyboard = [[InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}"), InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")]]
        await context.bot.send_photo(ADMIN_ID, photo=update.message.photo[-1].file_id, caption=f"Proof from @{user.username}", reply_markup=InlineKeyboardMarkup(keyboard))
        await update.message.reply_text("✅ Proof sent to admin.")
        context.user_data['waiting_for_proof'] = False

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("Bot is running...")
    app.run_polling()
    
