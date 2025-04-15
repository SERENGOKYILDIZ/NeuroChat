from chatbot import ChatBot
from ui import ChatUI

def main():
    bot = ChatBot()
    app = ChatUI(bot)
    app.run()

if __name__ == "__main__":
    main()
