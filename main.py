from chatbot import ChatBot
from ui import ChatUI

def main():
    bot = ChatBot()
    app = ChatUI(bot)

    #First text by Bot
    app.talking("Bot", "Merhaba ben kişisel asistanınız NeuroBot size nasıl yardımcı olabilirim?")

    app.run()

if __name__ == "__main__":
    main()
