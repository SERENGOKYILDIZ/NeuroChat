import tkinter as tk
from tkinter import scrolledtext
import datetime

class ChatUI:
    def __init__(self, bot_instance):
        self.bot = bot_instance
        self.window = tk.Tk()
        self.window.title("Sohbet Botu")
        self.window.geometry("520x640")

        # 🧠 Mesaj günlüğü
        self.chat_log = []

        # 🪟 Sohbet alanı
        self.chat_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, font=("Courier New", 11))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.config(state='disabled')

        # ✍️ Giriş kutusu
        self.entry = tk.Entry(self.window, font=("Arial", 14))
        self.entry.pack(padx=10, pady=(0, 5), fill=tk.X)
        self.entry.bind("<Return>", self.send_message)

        # 🔘 Butonlar
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=(0, 10))

        self.send_button = tk.Button(button_frame, text="Gönder", width=12, command=self.send_message)
        self.send_button.grid(row=0, column=0, padx=5)

        self.clear_button = tk.Button(button_frame, text="Temizle", width=12, command=self.clear_chat)
        self.clear_button.grid(row=0, column=1, padx=5)

        self.exit_button = tk.Button(button_frame, text="Çıkış", width=12, command=self.exit_app)
        self.exit_button.grid(row=0, column=2, padx=5)

    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
            return

        self.talking("Sen", user_input)

        bot_response = self.bot.handle_message(user_input)
        self.talking("Bot", bot_response)

        self.entry.delete(0, tk.END)

    def talking(self, person:str, text:str):
        self.display_message(person, text)
        self.chat_log.append(f"{person}: {text}")

    def display_message(self, sender, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_area.yview(tk.END)
        self.chat_area.config(state='disabled')

    def clear_chat(self):
        self.chat_area.config(state='normal')
        self.chat_area.delete(1.0, tk.END)
        self.chat_area.config(state='disabled')
        self.chat_log.clear()

    def exit_app(self):
        self.bot.save_log(self.chat_log)
        self.window.destroy()

    def run(self):
        self.window.mainloop()
