"""Oyun havuzu — oyunda oyunculara atanacak kategorize edilmiş kelimeler."""

import random

CATEGORIES = {
    "populer_ikonlar": [
        # ═══════════════ TÜRK ÜNLÜLERİ ═══════════════
        # Tarihi figürler / devlet adamları
        "Atatürk", "Fatih Sultan Mehmet", "Kanuni Sultan Süleyman", "Yavuz Sultan Selim",
        "II. Abdülhamid", "Vahdettin", "Osman Gazi", "Orhan Gazi", "I. Murat",
        "Yıldırım Beyazıt", "Sultan Alparslan", "Selçuklu Sultanı Melikşah",
        "Tuğrul Bey", "Çağrı Bey", "Atilla", "Mete Han", "Bilge Kağan", "Kül Tigin",
        "Mevlana", "Yunus Emre", "Nasreddin Hoca", "Şeyh Edebali", "Hacı Bektaş Veli",
        "Pir Sultan Abdal", "Karacaoğlan", "Köroğlu", "Dadaloğlu", "Şeyh Şamil",
        "Sabiha Gökçen", "Halide Edip Adıvar", "Nazım Hikmet", "Aziz Nesin",
        "Yaşar Kemal", "Orhan Pamuk", "Cemal Süreya", "Cahit Sıtkı Tarancı",
        "Necip Fazıl", "Mehmet Akif Ersoy", "Tevfik Fikret", "Sait Faik",
        "Aşık Veysel", "Neşet Ertaş", "Mahzuni Şerif", "Muharrem Ertaş",

        # Politikacılar
        "Recep Tayyip Erdoğan", "Kemal Kılıçdaroğlu", "Devlet Bahçeli",
        "Turgut Özal", "Bülent Ecevit", "Süleyman Demirel", "Adnan Menderes",
        "İsmet İnönü", "Necmettin Erbakan", "Tansu Çiller", "Mansur Yavaş",
        "Ekrem İmamoğlu", "Meral Akşener", "Ümit Özdağ", "Süleyman Soylu",
        "Cem Uzan", "Doğu Perinçek", "Mustafa Sarıgül", "Muharrem İnce",
        "Özgür Özel", "Hakan Fidan", "Mehmet Şimşek",

        # Sanatçılar / Şarkıcılar
        "Barış Manço", "Tarkan", "Müslüm Gürses", "Ajda Pekkan", "Zeki Müren",
        "Sezen Aksu", "Sertab Erener", "Murat Boz", "Bülent Ersoy", "Hadise",
        "Serdar Ortaç", "Aleyna Tilki", "Hande Yener", "Demet Akalın", "Petek Dinçöz",
        "Ebru Gündeş", "Sıla", "İbrahim Tatlıses", "Orhan Gencebay", "Ferdi Tayfur",
        "Kibariye", "Bergen", "Kayahan", "Ahmet Kaya", "Selda Bağcan",
        "Erkin Koray", "Cem Karaca", "Edip Akbayram", "Fikret Kızılok",
        "MFÖ", "Sezen Cumhur Önal", "Ceza", "Sagopa Kajmer", "Norm Ender",
        "Ezhel", "Khontkar", "Şanışer", "Ben Fero", "Lvbel C5", "Heijan",
        "Reynmen", "Mero", "Ufo361", "Massaka", "Allame", "Ais Ezhel",
        "Yıldız Tilbe", "Nilüfer", "Nükhet Duru", "Sezen Aksu", "Yonca Lodi",
        "Edis", "Mustafa Sandal", "Kenan Doğulu", "Hakan Peker", "Burcu Güneş",
        "Niran Ünsal", "Funda Arar", "Gülşen", "Hülya Avşar", "Tuğçe Kandemir",
        "Aydilge", "Manga", "Maneskin", "Mor ve Ötesi", "Duman", "Athena",
        "Pamela", "Doğuş", "Hakan Altun", "Gökhan Özen", "Soner Sarıkabadayı",

        # Sinema / TV
        "Kemal Sunal", "Adile Naşit", "Şener Şen", "Tarık Akan", "Türkan Şoray",
        "Cüneyt Arkın", "Filiz Akın", "Hülya Koçyiğit", "Fatma Girik", "Emel Sayın",
        "Müjde Ar", "Kadir İnanır", "Sadri Alışık", "Münir Özkul", "İlyas Salman",
        "Erdal Özyağcılar", "Haluk Bilginer", "Yılmaz Erdoğan", "Cem Yılmaz",
        "Şahan Gökbakar", "Ata Demirer", "Demet Evgar", "Beyazıt Öztürk",
        "Okan Bayülgen", "Mehmet Ali Erbil", "Acun Ilıcalı", "Esra Erol",
        "Müge Anlı", "Seda Sayan", "Hülya Avşar", "Songül Karlı", "Bülent Serttaş",
        "Kıvanç Tatlıtuğ", "Çağatay Ulusoy", "Can Yaman", "Burak Özçivit",
        "Engin Akyürek", "Halit Ergenç", "Beren Saat", "Hande Erçel", "Demet Özdemir",
        "Tuba Büyüküstün", "Fahriye Evcen", "Aras Bulut İynemli", "Birce Akalay",

        # Sporcular
        "Hakan Şükür", "Arda Turan", "Fatih Terim", "Metin Oktay", "Naim Süleymanoğlu",
        "Aziz Sancar", "Hidayet Türkoğlu", "Mehmet Okur", "Cedi Osman", "Şenol Güneş",
        "İlhan Mansız", "Rüştü Reçber", "Alpay Özalan", "Hasan Şaş", "Tugay Kerimoğlu",
        "Cenk Tosun", "Burak Yılmaz", "Hakan Çalhanoğlu", "Merih Demiral",
        "Çağlar Söyüncü", "Kaan Ayhan", "Ozan Tufan", "Yusuf Yazıcı", "Kerem Aktürkoğlu",
        "Mauro Icardi", "Edin Dzeko", "Dries Mertens", "Mert Günok", "Uğurcan Çakır",
        "Ersin Destanoğlu", "Sergen Yalçın", "Abdullah Avcı", "Vincenzo Montella",
        "Galip Öztürk", "Wilfried Zaha", "Kerem Demirbay", "Daniel Davari",
        "Mesut Özil", "İlkay Gündoğan", "Emre Can", "Süleyman Yıldırım",
        "Naim Süleymanoğlu", "Halil Mutlu", "Taha Akgül", "Rıza Kayaalp",
        "Yaşar Doğu", "Mahmut Atalay", "Hamza Yerlikaya", "Servet Tazegül",
        "Süreyya Ayhan", "Elvan Abeylegesse", "Nevin Yanıt", "Furkan Korkmaz",
        "Ersan İlyasova", "Hidayet Türkoğlu", "Mehmet Okur", "Ömer Aşık",

        # Bilim / Akademi
        "İlber Ortaylı", "Cahit Arf", "Oktay Sinanoğlu", "Feza Gürsey",
        "Aziz Sancar", "Canan Dağdeviren", "Ali Erdemir", "Murat Günak",
        "Halil İnalcık", "Doğan Kuban", "Celal Şengör",

        # Sosyal medya / YouTuber
        "Enes Batur", "Reynmen", "Orkun Işıtmak", "Danla Bilic", "Ruhi Çenet",
        "Berkcan Güven", "Kafalar", "Oğuzhan Uğur", "Hayrettin", "Mesut Süre",
        "Şahan Gökbakar", "Beyaz Show", "Pucca", "Kerimcan Durmaz", "Bilal Hancı",
        "Sefo", "Çağatay Akman", "Toprak Çelik", "Faruk Kuzu", "MidoNTW",
        "Wtcn", "PQueenLetsPlay", "Wolvoroth", "Jahrein", "Yiğit Talu",
        "Tuğkan", "Burak Reis", "Burak Oyunda", "Ebrar Karakaş", "İskender",

        # Zoktay & meşhur memeler (Türk internet kültürü)
        "Zoktay", "Hıçgıdık", "Dişsiz", "Enis Kirazoğlu",

        # ═══════════════ DÜNYA ÜNLÜLERİ ═══════════════
        # Bilim / Mucitler
        "Albert Einstein", "Nikola Tesla", "Isaac Newton", "Stephen Hawking",
        "Galileo Galilei", "Marie Curie", "Charles Darwin", "Thomas Edison",
        "Alexander Graham Bell", "Wright Kardeşler", "Henry Ford", "Karl Benz",
        "Rudolf Diesel", "James Watt", "Michael Faraday", "Max Planck",
        "Niels Bohr", "Werner Heisenberg", "Erwin Schrödinger", "Richard Feynman",
        "Carl Sagan", "Neil deGrasse Tyson", "Stephen Wolfram", "Alan Turing",
        "John von Neumann", "Ada Lovelace", "Grace Hopper", "Tim Berners-Lee",
        "Linus Torvalds", "Dennis Ritchie", "Ken Thompson", "Steve Wozniak",
        "Robert Oppenheimer", "Enrico Fermi", "Wernher von Braun", "Yuri Gagarin",
        "Neil Armstrong", "Buzz Aldrin", "Sergei Korolev", "Konstantin Tsiolkovsky",
        "Sigmund Freud", "Carl Jung", "Ivan Pavlov", "B.F. Skinner",
        "Louis Pasteur", "Alexander Fleming", "Jonas Salk", "Edward Jenner",
        "Gregor Mendel", "James Watson", "Francis Crick", "Rosalind Franklin",
        "Archimedes", "Pythagoras", "Euclid", "Hipokrat", "Aristoteles",
        "Eratosthenes", "Demokritos", "Empedokles", "Thales",

        # Filozoflar / Düşünürler
        "Sokrates", "Platon", "Aristoteles", "Konfüçyüs", "Lao Tzu", "Sun Tzu",
        "Friedrich Nietzsche", "Immanuel Kant", "Georg Hegel", "Karl Marx",
        "Friedrich Engels", "Voltaire", "Jean-Jacques Rousseau", "John Locke",
        "René Descartes", "Spinoza", "David Hume", "Adam Smith", "Søren Kierkegaard",
        "Jean-Paul Sartre", "Albert Camus", "Simone de Beauvoir", "Michel Foucault",
        "Noam Chomsky", "Slavoj Žižek", "Jordan Peterson", "Sam Harris",
        "Ibn Sina", "Farabi", "El-Kindi", "İbn-i Haldun", "İbn Rüşd",

        # Sanatçılar / Ressamlar / Müzisyenler
        "Leonardo da Vinci", "Michelangelo", "Raphael", "Donatello", "Botticelli",
        "Picasso", "Van Gogh", "Salvador Dalí", "Claude Monet", "Edvard Munch",
        "Rembrandt", "Vermeer", "Andy Warhol", "Frida Kahlo", "Henri Matisse",
        "Jackson Pollock", "Banksy", "Caravaggio", "Gustav Klimt", "M.C. Escher",
        "Mozart", "Beethoven", "Bach", "Chopin", "Tchaikovsky", "Vivaldi",
        "Wagner", "Brahms", "Schubert", "Handel", "Debussy", "Stravinsky",
        "Elvis Presley", "Michael Jackson", "Madonna", "Prince", "David Bowie",
        "Freddie Mercury", "John Lennon", "Paul McCartney", "Mick Jagger",
        "Bob Dylan", "Bruce Springsteen", "Stevie Wonder", "Aretha Franklin",
        "Whitney Houston", "Mariah Carey", "Beyoncé", "Rihanna", "Lady Gaga",
        "Taylor Swift", "Adele", "Ariana Grande", "Billie Eilish", "Dua Lipa",
        "Kanye West", "Jay-Z", "Drake", "Eminem", "Snoop Dogg", "Tupac Shakur",
        "Notorious B.I.G.", "Kendrick Lamar", "Travis Scott", "Post Malone",
        "Bad Bunny", "The Weeknd", "Bruno Mars", "Ed Sheeran", "Justin Bieber",
        "Selena Gomez", "Miley Cyrus", "Katy Perry", "Shakira", "Jennifer Lopez",
        "Bob Marley", "Tupac", "50 Cent", "Dr. Dre", "Lil Wayne", "Nicki Minaj",
        "Cardi B", "XXXTentacion", "Juice WRLD", "Lil Peep", "Mac Miller",
        "Pink Floyd üyesi", "Kurt Cobain", "Jim Morrison", "Jimi Hendrix",
        "Janis Joplin", "Amy Winehouse", "Tina Turner", "Cher", "Stevie Nicks",
        "Lana Del Rey", "Sia", "Olivia Rodrigo", "Doja Cat", "SZA",

        # Aktörler / Aktrisler
        "Charlie Chaplin", "Marilyn Monroe", "Audrey Hepburn", "Marlon Brando",
        "Robert De Niro", "Al Pacino", "Jack Nicholson", "Anthony Hopkins",
        "Morgan Freeman", "Tom Hanks", "Denzel Washington", "Samuel L. Jackson",
        "Leonardo DiCaprio", "Brad Pitt", "Johnny Depp", "Tom Cruise",
        "Will Smith", "Keanu Reeves", "Hugh Jackman", "Christian Bale",
        "Robert Downey Jr.", "Chris Hemsworth", "Chris Evans", "Mark Ruffalo",
        "Jeremy Renner", "Scarlett Johansson", "Angelina Jolie", "Jennifer Lawrence",
        "Emma Stone", "Emma Watson", "Anne Hathaway", "Natalie Portman",
        "Margot Robbie", "Zendaya", "Florence Pugh", "Anya Taylor-Joy",
        "Ryan Gosling", "Ryan Reynolds", "Matt Damon", "Ben Affleck",
        "Will Ferrell", "Jim Carrey", "Mike Myers", "Adam Sandler",
        "Eddie Murphy", "Chris Rock", "Kevin Hart", "Dave Chappelle",
        "Quentin Tarantino", "Steven Spielberg", "Christopher Nolan",
        "Martin Scorsese", "Francis Ford Coppola", "Stanley Kubrick",
        "Alfred Hitchcock", "Tim Burton", "James Cameron", "Peter Jackson",
        "Ridley Scott", "George Lucas", "Wes Anderson", "David Fincher",
        "Heath Ledger", "Joaquin Phoenix", "Cillian Murphy", "Pedro Pascal",
        "Henry Cavill", "Tom Holland", "Timothée Chalamet", "Andrew Garfield",
        "Tobey Maguire", "Daniel Radcliffe", "Rupert Grint", "Daniel Craig",
        "Pierce Brosnan", "Sean Connery", "Roger Moore", "Idris Elba",
        "Mr. Bean", "Rowan Atkinson", "Eddie Redmayne", "Benedict Cumberbatch",

        # Sporcular (Dünya)
        "Lionel Messi", "Cristiano Ronaldo", "Diego Maradona", "Pelé", "Zinedine Zidane",
        "Ronaldinho", "Ronaldo Nazario", "Neymar", "Kylian Mbappé", "Erling Haaland",
        "Vinicius Jr.", "Robert Lewandowski", "Kevin De Bruyne", "Mohamed Salah",
        "Sadio Mané", "Karim Benzema", "Luka Modric", "Toni Kroos", "Sergio Ramos",
        "Gerard Piqué", "Andrés Iniesta", "Xavi Hernández", "Iker Casillas",
        "Manuel Neuer", "Thibaut Courtois", "Gianluigi Buffon", "Iker Casillas",
        "David Beckham", "Frank Lampard", "Steven Gerrard", "Wayne Rooney",
        "Harry Kane", "Jude Bellingham", "Phil Foden", "Bukayo Saka",
        "Michael Jordan", "LeBron James", "Kobe Bryant", "Kareem Abdul-Jabbar",
        "Magic Johnson", "Larry Bird", "Shaquille O'Neal", "Tim Duncan",
        "Stephen Curry", "Kevin Durant", "Giannis Antetokounmpo", "Nikola Jokić",
        "Luka Dončić", "Joel Embiid", "Damian Lillard", "Russell Westbrook",
        "James Harden", "Chris Paul", "Kawhi Leonard", "Paul George",
        "Muhammad Ali", "Mike Tyson", "Floyd Mayweather", "Manny Pacquiao",
        "Anthony Joshua", "Tyson Fury", "Canelo Álvarez", "Sugar Ray Robinson",
        "Bruce Lee", "Conor McGregor", "Khabib Nurmagomedov", "Jon Jones",
        "Israel Adesanya", "Anderson Silva", "Georges St-Pierre", "Brock Lesnar",
        "The Rock", "John Cena", "Stone Cold Steve Austin", "Undertaker",
        "Hulk Hogan", "Triple H", "Roman Reigns", "CM Punk",
        "Usain Bolt", "Carl Lewis", "Michael Phelps", "Mark Spitz",
        "Tiger Woods", "Rory McIlroy", "Roger Federer", "Rafael Nadal",
        "Novak Djokovic", "Serena Williams", "Venus Williams", "Maria Sharapova",
        "Lewis Hamilton", "Max Verstappen", "Michael Schumacher", "Ayrton Senna",
        "Sebastian Vettel", "Fernando Alonso", "Charles Leclerc", "Niki Lauda",
        "Valentino Rossi", "Marc Marquez",

        # Politikacılar / Liderler / Tarihi figürler
        "Napoleon Bonaparte", "Kleopatra", "Jül Sezar", "Büyük İskender", "Cengiz Han",
        "Atilla", "Timur", "I. Petro", "Katherine the Great", "Kraliçe Elizabeth",
        "II. Elizabeth", "Kraliçe Victoria", "Kral Henry VIII", "Kraliçe Mary",
        "Louis XIV", "Marie Antoinette", "Maximilien Robespierre", "Napolyon III",
        "Bismarck", "Garibaldi", "Mahatma Gandhi", "Nelson Mandela", "Martin Luther King",
        "Malcolm X", "Rosa Parks", "Abraham Lincoln", "George Washington", "Thomas Jefferson",
        "Benjamin Franklin", "John F. Kennedy", "Richard Nixon", "Ronald Reagan",
        "Bill Clinton", "George W. Bush", "Barack Obama", "Donald Trump",
        "Joe Biden", "Kamala Harris", "Hillary Clinton", "Vladimir Putin",
        "Dmitry Medvedev", "Mikhail Gorbachev", "Boris Yeltsin", "Joseph Stalin",
        "Vladimir Lenin", "Leon Trotsky", "Karl Marx", "Friedrich Engels",
        "Adolf Hitler", "Benito Mussolini", "Francisco Franco", "Hirohito",
        "Hideki Tojo", "Mao Zedong", "Deng Xiaoping", "Xi Jinping", "Kim Il-sung",
        "Kim Jong-il", "Kim Jong-un", "Ho Chi Minh", "Pol Pot", "Saddam Hüseyin",
        "Muammer Kaddafi", "Bashar Esad", "Hafız Esad", "Mahmud Abbas", "Yaser Arafat",
        "Hassan Nasrallah", "Ayetullah Humeyni", "Şah Pehlevi", "Benyamin Netanyahu",
        "Golda Meir", "Yitzhak Rabin", "Ariel Sharon", "Margaret Thatcher",
        "Winston Churchill", "Tony Blair", "David Cameron", "Boris Johnson",
        "Liz Truss", "Rishi Sunak", "Keir Starmer", "Angela Merkel", "Olaf Scholz",
        "Helmut Kohl", "Konrad Adenauer", "Charles de Gaulle", "François Mitterrand",
        "Jacques Chirac", "Nicolas Sarkozy", "François Hollande", "Emmanuel Macron",
        "Silvio Berlusconi", "Mario Draghi", "Giorgia Meloni", "Justin Trudeau",
        "Stephen Harper", "Hugo Chávez", "Nicolás Maduro", "Fidel Castro",
        "Raúl Castro", "Che Guevara", "Salvador Allende", "Augusto Pinochet",
        "Juan Perón", "Eva Perón", "Lula da Silva", "Jair Bolsonaro",
        "Hz. Muhammed", "Hz. İsa", "Hz. Musa", "Hz. Adem", "Hz. Nuh",
        "Hz. İbrahim", "Hz. Yusuf", "Hz. Ali", "Hz. Ömer", "Hz. Ebu Bekir",
        "Hz. Osman", "Hz. Hatice", "Hz. Ayşe", "Hz. Fatma", "Hz. Hüseyin", "Hz. Hasan",
        "Buda", "Konfüçyüs", "Lao Tzu", "Zerdüşt", "Mahatma Gandhi",
        "Papa Francis", "Papa II. Jean Paul", "Anne Teresa",

        # İş insanları / Girişimciler
        "Elon Musk", "Jeff Bezos", "Bill Gates", "Steve Jobs", "Mark Zuckerberg",
        "Warren Buffett", "Larry Page", "Sergey Brin", "Sundar Pichai", "Tim Cook",
        "Satya Nadella", "Jensen Huang", "Sam Altman", "Bernard Arnault",
        "Carlos Slim", "Mukesh Ambani", "Jack Ma", "Pony Ma", "Masayoshi Son",
        "Larry Ellison", "Michael Bloomberg", "Rupert Murdoch", "Richard Branson",
        "Howard Schultz", "Walt Disney", "Henry Ford", "John D. Rockefeller",
        "Andrew Carnegie", "J.P. Morgan", "Cornelius Vanderbilt", "Rothschild",

        # Suçlular / Mafyalar / Kötü şöhretli
        "Jeffrey Epstein", "Diddy", "Al Capone", "Pablo Escobar", "El Chapo",
        "John Gotti", "Lucky Luciano", "Charles Manson", "Ted Bundy",
        "Jeffrey Dahmer", "Hannibal Lecter", "Jack the Ripper", "Bonnie ve Clyde",
        "Osama bin Laden", "Ebu Bekir el-Bağdadi", "Eyman Zevahiri",

        # Modeller / Sosyal medya / İnternet kişilikleri
        "Mia Khalifa", "Kim Kardashian", "Kylie Jenner", "Kendall Jenner",
        "Khloé Kardashian", "Kourtney Kardashian", "Paris Hilton", "Bella Hadid",
        "Gigi Hadid", "Cara Delevingne", "Naomi Campbell", "Heidi Klum",
        "Mr.Beast", "PewDiePie", "Markiplier", "Jacksepticeye", "Logan Paul",
        "Jake Paul", "KSI", "Sidemen", "Ninja", "Pokimane", "Shroud",
        "Tfue", "Dr Disrespect", "xQc", "Asmongold", "Kai Cenat", "IShowSpeed",
        "Andrew Tate", "Tristan Tate", "Joe Rogan", "Lex Fridman", "Ben Shapiro",

        # ═══════════════ KURGUSAL KARAKTERLER ═══════════════
        # Marvel
        "Iron Man", "Captain America", "Thor", "Hulk", "Black Widow", "Hawkeye",
        "Doctor Strange", "Spider-Man", "Black Panther", "Captain Marvel",
        "Scarlet Witch", "Vision", "Falcon", "Winter Soldier", "Ant-Man",
        "Wasp", "Star-Lord", "Gamora", "Drax", "Rocket Raccoon", "Groot",
        "Thanos", "Loki", "Ultron", "Magneto", "Professor X", "Wolverine",
        "Cyclops", "Storm", "Jean Grey", "Mystique", "Deadpool", "Venom",
        "Carnage", "Daredevil", "Punisher", "Ghost Rider", "Silver Surfer",
        "Galactus", "Kang the Conqueror", "Doctor Doom", "Green Goblin",
        "Doctor Octopus", "Sandman", "Lizard", "Rhino", "Kingpin", "Nick Fury",

        # DC
        "Batman", "Superman", "Wonder Woman", "Flash", "Aquaman", "Cyborg",
        "Green Lantern", "Green Arrow", "Martian Manhunter", "Shazam",
        "Black Canary", "Hawkgirl", "Zatanna", "Constantine", "Swamp Thing",
        "Joker", "Harley Quinn", "Penguin", "Riddler", "Two-Face", "Bane",
        "Scarecrow", "Mr. Freeze", "Poison Ivy", "Catwoman", "Killer Croc",
        "Lex Luthor", "Brainiac", "Darkseid", "Doomsday", "General Zod",
        "Black Manta", "Sinestro", "Reverse-Flash", "Captain Cold", "Deathstroke",
        "Robin", "Nightwing", "Red Hood", "Batgirl", "Supergirl", "Krypto",

        # Star Wars
        "Luke Skywalker", "Darth Vader", "Leia Organa", "Han Solo", "Chewbacca",
        "Obi-Wan Kenobi", "Yoda", "Mace Windu", "Anakin Skywalker", "Palpatine",
        "Darth Sidious", "Darth Maul", "Count Dooku", "General Grievous",
        "Kylo Ren", "Rey", "Finn", "Poe Dameron", "BB-8", "R2-D2", "C-3PO",
        "Padmé Amidala", "Qui-Gon Jinn", "Mandalorian", "Boba Fett", "Jango Fett",
        "Lando Calrissian", "Grand Moff Tarkin", "Captain Phasma", "Snoke",
        "Ahsoka Tano", "Grogu", "Cad Bane", "Bo-Katan",

        # Harry Potter
        "Harry Potter", "Hermione Granger", "Ron Weasley", "Albus Dumbledore",
        "Severus Snape", "Voldemort", "Sirius Black", "Remus Lupin", "Hagrid",
        "Draco Malfoy", "Lucius Malfoy", "Bellatrix Lestrange", "Minerva McGonagall",
        "Luna Lovegood", "Neville Longbottom", "Ginny Weasley", "Fred Weasley",
        "George Weasley", "Cedric Diggory", "Cho Chang", "Dobby", "Kreacher",
        "Nymphadora Tonks", "Mad-Eye Moody", "Dolores Umbridge", "Lily Potter",
        "James Potter", "Tom Riddle", "Newt Scamander", "Grindelwald",

        # Yüzüklerin Efendisi
        "Frodo Baggins", "Bilbo Baggins", "Gandalf", "Aragorn", "Legolas", "Gimli",
        "Samwise Gamgee", "Merry", "Pippin", "Boromir", "Faramir", "Sauron",
        "Saruman", "Gollum", "Smeagol", "Elrond", "Galadriel", "Arwen",
        "Théoden", "Éowyn", "Éomer", "Treebeard", "Tom Bombadil", "Witch-King",
        "Smaug", "Thorin Oakenshield", "Balrog", "Shelob",

        # Game of Thrones
        "Jon Snow", "Daenerys Targaryen", "Tyrion Lannister", "Cersei Lannister",
        "Jaime Lannister", "Tywin Lannister", "Robb Stark", "Sansa Stark",
        "Arya Stark", "Bran Stark", "Ned Stark", "Catelyn Stark", "Robert Baratheon",
        "Stannis Baratheon", "Renly Baratheon", "Joffrey Baratheon", "Tommen Baratheon",
        "Theon Greyjoy", "Yara Greyjoy", "Euron Greyjoy", "Brienne of Tarth",
        "Sandor Clegane", "Gregor Clegane", "Petyr Baelish", "Varys",
        "Melisandre", "Ramsay Bolton", "Roose Bolton", "Khal Drogo", "Hodor",
        "Night King", "Drogon", "Viserion", "Rhaegal",

        # Disney / Pixar / Animasyon
        "Mickey Mouse", "Minnie Mouse", "Donald Duck", "Goofy", "Pluto",
        "Buzz Lightyear", "Woody", "Jessie", "Mr. Potato Head", "Rex",
        "Çizmeli Kedi", "Shrek", "Fiona", "Lord Farquaad", "Eşek",
        "Aladdin", "Yasemin", "Cin", "Cafer", "Ariel", "Sebastian",
        "Külkedisi", "Pamuk Prenses", "Uyuyan Güzel", "Bella", "Canavar",
        "Karlar Ülkesi Elsa", "Anna", "Olaf", "Kristoff", "Sven",
        "Moana", "Maui", "Simba", "Mufasa", "Scar", "Timon", "Pumba",
        "Aslan Kral", "Tarzan", "Jane", "Pocahontas", "Mulan", "Mushu",
        "Stitch", "Lilo", "Wall-E", "EVE", "Nemo", "Marlin", "Dory",
        "Bay İnanılmaz", "Şirinler", "Şirine", "Gargamel", "Köfte",
        "Pinokyo", "Geppetto", "Cricket", "Peter Pan", "Tinkerbell",
        "Kaptan Hook", "Kara Sakal", "Süngerbob", "Patrick Star", "Octopus",
        "Plankton", "Sandy Cheeks", "Mr. Krabs", "Gary", "Pearl",
        "Bart Simpson", "Homer Simpson", "Marge Simpson", "Lisa Simpson",
        "Maggie Simpson", "Ned Flanders", "Mr. Burns", "Smithers", "Apu",
        "Peter Griffin", "Stewie Griffin", "Brian Griffin", "Lois Griffin",
        "Chris Griffin", "Meg Griffin", "Glenn Quagmire", "Joe Swanson",
        "Eric Cartman", "Stan Marsh", "Kyle Broflovski", "Kenny McCormick",
        "Rick Sanchez", "Morty Smith", "Summer Smith", "Beth Smith", "Jerry Smith",
        "Bob Belcher", "Linda Belcher", "Tina Belcher", "Gene Belcher", "Louise Belcher",
        "Finn", "Jake the Dog", "Princess Bubblegum", "Marceline", "Ice King",
        "BMO", "Lemongrab", "Gumball", "Darwin", "Anais", "Richard Watterson",
        "Mordecai", "Rigby", "Benson", "Pops", "Skips", "Muscle Man",
        "Doraemon", "Nobita", "Shizuka", "Dekisugi", "Gian", "Suneo",
        "Dexter", "Dee Dee", "Powerpuff Kızları", "Mojo Jojo", "Profesör Utonium",
        "Garfield", "Odie", "Jon Arbuckle", "Tom", "Jerry", "Tweety", "Sylvester",
        "Bugs Bunny", "Daffy Duck", "Porky Pig", "Yosemite Sam", "Foghorn Leghorn",
        "Wile E. Coyote", "Road Runner", "Pepe Le Pew", "Marvin the Martian",
        "Scooby-Doo", "Shaggy", "Fred", "Daphne", "Velma", "Hıçgıdık",
        "Çakıltaşları", "Caillou", "Sünger Bob", "Tom ve Jerry", "Heidi",
        "Pokoyo", "Maşa", "Maşa ile Koca Ayı", "Niloya", "Pepe",
        "Pikachu", "Charizard", "Mewtwo", "Mew", "Eevee", "Bulbasaur",
        "Squirtle", "Jigglypuff", "Snorlax", "Gengar", "Lucario", "Greninja",

        # Anime / Manga
        "Goku", "Vegeta", "Gohan", "Trunks", "Piccolo", "Freezer", "Cell",
        "Majin Buu", "Beerus", "Whis", "Bulma", "Chi-Chi", "Master Roshi",
        "Naruto Uzumaki", "Sasuke Uchiha", "Sakura Haruno", "Kakashi Hatake",
        "Itachi Uchiha", "Madara Uchiha", "Pain", "Obito", "Jiraiya",
        "Tsunade", "Orochimaru", "Hinata", "Gaara", "Rock Lee", "Neji",
        "Shikamaru", "Kiba", "Boruto", "Sarada", "Mitsuki", "Konohamaru",
        "Monkey D. Luffy", "Roronoa Zoro", "Nami", "Usopp", "Sanji", "Chopper",
        "Nico Robin", "Franky", "Brook", "Jinbei", "Shanks", "Whitebeard",
        "Kaido", "Big Mom", "Blackbeard", "Mihawk", "Boa Hancock", "Buggy",
        "Ace", "Sabo", "Doflamingo", "Crocodile", "Eren Yeager", "Mikasa Ackerman",
        "Armin Arlert", "Levi Ackerman", "Erwin Smith", "Hange Zoe", "Reiner Braun",
        "Bertholdt Hoover", "Annie Leonhart", "Historia Reiss", "Ymir",
        "Zeke Yeager", "Grisha Yeager", "Saitama", "Genos", "Tatsumaki",
        "Garou", "Boros", "King Saitama", "Light Yagami", "L Lawliet",
        "Ryuk", "Misa Amane", "Near", "Mello", "Soichiro Yagami",
        "Edward Elric", "Alphonse Elric", "Roy Mustang", "Riza Hawkeye",
        "Winry Rockbell", "Scar", "Father", "Greed", "Lust", "Envy",
        "Tanjiro Kamado", "Nezuko Kamado", "Zenitsu", "Inosuke", "Giyu Tomioka",
        "Shinobu Kocho", "Kyojuro Rengoku", "Muzan Kibutsuji", "Akaza",
        "Yuji Itadori", "Megumi Fushiguro", "Nobara Kugisaki", "Satoru Gojo",
        "Suguru Geto", "Sukuna", "Toji Fushiguro", "Mahito", "Choso",
        "Yuta Okkotsu", "Maki Zenin", "Toge Inumaki", "Panda",
        "Ichigo Kurosaki", "Rukia Kuchiki", "Renji Abarai", "Byakuya Kuchiki",
        "Kenpachi Zaraki", "Aizen", "Ulquiorra", "Grimmjow",
        "Killua Zoldyck", "Gon Freecss", "Kurapika", "Leorio", "Hisoka",
        "Chrollo Lucilfer", "Meruem", "Komugi", "Ging Freecss",
        "Ken Kaneki", "Touka Kirishima", "Rize Kamishiro", "Arima",
        "Spike Spiegel", "Jet Black", "Faye Valentine", "Ed", "Ein",
        "Vash the Stampede", "Trigun", "Roy Mustang", "Mob", "Reigen",
        "Senku Ishigami", "Taiju", "Tsukasa", "Asta", "Yuno", "Yami Sukehiro",
        "Noelle Silva", "Mereoleona", "Julius", "Inuyasha", "Kagome",
        "Sesshomaru", "Miroku", "Sango", "Kikyo", "Naraku", "Shippo",
        "Gintoki Sakata", "Hijikata", "Kondo", "Kagura", "Shinpachi",
        "Lelouch Lamperouge", "Suzaku", "C.C.", "Zero", "Korra", "Aang",
        "Katara", "Sokka", "Toph", "Zuko", "Iroh", "Azula", "Ozai",
        "Yusuke Urameshi", "Hiei", "Kurama", "Kuwabara", "Toguro", "Sensui",
        "Allen Walker", "Yu Kanda", "Lavi", "Lenalee", "Tyki Mikk",
        "Roronoa Zoro", "Portgas D. Ace", "Trafalgar Law", "Eustass Kid",
        "Killer", "Bonney", "Bege", "Caesar Clown", "Vergo", "Smoker",
        "Tashigi", "Coby", "Helmeppo", "Gyro Zeppeli", "Johnny Joestar",
        "Dio Brando", "Giorno Giovanna", "Jotaro Kujo", "Joseph Joestar",
        "Jonathan Joestar", "Josuke Higashikata", "Kira Yoshikage", "Bruno Bucciarati",
        "Guido Mista", "Pannacotta Fugo", "Narancia Ghirga", "Leone Abbacchio",
        "Reborn", "Tsuna", "Gokudera", "Yamamoto", "Hibari", "Mukuro",
        "Griffith", "Guts", "Casca", "Puck", "Skull Knight",
        "Asuka Langley", "Shinji Ikari", "Rei Ayanami", "Gendo Ikari", "Misato",
        "Edward Newgate", "Marshall D. Teach", "Sengoku", "Garp", "Akainu",

        # Filmler / Diziler / Diğer karakterler
        "Walter White", "Jesse Pinkman", "Saul Goodman", "Mike Ehrmantraut",
        "Gus Fring", "Tuco Salamanca", "Hector Salamanca", "Skyler White",
        "Hank Schrader", "Marie Schrader", "Tony Montana", "Vito Corleone",
        "Michael Corleone", "Sonny Corleone", "Fredo Corleone", "Don Vito",
        "Henry Hill", "Tommy DeVito", "Jimmy Conway", "Joe Pesci karakteri",
        "Rocky Balboa", "Apollo Creed", "Clubber Lang", "Ivan Drago", "Tommy Gunn",
        "Adrian", "Paulie", "Mickey", "Tony Soprano", "Carmela Soprano",
        "Christopher Moltisanti", "Paulie Walnuts", "Silvio Dante",
        "Tyler Durden", "Narrator (Fight Club)", "Marla Singer", "Patrick Bateman",
        "Travis Bickle", "Jules Winnfield", "Vincent Vega", "Marsellus Wallace",
        "Mia Wallace", "Jack Sparrow", "Will Turner", "Elizabeth Swann",
        "Davy Jones", "Hector Barbossa", "Blackbeard", "John Wick", "Winston",
        "Charon", "Bowery King", "Ms. Perkins", "Sherlock Holmes", "Dr. Watson",
        "Moriarty", "Mycroft", "Irene Adler", "James Bond", "M", "Q",
        "Le Chiffre", "Goldfinger", "Dr. No", "Blofeld", "Jaws", "Indiana Jones",
        "Mola Ram", "Short Round", "Marion Ravenwood", "Forrest Gump", "Jenny",
        "Lieutenant Dan", "Bubba", "Neo", "Morpheus", "Trinity", "Agent Smith",
        "Cypher", "Architect", "Oracle", "Niobe", "Maximus", "Commodus",
        "John McClane", "Hans Gruber", "Ellis", "Holly Gennaro", "Jason Bourne",
        "Ethan Hunt", "Marty McFly", "Doc Brown", "Biff Tannen", "Jennifer Parker",
        "Ron Burgundy", "Brick Tamland", "Anchorman", "Borat", "Bruno",
        "Ali G", "Ace Ventura", "The Mask", "Truman Burbank", "Andy Dufresne",
        "Red Redding", "Warden Norton", "Hannibal Lecter", "Clarice Starling",
        "Buffalo Bill", "Jason Voorhees", "Michael Myers", "Freddy Krueger",
        "Pinhead", "Chucky", "Pennywise", "Annabelle", "Samara", "Sadako",
        "Ghostface", "Leatherface", "Predator", "Alien", "Xenomorph", "Ripley",
        "T-800", "T-1000", "John Connor", "Sarah Connor", "Kyle Reese",
        "RoboCop", "ED-209", "Mad Max", "Furiosa", "Immortan Joe", "Joker (Phoenix)",
        "Arthur Fleck", "Ledger Joker", "Heath Ledger Joker", "Two-Face Dent",
        "Bruce Wayne", "Alfred Pennyworth", "Lucius Fox", "Commissioner Gordon",
        "Rachel Dawes", "Selina Kyle", "Talia al Ghul", "Ra's al Ghul",
        "Eleven", "Mike Wheeler", "Dustin", "Lucas", "Will Byers", "Max Mayfield",
        "Jim Hopper", "Joyce Byers", "Nancy Wheeler", "Steve Harrington", "Robin",
        "Vecna", "Demogorgon", "Mind Flayer", "Henry Creel",
        "Daenerys", "Drogo", "Tyrion", "Jon Snow", "Cersei",
        "Wednesday Addams", "Pugsley Addams", "Morticia Addams", "Gomez Addams",
        "Lurch", "Cousin Itt", "Geralt of Rivia", "Yennefer", "Triss",
        "Ciri", "Vesemir", "Lambert", "Eskel", "Joey Tribbiani",
        "Ross Geller", "Rachel Green", "Monica Geller", "Chandler Bing",
        "Phoebe Buffay", "Gunther", "Janice", "Barney Stinson", "Ted Mosby",
        "Marshall Eriksen", "Lily Aldrin", "Robin Scherbatsky", "Sheldon Cooper",
        "Leonard Hofstadter", "Howard Wolowitz", "Raj Koothrappali", "Penny",
        "Bernadette", "Amy Farrah Fowler", "Stuart", "Michael Scott",
        "Jim Halpert", "Pam Beesly", "Dwight Schrute", "Andy Bernard",
        "Stanley Hudson", "Kevin Malone", "Oscar Martinez", "Angela Martin",
        "Toby Flenderson", "Creed Bratton", "Kelly Kapoor", "Ryan Howard",
        "Erlich Bachman", "Richard Hendricks", "Gilfoyle", "Dinesh", "Jared",
        "Don Draper", "Peggy Olson", "Roger Sterling", "Joan Holloway",
        "House M.D.", "Dr. Cuddy", "Dr. Wilson", "Dexter Morgan", "Debra Morgan",
        "Trinity Killer", "Rita Bennett", "Hannah McKay", "Frank Underwood",
        "Claire Underwood", "Doug Stamper", "Olivia Pope", "Carrie Mathison",
        "Brody", "Saul Berenson", "Quinn", "Joel Miller", "Ellie",
        "Tommy Miller", "Tess", "Bill", "Frank", "Abby Anderson", "Owen",
        "Lev", "Yara", "Mufasa", "Boba Fett", "Mandalorian", "Din Djarin",
        "Grogu", "Bo-Katan", "Moff Gideon", "Cad Bane", "Mando", "Yoda Bebek",
        "Ash Ketchum", "Misty", "Brock", "Team Rocket", "Jessie", "James",
        "Meowth", "Gary Oak", "Squidward", "Sandy Cheeks", "Larry the Lobster",
        "Recep İvedik", "Şaban", "Çetin Çakır", "Çete Çakır", "Yavuz Bay",
        "Cüneyt Arkın karakteri", "Adanalı Maraz Ali", "Behzat Ç.", "Murat Boz",
        "Polat Alemdar", "Memati", "Ezel", "Cengiz Atay", "Ali Vefa",
        "Eşkıya Baran", "İskender Büyük", "Halil İbrahim", "Yaman", "Mira",

        # Video Oyun Karakterleri
        "Mario", "Luigi", "Princess Peach", "Bowser", "Yoshi", "Toad",
        "Donkey Kong", "Diddy Kong", "Wario", "Waluigi", "Daisy", "Rosalina",
        "Link", "Zelda", "Ganondorf", "Sheik", "Tingle", "Skull Kid",
        "Pikachu", "Charizard", "Mewtwo", "Snorlax", "Eevee", "Gengar",
        "Sonic the Hedgehog", "Tails", "Knuckles", "Amy Rose", "Shadow",
        "Dr. Eggman", "Silver", "Big the Cat", "Cream", "Rouge",
        "Master Chief", "Cortana", "Arbiter", "Sergeant Johnson", "Captain Keyes",
        "Kratos", "Atreus", "Faye", "Mimir", "Baldur", "Tyr", "Odin",
        "Geralt of Rivia", "Yennefer", "Triss Merigold", "Ciri", "Dandelion",
        "Vesemir", "Eredin", "Olgierd", "Lara Croft", "Crash Bandicoot",
        "Coco Bandicoot", "Aku Aku", "Doctor Cortex", "Spyro", "Sparx",
        "Sam Fisher", "Solid Snake", "Big Boss", "Liquid Snake", "Revolver Ocelot",
        "Raiden", "Psycho Mantis", "Sniper Wolf", "The Boss", "Otacon",
        "Doomguy", "Doom Slayer", "Cyberdemon", "Mancubus", "Imp",
        "Gordon Freeman", "Alyx Vance", "G-Man", "Combine Soldier", "Father Grigori",
        "Nathan Drake", "Sully", "Elena", "Chloe", "Sam Drake",
        "Ellie", "Joel", "Tommy", "Abby", "Lev", "Tess", "Riley",
        "Arthur Morgan", "John Marston", "Dutch van der Linde", "Sadie Adler",
        "Bill Williamson", "Javier Escuella", "Charles Smith", "Hosea Matthews",
        "Lenny Summers", "Micah Bell", "Karen Jones", "Tilly Jackson",
        "CJ", "Big Smoke", "Ryder", "Sweet", "Cesar", "Mike Toreno",
        "Officer Tenpenny", "Tommy Vercetti", "Lance Vance", "Sonny Forelli",
        "Niko Bellic", "Roman Bellic", "Brucie Kibbutz", "Patrick McReary",
        "Michael De Santa", "Trevor Philips", "Franklin Clinton", "Lamar Davis",
        "Lester Crest", "Chop", "Wei Cheng", "Steve Haines", "Jimmy De Santa",
        "Tracey De Santa", "Amanda De Santa", "Chun-Li", "Ryu", "Ken",
        "Akuma", "Cammy", "Sagat", "Vega", "M. Bison", "Zangief", "Dhalsim",
        "Blanka", "E. Honda", "Sub-Zero", "Scorpion", "Raiden", "Liu Kang",
        "Johnny Cage", "Sonya Blade", "Jax", "Kano", "Mileena", "Kitana",
        "Goro", "Shao Kahn", "Quan Chi", "Shang Tsung", "Reptile", "Smoke",
        "Steve (Minecraft)", "Alex (Minecraft)", "Creeper", "Enderman", "Zombie",
        "Skeleton", "Wither", "Ender Dragon", "Pillager", "Ravager",
        "Kirby", "Meta Knight", "King Dedede", "Waddle Dee", "Magolor",
        "Dante", "Vergil", "Nero", "Trish", "Lady", "Mundus", "V",
        "Ezio Auditore", "Altaïr", "Connor Kenway", "Edward Kenway", "Bayek",
        "Alexios", "Kassandra", "Eivor", "Leon S. Kennedy", "Claire Redfield",
        "Chris Redfield", "Jill Valentine", "Ada Wong", "Wesker", "Nemesis",
        "Mr. X", "Tyrant", "Lady Dimitrescu", "Ethan Winters", "Mia Winters",
        "Pac-Man", "Inky", "Blinky", "Pinky", "Clyde", "Ms. Pac-Man",
        "Sackboy", "Q*bert", "Mega Man", "Dr. Wily", "Roll", "Bass", "Proto Man",
        "Max Payne", "Mona Sax", "Vlad Lem", "Agent 47", "Diana Burnwood",
        "Yasuo", "Ahri", "Zed", "Darius", "Garen", "Lux", "Jinx", "Vayne",
        "Thresh", "Katarina", "Ezreal", "Yone", "Akali", "Kayn", "Pyke",
        "Caitlyn", "Vi", "Jayce", "Heimerdinger", "Viktor", "Mel Medarda",
        "Silco", "Singed", "Warwick", "Powder", "Violet", "Ekko",
        "Reaper", "Tracer", "Genji", "Hanzo", "Mercy", "D.Va", "Pharah",
        "Soldier 76", "Sombra", "Widowmaker", "Winston", "Lúcio", "Junkrat",
        "Roadhog", "Mei", "Zarya", "Symmetra", "Moira", "Doomfist",
        "V1", "V2", "Gabriel ULTRAKILL", "2B", "9S", "A2", "Pascal",
        "Adam", "Eve", "YoRHa", "Jin Sakai", "Yuna", "Ryuzo", "Khotun Khan",
        "Johnny Silverhand", "V (Cyberpunk)", "Jackie Welles", "Panam Palmer",
        "Judy Alvarez", "Rogue", "Adam Smasher", "Yorinobu Arasaka",
        "Malenia", "Radahn", "Marika", "Ranni", "Godrick", "Morgott",
        "Mohg", "Maliketh", "Radagon", "Elden Beast", "Margit", "Godfrey",
        "Captain Price", "Soap MacTavish", "Ghost", "Gaz", "Makarov",
        "Albert Wesker", "Hunk", "Sherry Birkin", "Tommy Vercetti", "CJ",
        "Donkey Kong", "Phoenix Wright", "Maya Fey", "Edgeworth", "Apollo Justice",
        "Cloud Strife", "Tifa Lockhart", "Aerith Gainsborough", "Barret Wallace",
        "Sephiroth", "Vincent Valentine", "Yuffie Kisaragi", "Cid Highwind",
        "Squall Leonhart", "Rinoa Heartilly", "Zidane Tribal", "Garnet Til Alexandros",
        "Vivi Ornitier", "Tidus", "Yuna", "Auron", "Wakka", "Lulu",
        "Lightning", "Snow", "Hope", "Vanille", "Sazh", "Noctis Lucis Caelum",
        "Gladiolus", "Ignis", "Prompto", "Crash Bandicoot", "Sora", "Riku",
        "Kairi", "Mickey", "Donald", "Goofy", "Ansem", "Xemnas",
        "Marcus Fenix", "Dom Santiago", "Cole Train", "Anya Stroud", "JD Fenix",
        "Isaac Clarke", "Nicole Brennan", "Booker DeWitt", "Elizabeth", "Songbird",
        "Andrew Ryan", "Atlas", "Big Daddy", "Little Sister", "Subject Delta",
        "Eleanor Lamb", "Tenenbaum", "Splicer", "Jack Ryan", "Frank Fontaine",
        "Lee Everett", "Clementine", "Kenny", "Carley", "AJ", "Christa",
        "Dishonored Corvo", "Emily Kaldwin", "Daud", "The Outsider", "Billie Lurk",
        "Tommy", "Joel", "Ellie", "Lara Croft", "Captain MacMillan",
        "Sam Greenfield", "Bayonetta", "Jeanne", "Cereza", "Rodin", "Luka",

        # Dini / Mitolojik figürler
        "Zeus", "Poseidon", "Hades", "Hera", "Athena", "Apollo", "Artemis",
        "Ares", "Aphrodite", "Hephaestus", "Hermes", "Demeter", "Dionysus",
        "Persephone", "Hestia", "Cronos", "Rhea", "Uranus", "Gaia",
        "Helios", "Selene", "Eros", "Pan", "Nike", "Iris", "Hekate",
        "Tyche", "Hypnos", "Thanatos", "Nyx", "Erebus",
        "Odin", "Thor", "Loki", "Frigg", "Freya", "Freyr", "Heimdall",
        "Tyr", "Balder", "Hodr", "Hel", "Fenrir", "Jormungandr", "Sleipnir",
        "Surtr", "Ymir", "Vidar", "Vali", "Bragi", "Idunn", "Sif",
        "Ra", "Anubis", "Horus", "Osiris", "Set", "Isis", "Thoth", "Bastet",
        "Sekhmet", "Hathor", "Sobek", "Maat", "Ptah", "Nephthys", "Khepri",
        "Vishnu", "Shiva", "Brahma", "Krishna", "Rama", "Hanuman", "Ganesha",
        "Kali", "Durga", "Lakshmi", "Saraswati", "Indra", "Agni", "Yama",
        "Sun Wukong", "Sisifus", "Theseus", "Perseus", "Hercules", "Akilles",
        "Odysseus", "Agamemnon", "Helen of Troy", "Paris", "Hector", "Priam",
        "Medusa", "Pandora", "Prometheus", "Atlas", "İcarus", "Daedalus",
        "Midas", "Orpheus", "Eurydice", "Echo", "Narcissus", "Pygmalion",
        "Asgardlı kahraman", "Anabis", "Cebrail", "Mikail", "İsrafil", "Azrail",

        # Pop Kültür Ekstra (Sonradan eklemeler)
        "Mr. Beast", "Logan Paul", "Jake Paul", "Charli D'Amelio",
        "Khaby Lame", "Bella Poarch", "Addison Rae", "James Charles",
        "Jeffree Star", "Ryan Higa", "Smosh", "Dude Perfect", "VanossGaming",
        "DanTDM", "Stampy", "Jelly", "Slogo", "Kwebbelkop", "Tubbo",
        "Ranboo", "Dream", "TommyInnit", "GeorgeNotFound", "Sapnap",
        "Ludwig", "Valkyrae", "Sykkuno", "Corpse Husband", "Disguised Toast",
        "Boxxy", "Nyan Cat", "Pepe the Frog", "Grumpy Cat", "Doge",
        "Cheems", "Drake meme", "Distracted Boyfriend", "Salt Bae", "Wojak",
        "Chad", "Virgin", "Karen", "Stonks", "Trade Offer",
    ],

    "tarihi_olaylar": [
        # Türk tarihi
        "İstanbul'un Fethi", "Kurtuluş Savaşı", "Çanakkale Savaşı", "Sakarya Meydan Muharebesi",
        "Büyük Taarruz", "Cumhuriyetin İlanı", "Harf Devrimi", "Şapka Kanunu",
        "Kadınlara Seçme ve Seçilme Hakkı", "Lozan Antlaşması", "Sevr Antlaşması",
        "Mondros Mütarekesi", "Anzavur Ayaklanması", "Şeyh Said İsyanı",
        "31 Mart Olayı", "II. Meşrutiyet İlanı", "I. Meşrutiyet İlanı",
        "Tanzimat Fermanı", "Islahat Fermanı", "Senedi İttifak", "Karlofça Antlaşması",
        "Pasarofça Antlaşması", "Küçük Kaynarca Antlaşması", "Yaş Antlaşması",
        "Manzikert Savaşı", "Malazgirt Zaferi", "Miryokefalon Savaşı",
        "I. Kosova Savaşı", "II. Kosova Savaşı", "Niğbolu Savaşı", "Varna Savaşı",
        "Mohaç Meydan Muharebesi", "Çaldıran Savaşı", "Ridaniye Savaşı",
        "Mercidabık Savaşı", "Otlukbeli Savaşı", "Ankara Savaşı",
        "İstanbul'un Kuşatması", "Viyana Kuşatması", "II. Viyana Kuşatması",
        "Belgrad'ın Fethi", "Rodos'un Fethi", "Kıbrıs'ın Fethi", "Girit'in Fethi",
        "İnebahtı Deniz Savaşı", "Preveze Deniz Zaferi", "Çeşme Baskını",
        "Sinop Baskını", "Plevne Savunması", "93 Harbi", "Trablusgarp Savaşı",
        "Balkan Savaşları", "I. Balkan Savaşı", "II. Balkan Savaşı",
        "Galiçya Cephesi", "Kafkas Cephesi", "Hicaz Cephesi", "Yemen Cephesi",
        "Sarıkamış Harekatı", "Kut'ül Amare Zaferi", "Kıbrıs Barış Harekatı",
        "1980 Askeri Darbesi", "12 Eylül Darbesi", "27 Mayıs İhtilali",
        "12 Mart Muhtırası", "28 Şubat Süreci", "15 Temmuz Darbe Girişimi",
        "Marmara Depremi", "1999 Gölcük Depremi", "Van Depremi", "Elazığ Depremi",
        "Maraş Depremi", "6 Şubat Depremleri", "Erzincan Depremi 1939",
        "Soma Faciası", "Çorlu Tren Kazası", "Ankara Garı Patlaması",
        "Türkiye'nin NATO'ya Girişi", "Türkiye'nin AB'ye Aday Olması",
        "Boğaziçi Köprüsü'nün Açılışı", "Fatih Sultan Mehmet Köprüsü Açılışı",
        "Yavuz Sultan Selim Köprüsü Açılışı", "Çanakkale 1915 Köprüsü Açılışı",
        "Marmaray'ın Açılışı", "Avrasya Tüneli", "İstanbul Havalimanı Açılışı",
        "Türksat 1B'nin Fırlatılması", "Türksat 5A", "İlk Yerli Otomobil TOGG",
        "Bayraktar TB2", "Akıncı İHA", "Kızılelma", "Anadol'un üretimi",
        "Tofaş'ın Açılışı", "Boğaziçi Üniversitesi Kuruluşu",

        # Dünya Tarihi - Antik
        "Piramitlerin İnşası", "Çin Seddi'nin İnşası", "Babil'in Yıkılışı",
        "Babil Asma Bahçeleri", "Truva Savaşı", "Maraton Savaşı", "Termopil Savaşı",
        "Salamis Deniz Savaşı", "Pers İmparatorluğu'nun Kuruluşu",
        "Büyük İskender'in Fetihleri", "Persepolis'in Yakılışı",
        "Roma'nın Kuruluşu", "Roma Cumhuriyeti'nin Kuruluşu",
        "Sezar'ın Suikastı", "Roma İmparatorluğu'nun Kuruluşu",
        "Vezüv Yanardağı'nın Patlaması", "Pompei'nin Yok Oluşu",
        "Roma'nın İkiye Bölünmesi", "Batı Roma'nın Yıkılışı", "Doğu Roma'nın Kuruluşu",
        "Hunların Avrupa'ya Akınları", "Kavimler Göçü", "Atilla'nın Roma'yı Kuşatması",
        "Yazının İcadı", "Tekerleğin İcadı", "Ateşin Bulunması", "Tarımın Başlaması",
        "Neolitik Devrim", "İlk Şehirlerin Kurulması", "Sümer Uygarlığı",
        "Hammurabi Kanunları", "Tarihin Babası Herodot", "Olimpiyatların Başlaması",

        # Orta Çağ
        "İslam'ın Doğuşu", "Hicret", "Bedir Savaşı", "Uhud Savaşı", "Hendek Savaşı",
        "Mekke'nin Fethi", "Veda Hutbesi", "Hz. Muhammed'in Vefatı",
        "Dört Halife Dönemi", "Emevi Devleti'nin Kuruluşu", "Abbasi Devleti'nin Kuruluşu",
        "Kerbela Olayı", "Talas Savaşı", "Endülüs'ün Fethi", "Endülüs'ün Yıkılışı",
        "Haçlı Seferleri", "I. Haçlı Seferi", "II. Haçlı Seferi", "III. Haçlı Seferi",
        "IV. Haçlı Seferi", "Hıttin Savaşı", "Kudüs'ün Fethi (Selahaddin)",
        "Magna Carta", "İngiltere'nin Normanlar Tarafından Fethi", "Hastings Savaşı",
        "Yüz Yıl Savaşları", "Çiçek Savaşları", "Joan of Arc", "Lutheran Reformasyonu",
        "Moğol İstilası", "Cengiz Han'ın Fetihleri", "Bağdat'ın Yıkılışı",
        "Timur'un Fetihleri", "Viking Çağı", "Vikinglerin İngiltere'ye Çıkışı",
        "Kara Veba", "Veba Salgını", "Kara Ölüm", "Rönesans", "Rönesans'ın Başlangıcı",
        "Reform Hareketi", "Martin Luther'in 95 Tezi", "Trent Konsili",
        "Hıristiyanlığın Bölünmesi", "Doğu-Batı Kilisesi Ayrılığı",
        "Endüljans Satışı", "Engizisyon Mahkemeleri", "Cadı Avı",

        # Yeni Çağ
        "Amerika'nın Keşfi", "Kolomb'un Yolculuğu", "Macellan'ın Dünya Turu",
        "Vasco da Gama'nın Hindistan Yolu", "Coğrafi Keşifler",
        "İnka İmparatorluğu'nun Yıkılışı", "Aztek İmparatorluğu'nun Yıkılışı",
        "Maya Uygarlığı'nın Çöküşü", "İlk Sömürgecilik Dönemi",
        "Otuz Yıl Savaşları", "Vestfalya Antlaşması", "Westfalya Barışı",
        "İngiliz İç Savaşı", "Cromwell'in İktidarı", "İngiltere'de Cumhuriyet İlanı",
        "Şanlı Devrim", "Amerikan Bağımsızlık Savaşı", "ABD'nin Kuruluşu",
        "Bağımsızlık Bildirgesi", "Boston Çay Partisi", "Yorktown Kuşatması",
        "Fransız İhtilali", "Bastille'in Düşüşü", "İnsan Hakları Bildirgesi",
        "Robespierre Dönemi", "Terör Dönemi", "Giyotin", "Napolyon'un İmparator Olması",
        "Napolyon Savaşları", "Trafalgar Deniz Savaşı", "Austerlitz Savaşı",
        "Borodino Savaşı", "Moskova Seferi", "Leipzig Savaşı", "Waterloo Savaşı",
        "Napolyon'un Sürgünü", "St. Helena'da Ölüm", "Viyana Kongresi",

        # Yakın Çağ
        "Sanayi Devrimi", "Buhar Makinesinin İcadı", "Demiryolunun İcadı",
        "İlk Lokomotif", "Elektriğin Keşfi", "Telgrafın İcadı", "Telefonun İcadı",
        "Ampulün İcadı", "Edison'un Ampulü", "İlk Otomobilin Yapımı",
        "Ford Model T'nin Üretimi", "İlk Uçak Uçuşu", "Wright Kardeşlerin Uçuşu",
        "Radyonun İcadı", "Televizyonun İcadı", "Bilgisayarın İcadı",
        "İnternetin İcadı", "World Wide Web", "Google'ın Kuruluşu",
        "Facebook'un Kuruluşu", "Twitter'ın Kuruluşu", "YouTube'un Kuruluşu",
        "iPhone'un Çıkışı", "ChatGPT'nin Çıkışı", "Yapay Zeka Devrimi",
        "Amerikan İç Savaşı", "Gettysburg Savaşı", "Lincoln Suikastı",
        "Köleliğin Kaldırılması", "Latin Amerika Bağımsızlık Hareketleri",
        "Bolivar'ın Mücadelesi", "İtalyan Birliği", "Alman Birliği",
        "Garibaldi'nin Seferleri", "Bismarck Dönemi", "Sedan Savaşı",
        "Fransa-Prusya Savaşı", "Krım Savaşı", "Boer Savaşları",
        "Çin-Japon Savaşı", "Rus-Japon Savaşı", "Mançurya'nın İşgali",

        # 20. Yüzyıl
        "1. Dünya Savaşı", "Saraybosna Suikastı", "Verdun Savaşı", "Somme Savaşı",
        "Marne Savaşı", "Galiçya Cephesi", "Çanakkale Cephesi", "Versailles Antlaşması",
        "Bolşevik Devrimi", "Ekim Devrimi", "Rus İç Savaşı", "Çarlık Rusyası'nın Yıkılışı",
        "SSCB'nin Kuruluşu", "Lenin'in Ölümü", "Stalin Dönemi", "Büyük Temizlik",
        "Holodomor", "Faşizmin Yükselişi", "Mussolini'nin İktidara Gelişi",
        "Hitler'in İktidara Gelişi", "Reichstag Yangını", "Nazi Almanyası",
        "Kristalnacht", "İspanya İç Savaşı", "Franco Dönemi",
        "2. Dünya Savaşı", "Polonya'nın İşgali", "Dunkirk Tahliyesi",
        "Britanya Savaşı", "Pearl Harbor Saldırısı", "Stalingrad Savaşı",
        "Kursk Savaşı", "El Alameyn Savaşı", "Normandiya Çıkarması", "D-Day",
        "Berlin'in Düşüşü", "Hitler'in İntiharı", "Hiroşima Bombalaması",
        "Nagasaki Bombalaması", "Japonya'nın Teslimi", "Holokost", "Auschwitz",
        "Yahudi Soykırımı", "Anne Frank", "Nüremberg Mahkemeleri",
        "BM'nin Kuruluşu", "NATO'nun Kuruluşu", "Varşova Paktı",
        "İsrail'in Kuruluşu", "Arap-İsrail Savaşı", "Süveyş Krizi",
        "Altı Gün Savaşı", "Yom Kippur Savaşı", "Camp David Antlaşması",
        "Filistin İntifadası", "Soğuk Savaş", "Berlin Hava Köprüsü",
        "Berlin Duvarı'nın Yapılışı", "Berlin Duvarı'nın Yıkılışı",
        "Küba Füze Krizi", "Domuzlar Körfezi Çıkarması", "Kennedy Suikastı",
        "Martin Luther King Suikastı", "Malcolm X Suikastı", "Lennon Suikastı",
        "Reagan Suikast Girişimi", "Papa Suikast Girişimi",
        "Mahatma Gandhi Suikastı", "İndira Gandhi Suikastı", "Rajiv Gandhi Suikastı",
        "Saddam'ın Asılması", "Bin Ladin'in Öldürülmesi", "Kaddafi'nin Öldürülmesi",
        "Kore Savaşı", "Vietnam Savaşı", "Tet Saldırısı", "Saygon'un Düşüşü",
        "Kamboçya Soykırımı", "Kızıl Kmerler", "Pol Pot Dönemi",
        "Çin Komünist Devrimi", "Mao'nun İktidara Gelişi", "Büyük İleri Atılım",
        "Kültür Devrimi", "Tienanmen Olayları", "Hong Kong'un Çin'e Devri",
        "Macar İhtilali 1956", "Prag Baharı 1968", "Solidarność",
        "Aya İniş", "Apollo 11", "Neil Armstrong'un Aya Ayak Basışı",
        "Sputnik'in Fırlatılması", "Gagarin'in Uzaya Çıkışı", "Uzay Yarışı",
        "Hubble Teleskobunun Fırlatılması", "Voyager Görevleri", "Mars'a İniş",
        "Uluslararası Uzay İstasyonu", "James Webb Teleskobu",
        "Sovyetlerin Dağılması", "Glasnost", "Perestroyka", "Gorbaçov Dönemi",
        "Yugoslavya'nın Dağılması", "Bosna Savaşı", "Srebrenitsa Katliamı",
        "Kosova Savaşı", "Kosova'nın Bağımsızlığı", "NATO'nun Sırbistan'ı Bombalaması",
        "Sırbistan-Karadağ'ın Ayrılması", "Çekoslovakya'nın Bölünmesi",
        "Apartheid Sonu", "Mandela'nın Serbest Bırakılması",
        "Ruanda Soykırımı", "Darfur Soykırımı", "Somali İç Savaşı",
        "İran İslam Devrimi", "İran-Irak Savaşı", "Körfez Savaşı I",
        "Körfez Savaşı II", "Irak'ın İşgali", "Afganistan'ın İşgali",
        "Sovyetlerin Afganistan İşgali", "Taliban'ın İktidara Gelişi",
        "Taliban'ın Yeniden İktidara Gelişi", "11 Eylül Saldırıları",
        "9/11 Saldırıları", "İkiz Kuleler", "Pentagon Saldırısı",
        "El-Kaide'nin Doğuşu", "IŞİD'in Kuruluşu", "Suriye İç Savaşı",
        "Arap Baharı", "Tunus Devrimi", "Mısır Devrimi", "Libya İç Savaşı",
        "Yemen İç Savaşı", "Filistin-İsrail Çatışması", "Gazze Savaşı",
        "Hamas-İsrail Savaşı", "Hizbullah-İsrail Çatışması",
        "Rusya'nın Kırım'ı İlhakı", "Ukrayna Savaşı", "Rusya-Ukrayna Savaşı",
        "Kerç Köprüsü Saldırısı", "Bahmut Kuşatması",

        # Doğal afetler / Faciaları
        "Titanik'in Batışı", "Hindenburg Faciası", "Çernobil Faciası",
        "Fukuşima Nükleer Felaketi", "Three Mile Island Kazası",
        "Bhopal Felaketi", "Exxon Valdez Petrol Sızıntısı",
        "Deepwater Horizon Felaketi", "Kasırga Katrina", "Kasırga Sandy",
        "Hint Okyanusu Tsunamisi 2004", "Japonya Tsunamisi 2011",
        "Haiti Depremi 2010", "Nepal Depremi 2015", "Tohoku Depremi",
        "San Francisco Depremi 1906", "Mexico City Depremi 1985",
        "Krakatoa Yanardağ Patlaması", "Tambora Patlaması", "Mt. St. Helens",
        "Aktivite Eyjafjallajökull", "Vezüv Patlaması",
        "İspanyol Gribi 1918", "Asya Gribi", "Hong Kong Gribi",
        "SARS Salgını", "MERS Salgını", "Ebola Salgını", "Domuz Gribi",
        "Covid-19 Pandemisi", "Dünya Çapında Karantina", "Wuhan Salgını",
        "AIDS Salgını", "Veba Salgını 14. Yüzyıl", "Kolera Salgınları",
        "Hindenburg Faciası", "Concorde Kazası", "Lockerbie Faciası",
        "MH370 Kayıp Uçak", "MH17 Faciası", "Germanwings 9525",
        "Columbia Uzay Mekiği Faciası", "Challenger Uzay Mekiği Faciası",
        "Apollo 1 Yangını", "Soyuz 11 Faciası",
        "Estonia Feribot Faciası", "Costa Concordia Faciası",
        "Lusitania'nın Batışı", "Bismarck'ın Batışı",

        # İcatlar / Keşifler
        "Matbaanın İcadı", "Gutenberg'in Matbaası", "Pusulanın İcadı",
        "Barutun İcadı", "Mikroskopun İcadı", "Teleskopun İcadı",
        "Aşı'nın Bulunması", "Penisilinin Keşfi", "DNA'nın Keşfi",
        "İnsan Genomu Projesi", "İlk Kalp Nakli", "İlk Tüp Bebek",
        "İlk Klonlama Dolly", "Atomun Parçalanması", "Çekirdek Tepkimesi",
        "Manhattan Projesi", "İlk Atom Bombası", "Termonükleer Bomba",
        "Radyasyon Keşfi", "X-Işınlarının Keşfi", "Görelilik Teorisi",
        "Kuantum Mekaniği", "Higgs Bozonu Keşfi", "CERN", "Kara Delik Fotoğrafı",
        "Yer Çekiminin Keşfi", "Newton'un Elması", "Evrim Teorisi",
        "Beagle Yolculuğu", "Dinozor Fosillerinin Keşfi", "Lucy Fosili",
        "Buz Adam Ötzi", "Pompeii Kazıları", "Truva'nın Keşfi",
        "Tutankamon'un Mezarının Bulunması", "Rosetta Taşı",
        "Hiyerogliflerin Çözülmesi", "Machu Picchu'nun Keşfi",
        "Antikythera Mekanizması", "Yedi Harikası", "Ölü Deniz Yazmaları",

        # Dini olaylar
        "İsa'nın Doğumu", "İsa'nın Çarmıha Gerilmesi", "Musa'nın Kızıldeniz'i Yarması",
        "On Emir'in İndirilmesi", "Nuh Tufanı", "İbrahim'in Sınanması",
        "Adem ile Havva", "Cennet'ten Kovulma", "Yusuf'un Mısır'a Götürülmesi",
        "Süleyman Tapınağı'nın Yapımı", "Tapınağın Yıkılışı", "Babil Sürgünü",
        "Buda'nın Aydınlanması", "Mevlana'nın Doğuşu", "İlk Cami İnşası",
        "Kabe'nin İnşası", "İbrahim'in Kabe'yi İnşa Etmesi",
        "Hac Farzının İnişi", "Kuran'ın İndirilmesi", "İlk Vahiy",

        # Diğer
        "Olimpiyatların Modern Çağda Başlaması", "FIFA Dünya Kupası'nın Başlaması",
        "İlk Eurovision", "İlk Nobel Ödülleri", "İlk Oscar Töreni",
        "İlk Cannes Film Festivali", "MTV'nin Kuruluşu", "Beatles'ın Dağılması",
        "Elvis'in Ölümü", "Michael Jackson'ın Ölümü", "Prenses Diana'nın Ölümü",
        "Kraliçe Elizabeth'in Ölümü", "Papa Jean Paul'un Ölümü",
        "Saddam'ın Yakalanması", "Bin Ladin'in Öldürülmesi",
        "ChatGPT'nin Yayınlanması", "Bitcoin'in İcadı", "Kripto Para Çağı",
        "Brexit", "Trump'ın Seçilmesi", "Trump'ın Suikast Girişimi",
        "ABD Kongre Baskını 6 Ocak", "Charlie Hebdo Saldırısı", "Bataclan Saldırısı",
        "Boston Maraton Bombalaması", "Oklahoma City Bombalaması",
        "Columbine Katliamı", "Sandy Hook Katliamı", "Las Vegas Saldırısı",
        "Yeni Zelanda Cami Saldırısı", "Norveç Utoya Adası Saldırısı",
        "Madrid Tren Saldırısı", "Londra Saldırıları 7/7",
    ],

    "hayvanlar": [
        # ═══════════════ MEMELİLER ═══════════════
        # Kediler (büyük ve küçük)
        "Aslan", "Kaplan", "Leopar", "Jaguar", "Çita", "Puma", "Vaşak",
        "Karakulak", "Kar Leoparı", "Siyah Panter", "Kedi",

        # Köpekgiller ve yakınları
        "Köpek", "Kurt", "Çakal", "Tilki", "Fenek", "Sırtlan", "Dingo",
        "Kangal", "Husky", "Bulldog", "Chihuahua", "Dalmaçyalı",

        # Atgiller
        "At", "Eşek", "Katır", "Zebra", "Midilli",

        # Çiftlik hayvanları
        "İnek", "Boğa", "Manda", "Koyun", "Keçi", "Domuz", "Yaban Domuzu",
        "Tavuk", "Horoz", "Hindi", "Ördek", "Kaz",
        "Yak", "Lama", "Alpaka", "Deve",

        # Büyük vahşi memeli
        "Fil", "Mamut", "Zürafa", "Okapi", "Gergedan", "Su Aygırı",
        "Bizon", "Geyik", "Karaca", "Ren Geyiği", "Sığın",
        "Ceylan", "Antilop", "Impala", "Gnu",

        # Primatlar
        "Goril", "Şempanze", "Orangutan", "Gibon", "Bonobo", "Babun",
        "Makak", "Kapuçin Maymunu", "Marmoset", "Tarsier", "Lemur", "Aye-Aye",

        # Avustralya / kese hayvanları
        "Kanguru", "Koala", "Wallaby", "Tasmanya Şeytanı", "Wombat",
        "Opossum", "Ornitorenk", "Echidna",

        # Kemirgenler ve küçük memeliler
        "Tavşan", "Sincap", "Uçan Sincap", "Marmot", "Çinçilla",
        "Kunduz", "Su Samuru", "Sansar", "Gelincik", "Porsuk",
        "Kokarca", "Rakun", "Tanuki", "Firavun Faresi",
        "Fare", "Sıçan", "Hamster", "Kobay", "Köstebek",
        "Karıncayiyen", "Pangolin", "Tembel Hayvan", "Kirpi",
        "Yarasa", "Vampir Yarasası",

        # Ayılar
        "Boz Ayı", "Kutup Ayısı", "Panda", "Kızıl Panda", "Güneş Ayısı",

        # ═══════════════ DENİZ CANLILARI ═══════════════
        # Memeliler ve büyük balıklar
        "Yunus", "Mavi Balina", "Orka", "Sperm Balinası", "Beluga",
        "Mors", "Fok", "Deniz Aslanı", "Manati",
        "Beyaz Köpekbalığı", "Çekiç Balığı", "Kaplan Köpekbalığı",
        "Megalodon", "Vatoz", "Manta", "Pirana",
        "Som Balığı", "Levrek", "Çipura", "Hamsi", "Sardalya",
        "Lüfer", "Palamut", "Orkinos", "Uskumru", "Kefal",
        "Mersin Balığı", "Yılan Balığı", "Kalkan", "Dil Balığı",
        "Japon Balığı", "Beta Balığı", "Lepistes", "Kılıçbalığı",
        "Kirpi Balığı", "Çıraklık Balığı", "Anglerfish", "Barakuda",

        # Yumuşakçalar ve kabuklular
        "Ahtapot", "Mavi Halkalı Ahtapot", "Nautilus", "Kalamar", "Dev Kalamar",
        "Mürekkep Balığı", "Denizatı", "Denizyıldızı", "Deniz Hıyarı",
        "Deniz Kestanesi", "Mercan", "Deniz Şakayığı", "Denizanası",
        "Yengeç", "Karides", "Istakoz", "Kerevit", "Mantis Karidesi",
        "Salyangoz", "Midye", "İstiridye",
        "Penguen",

        # ═══════════════ KUŞLAR ═══════════════
        "Serçe", "Güvercin", "Karga", "Saka", "Bülbül", "Kırlangıç",
        "Ağaçkakan", "Sığırcık", "İbibik",
        "Papağan", "Muhabbet Kuşu", "Kakadu", "Ara Papağanı",
        "Kanarya", "İskete",
        "Kartal", "Şahin", "Atmaca", "Doğan", "Akbaba",
        "Baykuş", "Puhu",
        "Karabatak", "Pelikan", "Flamingo", "Leylek", "Turna",
        "Albatros", "Martı", "Saksağan", "Alakarga",
        "Sülün", "Keklik", "Tavus Kuşu",
        "Yaban Ördeği", "Karatavuk", "Çulluk",
        "Devekuşu", "Emu", "Kazuar", "Kivi",
        "Tukan", "Sinek Kuşu", "Cennet Kuşu",

        # ═══════════════ SÜRÜNGENLER ve AMFİBİLER ═══════════════
        "Yılan", "Kobra", "Çıngıraklı Yılan", "Kara Mamba",
        "Anakonda", "Boa", "Piton", "Engerek",
        "Timsah", "Aligatör", "Kayman",
        "Kaplumbağa", "Caretta Caretta", "Galapagos Kaplumbağası",
        "Kertenkele", "Geko", "Bukalemun", "İguana", "Komodo Ejderi",
        "Kurbağa", "Karakurbağası", "Semender", "Aksolotl",

        # ═══════════════ BÖCEKLER VE ÖRÜMCEKLER ═══════════════
        "Karınca", "Bal Arısı", "Eşek Arısı", "Yaban Arısı",
        "Sinek", "Sivrisinek", "Meyve Sineği",
        "Çekirge", "Cırcır Böceği", "Ağustos Böceği", "Peygamber Devesi",
        "Ateş Böceği", "Hamamböceği", "Termit",
        "Kelebek", "Monark Kelebeği", "Güve", "Tırtıl",
        "Akrep", "Örümcek", "Tarantula", "Karadul",
        "Uğur Böceği", "Gergedan Böceği", "Bok Böceği",
        "Bit", "Pire", "Kene", "Sülük", "Solucan",

        # ═══════════════ KURGUSAL / MİTOLOJİK YARATIKLAR ═══════════════
        "Unicorn", "Pegasus", "Ejderha", "Hydra", "Griffin",
        "Phoenix", "Simurg", "Kraken", "Leviathan", "Behemoth",
        "Minotor", "Centaur", "Satyr", "Medusa", "Siren",
        "Deniz Kızı", "Triton", "Naga",
        "Goblin", "Trol", "Cüce", "Orc", "Elf", "Hobbit", "Peri",
        "Kurt Adam", "Vampir", "Zombi", "Hayalet", "Cadı",
        "Yeti", "Bigfoot", "Loch Ness Canavarı", "Chupacabra",
        "Banshee", "Wendigo", "Manticore", "Basilisk",
        "Wyvern", "Cerberus", "Sfenks", "Chimera",
        "Leprechaun", "Golem",
        "King Kong", "Godzilla", "Mothra", "Ghidorah",
        "Cthulhu", "Mind Flayer", "Beholder", "Owlbear",
        "Fenrir", "Sleipnir", "Jormungandr",
        "Hippogriff", "Thestral", "Buckbeak", "Nagini", "Hedwig",
        "Smaug", "Drogon", "Balerion", "Vhagar",
        "Ghost (Direwolf)", "Nymeria",
        "Pikachu", "Charizard", "Bulbasaur", "Squirtle", "Mewtwo",
        "Eevee", "Snorlax", "Gengar", "Lucario", "Magikarp", "Gyarados",
        "Garfield", "Snoopy", "Tom", "Jerry", "Tweety", "Bugs Bunny",
        "Pluto", "Goofy", "Donald Duck", "Mickey Mouse",
        "Çizmeli Kedi", "Süngerbob", "Patrick Star", "Gary",
        "Nemo", "Dory", "Bambi", "Dumbo", "Hachiko", "Scooby-Doo",
        "Brian Griffin", "Dişsiz", "Stitch", "Maximus",

        # ═══════════════ DİNOZORLAR ve PREHİSTORİK HAYVANLAR ═══════════════
        "T-Rex", "Velociraptor", "Stegosaurus", "Triceratops",
        "Brachiosaurus", "Brontosaurus", "Diplodocus", "Ankylosaurus",
        "Pterodactyl", "Spinosaurus", "Allosaurus", "Carnotaurus",
        "Giganotosaurus", "Parasaurolophus", "Pachycephalosaurus",
        "Dilophosaurus", "Mosasaurus", "Plesiosaurus", "Liopleurodon",
        "Kılıç Dişli Kaplan", "Megatherium",
        "Argentinosaurus", "Quetzalcoatlus",
        "Archaeopteryx", "Dimetrodon", "Trilobit", "Anomalocaris",
        "Dodo", "Tasmanya Kaplanı", "Yolcu Güvercini",
        "Quagga", "Steller Deniz İneği",
    ],

    "yemekler": [
        # Türk yemekleri — ana yemekler
        "Lahmacun", "Pide", "Karadeniz Pidesi", "Kıymalı Pide", "Kuşbaşılı Pide", "Kaşarlı Pide",
        "Mantı", "Kayseri Mantısı", "Çiğ Köfte", "İçli Köfte", "Kısır", "Mercimek Köftesi",
        "Döner", "Tavuk Döner", "Et Döner", "İskender Kebap", "Adana Kebap", "Urfa Kebap",
        "Şiş Kebap", "Beyti Kebap", "Patlıcan Kebap", "Tas Kebabı", "Kuzu Tandır", "Kuzu Çevirme",
        "Köfte", "Sulu Köfte", "İzmir Köfte", "Tekirdağ Köfte", "Akçaabat Köftesi", "İnegöl Köfte",
        "Karnıyarık", "Musakka", "İmam Bayıldı", "Etli Biber Dolması", "Yaprak Sarma", "Lahana Sarması",
        "Mercimek Çorbası", "Tarhana Çorbası", "Yayla Çorbası", "Düğün Çorbası", "Ezogelin Çorbası",
        "İşkembe Çorbası", "Domates Çorbası", "Tavuk Çorbası", "Şehriye Çorbası",
        "Menemen", "Sucuklu Yumurta", "Çılbır", "Kahvaltı Tabağı", "Simit", "Açma", "Poğaça",
        "Su Böreği", "Sigara Böreği", "Talaş Böreği", "Çiğ Börek", "Patatesli Börek", "Ispanaklı Börek",
        "Künefe", "Baklava", "Kadayıf", "Şekerpare", "Revani", "Tulumba Tatlısı", "Lokma",
        "Kazandibi", "Sütlaç", "Aşure", "Helva", "Tahin Helvası", "Pişmaniye", "Cevizli Sucuk",
        "Pestil", "Lokum", "Maraş Dondurması", "Kemalpaşa Tatlısı",
        "Hamsi Tava", "Levrek Buğulama", "Çupra Izgara", "Palamut Buğulama", "Hamsili Pilav",
        "Mıhlama", "Muhlama", "Karadeniz Hamsisi",
        "Pilav", "Bulgur Pilavı", "İç Pilav", "Şehriyeli Pilav", "Erişte",
        "Hünkar Beğendi", "Etli Ekmek", "Kuru Fasulye", "Nohut Yemeği", "Pilaki", "Türlü",
        "Patlıcan Musakka", "Etli Patlıcan", "Etli Bamya", "Etli Kabak",
        "Ayran", "Şalgam Suyu", "Boza", "Salep", "Türk Kahvesi", "Türk Çayı",

        # Dünya mutfağı
        "Pizza", "Margherita Pizza", "Pepperoni Pizza", "Hawai Pizzası", "Lazanya", "Spagetti",
        "Carbonara", "Bolognese", "Risotto", "Ravioli", "Bruschetta", "Tiramisu", "Gelato", "Cannoli",
        "Sushi", "Sashimi", "Maki", "Ramen", "Udon", "Tempura", "Yakitori", "Onigiri",
        "Miso Çorbası", "Mochi",
        "Pad Thai", "Tom Yum", "Pho", "Bibimbap", "Kimchi", "Bulgogi", "Dim Sum", "Spring Roll",
        "Hamburger", "Cheeseburger", "Hot Dog", "Sandviç", "Cheesecake", "Pancake", "Waffle",
        "Donut", "Brownie", "Muffin", "Cupcake", "Sufle",
        "Taco", "Burrito", "Nachos", "Quesadilla", "Guacamole", "Fajitas", "Enchilada", "Salsa",
        "Croissant", "Baguette", "Macaron", "Crème Brûlée", "Fondü", "Ratatouille", "Quiche",
        "Falafel", "Humus", "Tabule", "Şawarma", "Pita",
        "Paella", "Tapas", "Gazpacho", "Churros", "Tortilla",
        "Schnitzel", "Bratwurst", "Pretzel", "Strudel",
        "Curry", "Tandoori Tavuk", "Biryani", "Naan", "Samosa", "Tikka Masala", "Butter Chicken",
        "Borç Çorbası", "Stroganoff",
        "Patates Kızartması", "Patates Püresi", "Patates Salatası", "Fish and Chips",
        "Omlet", "Sahanda Yumurta", "Haşlanmış Yumurta", "Yumurta Salatası",
        "Salata", "Sezar Salata", "Çoban Salata", "Akdeniz Salatası",
        "Kruvasan", "Tost", "Karışık Tost", "Kumru",

        # İçecekler
        "Kola", "Pepsi", "Fanta", "Sprite", "Limonata", "Portakal Suyu", "Vişne Suyu", "Süt",
        "Smoothie", "Milkshake", "Latte", "Cappuccino", "Espresso", "Mocha", "Frappe",
        "Sıcak Çikolata", "Soğuk Kahve",
        "Şarap", "Bira", "Şampanya", "Votka", "Viski", "Cin", "Tekila", "Rakı",

        # Atıştırmalık & şekerleme
        "Çikolata", "Çikolatalı Gofret", "Sütlü Çikolata", "Bitter Çikolata", "Beyaz Çikolata",
        "Patates Cipsi", "Patlamış Mısır", "Kuruyemiş", "Fıstık", "Badem", "Ceviz", "Fındık",
        "Ayçekirdeği", "Antep Fıstığı", "Kestane Kebabı", "Kuru Yemiş Karışımı",
        "Dondurma", "Marshmallow", "Sakız", "Lolipop", "Karamel", "Reçel", "Bal", "Pekmez",
        "Yoğurt", "Cacık", "Tzatziki", "Peynir Tabağı", "Beyaz Peynir", "Kaşar", "Tulum Peyniri",
        "Mozzarella", "Parmesan", "Cheddar", "Feta",
    ],

    "filmler": [
        # Hollywood — gişe & kült (yaygın bilindik)
        "Titanik", "Avatar", "Avatar 2: Suyun Yolu", "Avengers", "Avengers: Yenilmezler",
        "Avengers: Sonsuzluk Savaşı", "Avengers: Endgame", "Iron Man", "Captain America",
        "Thor", "Hulk", "Spider-Man", "Black Panther", "Doctor Strange", "Black Widow",
        "Aquaman", "Wonder Woman", "Justice League", "Man of Steel", "Shazam",
        "Batman", "The Dark Knight", "Kara Şövalye", "Joker", "Suicide Squad",
        "Star Wars", "Yıldız Savaşları", "Star Wars: Yeni Bir Umut", "İmparator'un Geri Dönüşü",
        "Harry Potter ve Felsefe Taşı", "Harry Potter ve Sırlar Odası", "Harry Potter ve Azkaban Tutsağı",
        "Harry Potter ve Ateş Kadehi", "Harry Potter ve Zümrüdüanka Yoldaşlığı",
        "Harry Potter ve Melez Prens", "Harry Potter ve Ölüm Yadigarları",
        "Yüzüklerin Efendisi: Yüzük Kardeşliği", "Yüzüklerin Efendisi: İki Kule",
        "Yüzüklerin Efendisi: Kralın Dönüşü", "Hobbit",
        "Inception (Başlangıç)", "Interstellar (Yıldızlararası)", "Tenet", "Memento",
        "The Prestige", "Dunkirk", "Oppenheimer",
        "The Matrix", "Matrix Reloaded", "Matrix Revolutions",
        "Forrest Gump", "Esaretin Bedeli", "Pulp Fiction", "Reservoir Dogs", "Kill Bill",
        "Django Zincirsiz", "Soysuzlar Çetesi", "Bir Zamanlar Hollywood'da",
        "Baba", "Baba 2", "Sıkı Dostlar", "Yara İzi", "Casino", "Irlandalı",
        "Jurassic Park", "Jurassic World", "Indiana Jones", "E.T.", "Schindler'in Listesi",
        "Er Ryan'ı Kurtarmak",
        "Dövüş Kulübü", "Yedi", "Sosyal Ağ", "Kayıp Kız", "Zodiac",
        "Gladyatör", "Cesur Yürek", "300 Spartalı", "Truva",
        "Rocky", "Rambo", "Terminator", "Yokedici", "Predator", "Yırtıcı", "Alien", "Yaratık",
        "Zor Ölüm", "Görevimiz Tehlike", "John Wick", "James Bond", "Casino Royale", "Skyfall",
        "Ölmek İçin Yaşamak", "Hızlı ve Öfkeli",
        "Karayip Korsanları", "Karayip Korsanları: Siyah İnci'nin Laneti",
        "Oyuncak Hikayesi", "Kayıp Balık Nemo", "Yukarı Bak", "Aslan Kral",
        "Karlar Ülkesi", "Karlar Ülkesi 2",
        "Şrek", "Madagaskar", "Buz Devri", "Kung Fu Panda", "Ratatuy", "Wall-E",
        "Coco", "Encanto", "Moana", "Ters Yüz",
        "Çılgın Hırsız", "Minyonlar", "Sing",
        "Hayalet Avcıları",
        "Wall Street Kurdu", "Sıkı Yakaladım Seni", "Zindan Adası",
        "Siyah Kuğu", "Defter", "Pretty Woman",
        "Açlık Oyunları", "Alacakaranlık", "Maze Runner",
        "Joy Köpeğim Eve Dön Hachi", "Joker (2019)",
        "Top Gun", "Top Gun: Maverick",
        "La La Land", "Whiplash", "Bohemian Rhapsody",
        "Parazit (Parasite)",
        "Cast Away (Yaşam Mücadelesi)",
        "Aşk-ı Memnu", "Yedinci Koğuştaki Mucize",
        "Saw", "Testere", "Conjuring", "Korku Seansı", "It (O)", "Annabelle",
        "Sevgili Lara", "Yüzüklerin Efendisi",
        "Ev Yalnız", "Evde Tek Başına",
        "Polis Akademisi",
        "Geri Dönüş Yok", "Geleceğe Dönüş",

        # Türk gişe filmleri (bilindik)
        "GORA", "AROG", "ARIF V 216", "Cem Yılmaz'ın CMYLMZ",
        "Recep İvedik", "Recep İvedik 2", "Recep İvedik 3", "Recep İvedik 4",
        "Recep İvedik 5", "Recep İvedik 6", "Recep İvedik 7",
        "Vizontele", "Vizontele Tuuba",
        "Babam ve Oğlum", "Eşkıya", "Hababam Sınıfı", "Hababam Sınıfı Sınıfta Kaldı",
        "Süt Kardeşler", "Salako", "Şaban", "Korkusuz Korkak",
        "Pek Yakında", "Kelebeğin Rüyası", "Issız Adam",
        "Düğün Dernek", "Düğün Dernek 2", "Patron Mutlu Son İstiyor",
        "Cep Herkülü", "Av Mevsimi",
        "Kara Murat", "Tarkan", "Cesur Tarkan",
        "Müslüm",
    ],

    "markalar": [
        # Tech / sosyal medya
        "Apple", "Google", "Microsoft", "Amazon", "Facebook", "Meta", "Instagram",
        "WhatsApp", "TikTok", "Twitter", "X (Twitter)", "YouTube", "Netflix", "Spotify",
        "Snapchat", "Telegram", "Discord", "Zoom", "Skype", "LinkedIn", "Pinterest",
        "Reddit", "Twitch", "Steam", "Epic Games",

        # Yiyecek-içecek
        "Coca-Cola", "Pepsi", "Fanta", "Sprite", "7UP", "Red Bull", "Nestlé", "Lipton",
        "Nescafé", "Starbucks", "McDonald's", "Burger King", "KFC", "Pizza Hut",
        "Domino's Pizza", "Subway", "Popeyes", "Taco Bell", "Wendy's",
        "Snickers", "Mars", "Twix", "Bounty", "Kit Kat", "Toblerone", "Ferrero Rocher",
        "Milka", "Nutella", "Oreo", "Pringles", "Lay's", "Doritos", "Cheetos",

        # Spor giyim & ayakkabı
        "Nike", "Adidas", "Puma", "Reebok", "Under Armour", "New Balance", "Converse",
        "Vans", "Asics",

        # Moda lüks
        "Lacoste", "Gucci", "Louis Vuitton", "Chanel", "Versace", "Prada", "Dior",
        "Armani", "Hugo Boss", "Calvin Klein", "Tommy Hilfiger", "Ralph Lauren",
        "Burberry", "Rolex", "Omega", "Cartier",

        # Hızlı moda
        "Zara", "H&M", "Mango", "Uniqlo", "Bershka", "Pull&Bear", "Stradivarius",
        "GAP", "Levi's",

        # Otomotiv
        "BMW", "Mercedes-Benz", "Audi", "Volkswagen", "Porsche", "Ferrari", "Lamborghini",
        "Bugatti", "Bentley", "Rolls-Royce", "Maserati",
        "Toyota", "Honda", "Nissan", "Mazda", "Mitsubishi", "Hyundai", "Kia",
        "Ford", "Chevrolet", "Tesla", "Cadillac", "Jeep", "Dodge",
        "Renault", "Peugeot", "Citroën", "Fiat", "Alfa Romeo",
        "Volvo", "Skoda", "Seat", "Opel",

        # Elektronik / beyaz eşya
        "Samsung", "LG", "Sony", "Panasonic", "Toshiba", "Philips", "Bosch", "Siemens",
        "Whirlpool", "Arçelik", "Beko", "Vestel",
        "Huawei", "Xiaomi", "OnePlus", "Oppo",
        "Intel", "AMD", "Nvidia", "IBM",
        "HP", "Dell", "Lenovo", "Asus", "Acer", "MSI", "Razer", "Logitech",
        "Canon", "Nikon", "GoPro",

        # Yazılım & dijital
        "Adobe", "Photoshop", "Windows", "Android", "iOS", "macOS", "Linux",
        "Chrome", "Firefox", "Safari", "Edge",

        # Finans / ödeme
        "PayPal", "Visa", "Mastercard", "American Express",
        "Yapı Kredi", "Ziraat Bankası", "İş Bankası", "Garanti BBVA", "Akbank",
        "Halkbank", "Vakıfbank", "Denizbank", "QNB Finansbank", "ING",

        # Eğlence / medya
        "Disney", "Pixar", "Warner Bros", "Universal", "Paramount", "Marvel", "DC",
        "HBO", "Amazon Prime", "Disney+",
        "Nintendo", "PlayStation", "Xbox", "Sega",

        # Perakende & e-ticaret
        "IKEA", "Walmart", "Carrefour", "Migros", "BİM", "A101", "Şok Market",
        "MediaMarkt", "Teknosa", "Vatan Bilgisayar",
        "Hepsiburada", "Trendyol", "n11", "Amazon Türkiye", "GittiGidiyor",

        # Oyuncak & ev
        "Lego", "Mattel", "Hasbro", "Barbie", "Hot Wheels", "Playmobil",

        # Kişisel bakım
        "Gillette", "Colgate", "Pantene", "Head & Shoulders", "Nivea", "Dove",
        "Old Spice", "Axe", "Garnier", "L'Oréal", "Maybelline",

        # Türk markaları
        "Mavi Jeans", "DeFacto", "LC Waikiki", "Koton", "Polo Garage",
        "Turkcell", "Vodafone", "Türk Telekom", "Türksat",
        "THY", "Pegasus", "AnadoluJet",
        "TOGG", "Otokar", "TEMSA",
        "Eti", "Ülker", "Torku", "Pınar", "Sütaş", "İçim",
        "Çaykur", "Doğadan", "Doğuş Çay",
        "Erikli", "Damla Su", "Hayat Su",
        "Komagene", "HD İskender",
    ],

    "sehirler": [
        # Türkiye — 81 il + büyük ilçeler
        "İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Adana", "Konya", "Gaziantep",
        "Mersin", "Kayseri", "Eskişehir", "Diyarbakır", "Şanlıurfa", "Trabzon", "Samsun",
        "Erzurum", "Van", "Malatya", "Kahramanmaraş", "Denizli", "Sakarya", "Aydın",
        "Tekirdağ", "Muğla", "Hatay", "Manisa", "Balıkesir", "Çanakkale", "Mardin",
        "Ordu", "Rize", "Sivas", "Tokat", "Edirne", "Kırıkkale", "Karabük", "Zonguldak",
        "Kütahya", "Afyonkarahisar", "Isparta", "Burdur", "Yalova", "Düzce", "Kilis",
        "Karaman", "Bartın", "Iğdır", "Ardahan", "Şırnak", "Bayburt", "Tunceli", "Kars",
        "Erzincan", "Bitlis", "Bingöl", "Muş", "Siirt", "Hakkari", "Ağrı", "Adıyaman",
        "Niğde", "Nevşehir", "Aksaray", "Yozgat", "Çorum", "Çankırı", "Bolu", "Sinop",
        "Amasya", "Kastamonu", "Kırşehir", "Kırklareli", "Bilecik", "Uşak", "Osmaniye",
        "Artvin", "Giresun", "Gümüşhane", "Elazığ", "Batman",
        # Önemli ilçeler
        "Bodrum", "Marmaris", "Fethiye", "Alanya", "Kemer", "Kuşadası", "Çeşme",
        "Şile", "Sapanca", "Abant", "Uludağ", "Kapadokya", "Pamukkale", "Mardin",

        # Avrupa başkentleri & büyük şehirler
        "Londra", "Paris", "Berlin", "Roma", "Madrid", "Lizbon", "Amsterdam", "Brüksel",
        "Viyana", "Atina", "Dublin", "Stockholm", "Oslo", "Helsinki", "Kopenhag",
        "Varşova", "Prag", "Budapeşte", "Bükreş", "Sofya", "Belgrad", "Saraybosna",
        "Üsküp", "Zagreb", "Ljubljana", "Tiran", "Reykjavik", "Riga", "Vilnius", "Tallinn",
        "Bratislava", "Lefkoşa", "Valletta",
        "Manchester", "Liverpool", "Birmingham", "Edinburgh", "Glasgow", "Oxford", "Cambridge",
        "Marsilya", "Lyon", "Nice", "Cannes", "Strasbourg", "Bordeaux",
        "Münih", "Hamburg", "Frankfurt", "Köln", "Stuttgart", "Düsseldorf",
        "Milano", "Venedik", "Napoli", "Floransa", "Torino", "Bologna", "Pisa",
        "Barselona", "Sevilla", "Valencia", "Bilbao", "Granada",
        "Rotterdam", "Lahey",
        "Zürih", "Cenevre", "Bern",
        "Salzburg", "Innsbruck",
        "Selanik", "Santorini", "Mykonos", "Girit",
        "Moskova", "St. Petersburg", "Soçi",
        "Kiev", "Lviv", "Odessa",
        "Porto", "Krakow",

        # ABD & Kanada
        "New York", "Los Angeles", "Chicago", "Houston", "Miami", "Las Vegas",
        "San Francisco", "Boston", "Washington", "Seattle", "Dallas", "Philadelphia",
        "Atlanta", "Detroit", "Phoenix", "San Diego", "Orlando", "New Orleans",
        "Toronto", "Montreal", "Vancouver", "Ottawa", "Calgary",

        # Asya
        "Tokyo", "Osaka", "Kyoto", "Yokohama", "Hiroşima", "Sapporo",
        "Seul", "Busan",
        "Pekin", "Şangay", "Hong Kong", "Guangzhou", "Şenzhen",
        "Taipei", "Singapur",
        "Bangkok", "Pattaya", "Phuket",
        "Hanoi", "Ho Chi Minh",
        "Manila", "Jakarta", "Bali", "Kuala Lumpur",
        "Yeni Delhi", "Bombay", "Bangalore", "Kalküta",
        "Karaçi", "İslamabad", "Lahor",
        "Kabil", "Tahran", "Tebriz", "İsfahan", "Şiraz",
        "Bağdat", "Basra", "Erbil",
        "Şam", "Halep", "Beyrut", "Amman",
        "Kudüs", "Tel Aviv",
        "Dubai", "Abu Dabi", "Doha", "Riyad", "Cidde", "Mekke", "Medine", "Kuveyt",
        "Maskat", "Manama",
        "Bakü", "Tiflis", "Yerevan", "Astana", "Almatı", "Taşkent", "Bişkek", "Aşgabat",
        "Duşanbe", "Ulan Batur",

        # Afrika
        "Kahire", "İskenderiye", "Luksor", "Cezayir", "Tunus", "Rabat", "Kazablanka",
        "Marakeş", "Fes", "Trablus", "Hartum", "Addis Ababa", "Nairobi", "Lagos",
        "Cape Town", "Johannesburg", "Pretoria", "Durban", "Akra", "Dakar",

        # Avustralya & Okyanusya
        "Sidney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Canberra",
        "Auckland", "Wellington",

        # Latin Amerika
        "Mexico City", "Cancun", "Guadalajara",
        "Havana", "Santo Domingo",
        "Rio de Janeiro", "Sao Paulo", "Brasilia", "Salvador",
        "Buenos Aires", "Santiago", "Lima", "Bogotá", "Caracas", "Quito", "La Paz",
    ],

    "meslekler": [
        # Sağlık
        "Doktor", "Hemşire", "Diş Hekimi", "Eczacı", "Veteriner", "Psikolog",
        "Psikiyatrist", "Cerrah", "Anestezi Uzmanı", "Radyolog", "Patolog",
        "Fizyoterapist", "Diyetisyen", "Ebe", "Optisyen", "Odyolog", "Hayvan Hekimi",

        # Akademi & bilim
        "Öğretmen", "Profesör", "Akademisyen", "Araştırmacı", "Bilim İnsanı",
        "Matematikçi", "Fizikçi", "Kimyager", "Biyolog", "Astronom", "Jeolog",
        "Antropolog", "Sosyolog", "Tarihçi", "Arkeolog", "Filozof",

        # Hukuk & devlet
        "Avukat", "Hakim", "Savcı", "Noter", "Müfettiş", "Diplomat", "Büyükelçi",
        "Vali", "Belediye Başkanı", "Milletvekili", "Bakan", "Cumhurbaşkanı", "Başbakan",
        "Müsteşar",

        # Mühendislik
        "Mühendis", "Yazılım Mühendisi", "Makine Mühendisi", "Elektrik Mühendisi",
        "İnşaat Mühendisi", "Endüstri Mühendisi", "Bilgisayar Mühendisi",
        "Kimya Mühendisi", "Genetik Mühendisi", "Çevre Mühendisi", "Maden Mühendisi",
        "Uzay Mühendisi",
        "Mimar", "İç Mimar", "Şehir Plancısı", "Peyzaj Mimarı",

        # Güvenlik & ordu
        "Polis", "Asker", "Komutan", "Subay", "İtfaiyeci", "Bekçi", "Güvenlik Görevlisi",
        "Korsan", "Casus", "Komando",

        # Ulaşım
        "Pilot", "Hostes", "Kaptan", "Şoför", "Taksici", "Otobüs Şoförü", "Tır Şoförü",
        "Tren Makinisti", "Vatman", "Vagon Şefi", "Hava Trafik Kontrolörü",

        # Gıda & hizmet
        "Aşçı", "Şef", "Garson", "Komi", "Pastacı", "Pasta Şefi", "Fırıncı", "Kasap",
        "Manav", "Sucu", "Sütçü", "Bakkal",

        # Güzellik & moda
        "Kuaför", "Berber", "Estetisyen", "Manikürcü", "Makyöz",
        "Terzi", "Modacı", "Stilist", "Manken", "Ayakkabı Tamircisi",

        # Doğa & tarım
        "Çiftçi", "Bahçıvan", "Çoban", "Balıkçı", "Avcı", "Arıcı", "Bağcı",

        # Sanat & medya
        "Müzisyen", "Şarkıcı", "Besteci", "Orkestra Şefi", "DJ", "Gitarist", "Davulcu",
        "Piyanist", "Kemancı", "Bağlama Sanatçısı",
        "Aktör", "Aktris", "Yönetmen", "Senarist", "Yapımcı", "Kameraman", "Ses Mühendisi",
        "Yazar", "Şair", "Gazeteci", "Muhabir", "Editör", "Çevirmen", "Spiker",
        "Ressam", "Heykeltıraş", "Karikatürist", "Grafik Tasarımcı", "İllüstratör",
        "Animatör", "Fotoğrafçı",

        # Spor
        "Sporcu", "Futbolcu", "Basketbolcu", "Voleybolcu", "Tenisçi", "Boksör", "Güreşçi",
        "Yüzücü", "Atlet", "Kayakçı", "Snowboardcu", "Sörfçü", "Dağcı",
        "Antrenör", "Hakem", "Spor Yorumcusu", "Kondisyoner",

        # Zanaat & teknik
        "Çilingir", "Tesisatçı", "Elektrikçi", "Tornacı", "Marangoz", "Doğramacı",
        "Boyacı", "Sıvacı", "Demirci", "Kaynakçı", "Camcı", "Sıhhi Tesisatçı",
        "Çatıcı", "Lehimci", "Saatçi", "Kuyumcu", "Halıcı",

        # Endüstriyel & ağır
        "Madenci", "Petrol İşçisi", "Astronot", "Dalgıç", "Denizci", "Gemici",

        # Hizmet sektörü
        "Çöpçü", "Postacı", "Kapıcı", "Temizlikçi", "Bebek Bakıcısı", "Hizmetçi",
        "Bahçıvan", "Şoför", "Hamal", "Mektup Dağıtıcısı", "Resepsiyonist", "Sekreter",

        # Din
        "İmam", "Papaz", "Haham", "Rahip", "Keşiş", "Müezzin",

        # İş & finans
        "Tüccar", "Esnaf", "Satıcı", "Mağaza Sahibi", "CEO", "Patron", "Banker",
        "Yatırımcı", "Borsacı", "Komisyoncu", "Pazarlamacı", "Reklamcı", "Halkla İlişkiler",
        "Muhasebeci", "Mali Müşavir", "Sigortacı", "Emlakçı",

        # Eğlence & yeni
        "Sihirbaz", "Palyaço", "Akrobat", "Cambaz", "Animatör", "İllüzyonist",
        "Sunucu", "Showmen",
        "YouTuber", "TikToker", "Influencer", "Streamer", "Blogger", "Podcaster",
        "Veri Analisti", "Yapay Zeka Mühendisi", "Siber Güvenlik Uzmanı", "Veri Bilimci",
        "Oyun Geliştirici", "UX Tasarımcı",
    ],

    "sporlar": [
        # Takım sporları
        "Futbol", "Basketbol", "Voleybol", "Hentbol", "Beyzbol", "Softbol",
        "Amerikan Futbolu", "Ragbi", "Avustralya Futbolu",
        "Buz Hokeyi", "Çim Hokeyi", "Lacrosse", "Kabaddi", "Polo",

        # Raket sporları
        "Tenis", "Masa Tenisi", "Badminton", "Squash", "Padel", "Plaj Tenisi",

        # Su sporları
        "Yüzme", "Su Topu", "Senkronize Yüzme", "Dalış", "Tüplü Dalış", "Sörf",
        "Rüzgar Sörfü", "Yelken", "Kürek", "Kano", "Kayak (Su)", "Rafting",
        "Jet Ski", "Flyboard", "Stand Up Paddle",

        # Dövüş sanatları
        "Boks", "Güreş", "Karate", "Tekvando", "Aikido", "Kung Fu", "Judo",
        "Muay Thai", "Kick Boks", "Sumo", "MMA", "Eskrim", "Kendo", "Capoeira",
        "Brezilya Jiu Jitsu",

        # Atletizm
        "Atletizm", "Maraton", "100 Metre Koşu", "200 Metre Koşu", "Sprint",
        "Yüksek Atlama", "Uzun Atlama", "Üç Adım Atlama", "Sırıkla Atlama",
        "Disk Atma", "Cirit Atma", "Gülle Atma", "Çekiç Atma", "Engelli Koşu",

        # Salon / form
        "Halter", "Vücut Geliştirme", "Strongman", "Crossfit", "Yoga", "Pilates",
        "Aerobik", "Step", "Zumba",

        # Kış sporları
        "Kayak", "Snowboard", "Buz Pateni", "Buz Dansı", "Curling", "Skeleton",
        "Bobsled", "Biathlon", "Kayaklı Koşu", "Slalom", "Kar Motoru",

        # Bisiklet & motor
        "Bisiklet", "Dağ Bisikleti", "BMX", "Yol Bisikleti",
        "Motokros", "Süpermotokros", "Enduro",
        "Formula 1", "Rally", "NASCAR", "MotoGP", "Karting", "Drag Yarışı",

        # Atlı sporlar
        "At Yarışı", "Binicilik", "Engel Atlama", "Cirit",

        # Hedef sporları
        "Golf", "Mini Golf", "Disk Golf",
        "Bilardo", "Snooker", "Pool",
        "Bowling", "Bocce", "Petanca",
        "Dart", "Okçuluk", "Atıcılık", "Trap", "Skeet",

        # Zihin sporları
        "Satranç", "Briç", "Tavla", "Go", "Poker", "Dama",

        # Hava / ekstrem
        "Paraşüt", "Yamaç Paraşütü", "Bungee Jumping", "Wingsuit", "Base Jumping",
        "Dağcılık", "Tırmanma", "Sportif Tırmanış", "Buz Tırmanışı", "Kayalara Tırmanış",

        # Karma
        "Triatlon", "Demir Adam (Ironman)", "Modern Pentatlon", "Heptatlon", "Dekatlon",

        # Cimnastik
        "Cimnastik", "Ritmik Cimnastik", "Trambolin", "Akrobasi", "Parkur",

        # Diğer
        "Paintball", "Airsoft", "Lazer Tag",
        "Esports", "FIFA (Esports)", "League of Legends (Esports)",
        "Yağlı Güreş", "Kuzey Disiplini", "Köpek Yarışı", "Boğa Güreşi",
        "Sandboarding", "Skateboard", "Paten",
    ],

    "esyalar": [
        # Mobilya
        "Masa", "Sandalye", "Kanepe", "Koltuk", "Berjer", "Yatak", "Karyola", "Dolap",
        "Gardırop", "Komodin", "Sehpa", "Vitrin", "Ayakkabılık", "Şifonyer", "Konsol",
        "Salıncak", "Hamak", "Şezlong", "Tabure", "Bank",

        # Beyaz eşya & elektronik
        "Buzdolabı", "Çamaşır Makinesi", "Bulaşık Makinesi", "Fırın", "Mikrodalga Fırın",
        "Ocak", "Aspiratör", "Klima", "Ütü", "Süpürge", "Robot Süpürge",
        "Tost Makinesi", "Kahve Makinesi", "Mikser", "Blender", "Su Isıtıcısı",
        "Çaydanlık", "Semaver", "Fritöz", "Ekmek Yapma Makinesi",
        "Televizyon", "Bilgisayar", "Laptop", "Tablet", "Telefon", "Akıllı Telefon",
        "Kulaklık", "Hoparlör", "Müzik Seti", "Radyo", "Kamera", "Fotoğraf Makinesi",
        "Yazıcı", "Tarayıcı", "Klavye", "Mouse", "Monitör", "Projeksiyon",
        "Modem", "Router", "Webcam",

        # Saatler
        "Kol Saati", "Duvar Saati", "Masa Saati", "Kum Saati", "Çalar Saat", "Guguklu Saat",

        # Yazı / okul
        "Kalem", "Tükenmez Kalem", "Kurşun Kalem", "Dolma Kalem", "Keçeli Kalem", "Silgi",
        "Kalemtıraş", "Cetvel", "Açıölçer", "Pergel", "Defter", "Kitap", "Dergi",
        "Sözlük", "Atlas", "Harita", "Globe", "Yer Küre",
        "Yapıştırıcı", "Bant", "Selobant", "Zarf", "Pul", "Mektup",

        # Mutfak araçları
        "Çatal", "Kaşık", "Bıçak", "Tabak", "Bardak", "Kase", "Tencere", "Tava",
        "Kepçe", "Spatula", "Rende", "Süzgeç", "Karavana", "Kavanoz", "Şişe",
        "Tepsi", "Kürdan", "Peçete", "Servis Tabağı",

        # Alet edevat
        "Çekiç", "Tornavida", "Mengene", "Kerpeten", "Pense", "İngiliz Anahtarı",
        "Matkap", "Testere", "Eğe", "Şerit Metre", "Şakül", "Su Terazisi", "Tornavida Seti",
        "Tıraş Makinesi (Erkek)", "Çivi", "Vida", "Cıvata", "Somun", "Halat", "İp",

        # Tekstil ev
        "Halı", "Kilim", "Perde", "Tül", "Yastık", "Yorgan", "Çarşaf", "Battaniye",
        "Havlu", "Bornoz", "Terlik", "Nevresim",

        # Kapı pencere
        "Kapı", "Pencere", "Anahtar", "Kapı Kolu", "Zil", "Kilit", "Asma Kilit",
        "Kasa", "Sürgü",

        # Kişisel bakım
        "Diş Fırçası", "Diş Macunu", "Tarak", "Fırça", "Tıraş Bıçağı", "Sabun",
        "Şampuan", "Saç Kremi", "Kolonya", "Parfüm", "Deodorant", "Krem", "Losyon",
        "Ayna", "El Aynası", "Cımbız", "Tırnak Makası",

        # Giyim aksesuar
        "Şemsiye", "Çanta", "El Çantası", "Sırt Çantası", "Cüzdan", "Anahtarlık",
        "Şapka", "Bere", "Atkı", "Eldiven", "Gözlük", "Güneş Gözlüğü", "Kemer",
        "Kravat", "Papyon", "Bilezik", "Yüzük", "Kolye", "Küpe",

        # Aydınlatma / küçük ev
        "Lamba", "Avize", "Abajur", "Mum", "Çakmak", "Kibrit", "El Feneri", "Pil",
        "Şarj Aleti", "Adaptör", "Uzatma Kablosu", "Priz",

        # Dekorasyon
        "Resim Çerçevesi", "Tablo", "Heykel", "Vazo", "Saksı", "Süs Eşyası", "Biblo",
        "Halı", "Kilim",

        # Saklama / taşıma
        "Termos", "Matara", "Soğutucu Çanta", "Sepet", "Çekmece", "Kutu", "Sandık",
        "Bavul", "Valiz", "Spor Çantası",

        # Oyun / hobi
        "Top", "Lego", "Puzzle", "Yapboz", "Tabu", "Monopoly", "Tavla Takımı",
        "Satranç Takımı", "Domino Taşı", "Zar", "İskambil Destesi", "Uno Kartları",
        "Dart Tahtası", "Bilardo Topu",

        # Diğer
        "Pusula", "Düdük", "Sapan", "Yelek", "Bıçak (Çakı)", "Çuval", "Süpürge Sapı",
    ],

    "deyimler": [
        # Beden deyimleri
        "Ağzı kulaklarına varmak", "Burnu büyümek", "Burnundan kıl aldırmamak",
        "Burun kıvırmak", "Gözü doymak", "Gözü açık gitmek", "Göz kulak olmak",
        "Gözünü dört açmak", "Gözden düşmek", "Kulak misafiri olmak", "Kulak vermek",
        "Kulağına küpe olmak", "Dil dökmek", "Dilini tutmak", "Diş bilemek",
        "Boğazına düğümlenmek", "Karnı zil çalmak", "Karnı tok sırtı pek",
        "Kalp kırmak", "Yüreği ağzına gelmek", "Yüreği yanmak",
        "Eli kolu bağlı", "Eli açık", "Eli sıkı", "El üstünde tutmak",
        "Ayak diremek", "Ayakta kalmak", "Ayakları yere değmemek",
        "Ayağına dolanmak", "Ayağına çorap olmak",

        # Deyimler
        "Üç maymunu oynamak", "Bir taşla iki kuş vurmak", "Bardağı taşıran son damla",
        "Baltayı taşa vurmak", "Çantada keklik", "Foyası meydana çıkmak",
        "Pireyi deve yapmak", "Sinekten yağ çıkarmak", "Kazın ayağı öyle değil",
        "Damdan düşer gibi", "Saman altından su yürütmek", "Etekleri zil çalmak",
        "Pabucu dama atılmak", "Pabucu büyük çıkmak", "Çiğnemeden yutmak",
        "Tereyağından kıl çeker gibi", "Atı alan Üsküdar'ı geçti",
        "İçi içine sığmamak", "Kafayı yemek", "Kafa göz yarmak", "Kafa kola almak",
        "Surat asmak", "Yüz çevirmek", "Yüz vermek", "Yüzü kızarmak",
        "Yağ çekmek", "Pul kadar suyu olmak", "İğneyle kuyu kazmak",
        "Damarına basmak", "Burun buruna gelmek", "Boyun eğmek",
        "Kuyruğunu kıstırmak", "Kuyruğunu titretmek", "Kapıyı yüzüne kapamak",
        "Su koyuvermek", "Eline su dökemez", "Avucunu yalamak",
        "Boş boğazlık etmek", "Çenesi düşmek", "Lafı ağzına tıkamak",

        # Atasözleri
        "Damlaya damlaya göl olur",
        "Bal tutan parmağını yalar",
        "Tatlı dil yılanı deliğinden çıkarır",
        "Acele işe şeytan karışır",
        "Aç tavuk kendini buğday ambarında sanır",
        "Akıllı düşman akılsız dosttan iyidir",
        "Az tamah çok ziyan getirir",
        "Bir elin nesi var iki elin sesi var",
        "Boş çuval ayakta durmaz",
        "Bugünün işini yarına bırakma",
        "Çürük tahta çivi tutmaz",
        "Ektiğini biçersin",
        "El elden üstündür",
        "Erken kalkan yol alır",
        "Görünen köy kılavuz istemez",
        "Güneş balçıkla sıvanmaz",
        "İğneyi kendine batır çuvaldızı başkasına",
        "İnsan yedisinde ne ise yetmişinde de odur",
        "Komşu komşunun külüne muhtaçtır",
        "Kuzguna yavrusu güzel görünür",
        "Lafla peynir gemisi yürümez",
        "Misafir umduğunu değil bulduğunu yer",
        "Olacakla öleceğe çare yoktur",
        "Para parayı çeker",
        "Sakla samanı gelir zamanı",
        "Söz gümüşse sükut altındır",
        "Üzüm üzüme baka baka kararır",
        "Vakit nakittir",
        "Yalancının mumu yatsıya kadar yanar",
        "Yiğit lafının eridir",
        "Damlaya damlaya göl olur",
        "Ağaç yaşken eğilir",
        "Bir musibet bin nasihatten yeğdir",
        "İki dinle bir söyle",
        "Ne ekersen onu biçersin",
        "Sona kalan dona kalır",
        "Ucuz etin yahnisi yavan olur",
        "Yuvarlanan taş yosun tutmaz",
        "Çıkmadık candan ümit kesilmez",
        "İti an çomağı hazırla",
        "Bir fincan kahvenin kırk yıl hatırı vardır",
        "Eğri otur doğru konuş",
        "Sakınılan göze çöp batar",
        "Söz uçar yazı kalır",
        "Kavak yeli esmek",
        "İşi tıkırında",
        "Armut piş ağzıma düş",
        "Misafir on kısmetle gelir",
        "Devlet kuşu", "Devekuşu gibi davranmak",
        "Su uyur düşman uyumaz",
        "Tilkinin dönüp dolaşıp geleceği yer kürkçü dükkanıdır",
        "Tencere yuvarlanmış kapağını bulmuş",
        "Bana arkadaşını söyle sana kim olduğunu söyleyeyim",
        "İt ürür kervan yürür",
        "Sabreden derviş muradına ermiş",
        "Damdan düşenin halinden damdan düşen anlar",
        "Hamama giren terler",
        "Bir koyundan iki post çıkmaz",
        "Çok bilen çok yanılır",
        "Üzümünü ye bağını sorma",
        "Söyleyenden dinleyen arif gerek",
        "Kel ölür sırma saçlı olur, kör ölür badem gözlü olur",
    ],

}

