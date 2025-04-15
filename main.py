import json
import os

MEMORY_FILE = "memory.json"

# --- Hafıza işlemleri
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4, ensure_ascii=False)

def basic_bot():
    memory = load_memory()
    last_question = None  # Henüz cevabı alınmamış bir soru var mı?

    print("Bot: Merhaba! Ben öğrenebilen bir botum. (Çıkmak için 'çık' yaz)")

    while True:
        user_input = input("Sen: ").strip().lower()

        if user_input == "çık":
            print("Bot: Görüşürüz!")
            break

        # Öğrenme aşaması: bir önceki soru için cevap verildi mi?
        if last_question:
            memory[last_question] = user_input
            save_memory(memory)
            print("Bot: Teşekkürler! Artık bunu biliyorum.")
            last_question = None
            continue

        # Eğer soru daha önce öğrenilmişse cevapla
        if user_input in memory:
            print(f"Bot: {memory[user_input]}")
            continue

        # Bilinmeyen soruya geldiğimizde öğrenme tetiklenir
        print("Bot: Bu soruyu bilmiyorum. Cevabını öğretmek ister misin?")
        last_question = user_input

basic_bot()