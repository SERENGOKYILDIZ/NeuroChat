import json
import os

class ChatBot:
    def __init__(self, memory_file="memory.json"):
        self.memory_file = memory_file
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
            return self.memory[user_input]

        self.last_question = user_input
        return "Bu soruyu bilmiyorum. Cevabını öğretmek ister misin?"
