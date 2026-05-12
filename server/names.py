"""Ünlü isimler havuzu — oyunda oyunculara atanacak isimler."""

import random

FAMOUS_NAMES = [
    # Türk ünlüler
    "Atatürk",
    "Barış Manço",
    "Tarkan",
    "Müslüm Gürses",
    "Ajda Pekkan",
    "Kemal Sunal",
    "Adile Naşit",
    "Zeki Müren",
    "Fatih Sultan Mehmet",
    "Kanuni Sultan Süleyman",
    "Mevlana",
    "Nasreddin Hoca",
    "Hakan Şükür",
    "Arda Turan",
    "Kıvanç Tatlıtuğ",
    "Çağatay Ulusoy",
    "Haluk Bilginer",
    "Şener Şen",

    # Dünya ünlüleri
    "Albert Einstein",
    "Nikola Tesla",
    "Leonardo da Vinci",
    "Napoleon",
    "Kleopatra",
    "Mozart",
    "Beethoven",
    "Michael Jackson",
    "Elvis Presley",
    "Marilyn Monroe",
    "Charlie Chaplin",
    "Bruce Lee",
    "Muhammad Ali",
    "Lionel Messi",
    "Cristiano Ronaldo",
    "Michael Jordan",
    "Elon Musk",
    "Steve Jobs",
    "Bill Gates",
    "Mark Zuckerberg",

    # Film / Dizi / Oyun karakterleri
    "Darth Vader",
    "Harry Potter",
    "Gandalf",
    "Batman",
    "Spider-Man",
    "Sherlock Holmes",
    "James Bond",
    "Mario",
    "Sonic",
    "Pikachu",
    "Shrek",
    "Jack Sparrow",
    "Joker",
    "Thanos",
    "Goku",
    "Naruto",
    "Eren Jaeger",
    "Walter White",
    "Tony Montana",
    "Rocky Balboa",
]


def get_random_names(count: int) -> list[str]:
    """Havuzdan belirtilen sayıda benzersiz rastgele isim seç."""
    if count > len(FAMOUS_NAMES):
        raise ValueError(
            f"En fazla {len(FAMOUS_NAMES)} isim seçilebilir, {count} istendi."
        )
    return random.sample(FAMOUS_NAMES, count)
