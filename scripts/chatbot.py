import json
import os
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

THRESHOLD = 0.4 # Sayı azaldıkça cevap daha hassas alınır.

class ChatBot:
    def __init__(self, memory_file="memory.json", log_file="log.txt"):
        self.memory_file = memory_file
        self.log_file = log_file
        self.memory = self.load_memory()
        self.last_question = None
        self.user_name = self.memory.get("kullanici_adi", None)

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

        # 1. Çıkış
        if user_input == "çık":
            return "Görüşürüz."

        # 2. Öğrendiklerini listeleme
        if user_input == "ne öğrendin?":
            if not self.memory:
                return "Henüz hiçbir şey öğrenmedim."
            response = "İşte öğrendiklerim:\n"
            for q, a in self.memory.items():
                response += f"• {q.capitalize()} → {a}\n"
            return response.strip()

        # 3. Unut komutu
        if user_input.startswith("unut "):
            key = user_input.replace("unut ", "").strip()
            if key in self.memory:
                del self.memory[key]
                self.save_memory()
                return f"'{key}' sorusunu hafızamdan sildim."
            else:
                return "Bunu zaten bilmiyordum."

        # 4. Tüm hafızayı sil
        if user_input == "hepsini sil":
            self.delete_memory()
            return "Tüm bilgileri hafızamdan sildim."

        # 5. Kullanıcının adını öğrenme
        if "benim adım" in user_input:
            name = user_input.split("benim adım")[-1].strip().capitalize()
            self.memory["kullanıcı_adı"] = name
            self.user_name = name
            self.save_memory()
            return f"Merhaba {name}, seni hatırlayacağım!"

        # 6. Adı hatırlama
        if "adımı biliyor musun" in user_input:
            if self.user_name:
                return f"Evet, adın {self.user_name}!"
            else:
                return "Henüz adını öğrenmedim. Söyler misin?"

        # 7. Cevap öğrenme durumu
        if self.last_question:
            self.memory[self.last_question] = user_input
            self.save_memory()
            self.last_question = None
            return "Teşekkürler! Artık bunu biliyorum."

        # 8. Doğrudan eşleşme varsa
        if user_input in self.memory:
            return self.memory[user_input].capitalize()

        # 9. TF-IDF benzerlik kontrolü
        similar_q, score = self.find_similar_question(user_input)
        if similar_q:
            return f"Bu soruyu bilmiyorum. Ama '{similar_q}' sorusuna şöyle cevap vermiştim:\n{self.memory[similar_q]}"

        # 10. Hiçbir eşleşme yoksa öğrenme başlat
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
        if self.user_name:
            return f"Merhaba {self.user_name}, ben kişisel asistanınız NeuroBot!"
        return "Merhaba! Ben kişisel asistanınız NeuroBot. Size nasıl yardımcı olabilirim?"

    def find_similar_question(self, new_question, threshold=THRESHOLD):
        if not self.memory:
            return None, 0.0

        questions = list(self.memory.keys())
        vectorizer = TfidfVectorizer().fit(questions + [new_question])
        vectors = vectorizer.transform(questions + [new_question])

        similarity_scores = cosine_similarity(vectors[-1], vectors[:-1])
        max_score = similarity_scores.max()
        index = similarity_scores.argmax()

        if max_score >= threshold:
            return questions[index], max_score
        return None, 0.0