# Her kategorideki duplikatları sırayı bozmadan temizle.
CATEGORIES = {k: list(dict.fromkeys(v)) for k, v in CATEGORIES.items()}


# "Kolay" mod için her kategoriden en yaygın bilinen seçimler.
EASY_NAMES = {
    "populer_ikonlar": [
        "Atatürk", "Tarkan", "Barış Manço", "Kemal Sunal", "Cem Yılmaz",
        "Şener Şen", "Sezen Aksu", "Türkan Şoray", "Fatih Terim", "Recep İvedik",
        "Recep Tayyip Erdoğan", "Fatih Sultan Mehmet", "Mevlana", "Nasreddin Hoca",
        "Albert Einstein", "Leonardo da Vinci", "Napoleon", "Kleopatra",
        "Mozart", "Beethoven", "Michael Jackson", "Elvis Presley",
        "Charlie Chaplin", "Bruce Lee", "Muhammad Ali", "Lionel Messi",
        "Cristiano Ronaldo", "Michael Jordan", "Elon Musk", "Steve Jobs",
        "Bill Gates", "Mark Zuckerberg", "Mr.Beast", "Adolf Hitler",
        "Obama", "Putin", "Trump", "Hz. Muhammed", "İsa Mesih",
        "Darth Vader", "Harry Potter", "Gandalf", "Batman", "Spider-Man",
        "Sherlock Holmes", "James Bond", "Shrek", "Jack Sparrow", "Joker",
        "Iron Man", "Superman", "Walter White", "Pikachu", "Goku",
        "Naruto", "Mario", "Sonic", "Master Chief", "Kratos",
        "Lara Croft", "Mickey Mouse", "Süngerbob", "Garfield", "Yoda",
        "Zeus", "Hades",
    ],
    "tarihi_olaylar": [
        "İstanbul'un Fethi", "Kurtuluş Savaşı", "Çanakkale Savaşı",
        "Cumhuriyetin İlanı", "1. Dünya Savaşı", "2. Dünya Savaşı",
        "Fransız İhtilali", "Sanayi Devrimi", "Amerika'nın Keşfi",
        "Aya İniş", "Çernobil Faciası", "Berlin Duvarı'nın Yıkılışı",
        "Titanik'in Batışı", "Hiroşima Bombalaması", "9/11 Saldırıları",
        "Covid-19 Pandemisi", "Matbaanın İcadı", "Tekerleğin İcadı",
        "Rönesans", "Haçlı Seferleri", "Kara Veba", "Holokost",
        "Soğuk Savaş", "Kennedy Suikastı", "Truva Savaşı",
        "Piramitlerin İnşası", "İslam'ın Doğuşu", "Bolşevik Devrimi",
        "Pearl Harbor Saldırısı",
    ],
    "hayvanlar": [
        "Aslan", "Kaplan", "Fil", "Zürafa", "Panda", "Kanguru", "Zebra",
        "Goril", "Timsah", "Ayı", "Kurt", "Tilki", "Kedi", "Köpek",
        "At", "İnek", "Koyun", "Domuz", "Tavuk", "Ördek", "Sincap",
        "Fare", "Yarasa", "Papağan", "Penguen", "Ahtapot", "Yunus",
        "Balina", "Beyaz Köpekbalığı", "T-Rex", "Unicorn", "Ejderha",
        "Phoenix", "Kraken", "Pikachu", "Çita", "Kanarya", "Tavşan",
        "Devekuşu", "Yılan",
    ],
    "yemekler": [
        "Lahmacun", "Pide", "Pizza", "Hamburger", "Döner", "İskender Kebap", "Adana Kebap",
        "Mantı", "Çiğ Köfte", "Köfte", "Karnıyarık", "Mercimek Çorbası", "Menemen",
        "Simit", "Börek", "Sucuklu Yumurta", "Künefe", "Baklava", "Sütlaç", "Dondurma",
        "Kuru Fasulye", "Pilav", "Sushi", "Ramen", "Lazanya", "Spagetti", "Carbonara",
        "Cheeseburger", "Hot Dog", "Sandviç", "Cheesecake", "Pancake", "Waffle", "Donut",
        "Taco", "Burrito", "Croissant", "Falafel", "Humus", "Tiramisu",
        "Coca-Cola", "Ayran", "Türk Kahvesi", "Çay", "Kola",
        "Çikolata", "Patates Kızartması", "Salata", "Patlamış Mısır", "Tost",
    ],
    "filmler": [
        "Titanik", "Avatar", "Avengers", "Iron Man", "Spider-Man", "Batman", "Joker",
        "The Dark Knight", "Star Wars", "Harry Potter ve Felsefe Taşı",
        "Yüzüklerin Efendisi", "Inception (Başlangıç)", "Interstellar (Yıldızlararası)",
        "The Matrix", "Forrest Gump", "Esaretin Bedeli", "Pulp Fiction", "Baba",
        "Jurassic Park", "E.T.", "Gladyatör", "Rocky", "Terminator", "Alien",
        "John Wick", "James Bond", "Hızlı ve Öfkeli", "Karayip Korsanları",
        "Aslan Kral", "Karlar Ülkesi", "Şrek", "Buz Devri", "Kung Fu Panda",
        "Top Gun", "La La Land", "Parazit (Parasite)",
        "GORA", "Recep İvedik", "Vizontele", "Babam ve Oğlum", "Eşkıya",
        "Hababam Sınıfı", "Düğün Dernek", "Yedinci Koğuştaki Mucize",
    ],
    "markalar": [
        "Apple", "Google", "Microsoft", "Amazon", "Facebook", "Instagram", "WhatsApp",
        "TikTok", "YouTube", "Netflix", "Spotify",
        "Coca-Cola", "Pepsi", "Fanta", "Red Bull", "Starbucks", "McDonald's", "Burger King",
        "KFC", "Domino's Pizza", "Nutella", "Oreo", "Pringles", "Snickers", "Kit Kat",
        "Nike", "Adidas", "Puma", "Lacoste", "Gucci", "Louis Vuitton", "Chanel",
        "Zara", "H&M", "Mango",
        "BMW", "Mercedes-Benz", "Audi", "Volkswagen", "Ferrari", "Lamborghini",
        "Toyota", "Honda", "Tesla", "Ford",
        "Samsung", "Sony", "LG", "Huawei", "Xiaomi",
        "Disney", "Marvel", "Nintendo", "PlayStation", "Xbox", "Lego",
        "IKEA", "Migros", "BİM", "Hepsiburada", "Trendyol",
        "Turkcell", "THY", "Arçelik", "Ülker", "Eti",
    ],
    "sehirler": [
        "İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Adana", "Konya", "Gaziantep",
        "Kayseri", "Eskişehir", "Trabzon", "Samsun", "Diyarbakır", "Şanlıurfa",
        "Bodrum", "Marmaris", "Fethiye", "Kapadokya", "Pamukkale",
        "Londra", "Paris", "Berlin", "Roma", "Madrid", "Lizbon", "Amsterdam", "Viyana",
        "Atina", "Moskova", "Prag", "Budapeşte", "Barselona", "Venedik",
        "New York", "Los Angeles", "Las Vegas", "Miami", "Washington",
        "Tokyo", "Seul", "Pekin", "Şangay", "Hong Kong", "Singapur", "Bangkok", "Dubai",
        "Mekke", "Medine", "Kahire", "Cape Town", "Sidney", "Rio de Janeiro",
    ],
    "meslekler": [
        "Doktor", "Hemşire", "Diş Hekimi", "Eczacı", "Veteriner", "Psikolog",
        "Öğretmen", "Profesör", "Avukat", "Hakim", "Polis", "Asker", "İtfaiyeci",
        "Pilot", "Hostes", "Şoför", "Taksici", "Kaptan",
        "Mühendis", "Yazılım Mühendisi", "Mimar",
        "Aşçı", "Şef", "Garson", "Fırıncı", "Kasap", "Manav",
        "Kuaför", "Berber", "Terzi", "Modacı", "Manken",
        "Çiftçi", "Bahçıvan", "Çoban", "Balıkçı",
        "Müzisyen", "Şarkıcı", "DJ", "Aktör", "Yönetmen", "Yazar", "Gazeteci",
        "Ressam", "Fotoğrafçı",
        "Futbolcu", "Basketbolcu", "Boksör", "Antrenör", "Hakem",
        "Marangoz", "Elektrikçi", "Tesisatçı", "Çilingir", "Boyacı",
        "Postacı", "Temizlikçi",
        "İmam", "Papaz",
        "Sihirbaz", "Palyaço",
        "YouTuber", "TikToker", "Influencer", "Streamer",
    ],
    "sporlar": [
        "Futbol", "Basketbol", "Voleybol", "Tenis", "Masa Tenisi", "Badminton",
        "Yüzme", "Sörf", "Yelken", "Kürek",
        "Boks", "Güreş", "Karate", "Tekvando", "Judo", "MMA",
        "Atletizm", "Maraton", "100 Metre Koşu", "Uzun Atlama",
        "Halter", "Yoga", "Pilates",
        "Kayak", "Snowboard", "Buz Pateni", "Buz Hokeyi",
        "Bisiklet", "Formula 1", "MotoGP",
        "Golf", "Bilardo", "Bowling", "Dart", "Okçuluk",
        "Satranç", "Poker",
        "Dağcılık", "Paraşüt", "Bungee Jumping",
        "Cimnastik", "Skateboard",
        "Amerikan Futbolu", "Ragbi", "Beyzbol", "Hentbol",
        "Binicilik", "At Yarışı",
    ],
    "esyalar": [
        "Masa", "Sandalye", "Kanepe", "Yatak", "Dolap", "Sehpa",
        "Buzdolabı", "Çamaşır Makinesi", "Fırın", "Mikrodalga Fırın", "Ütü", "Süpürge",
        "Televizyon", "Bilgisayar", "Laptop", "Tablet", "Telefon", "Kulaklık",
        "Saat", "Kol Saati", "Duvar Saati",
        "Kalem", "Defter", "Kitap", "Silgi", "Makas", "Cetvel",
        "Çatal", "Kaşık", "Bıçak", "Tabak", "Bardak", "Tencere", "Tava",
        "Çekiç", "Tornavida", "Matkap",
        "Halı", "Perde", "Yastık", "Battaniye", "Havlu", "Terlik",
        "Diş Fırçası", "Sabun", "Şampuan", "Ayna", "Tarak",
        "Şemsiye", "Çanta", "Cüzdan", "Anahtar", "Gözlük", "Şapka",
        "Lamba", "Mum", "El Feneri",
        "Top", "Lego", "Puzzle", "Tavla Takımı", "Satranç Takımı",
    ],
    "deyimler": [
        "Damlaya damlaya göl olur",
        "Bir elin nesi var iki elin sesi var",
        "Tatlı dil yılanı deliğinden çıkarır",
        "Ağaç yaşken eğilir",
        "Acele işe şeytan karışır",
        "Erken kalkan yol alır",
        "Söz gümüşse sükut altındır",
        "Para parayı çeker",
        "Vakit nakittir",
        "Bal tutan parmağını yalar",
        "Yalancının mumu yatsıya kadar yanar",
        "Bir taşla iki kuş vurmak",
        "Pireyi deve yapmak",
        "Etekleri zil çalmak",
        "Burnu büyümek",
        "Kulak misafiri olmak",
        "Karnı zil çalmak",
        "Üç maymunu oynamak",
        "Çantada keklik",
        "Bardağı taşıran son damla",
        "Atı alan Üsküdar'ı geçti",
        "Tencere yuvarlanmış kapağını bulmuş",
        "İt ürür kervan yürür",
        "Görünen köy kılavuz istemez",
        "Armut piş ağzıma düş",
        "Su uyur düşman uyumaz",
        "Damdan düşer gibi",
        "Ağzı kulaklarına varmak",
        "Gözünü dört açmak",
        "Kalp kırmak",
    ],
}


