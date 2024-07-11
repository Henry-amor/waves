from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import traceback
import aiocron

# Global variable to store user IDs
user_ids = set()  # Use a set to store unique user IDs

# Define the start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id  # Retrieve user ID
    user_ids.add(user_id)  # Add user ID to the set

    keyboard = [
        [InlineKeyboardButton("Tap?Touch", url=f'http://t.me/Wavescoins_bot/Waves?start={user_id}')],
        [InlineKeyboardButton("Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Welcome to WavesCoin Bot! Please choose an option:', reply_markup=reply_markup)

# Define the callback query handler for buttons
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'help':
        await query.edit_message_text(text="Here is some help text.")
        # Provide help information

# Function to send notifications every 5 minutes
async def send_notifications(context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        global user_ids
        for user_id in user_ids:
            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text="🔔 Get ready to tap! The Wavescoin Bot is waiting for you!\n\n"
                         "💰 Earn rewards and have fun!\n\n"
                         "🚀 Click here to play now: http://t.me/Wavescoins_bot/Waves"
                )
            except Exception as e:
                print(f"Error sending notification to user {user_id}: {e}")
                traceback.print_exc()

    except Exception as e:
        print(f"Error in sending notifications: {e}")
        traceback.print_exc()

# Define the main function to start the bot
def main() -> None:
    try:
        global application
        application = Application.builder().token("7213090736:AAFYIpOpzlnLezE2WtI8ogR1r_D-DIn6QcU").build()

        updater = application.updater

        # Add handlers
        application.add_handler(CommandHandler('start', start))
        application.add_handler(CallbackQueryHandler(button))

        print("Bot started. Listening for commands...")

        # Ensure the job queue is properly set up
        if application.job_queue:
            application.job_queue.run_repeating(send_notifications, interval=300, first=0)
        else:
            print("Job queue not initialized correctly.")

        application.run_polling()

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

if __name__ == '__main__':
    main()
