def basic_bot():
    print("Bot: Merhaba! Ben senin ilk yapay zekanım. Sohbete başlayalım! (Çıkmak için 'çık' yaz)")

    while True:
        user_input = input("Sen: ").lower()

        if user_input == "çık":
            print("Bot: Görüşürüz!")
            break

        elif "merhaba" in user_input:
            print("Bot: Merhaba! Sana nasıl yardımcı olabilirim?")

        elif "adın ne" in user_input or "kimsin" in user_input:
            print("Bot: Ben senin kendi yazdığın bir sohbet botuyum!")

        elif "nasılsın" in user_input:
            print("Bot: Harikayım! Seninle konuşmak güzel.")

        elif "hava" in user_input:
            print("Bot: Havanın nasıl olduğunu öğrenmek için webte arama yapmam gerek!")

        else:
            print("Bot: Bu konuyu bilmiyorum, ama istersen öğrenebilirim!")


basic_bot()
