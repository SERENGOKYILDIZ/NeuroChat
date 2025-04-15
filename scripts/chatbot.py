import json
import os
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob

THRESHOLD = 0.4 # Sayı azaldıkça cevap daha hassas alınır.

class ChatBot:
    def __init__(self, memory_file="memory.json", log_file="log.txt"):
        self.memory_file = memory_file
        self.log_file = log_file
        self.memory = self.load_memory()
        self.last_question = None
        self.user_name = self.memory.get("kullanici_adi", None)
        self.reactions = self.load_reactions()

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

    def handle_message(self, user_input, return_avatar=False):
        user_input = user_input.strip().lower()
        name = self.user_name or ""
        response, avatar = None, None

        # 1. Duygusal tepki
        emotion = self.detect_emotion(user_input)
        if emotion:
            response, avatar = self.generate_emotional_response(emotion)
            if response:
                return (response, avatar) if return_avatar else response

        # 2. Özel komutlar
        if user_input == "çık":
            response = "Görüşürüz."
        elif user_input == "ne öğrendin?":
            response = "İşte öğrendiklerim:\n" + "\n".join(
                f"• {q.capitalize()} → {a}" for q, a in self.memory.items()
            ) if self.memory else "Henüz hiçbir şey öğrenmedim."
        elif user_input.startswith("unut "):
            key = user_input.replace("unut ", "").strip()
            if key in self.memory:
                del self.memory[key]
                self.save_memory()
                response = f"'{key}' sorusunu hafızamdan sildim."
            else:
                response = "Bunu zaten bilmiyordum."
        elif user_input == "hepsini sil":
            self.delete_memory()
            response = "Tüm bilgileri hafızamdan sildim."
        elif "benim adım" in user_input:
            name = user_input.split("benim adım")[-1].strip().capitalize()
            self.memory["kullanıcı_adı"] = name
            self.user_name = name
            self.save_memory()
            response = f"Merhaba {name}, seni hatırlayacağım!"
        elif "adımı biliyor musun" in user_input:
            response = f"Evet, adın {self.user_name}!" if self.user_name else "Henüz adını öğrenmedim. Söyler misin?"
        elif self.last_question:
            self.memory[self.last_question] = user_input
            self.save_memory()
            self.last_question = None
            response = "Teşekkürler! Artık bunu biliyorum."
        elif user_input in self.memory:
            response = self.memory[user_input].capitalize()
        else:
            similar_q, _ = self.find_similar_question(user_input)
            if similar_q:
                response = f"Bu soruyu bilmiyorum. Ama '{similar_q}' sorusuna şöyle cevap vermiştim:\n{self.memory[similar_q]}"
            else:
                self.last_question = user_input
                response = "Bu soruyu bilmiyorum. Cevabını öğretmek ister misin?"

        return (response, avatar) if return_avatar else response

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

    def detect_emotion(self, user_input):
        # Anahtar kelimeye göre duygu
        emotion_keywords = {
            "mutlu": ["teşekkür", "harika", "çok güzel", "mükemmel", "seviyorum"],
            "üzgün": ["üzgünüm", "canım sıkkın", "moralim bozuk", "yalnızım", "ağlıyorum"],
            "sinirli": ["nefret", "sinirliyim", "bıktım", "deliriyorum"],
            "övgü": ["aferin", "bravo", "çok iyisin", "helal"]
        }

        for emotion, keywords in emotion_keywords.items():
            for word in keywords:
                if word in user_input:
                    return emotion

        # TextBlob ile skor bazlı duygu
        blob = TextBlob(user_input)
        polarity = blob.sentiment.polarity

        if polarity > 0.3:
            return "mutlu"
        elif polarity < -0.3:
            return "üzgün"

        return None

    def load_reactions(self, path="reactions.json"):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def generate_emotional_response(self, emotion):
        if emotion in self.reactions:
            name = self.user_name or ""
            raw_text = self.reactions[emotion]["response"]
            response = raw_text.replace("{name}, ", f"{name}, " if name else "")
            avatar = self.reactions[emotion]["avatar"]
            return response, avatar
        return None, None

