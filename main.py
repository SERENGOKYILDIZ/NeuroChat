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

def delete_memory():
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)

def basic_bot():
    memory = load_memory()
    last_question = None

    print("Bot: Merhaba! Ben öğrenebilen bir botum. (Çıkmak için 'çık' yaz)")

    while True:
        user_input = input("Sen: ").strip().lower()

        if user_input == "çık":
            print("Bot: Görüşürüz!")
            break

        elif user_input == "ne öğrendin?":
            if not memory:
                print("Bot: Henüz hiçbir şey öğrenmedim.")
            else:
                print("Bot: İşte öğrendiklerim:")
                for q, a in memory.items():
                    print(f"  • {q.capitalize()} → {a}")
            continue

        elif user_input.startswith("unut "):
            key = user_input.replace("unut ", "").strip()
            if key in memory:
                del memory[key]
                save_memory(memory)
                print(f"Bot: '{key}' sorusunu hafızamdan sildim.")
            else:
                print("Bot: Bunu zaten bilmiyordum.")
            continue

        elif user_input == "hepsini unut":
            confirm = input("Bot: Emin misin? (evet/hayır): ").strip().lower()
            if confirm == "evet":
                delete_memory()
                memory = {}
                print("Bot: Tüm bilgileri hafızamdan sildim.")
            else:
                print("Bot: Vazgeçtim, silmedim.")
            continue

        # Eğer bot cevap bekliyorsa, öğretme aşamasındayız
        if last_question:
            memory[last_question] = user_input
            save_memory(memory)
            print("Bot: Teşekkürler! Artık bunu biliyorum.")
            last_question = None
            continue

        # Öğrenilmiş bir soruysa cevap ver
        if user_input in memory:
            print(f"Bot: {memory[user_input]}")
            continue

        # Yeni soru: bilmediği şeyi öğren
        print("Bot: Bu soruyu bilmiyorum. Cevabını öğretmek ister misin?")
        last_question = user_input

basic_bot()