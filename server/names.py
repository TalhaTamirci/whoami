"""Oyun havuzu — oyunda oyunculara atanacak kategorize edilmiş kelimeler."""

import random

CATEGORIES = {
    "unluler": [
        # Türk ünlüler
        "Atatürk", "Barış Manço", "Tarkan", "Müslüm Gürses", "Ajda Pekkan",
        "Kemal Sunal", "Adile Naşit", "Zeki Müren", "Fatih Sultan Mehmet",
        "Kanuni Sultan Süleyman", "Mevlana", "Nasreddin Hoca", "Hakan Şükür",
        "Arda Turan", "Kıvanç Tatlıtuğ", "Çağatay Ulusoy", "Haluk Bilginer", "Şener Şen",
        
        # Dünya ünlüleri
        "Albert Einstein", "Nikola Tesla", "Leonardo da Vinci", "Napoleon",
        "Kleopatra", "Mozart", "Beethoven", "Michael Jackson", "Elvis Presley",
        "Marilyn Monroe", "Charlie Chaplin", "Bruce Lee", "Muhammad Ali",
        "Lionel Messi", "Cristiano Ronaldo", "Michael Jordan", "Elon Musk",
        "Steve Jobs", "Bill Gates", "Mark Zuckerberg",
        
        # Karakterler
        "Darth Vader", "Harry Potter", "Gandalf", "Batman", "Spider-Man",
        "Sherlock Holmes", "James Bond", "Mario", "Sonic", "Pikachu",
        "Shrek", "Jack Sparrow", "Joker", "Thanos", "Goku", "Naruto",
        "Eren Jaeger", "Walter White", "Tony Montana", "Rocky Balboa"
    ],
    
    "irklar": [
        "İtalyan", "Amerikalı", "Hintli", "Yahudi", "Rus", "Türk", 
        "Japon", "İngiliz", "Alman", "Fransız", "Arap", "Çinli"
    ],
    
    "tarihi_olaylar": [
        "İstanbul'un Fethi", "Fransız İhtilali", "1. Dünya Savaşı", "2. Dünya Savaşı",
        "Aya İniş", "Kavimler Göçü", "Sanayi Devrimi", "Çernobil Faciası", 
        "Holokost", "Soğuk Savaş", "Haçlı Seferleri", "Rönesans",
        "Amerika'nın Keşfi", "Berlin Duvarı'nın Yıkılışı", "Sovyetlerin Dağılması"
    ]
}


def get_random_names(count: int, category: str = "unluler") -> list[str]:
    """Seçilen kategoriden belirtilen sayıda benzersiz rastgele isim seç."""
    if category not in CATEGORIES:
        category = "unluler"  # varsayılan veya hatalı kategori ise
        
    pool = CATEGORIES[category]
    
    if count > len(pool):
        raise ValueError(
            f"Seçilen kategoride en fazla {len(pool)} kelime var, {count} istendi."
        )
    return random.sample(pool, count)
