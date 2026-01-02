from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import json, os

BOT_TOKEN = "8235928800:AAHyjB-yxeMv7Tk01mh_ABL-k5xm5Q5pIwc"
OWNER_ID = 8541526129
ALLOWED_GROUP_ID = -5123749208
DATA_FILE = "data.json"

pending = {}

# ---------- Data ----------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE) as f:
        return json.load(f)

def save_data(d):
    with open(DATA_FILE, "w") as f:
        json.dump(d, f, indent=2)

# ---------- Start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            "✨ 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 ✨\n\n"
            "𝐀𝐥𝐢𝐠𝐡𝐭 𝐌𝐨𝐭𝐢𝐨𝐧 𝐇𝐞𝐥𝐩𝐞𝐫 𝐁𝐨𝐭 🤍\n\n"
            "📌 XML • Shake • CC • Preset\n\n"
            "🔒 XML add: Owner only\n"
            "👉 /help"
        )

# ---------- Help ----------
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            "🆘 𝐇𝐄𝐋𝐏\n\n"
            "📥 Inbox:\n"
            "➤ /newxml <name>\n"
            "➤ Send XML links\n"
            "➤ /done\n\n"
            "📢 Group:\n"
            "➤ /xml /shake /cc /smooth"
        )

# ---------- New XML (Inbox only) ----------
async def newxml(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("⛔ Admin only")
        return

    if update.effective_chat.type != "private":
        await update.message.reply_text("⚠️ Inbox only")
        return

    if not context.args:
        await update.message.reply_text("❌ Usage:\n/newxml shake")
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
        "✔️ /done to finish"
    )

# ---------- Receive XML ----------
async def receive(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

# ---------- Done ----------
async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in pending:
        del pending[uid]
        await update.message.reply_text("✅ XML save completed")

# ---------- Show XML (Group only) ----------
async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ALLOWED_GROUP_ID:
        return

    cmd = update.message.text.replace("/", "").lower()
    data = load_data()

    if cmd == "xml":
        msg = "📂 𝐗𝐌𝐋 𝐂𝐀𝐓𝐄𝐆𝐎𝐑𝐈𝐄𝐒\n\n"
        for c in data:
            msg += f"➤ /{c}\n"
        await update.message.reply_text(msg)
        return

    if cmd not in data:
        await update.message.reply_text("❌ No XML found")
        return

    msg = f"📄 𝐗𝐌𝐋 𝐋𝐈𝐒𝐓 ({cmd.upper()})\n\n"
    for i, l in enumerate(data[cmd], 1):
        msg += f"{i}. {l}\n"
    await update.message.reply_text(msg)

# ---------- Main ----------
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("newxml", newxml))
app.add_handler(CommandHandler("done", done))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive))
app.add_handler(MessageHandler(filters.COMMAND, show))

app.run_polling()