def _resolve_pool(category: str, difficulty: str = "hepsi",
                  custom_words: list[str] | None = None) -> list[str]:
    """Verilen ayarlara göre öğe havuzunu döndür."""
    # Özel kategori — host'un girdiği kelimeler
    if category == "ozel":
        return list(dict.fromkeys([w.strip() for w in (custom_words or []) if w and w.strip()]))

    # Karma mod — tüm kategorileri birleştir
    if category == "karma":
        if difficulty == "kolay":
            merged = []
            for v in EASY_NAMES.values():
                merged.extend(v)
            return list(dict.fromkeys(merged))
        merged = []
        for v in CATEGORIES.values():
            merged.extend(v)
        return list(dict.fromkeys(merged))

    if category not in CATEGORIES:
        category = "populer_ikonlar"

    # "ozel_sayi" zorluğu = tam havuzdan al (Room sub-sample edecek)
    if difficulty == "kolay" and category in EASY_NAMES:
        return EASY_NAMES[category]

    return CATEGORIES[category]


def resolve_pool(category: str, difficulty: str = "hepsi",
                 custom_words: list[str] | None = None) -> list[str]:
    """Public: kategoriye göre tam havuzu döndür."""
    return _resolve_pool(category, difficulty, custom_words)


def get_random_names(count: int, category: str = "populer_ikonlar",
                     difficulty: str = "hepsi",
                     custom_words: list[str] | None = None) -> list[str]:
    """Seçilen kategoriden belirtilen sayıda benzersiz rastgele isim seç."""
    pool = _resolve_pool(category, difficulty, custom_words)

    if not pool:
        raise ValueError("Kategori boş, oyun başlatılamaz.")

    if count > len(pool):
        raise ValueError(
            f"Seçilen kategoride en fazla {len(pool)} kelime var, {count} istendi."
        )
    return random.sample(pool, count)


def get_all_names(category: str = "populer_ikonlar",
                  difficulty: str = "hepsi",
                  custom_words: list[str] | None = None) -> list[str]:
    """Bir kategorideki tüm öğeleri alfabetik sırada döndür (eleme paneli için)."""
    pool = _resolve_pool(category, difficulty, custom_words)
    return sorted(pool, key=lambda s: s.lower())
