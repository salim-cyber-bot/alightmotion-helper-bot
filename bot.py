import json
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# ========= ENV =========
BOT_TOKEN = os.getenv("8235928800:AAHyjB-yxeMv7Tk01mh_ABL-k5xm5Q5pIwc")
ADMIN_ID = int(os.getenv("8541526129"))          # your Telegram user ID
ALLOWED_GROUP_ID = int(os.getenv("-1002425643589"))  # your group ID

XML_FILE = "data/xml.json"

# ========= HELPERS =========
def is_private(update: Update):
    return update.effective_chat.type == "private"

def is_allowed_group(update: Update):
    return update.effective_chat.id == ALLOWED_GROUP_ID

def load_xml():
    with open(XML_FILE, "r") as f:
        return json.load(f)

def save_xml(data):
    with open(XML_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ========= COMMON MESSAGES =========
ONLY_GROUP = (
    "⚠️ **Group Only Command**\n"
    "এই কমান্ড শুধু Owner-এর Group-এ কাজ করবে"
)

ACCESS_DENIED = (
    "⛔ **Access Denied**\n\n"
    "This bot is restricted\n"
    "এই bot শুধু Owner-এর Group-এর জন্য"
)

# ========= COMMANDS =========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_private(update):
        await update.message.reply_text(
            "✨ **Welcome!** ✨\n\n"
            "👋 Hello & স্বাগতম\n"
            "This is **Alight Motion Helper Bot**\n\n"
            "📌 This bot works mainly in **GROUP**\n"
            "এই bot মূলত Group-এর জন্য\n\n"
            "Use `/help` for info",
            parse_mode="Markdown"
        )
    else:
        if not is_allowed_group(update):
            await update.message.reply_text(ACCESS_DENIED, parse_mode="Markdown")
            return

        await update.message.reply_text(
            "👋 **Bot Activated**\nUse `/help`",
            parse_mode="Markdown"
        )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_private(update):
        await update.message.reply_text(
            "ℹ️ **Help**\n\n"
            "This bot works only in **Owner Group**\n"
            "এই bot শুধু Owner-এর Group-এ কাজ করবে\n\n"
            "Inbox commands:\n"
            "• /start\n"
            "• /help\n"
            "• /owner",
            parse_mode="Markdown"
        )
        return

    if not is_allowed_group(update):
        await update.message.reply_text(ACCESS_DENIED, parse_mode="Markdown")
        return

    await update.message.reply_text(
        "📜 **Command List**\n\n"
        "/preset\n"
        "/xml\n"
        "/shake\n"
        "/smooth\n"
        "/cc\n"
        "/amexport\n"
        "/owner",
        parse_mode="Markdown"
    )

async def preset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed_group(update):
        await update.message.reply_text(ACCESS_DENIED, parse_mode="Markdown")
        return

    await update.message.reply_text(
        "🎨 **Alight Motion Preset**\n\n"
        "• Shake\n• Smooth\n• CC\n\n"
        "Use `/xml`",
        parse_mode="Markdown"
    )

async def xml_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed_group(update):
        await update.message.reply_text(ACCESS_DENIED, parse_mode="Markdown")
        return

    data = load_xml()
    msg = "📂 **Available XML**\n\n"
    for k in data:
        msg += f"• {data[k]['name']}\n"
    msg += "\nUse: /shake /smooth /cc"

    await update.message.reply_text(msg, parse_mode="Markdown")

async def send_xml(update: Update, context: ContextTypes.DEFAULT_TYPE, key):
    if not is_allowed_group(update):
        await update.message.reply_text(ACCESS_DENIED, parse_mode="Markdown")
        return

    data = load_xml()
    item = data.get(key)

    await update.message.reply_text(
        f"📄 **{item['name']}**\n\n"
        f"🔗 {item['link']}",
        parse_mode="Markdown"
    )

async def amexport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed_group(update):
        await update.message.reply_text(ACCESS_DENIED, parse_mode="Markdown")
        return

    await update.message.reply_text(
        "📤 **AM Export Settings**\n\n"
        "Resolution: 1080p\n"
        "FPS: 30 / 60\n"
        "Bitrate: High\n"
        "Device: Redmi 13C Optimized",
        parse_mode="Markdown"
    )

async def owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 **Owner**\n\n"
        "📱 TikTok:\nhttps://tiktok.com/@YOUR_ID\n\n"
        "▶️ YouTube:\nhttps://youtube.com/@YOUR_CHANNEL",
        parse_mode="Markdown"
    )

# ========= ADMIN =========
async def newxml(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Admin only")
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage:\n/newxml <shake|smooth|cc> <drive_link>"
        )
        return

    key = context.args[0].lower()
    link = context.args[1]

    data = load_xml()
    if key not in data:
        await update.message.reply_text("❌ Invalid XML name")
        return

    data[key]["link"] = link
    save_xml(data)

    await update.message.reply_text("✅ XML Updated Successfully")

# ========= MAIN =========
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("preset", preset))
app.add_handler(CommandHandler("xml", xml_list))
app.add_handler(CommandHandler("shake", lambda u, c: send_xml(u, c, "shake")))
app.add_handler(CommandHandler("smooth", lambda u, c: send_xml(u, c, "smooth")))
app.add_handler(CommandHandler("cc", lambda u, c: send_xml(u, c, "cc")))
app.add_handler(CommandHandler("amexport", amexport))
app.add_handler(CommandHandler("owner", owner))
app.add_handler(CommandHandler("newxml", newxml))

app.run_polling()
