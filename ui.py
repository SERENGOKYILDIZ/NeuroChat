import tkinter as tk
from tkinter import scrolledtext

class ChatUI:
    def __init__(self, bot_instance):
        self.bot = bot_instance
        self.window = tk.Tk()
        self.window.title("Sohbet Botu")
        self.window.geometry("500x600")

        self.chat_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD)
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.config(state='disabled')

        self.entry = tk.Entry(self.window, font=("Arial", 14))
        self.entry.pack(padx=10, pady=10, fill=tk.X)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.window, text="Gönder", command=self.send_message)
        self.send_button.pack(pady=(0, 10))

    def send_message(self, event=None):
        user_input = self.entry.get()
        if not user_input.strip():
            return

        self.display_message("Sen", user_input)
        bot_response = self.bot.handle_message(user_input)
        self.display_message("Bot", bot_response)
        self.entry.delete(0, tk.END)

    def display_message(self, sender, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_area.yview(tk.END)
        self.chat_area.config(state='disabled')

    def run(self):
        self.window.mainloop()
