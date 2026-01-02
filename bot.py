from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import json, os

BOT_TOKEN = "8235928800:AAHyjB-yxeMv7Tk01mh_ABL-k5xm5Q5pIwc"
OWNER_ID = 8541526129
ALLOWED_GROUP_ID = -5123749208

DATA_FILE = "data.json"
pending_category = {}

# ---------- Data ----------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ---------- Start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            "✨ 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 ✨\n\n"
            "𝐀𝐥𝐢𝐠𝐡𝐭 𝐌𝐨𝐭𝐢𝐨𝐧 𝐇𝐞𝐥𝐩𝐞𝐫 𝐁𝐨𝐭 🤍\n\n"
            "📌 Preset • XML • Shake • CC\n\n"
            "👉 Type /help"
        )

# ---------- Help ----------
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ALLOWED_GROUP_ID:
        await update.message.reply_text(
            "⚠️ Group only command\nএই bot শুধু Owner group-এ কাজ করে"
        )
        return

    await update.message.reply_text(
        "📖 𝐂𝐎𝐌𝐌𝐀𝐍𝐃 𝐋𝐈𝐒𝐓\n\n"
        "➤ /xml → All XML category\n"
        "➤ /shake /cc /smooth /preset\n\n"
        "👑 Admin only:\n"
        "➤ /newxml <name>\n"
        "➤ Send unlimited XML links\n"
        "➤ /done to save"
    )

# ---------- New XML ----------
async def newxml(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("⛔ Admin only")
        return

    if update.effective_chat.id != ALLOWED_GROUP_ID:
        return

    if not context.args:
        await update.message.reply_text(
            "❌ Usage:\n/newxml shake"
        )
        return

    cat = context.args[0].lower()
    pending_category[update.effective_user.id] = cat

    data = load_data()
    if cat not in data:
        data[cat] = []
        save_data(data)

    await update.message.reply_text(
        f"✅ 𝐀𝐃𝐃 𝐌𝐎𝐃𝐄 𝐎𝐍\n\n"
        f"📂 Category: {cat.upper()}\n"
        "📩 Now send XML / Drive links\n"
        "✔️ Send /done when finished"
    )

# ---------- Receive XML ----------
async def receive_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in pending_category:
        return

    if update.text.startswith("/"):
        return

    data = load_data()
    cat = pending_category[uid]
    data[cat].append(update.text)
    save_data(data)

    await update.message.reply_text("➕ XML Added")

# ---------- Done ----------
async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in pending_category:
        del pending_category[uid]
        await update.message.reply_text("✅ XML save completed")

# ---------- Show XML ----------
async def show_xml(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ALLOWED_GROUP_ID:
        return

    cmd = update.message.text.replace("/", "").lower()
    data = load_data()

    if cmd == "xml":
        if not data:
            await update.message.reply_text("❌ No XML added")
            return
        msg = "📂 𝐀𝐕𝐀𝐈𝐋𝐀𝐁𝐋𝐄 𝐂𝐀𝐓𝐄𝐆𝐎𝐑𝐈𝐄𝐒\n\n"
        for c in data:
            msg += f"➤ /{c}\n"
        await update.message.reply_text(msg)
        return

    if cmd not in data or not data[cmd]:
        await update.message.reply_text("❌ No XML found")
        return

    msg = f"📄 𝐗𝐌𝐋 𝐋𝐈𝐒𝐓 ({cmd.upper()})\n\n"
    for i, link in enumerate(data[cmd], 1):
        msg += f"{i}. {link}\n"
    await update.message.reply_text(msg)

# ---------- Main ----------
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("newxml", newxml))
app.add_handler(CommandHandler("done", done))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_link))
app.add_handler(MessageHandler(filters.COMMAND, show_xml))

app.run_polling()
