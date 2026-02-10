import os
import logging
import tempfile
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from gtts import lang,gTTS
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)
logger = logging.getLogger(__name__)
l = {k.lower():v for k, v in lang.tts_langs().items()}
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, I am gTTSBot!")
async def table(update: Update, context: ContextTypes.DEFAULT_TYPE):
    languages_text=""
    for k,v in lang.tts_langs().items():
        languages_text += f"{k}: {v}\n"
    await update.message.reply_text(languages_text)
def text_to_speech(text,language_code):
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
        mp3_path = tmp_file.name
    tts = gTTS(text, lang=language_code)
    tts.save(mp3_path)
    return mp3_path
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    parts = text.split(maxsplit=1)
    if len(parts)<2:
        return 
    lang_code = parts[0].lower()
    user_text = parts[1]
    if lang_code not in l:
        return
    processing_msg = await update.message.reply_text(f"Just a moment.")
    mp3_path = text_to_speech(user_text, lang_code)
    with open(mp3_path,'rb') as audio_file:
        await update.message.reply_audio(audio=audio_file, caption="", performer="githubtts_bot")
        os.unlink(mp3_path)
        await processing_msg.delete()
def main():
    logger.info("RUNNING")
    application=Application.builder().token(os.getenv('token')).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("table", table))
    application.add_handler(MessageHandler(filters.TEXT&~filters.COMMAND, handle_message))
    logger.info(f"@githubtts_bot")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
if __name__ == "__main__":
    main()
