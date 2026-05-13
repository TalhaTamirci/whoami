"""Oyun havuzu — oyunda oyunculara atanacak kategorize edilmiş kelimeler."""

import random

CATEGORIES = {
    "populer_ikonlar": [
        # Türk ünlüler
        "Atatürk", "Barış Manço", "Tarkan", "Müslüm Gürses", "Ajda Pekkan",
        "Kemal Sunal", "Adile Naşit", "Zeki Müren", "Fatih Sultan Mehmet",
        "Kanuni Sultan Süleyman", "Mevlana", "Nasreddin Hoca", "Hakan Şükür",
        "Arda Turan", "Kıvanç Tatlıtuğ", "Çağatay Ulusoy", "Haluk Bilginer", 
        "Şener Şen", "Sabiha Gökçen", "Aziz Sancar", "Naim Süleymanoğlu", 
        "Metin Oktay", "Recep Tayyip Erdoğan", "İlber Ortaylı", "Cüneyt Arkın",
        "Türkan Şoray", "Tarık Akan", "Ceza", "Neşet Ertaş", "Aşık Veysel",
        "Sezen Aksu", "Sertab Erener", "Cem Yılmaz", "Murat Boz", "Bülent Ersoy", 
        "Hadise", "Serdar Ortaç", "Enes Batur", "Aleyna Tilki", "Zoktay", "Ümit Özdağ",
        "Cem Uzan", "Turgut Özal", "Bülent Ecevit", "Mansur Yavaş", "Süleyman Soylu",
        "Enis Kirazoğlu", "Can Yaman", "Lebel C5", "Fatih Terim", "Yıldırım Beyazıt",
        
        # Dünya ünlüleri
        "Albert Einstein", "Nikola Tesla", "Leonardo da Vinci", "Napoleon",
        "Kleopatra", "Mozart", "Beethoven", "Michael Jackson", "Elvis Presley",
        "Mia Khalifa", "Charlie Chaplin", "Bruce Lee", "Muhammad Ali",
        "Lionel Messi", "Cristiano Ronaldo", "Michael Jordan", "Elon Musk",
        "Steve Jobs", "Bill Gates", "Mark Zuckerberg", "Stephen Hawking",
        "Mr.Beast", "Isaac Newton", "Freddie Mercury", "Lebron James",
        "Robert Oppenheimer", "Angeline Jolie", "Brad Pitt", "Kanye West",
        "Leaonardo DiCaprio", "Scarlett Johansson", "Adolf Hitler", "Obama",
        "Putin", "Saddam Hüseyin", "Bashar Esad", "Lenin", "Stalin", "Trump",
        "Jeffrey Epstein", "Diddy", "İsa Mesih", "Musa", "Hz. Muhammed", "Buda", 
        "Edison", "Sokrates", "Bob Marley", "Picasso", "Van Gogh", "Martin Luther",
        
        # Kurgusal karakterler dizi/çizgi-film/anime/film vb.
        "Darth Vader", "Harry Potter", "Gandalf", "Batman", "Spider-Man",
        "Sherlock Holmes", "James Bond", "Shrek", "Jack Sparrow", "Joker", 
        "Thanos", "Walter White", "Tony Montana", "Rocky Balboa", "Ironman",
        "Superman", "Jon Snow", "Mordecai", "Deep", "Tyler Durden",
        "Patrick Bateman", "Dişsiz", "Voldemort", "Doctor Strange",
        "Monkey D. Luffy", "Recep İvedik", "Pikachu", "Goku", "Naruto", 
        "Eren Jaeger", "Levi Ackerman", "Saitama", "Light Yagami", "L Lawliet", 
        "Griffith", "Sasuke Uchiha", "Roronoa Zoro", "Satoru Gojo", "Sukuna", 
        "Ken Kaneki", "Gyro Zeppeli", "Hıçgıdık", "Mikasa Ackerman", "Dio Brando", 
        "Johnny Joestar", "Homelander", "John Wick", "Aladdin", "Buzz Lightyear",
        "Çizmeli Kedi", "Garfield", "SüngerBob", "Doraemon", "Mickey Mouse",
        "Rick Sanchez", "Finn", "Gumball", "Scooby-Doo", "Yoda", "Gollum",
        "Zeus", "Hades", "Poseidon", "Ares", "Loki", "Odin", "Anubis", "Sisifus", 

        # Kurgusal karakterler oyunlardan
        "Mario", "Luigi", "Link", "Zelda", "Pikachu", "Sonic", "Master Chief",
        "Kratos", "Geralt of Rivia", "Lara Croft", "Crash Bandicoot", "Sam Fisher", 
        "Solid Snake", "Doomguy", "Gordon Freeman", "Nathan Drake", "Ellie", 
        "Arthur Morgan", "Chun-Li", "Sub-Zero", "Scorpion", "Steve Minecraft", 
        "G-man", "Kirby", "Dante", "Vergil", "Ezio Auditore", "Leon S. Kennedy", 
        "Pac Man", "Sackboy", "CJ","Max Payne", "Agent 47", "Yasuo", "Ahri", "Zed", 
        "Darius", "Garen", "Lux", "Jinx", "Vayne", "Thresh", "Katarina", "V1", "2B", 
        "Jin Sakai", "Johnny Silverhand", "Malenia", "Dutch van der Linde", "Captain Price",
        "Albert Wesker", "Zelda", "Donkey Kong", "Tommy Vercetti", "Creeper", "Gabriel ULTRAKILL",
    ],
    
    
    
    "tarihi_olaylar": [
        "İstanbul'un Fethi", "Fransız İhtilali", "1. Dünya Savaşı", "2. Dünya Savaşı",
        "Aya İniş", "Kavimler Göçü", "Sanayi Devrimi", "Çernobil Faciası", 
        "Holokost", "Soğuk Savaş", "Haçlı Seferleri", "Rönesans",
        "Amerika'nın Keşfi", "Berlin Duvarı'nın Yıkılışı", "Sovyetlerin Dağılması"
        "İslam'ın Doğuşu", "Moğol İstilası", "Viking Çağı", "Roma'nın Yıkılışı",
        "Kurtuluş Savaşı", "İlk Atom Bombası", "Titanik'in Batışı", "9/11 Saldırıları",
        "Truva Savaşı", "Covid-19 Pandemisi", "Matbaanın İcadı", "Tekerleğin İcadı", 
        "Yazının İcadı", "Viyana Kuşatması", "Piramitlerin İnşası", "Atomun Parçalanması",
        "Kennedy Suikastı", "Kara Veba", "Babil'in Yıkılışı", "Çin Seddi'nin İnşası",
        "İsa'nın Doğumu", "Musa'nın Kızıldeniz'i Yarması", "Dinozor Fosillerinin Keşfi",
    ],
    
    "hayvanlar": [
        "Aslan", "Kaplan", "Fil", "Zürafa", "Panda", "Kanguru", "Zebra", "Goril",
        "Timsah", "Ayı", "Kurt", "Tilki", "Kedi", "Köpek", "At", "İnek", "Koyun",
        "Domuz", "Tavuk", "Ördek", "Kaz", "Sincap", "Fare", "Yarasa", "Papağan", 
        "Penguen", "Denizatı", "Ahtapot", "Yunus", "Balina", "Köpekbalığı", 
        "Denizanası", "T-Rex", "Yengeç", "Karides", "Istakoz", "Denizkızı", 
        "Megaladon", "Dodo", "Unicorn", "Griffin", "Phoenix", "Golem", "Hydra",
        "Kraken", "Minator", "Godzilla", "King Kong", "Çita", "Ejderha", "Kanarya",
    ],
    
}


def get_random_names(count: int, category: str = "populer_ikonlar") -> list[str]:
    """Seçilen kategoriden belirtilen sayıda benzersiz rastgele isim seç."""
    if category not in CATEGORIES:
        category = "populer_ikonlar"  # varsayılan veya hatalı kategori ise
        
    pool = CATEGORIES[category]
    
    if count > len(pool):
        raise ValueError(
            f"Seçilen kategoride en fazla {len(pool)} kelime var, {count} istendi."
        )
    return random.sample(pool, count)
