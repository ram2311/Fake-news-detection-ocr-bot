from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import os
import pickle
import re
pickle_in = open("Countvec.pkl","rb")
cv=pickle.load(pickle_in)
pickle_in = open("classifierNB.pkl","rb")
model=pickle.load(pickle_in)

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import numpy as np
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

myCommands = {
    "start": "start",
    "help": "help",
}

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('OCR Bot for detecting fake news is working fine....')


def help(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    s = ""
    for i in myCommands:
        s += '/'+myCommands[i]+" - "+i+"\n"
    update.message.reply_text('Help!\n' + s)

""""
def read_image(update: Update, context: CallbackContext) -> None:
    #Send reply of user's message.
    chat_id = update.message.chat_id
    try:
        photo_file = update.message.photo[-1].get_file()
        img_name = str(chat_id)+'.jpg'
        photo_file.download(img_name)
        output=pytesseract.image_to_string(Image.open(img_name))
        #Output is generated from the image and is a string 
        if output:
            update.message.reply_text('`'+str(output)+'`\n\nImage to Text Generated', parse_mode=ParseMode.MARKDOWN, reply_to_message_id = update.message.message_id)
            ps = PorterStemmer()
            test_txt = []
            input_txt = ['Months of anti-government protests in Hong Kong began in June, when more than 1 million people marched to protest a bill that would allow the extradition of people to mainland China to stand trial. Hong Kong, a British colony until 1997, allows more autonomy to its citizens than mainland China, and protesters feared the bill could undermine this independence and endanger journalists and political activists. Though the bill was withdrawn in September, the unrest continued, including increasingly violent clashes between protesters and police.']
            input_txt.append(output)
            test = re.sub('[^a-zA-Z]',' ',input_txt[1])
            test = test.lower()
            test = test.split()
            test = [ps.stem(word) for word in test if not word in stopwords.words('english')]
            test = ' '.join(test)
            test_txt.append(test)
            X=cv.transform(test_txt).toarray()
            Y=model.predict(X)
            if Y==1:
                update.message.reply_text('It is a fake news')
            else:
                update.message.reply_text('It is an original news')
        else:
            update.message.reply_text("No text found")
    except Exception as e:
        update.message.reply_text("Please Resend, Error Occured: `"+str(e)+"`")
    finally:
        try:
            os.remove(img_name)
        except Exception:
            pass
"""
def reply_to_text_message(update: Update, context: CallbackContext) -> None:
    output=update.message.text
    if output:
            update.message.reply_text('`'+str(output)+'`\n\nImage to Text Generated', parse_mode=ParseMode.MARKDOWN, reply_to_message_id = update.message.message_id)
            ps = PorterStemmer()
            test_txt = []
            input_txt = ['Months of anti-government protests in Hong Kong began in June, when more than 1 million people marched to protest a bill that would allow the extradition of people to mainland China to stand trial. Hong Kong, a British colony until 1997, allows more autonomy to its citizens than mainland China, and protesters feared the bill could undermine this independence and endanger journalists and political activists. Though the bill was withdrawn in September, the unrest continued, including increasingly violent clashes between protesters and police.']
            input_txt.append(output)
            test = re.sub('[^a-zA-Z]',' ',input_txt[1])
            test = test.lower()
            test = test.split()
            test = [ps.stem(word) for word in test if not word in stopwords.words('english')]
            test = ' '.join(test)
            test_txt.append(test)
            X=cv.transform(test_txt).toarray()
            Y=model.predict(X)
            if Y==1:
                update.message.reply_text('It is a fake news')
            else:
                update.message.reply_text('It is an original news')
        else:
            update.message.reply_text("No text found")


def main():
    import os
PORT = int(os.environ.get('PORT', 5000))

    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    ocr_bot_token=os.environ.get("BOT_TOKEN", "1877520328:AAGKcLZmKRE9uxZBEU3rpiYp4oQOku08WAU")
    updater = Updater(ocr_bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler(myCommands["start"], start))
    dispatcher.add_handler(CommandHandler(myCommands["help"], help))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_to_text_message))
    dispatcher.add_handler(MessageHandler(Filters.photo, read_image))
    # Start the Bot
updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
updater.bot.setWebhook('https://fake-news-detectable-ocr-bot.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
