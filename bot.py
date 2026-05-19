import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("لم يتم العثور على BOT_TOKEN!")

auto_replies = {
    "مرحبا": "مرحبا! كيف يمكنني مساعدتك؟ 😊",
    "هاي": "هاي! 👋",
    "كيف حالك": "الحمد لله بخير، وأنت؟",
    "شكرا": "عفواً! سعيد بمساعدتك ✨",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"مرحبا {update.effective_user.first_name}! 👋\nالبوت يعمل 24/7")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("الأوامر:\n/start\n/help\n/addreply <كلمة> <الرد>")

async def add_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("استخدام: /addreply <الكلمة> <الرد>")
        return
    trigger = context.args[0].lower()
    response = ' '.join(context.args[1:])
    auto_replies[trigger] = response
    await update.message.reply_text(f"✅ تم إضافة: {trigger} → {response}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    text = update.message.text.lower()
    for trigger, reply in auto_replies.items():
        if trigger in text:
            await update.message.reply_text(reply)
            return

async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("addreply", add_reply))
    application.add_handler(MessageHandler(filters.TEXT & \~filters.COMMAND, handle_message))
    
    print("✅ البوت يعمل الآن...")
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())