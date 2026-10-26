# Klipo – AI Clipper

Ubah satu video panjang jadi klip vertikal berkaption. Semua pemrosesan video berjalan di browser, tidak ada yang diunggah ke server.

## Fitur
- Upload video (MP4, MOV, WebM) atau ambil dari link YouTube, Instagram, TikTok
- Mode Auto, Manual, dan Manual + AI dengan skor tiap klip
- Trim klip di timeline, undo dan redo
- Preview 9:16, 1:1, dan 16:9
- Caption editor: font, warna, animasi, garis tepi, preset gaya, watermark
- Judul dan hashtag otomatis
- Ekspor satu klip atau semua klip (MP4 jika didukung browser, selain itu WebM)
- Simpan proyek di browser

## Menjalankan secara lokal (dengan fitur link)
```bash
pip install -r requirements.txt
python server.py
```
Buka http://localhost:8765

## Hanya upload file (tanpa server)
Buka `index.html` langsung di browser, atau aktifkan GitHub Pages:
**Settings → Pages → Deploy from a branch → main → / (root)**.
Di GitHub Pages fitur "Ambil dari link" tidak aktif karena membutuhkan `server.py`.

## Catatan
- "AI" saat ini memilih momen dari volume dan dinamika audio, belum memahami isi ucapan.
- Caption diketik manual. Transkripsi otomatis membutuhkan layanan di server.
- Pakai fitur link hanya untuk video milikmu atau yang kamu punya izinnya.
- Jika pengambilan link gagal, perbarui yt-dlp: `pip install -U yt-dlp`.
