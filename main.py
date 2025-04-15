import json
import os

# --- Hafıza dosyası
MEMORY_FILE = "memory.json"

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
    print("Bot: Merhaba! Ben geliştirilebilir bir botum. (Çıkmak için 'çık' yaz)")

    while True:
        user_input = input("Sen: ").lower()

        if user_input == "çık":
            print("Bot: Görüşürüz!")
            break

        # Öğrenme: "Benim adım Ahmet." gibi
        elif "benim adım" in user_input:
            name = user_input.split("benim adım")[-1].strip().capitalize()
            memory["kullanıcı_adı"] = name
            save_memory(memory)
            print(f"Bot: Merhaba {name}, seni hatırlayacağım!")

        # Hatırlama: Adı hatırlat
        elif "adımı biliyor musun" in user_input:
            if "kullanıcı_adı" in memory:
                print(f"Bot: Evet, adın {memory['kullanıcı_adı']}!")
            else:
                print("Bot: Henüz adını öğrenmedim. Söyler misin?")

        # Yeni konu örnekleri
        elif "okul" in user_input:
            print("Bot: Okul hayatı bazen zor olabiliyor ama öğrenmek güzeldir!")

        elif "müzik" in user_input:
            print("Bot: En sevdiğin müzik türü nedir?")

        elif "oyun" in user_input:
            print("Bot: Ben yapay zekayım ama oyunları çok severim!")

        elif "yemek" in user_input:
            print("Bot: Bugün ne yedin? Ben sadece veri yiyorum :)")

        else:
            print("Bot: Bu konuyu bilmiyorum, ama öğrenebilirim!")

basic_bot()
