import json
import os
from datetime import datetime

class ChatBot:
    def __init__(self, memory_file="memory.json", log_file="log.txt"):
        self.memory_file = memory_file
        self.log_file = log_file
        self.memory = self.load_memory()
        self.last_question = None

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_memory(self):
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=4, ensure_ascii=False)

    def delete_memory(self):
        if os.path.exists(self.memory_file):
            os.remove(self.memory_file)
        self.memory = {}

    def handle_message(self, user_input):
        user_input = user_input.strip().lower()

        if user_input == "çık":
            return "Görüşürüz."

        elif user_input == "ne öğrendin?":
            if not self.memory:
                return "Henüz hiçbir şey öğrenmedim."
            response = "İşte öğrendiklerim:\n"
            for q, a in self.memory.items():
                response += f"• {q.capitalize()} → {a}\n"
            return response.strip()

        elif user_input.startswith("unut "):
            key = user_input.replace("unut ", "").strip()
            if key in self.memory:
                del self.memory[key]
                self.save_memory()
                return f"'{key}' sorusunu hafızamdan sildim."
            else:
                return "Bunu zaten bilmiyordum."

        elif user_input == "hepsini sil":
            self.delete_memory()
            return "Tüm bilgileri hafızamdan sildim."

        if self.last_question:
            self.memory[self.last_question] = user_input
            self.save_memory()
            self.last_question = None
            return "Teşekkürler! Artık bunu biliyorum."

        if user_input in self.memory:
            return self.memory[user_input].capitalize()

        self.last_question = user_input
        return "Bu soruyu bilmiyorum. Cevabını öğretmek ister misin?"

    def save_log(self, chat_lines):
        if not chat_lines:
            return
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"\n--- Yeni Oturum ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---\n")
            for line in chat_lines:
                f.write(line + "\n")
            f.write(f"--- {len(chat_lines) // 2} mesajlık sohbet tamamlandı. ---\n")

    def greeting(self):
        return "Merhaba ben kişisel asistanınız NeuroBot. Size nasıl yardımcı olabilirim?"
