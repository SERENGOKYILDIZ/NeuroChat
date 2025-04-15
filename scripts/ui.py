import os
import tkinter as tk
from tkinter import scrolledtext
import datetime
from PIL import Image, ImageTk  # Pillow kullanılıyor

RES_AVATAR = "./assetes/avatars/"

class ChatUI:
    def __init__(self, bot_instance):
        # self.theme = "light"  # başlangıç modu
        self.theme = "dark"  # başlangıç modu
        self.themes = {
            "light": {
                "bg": "#ffffff",
                "fg": "#000000",
                "entry_bg": "#f0f0f0",
                "text_bg": "#ffffff",
                "button_bg": "#dddddd"
            },
            "dark": {
                "bg": "#2e2e2e",
                "fg": "#ffffff",
                "entry_bg": "#3c3c3c",
                "text_bg": "#2e2e2e",
                "button_bg": "#444444"
            }
        }
        self.bot = bot_instance
        self.window = tk.Tk()
        self.window.title("Sohbet Botu")
        self.window.geometry("520x740")

        # 🧠 Mesaj günlüğü
        self.chat_log = []

        # 🖼️ Avatar resmi
        # 🖼️ Avatar
        default_avatar = os.path.join("assets", "avatars", "avatar.png")
        self.avatar_image = Image.open(default_avatar).resize((150, 150))
        self.avatar_photo = ImageTk.PhotoImage(self.avatar_image)
        self.avatar_label = tk.Label(self.window, image=self.avatar_photo)
        self.avatar_label.pack(pady=(5, 0))

        # 🪟 Sohbet alanı
        self.chat_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, font=("Courier New", 11))
        self.chat_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.chat_area.config(state='disabled')

        # ✍️ Giriş kutusu
        self.entry = tk.Entry(self.window, font=("Arial", 14))
        self.entry.pack(padx=10, pady=(0, 5), fill=tk.X)
        self.entry.bind("<Return>", self.send_message)

        # 🔘 Butonlar
        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(pady=(0, 10))

        self.send_button = tk.Button(self.button_frame, text="Gönder", width=12, command=self.send_message)
        self.send_button.grid(row=0, column=0, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="Temizle", width=12, command=self.clear_chat)
        self.clear_button.grid(row=0, column=1, padx=5)

        self.exit_button = tk.Button(self.button_frame, text="Çıkış", width=12, command=self.exit_app)
        self.exit_button.grid(row=0, column=2, padx=5)

        self.theme_button = tk.Button(self.button_frame, text="Tema Değiştir", width=12, command=self.toggle_theme)
        self.theme_button.grid(row=0, column=3, padx=5)

        self.apply_theme()  # tema başlangıçta uygulanır

    def send_message(self, event=None):
        user_input = self.entry.get().strip()
        if not user_input:
            return

        #Senin konuşman
        self.talking("Sen", user_input)

        #Botun konuşması
        bot_response, emotion_avatar = self.bot.handle_message(user_input, return_avatar=True)
        self.talking("Bot", bot_response)
        # ✅ Avatar değiştir (varsa)
        if emotion_avatar:
            self.update_avatar(emotion_avatar)

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

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.apply_theme()

    def apply_theme(self):
        theme = self.themes[self.theme]
        self.button_frame.configure(bg=theme["bg"])
        self.window.configure(bg=theme["bg"])
        self.chat_area.configure(bg=theme["text_bg"], fg=theme["fg"])
        self.entry.configure(bg=theme["entry_bg"], fg=theme["fg"])
        self.avatar_label.configure(bg=theme["bg"])  # avatar zeminini güncelle
        for btn in [self.send_button, self.clear_button, self.exit_button, self.theme_button]:
            btn.configure(
                bg=theme["button_bg"],
                fg=theme["fg"],
                activebackground=theme["button_bg"],
                activeforeground=theme["fg"],
                highlightbackground=theme["bg"],
                highlightthickness=0,
                borderwidth=0,
                relief="flat"
            )

    def update_avatar(self, filename):
        image_path = os.path.join(".", "assets", "avatars", filename)
        if os.path.exists(image_path):
            avatar_image = Image.open(image_path).resize((150, 150))
            self.avatar_photo = ImageTk.PhotoImage(avatar_image)
            self.avatar_label.configure(image=self.avatar_photo)

    def exit_app(self):
        self.bot.save_log(self.chat_log)
        print("Sohbet günlüğü kaydedildi.")  # veya tkinter ile popup ekleyebilirsin
        self.window.destroy()

    def run(self):
        self.window.mainloop()
