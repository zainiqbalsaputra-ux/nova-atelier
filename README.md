# NOVA ATELIER — Fashion Web Store Prototype

Prototype web store fashion UMKM untuk tugas E-Commerce Ops. Pengalaman belanja dibuat sebagai simulasi end-to-end dengan visual premium minimalist.

## Fitur

- Home editorial, katalog dengan pencarian/filter/sort, dan halaman detail produk
- Shopping bag interaktif (quantity, remove, subtotal, ongkir, promo)
- Promo dummy: `NOVA10` dan `WELCOME15`
- Checkout simulasi dengan validasi, konfirmasi pesanan, dan order tracking timeline
- Customer service: FAQ dan template auto-reply
- 12 data produk statis; cart serta pesanan dikelola memakai `st.session_state`

## Teknologi

- Python
- Streamlit
- Tidak menggunakan database, backend API, autentikasi, atau payment gateway.

## Menjalankan lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy ke Streamlit Community Cloud

1. Push folder project ini ke repository GitHub.
2. Buat aplikasi baru pada Streamlit Community Cloud dan pilih repository tersebut.
3. Set **Main file path** ke `app.py`.
4. Klik deploy. Dependensi akan diinstal dari `requirements.txt`.

## Catatan

Seluruh transaksi, pembayaran, order ID, dan tracking pada aplikasi ini bersifat **simulasi untuk demonstrasi akademik**. State hanya tersimpan selama sesi browser aktif dan akan hilang ketika sesi di-refresh.
