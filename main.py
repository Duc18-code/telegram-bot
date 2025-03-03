import openai
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Thay thế bằng token của bạn
BOT_TOKEN = "7873797171:AAHu6M3GRtgCcw-JHwu2uvYUGcFSq-7xaIQ"
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

# Cấu hình logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

def chatgpt_response(prompt):
    """Gửi prompt đến OpenAI API và nhận phản hồi"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Lỗi: {str(e)}"

async def start(update: Update, context: CallbackContext) -> None:
    """Lệnh /start"""
    await update.message.reply_text("Xin chào! Gửi tin nhắn để trò chuyện với ChatGPT.")

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Xử lý tin nhắn người dùng"""
    user_message = update.message.text
    chatgpt_reply = chatgpt_response(user_message)
    await update.message.reply_text(chatgpt_reply)

async def error_handler(update: object, context: CallbackContext) -> None:
    """Ghi log lỗi"""
    logger.warning(f"Update {update} gây lỗi {context.error}")

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)
    
    print("Bot đang chạy...")
    app.run_polling()
