from telegram import Update, constants
from telegram.ext import  CommandHandler, ApplicationBuilder,     MessageHandler, filters,ContextTypes
import openai
from collections import deque
import time

# Define a rate limit, in this case, 1 request per second
RATE_LIMIT = 1

# Define a queue to store the timestamps of requests
request_queue = deque()

# Define the token for your bot
TOKEN = "5361363661:AAEJEuY1Tjalf1OfWM3tphsgFlskrFn9JDk"

async def start(update: Update, context):
   await update.message.reply_text(
        "Hello and welcome! I am ChatGPT, your AI-powered personal chatbot. \nI am here to help you with anything you need. \nWhether you're looking for information, want to chat, or just need some advice, I'm here for you. \nLet's get started! How can I help you today? \n\n to use me, you can: \n type message in chatbox")



async def echo_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    reply = update.message.text
    await context.bot.send_chat_action(chat_id=update.message.chat_id, action=constants.ChatAction.TYPING)
   
    openai.api_key = "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"

    # Check if the rate limit has been exceeded
    if len(request_queue) >= RATE_LIMIT and time.time() - request_queue[0] < 1:
        await update.message.reply_text("You are sending messages too fast. Please wait a moment and try again.")
        return

    # Add the current timestamp to the request queue
    request_queue.append(time.time())

    # If the request queue exceeds the defined limit, remove the oldest item
    if len(request_queue) > RATE_LIMIT:
        request_queue.popleft()


    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly. Human : {reply}",
    temperature=1,
    max_tokens=999, 
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
    )

    data = response.choices[0].text

    await update.message.reply_text(data)

# Create an Updater object
updater = ApplicationBuilder().token(TOKEN).build()

updater.add_handler(CommandHandler('start',start))
updater.add_handler(MessageHandler(filters.TEXT, echo_text))


# Start the bot
updater.run_polling()
