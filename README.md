# Ben Kimim? 🎭

Discord'da arka planda oynanan çok oyunculu "Ben Kimim?" tahmin oyunu.

## Kurulum

### Gereksinimler
- Python 3.11+
- Modern tarayıcı (Chrome, Firefox, Edge)

### Sunucu kurulumu

```bash
cd server
pip install -r requirements.txt
python main.py
```

Sunucu `ws://localhost:8765` adresinde başlayacak.

### Client

`client/index.html` dosyasını tarayıcıda aç. Hepsi bu!

## Nasıl Oynanır?

1. Tarayıcıda `index.html`'i aç
2. Adını yaz, **Odaya Katıl**'a tıkla (yeni oda oluşur)
3. Oda kodunu arkadaşlarınla paylaş
4. Herkes katılınca host **Oyunu Başlat**'a tıklar
5. Herkesin kafasına bir ünlü ismi atanır — kendi ismini göremezsin, sadece "???" yazar
6. Alttaki kutudan kafandaki ismi tahmin etmeye çalış
7. Doğru tahmin eden oyuncunun ismi açılır
8. Herkes doğru tahmin ettiğinde oyun biter, sıralama gösterilir

## Teknik Notlar

- Backend: Python + `websockets`
- Frontend: Vanilla HTML/CSS/JS
- WebSocket portu: 8765
- Minimum oyuncu: 2
site:https://talhatamirci.github.io/whoami/client/index.html
