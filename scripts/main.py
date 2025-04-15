from scripts.chatbot import ChatBot
from ui import ChatUI

def main():
    bot = ChatBot()
    app = ChatUI(bot)

    #First text by Bot
    app.talking("Bot", bot.greeting())

    app.run()

if __name__ == "__main__":
    main()
