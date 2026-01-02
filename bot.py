from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import json, os

# ================= CONFIG =================
BOT_TOKEN = "8235928800:AAHyjB-yxeMv7Tk01mh_ABL-k5xm5Q5pIwc"
OWNER_ID = 8541526129
ALLOWED_GROUP_ID = -1005123749208   # ⚠️ replace with real group id
DATA_FILE = "data.json"

pending = {}

# ================= DATA =================
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            "✨ 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 ✨\n\n"
            "𝐀𝐥𝐢𝐠𝐡𝐭 𝐌𝐨𝐭𝐢𝐨𝐧 𝐇𝐞𝐥𝐩𝐞𝐫 𝐁𝐨𝐭 🤍\n\n"
            "📌 XML • Shake • CC • Preset\n\n"
            "🔒 XML add: Owner only\n"
            "👑 Credit: Salim Ahmad\n\n"
            "👉 Type /help"
        )

# ================= HELP =================
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            "🆘 𝐇𝐄𝐋𝐏 𝐌𝐄𝐍𝐔\n\n"
            "📥 Inbox (Owner):\n"
            "➤ /newxml <name>\n"
            "➤ Send XML links\n"
            "➤ /done\n\n"
            "📢 Group:\n"
            "➤ /xml\n"
            "➤ /shake /cc /smooth /preset\n\n"
            "👑 Credit: Salim Ahmad"
        )
    else:
        await update.message.reply_text(
            "⚠️ Inbox use /help\n"
            "এই bot শুধু নির্দিষ্ট group এ কাজ করে"
        )

# ================= NEW XML (INBOX) =================
async def newxml(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("⛔ Admin only")
        return

    if update.effective_chat.type != "private":
        await update.message.reply_text("⚠️ Inbox only")
        return

    if not context.args:
        await update.message.reply_text(
            "❌ Usage:\n/newxml shake"
        )
        return

    cat = context.args[0].lower()
    pending[update.effective_user.id] = cat

    data = load_data()
    data.setdefault(cat, [])
    save_data(data)

    await update.message.reply_text(
        f"✅ 𝐀𝐃𝐃 𝐌𝐎𝐃𝐄 𝐎𝐍\n\n"
        f"📂 Category: {cat.upper()}\n"
        "📩 Send XML / Drive links\n"
        "✔️ Send /done when finished"
    )

# ================= RECEIVE XML =================
async def receive_xml(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in pending:
        return

    if update.text.startswith("/"):
        return

    data = load_data()
    cat = pending[uid]
    data[cat].append(update.text)
    save_data(data)

    await update.message.reply_text("➕ XML Added")

# ================= DONE =================
async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in pending:
        del pending[uid]
        await update.message.reply_text("✅ XML save completed")

# ================= SHOW XML (GROUP) =================
async def show_xml(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ALLOWED_GROUP_ID:
        await update.message.reply_text(
            "⛔ Access denied\nএই bot শুধু Owner group এ কাজ করে"
        )
        return

    cmd = update.message.text.replace("/", "").lower()
    data = load_data()

    if cmd == "xml":
        if not data:
            await update.message.reply_text("❌ No XML added yet")
            return

        msg = "📂 𝐀𝐕𝐀𝐈𝐋𝐀𝐁𝐋𝐄 𝐗𝐌𝐋 𝐂𝐀𝐓𝐄𝐆𝐎𝐑𝐈𝐄𝐒\n\n"
        for c in data:
            msg += f"➤ /{c}\n"
        await update.message.reply_text(msg)
        return

    if cmd not in data or not data[cmd]:
        await update.message.reply_text(
            f"📄 𝐗𝐌𝐋 𝐋𝐈𝐒𝐓 ({cmd.upper()})\n\n❌ No XML found"
        )
        return

    msg = f"📄 𝐗𝐌𝐋 𝐋𝐈𝐒𝐓 ({cmd.upper()})\n\n"
    for i, link in enumerate(data[cmd], 1):
        msg += f"{i}. {link}\n"

    msg += "\n👑 Credit: Salim Ahmad"
    await update.message.reply_text(msg)

# ================= MAIN =================
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("newxml", newxml))
app.add_handler(CommandHandler("done", done))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_xml))
app.add_handler(MessageHandler(filters.COMMAND, show_xml))

app.run_polling()
