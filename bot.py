
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Bug Testing Bot!\n\n"
        "Use /bug followed by your bug description.\n"
        "Example: /bug Login button is not working"
    )

async def bug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Please describe the bug.\n"
            "Example: /bug Login page has an error"
        )
        return

    description = " ".join(context.args)

    report = (
        "🐛 NEW BUG REPORT\n\n"
        f"User: {update.effective_user.id}\n"
        f"Bug: {description}"
    )

    if ADMIN_ID:
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=report
            )
        except Exception:
            await update.message.reply_text(
                "Report could not be delivered. Try again later."
            )
            return

    await update.message.reply_text(
        "✅ Bug report received!\n"
        "Thank you for testing."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Start bot\n"
        "/bug - Report a software bug\n"
        "/help - Show help"
    )

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is missing")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bug", bug))
    app.add_handler(CommandHandler("help", help_command))

    app.run_polling()

if __name__ == "__main__":
    main()
