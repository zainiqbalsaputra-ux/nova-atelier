import streamlit as st
from components.ui import BRAND, footer, inject_css, mobile_navigation, navigation, product_card
from data.products import PRODUCTS, get_product
from utils.store import PROMOS, add_item, create_order, initialize_state, navigate, order_totals, rupiah

st.set_page_config(page_title=BRAND["name"], page_icon="N", layout="wide", initial_sidebar_state="collapsed")

def title(label, text): st.markdown(f'<div class="eyebrow">{label}</div><h1 style="margin:.3rem 0">{text}</h1>',unsafe_allow_html=True)
def section(label,text): st.markdown(f'<div class="line" style="margin-top:3rem"></div><div class="eyebrow">{label}</div><h2 style="margin:.25rem 0 1rem">{text}</h2>',unsafe_allow_html=True)

def home():
    st.markdown('<div class="promo">Promo hari ini · Gratis ongkir untuk pembelian di atas Rp 500.000</div>',unsafe_allow_html=True)
    st.markdown('<div class="eyebrow" style="margin:.75rem 0">Kategori</div>',unsafe_allow_html=True)
    labels=[("AT","Atasan"),("KM","Kemeja"),("HD","Hoodie"),("CL","Celana"),("OT","Outer"),("SL","Semua")]
    category_html=''.join(f'<div class="category-shortcut"><div class="category-icon">{icon}</div><div class="category-name">{label}</div></div>' for icon,label in labels)
    st.markdown(f'<div class="category-rail">{category_html}</div>',unsafe_allow_html=True)
    st.markdown('<div class="line" style="margin-top:1.1rem"></div>',unsafe_allow_html=True)
    with st.container(key="home-hero"):
        a,b=st.columns([1,1.05],gap="large")
        with a:
            st.markdown('<div class="market-banner"><div class="eyebrow">Promo koleksi terbaru</div><h1>Diskon hingga 30%</h1><p class="muted">Pilihan pakaian sehari-hari dengan harga khusus untuk periode terbatas.</p></div>',unsafe_allow_html=True)
            if st.button("Belanja Sekarang",type="primary"): navigate("Koleksi")
        with b: st.image("https://images.unsplash.com/photo-1496217590455-aa63a8350eea?auto=format&fit=crop&w=1200&q=85",use_container_width=True)
    section("Promo pilihan","Flash Sale")
    with st.container(key="home-grid"):
        for col,p in zip(st.columns(4),PRODUCTS[:4]):
            with col: product_card(p,"featured")
    section("Produk terlaris","Pilihan untuk Anda")
    with st.container(key="home-grid-two"):
        for col,p in zip(st.columns(4),PRODUCTS[4:8]):
            with col: product_card(p,"new")
    section("Rekomendasi produk","Temukan produk lainnya")
    with st.container(key="home-grid-three"):
        for col,p in zip(st.columns(4),PRODUCTS[8:12]):
            with col: product_card(p,"recommend")
    footer()

def catalog():
    title("NOVA ATELIER","Koleksi");st.markdown('<p class="muted">Pilihan pakaian untuk kebutuhan sehari-hari.</p>',unsafe_allow_html=True)
    a,b,c=st.columns([2.1,1,1])
    with a:q=st.text_input("Cari produk",placeholder="Cari produk...",value=st.session_state.pop("catalog_query", ""))
    with b:cat=st.selectbox("Kategori",["Semua","T-Shirt","Kemeja","Hoodie","Celana","Outerwear"])
    with c:sorting=st.selectbox("Urutkan",["Pilihan terbaru","Harga terendah","Harga tertinggi"])
    items=[p for p in PRODUCTS if (cat=="Semua" or p["category"]==cat) and (q.lower() in p["name"].lower() or q.lower() in p["category"].lower())]
    if sorting=="Harga terendah":items.sort(key=lambda x:x["price"])
    if sorting=="Harga tertinggi":items.sort(key=lambda x:x["price"],reverse=True)
    st.caption(f"Menampilkan {len(items)} produk")
    with st.container(key="catalog-grid"):
        for start in range(0,len(items),4):
            for col,p in zip(st.columns(4),items[start:start+4]):
                with col:product_card(p,"catalog")
    footer()

def product():
    p=get_product(st.session_state.selected_product) or PRODUCTS[0]
    if st.button("← Kembali ke koleksi",type="tertiary"):navigate("Koleksi")
    a,b=st.columns([1.12,.88],gap="large")
    with a:st.image(p["image"],use_container_width=True)
    with b:
        st.markdown(f'<div class="eyebrow">{p["category"]}</div><h1 style="margin:.3rem 0">{p["name"]}</h1><div class="product-price" style="font-size:1.15rem">{rupiah(p["price"])}</div><p class="muted">★ {p["rating"]} dari 5</p><div class="line"></div><p style="line-height:1.65">{p["description"]}</p>',unsafe_allow_html=True)
        with st.form("add"):
            color=st.selectbox("Warna",p["colors"]);size=st.selectbox("Ukuran",p["sizes"]);qty=st.number_input("Jumlah",1,p["stock"],1);submit=st.form_submit_button("Tambah ke Keranjang",type="primary")
        if submit:add_item(p,size,color,qty);st.toast("Produk ditambahkan ke keranjang.")
        st.caption(f"Stok tersedia: {p['stock']} · Estimasi pengiriman 2–4 hari kerja")
        with st.expander("Material & perawatan"):st.write(f"**Material:** {p['material']}  \n**Perawatan:** {p['care']}")
    footer()

def summary(promo=False,action=None):
    total=order_totals();st.markdown('<div class="summary"><div class="eyebrow">Ringkasan pesanan</div>',unsafe_allow_html=True)
    if promo:
        code=st.text_input("Kode promo",placeholder="NOVA10 atau WELCOME15")
        if st.button("Gunakan kode",key="promo",type="tertiary"):
            if code.strip().upper() in PROMOS:st.session_state.promo=code.strip().upper();st.success("Kode promo berhasil digunakan.");st.rerun()
            else:st.error("Kode promo tidak tersedia.")
        if st.session_state.promo:st.caption(f"Promo aktif: {st.session_state.promo}")
    ship="Gratis" if not total["shipping"] else rupiah(total["shipping"])
    st.markdown(f'<p>Subtotal <span style="float:right">{rupiah(total["subtotal"])}</span></p><p>Diskon <span style="float:right">− {rupiah(total["discount"])}</span></p><p>Ongkir <span style="float:right">{ship}</span></p><div class="line"></div><p><b>Total</b><b style="float:right">{rupiah(total["total"])}</b></p></div>',unsafe_allow_html=True)
    if action and st.button(action,type="primary"):navigate("Checkout")

def cart():
    title("Pilihan Anda","Keranjang")
    if not st.session_state.cart:
        st.markdown('<div class="empty"><h2>Keranjang Anda masih kosong.</h2><p class="muted">Temukan produk yang sesuai untuk Anda.</p></div>',unsafe_allow_html=True)
        if st.button("Lihat Koleksi",type="primary"):navigate("Koleksi")
        return
    a,b=st.columns([1.55,.72],gap="large")
    with a:
        for i,item in enumerate(st.session_state.cart):
            im,detail,price,control=st.columns([.18,.43,.16,.23])
            with im:st.image(item["image"],use_container_width=True)
            with detail:st.markdown(f'<div class="product-name">{item["name"]}</div><div class="product-meta">{item["color"]} · Ukuran {item["size"]}</div>',unsafe_allow_html=True)
            with price:st.markdown(f'<div class="product-price">{rupiah(item["price"]*item["quantity"])}</div>',unsafe_allow_html=True)
            with control:
                x,y,z=st.columns(3)
                with x:
                    if st.button("−",key=f"minus{i}",type="tertiary"):item["quantity"]=max(1,item["quantity"]-1);st.rerun()
                with y:st.markdown(f'<p style="text-align:center">{item["quantity"]}</p>',unsafe_allow_html=True)
                with z:
                    if st.button("+",key=f"plus{i}",type="tertiary") and item["quantity"]<item["stock"]:item["quantity"]+=1;st.rerun()
                if st.button("Hapus",key=f"remove{i}",type="tertiary"):st.session_state.cart.pop(i);st.rerun()
            st.markdown('<div class="line"></div>',unsafe_allow_html=True)
    with b:summary(True,"Lanjut ke Pembayaran")
    footer()

def checkout():
    if not st.session_state.cart:navigate("Keranjang")
    title("Pemeriksaan pesanan","Pembayaran");a,b=st.columns([1.2,.8],gap="large")
    with a:
        st.markdown('<h3 style="font-family:DM Sans!important;font-size:1.05rem!important">Informasi pengiriman</h3>',unsafe_allow_html=True)
        with st.form("checkout"):
            name=st.text_input("Nama lengkap");phone=st.text_input("Nomor HP");address=st.text_area("Alamat lengkap");city,postal=st.columns(2)
            with city:city_val=st.text_input("Kota")
            with postal:postal_val=st.text_input("Kode pos")
            payment=st.radio("Metode pembayaran",["QRIS","Transfer Bank","COD"],help="Seluruh metode pembayaran hanya simulasi.");submit=st.form_submit_button("Buat Pesanan",type="primary")
        if submit:
            if not all(x.strip() for x in [name,phone,address,city_val,postal_val]):st.error("Mohon lengkapi seluruh informasi pengiriman.")
            else:create_order({"name":name,"phone":phone,"address":f"{address}, {city_val}, {postal_val}"},payment);navigate("Berhasil")
    with b:
        st.markdown('<div class="summary"><div class="eyebrow">Produk</div>',unsafe_allow_html=True)
        for item in st.session_state.cart:st.markdown(f'<p class="muted">{item["name"]} × {item["quantity"]}<span style="float:right">{rupiah(item["price"]*item["quantity"])}</span></p>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True);summary()

def success():
    o=st.session_state.order
    if not o:navigate("Beranda")
    st.markdown(f'<div style="border-top:2px solid #1D1D1B;padding:2.2rem 0 1.5rem"><div class="eyebrow">Pesanan berhasil dibuat</div><h1>Terima kasih telah berbelanja di {BRAND["name"]}.</h1><p class="muted">Pesanan Anda telah kami terima dan akan diproses sesuai metode pembayaran yang dipilih.</p></div>',unsafe_allow_html=True)
    a,b=st.columns(2,gap="large")
    with a:st.markdown(f'<div class="summary"><div class="eyebrow">Nomor pesanan</div><h3 style="font-family:DM Sans!important">{o["id"]}</h3><p class="muted">Dibuat pada {o["date"]}</p></div>',unsafe_allow_html=True)
    with b:st.markdown(f'<div class="summary"><div class="eyebrow">Total pesanan</div><h3 style="font-family:DM Sans!important">{rupiah(o["total"])}</h3><p class="muted">{o["payment"]} · Simulasi pembayaran</p></div>',unsafe_allow_html=True)
    a,b=st.columns(2)
    with a:
        if st.button("Lihat Status Pesanan",type="primary"):navigate("Status")
    with b:
        if st.button("Kembali ke Koleksi",type="tertiary"):navigate("Koleksi")

def tracking():
    title("Informasi pesanan","Status Pesanan");o=st.session_state.order
    if not o:st.info("Belum ada pesanan pada sesi ini.");return
    st.markdown(f'<div class="summary"><div class="eyebrow">Nomor pesanan</div><h3 style="font-family:DM Sans!important;margin:.3rem 0">{o["id"]}</h3><p class="muted">Estimasi pengiriman 2–4 hari kerja setelah pesanan dikirim.</p></div><br>',unsafe_allow_html=True)
    for i,(t,d) in enumerate([("Pesanan dibuat","Pesanan Anda telah kami terima."),("Pembayaran dikonfirmasi","Metode pembayaran tercatat untuk simulasi."),("Sedang dikemas","Produk sedang disiapkan."),("Diserahkan ke kurir","Informasi kurir akan ditampilkan pada toko aktif."),("Dalam perjalanan","Pesanan sedang menuju alamat Anda."),("Selesai","Pesanan telah diterima.")]):st.markdown(f'<div class="timeline {"pending" if i>2 else ""}"><b>{t}</b><br><span class="muted">{d}</span></div>',unsafe_allow_html=True)
    st.caption("Status pesanan adalah simulasi untuk keperluan demonstrasi.")

def help_page():
    title("Informasi dan dukungan","Bantuan & Layanan");st.markdown('<p class="muted">Informasi yang Anda butuhkan sebelum dan setelah berbelanja.</p>',unsafe_allow_html=True);section("","Pertanyaan yang sering diajukan")
    for q,a in [("Bagaimana cara melakukan pemesanan?","Pilih produk, tentukan warna dan ukuran, lalu tambahkan ke keranjang. Lanjutkan ke pembayaran untuk mengisi data pengiriman."),("Berapa lama pesanan diproses?","Pesanan diproses dalam 1–2 hari kerja. Estimasi pengiriman 2–4 hari kerja setelah dikirim."),("Bagaimana cara mengecek status pesanan?","Setelah pesanan dibuat, buka halaman Status Pesanan."),("Apakah produk dapat ditukar?","Tukar ukuran dapat diajukan maksimal 7 hari setelah produk diterima, selama produk belum dipakai dan label masih lengkap."),("Metode pembayaran apa yang tersedia?","QRIS, Transfer Bank, dan COD tersedia sebagai simulasi.")]:
        with st.expander(q):st.write(a)
    section("","Template respons pelanggan")
    texts=[("Status pesanan","Halo Kak, terima kasih sudah menghubungi NOVA ATELIER. Pesanan Kakak sedang kami proses. Silakan cek halaman Status Pesanan menggunakan nomor pesanan Kakak."),("Informasi ukuran","Halo Kak, panduan ukuran tersedia pada halaman produk. Untuk tampilan lebih santai, Kakak dapat mempertimbangkan naik satu ukuran."),("Pengiriman","Halo Kak, pesanan diproses 1–2 hari kerja. Estimasi pengiriman 2–4 hari kerja setelah pesanan diserahkan ke kurir."),("Tukar ukuran","Halo Kak, kami dapat membantu pengajuan tukar ukuran maksimal 7 hari setelah barang diterima. Produk harus baru dan label masih lengkap.")]
    for row in range(0,4,2):
        for col,(h,t) in zip(st.columns(2),texts[row:row+2]):
            with col:st.markdown(f'<div class="summary"><div class="eyebrow">{h}</div><p style="line-height:1.6">{t}</p></div>',unsafe_allow_html=True)
    footer()

def about():
    title(f"Tentang {BRAND['name']}","Pakaian yang dibuat untuk digunakan setiap hari.");st.markdown(f'<p class="muted" style="max-width:600px;line-height:1.75;font-size:1.05rem">{BRAND["name"]} adalah brand fashion UMKM dengan pendekatan minimal dan modern. Kami berfokus pada pakaian yang nyaman, mudah dipadukan, dan relevan untuk keseharian.</p>',unsafe_allow_html=True);section("","")
    for col,h,t in zip(st.columns(3),["Bahan yang dipilih","Potongan yang fungsional","Dibuat dengan fokus"],["Kami memilih material yang nyaman dan mudah dirawat.","Siluet sederhana yang mendukung aktivitas sehari-hari.","Koleksi dirancang dengan perhatian pada hal yang esensial."]):
        with col:st.markdown(f'<h3>{h}</h3><p class="muted">{t}</p>',unsafe_allow_html=True)
    footer()

initialize_state();inject_css();navigation()
{"Beranda":home,"Koleksi":catalog,"Produk":product,"Keranjang":cart,"Checkout":checkout,"Berhasil":success,"Status":tracking,"Bantuan":help_page,"Tentang":about}[st.session_state.page]()
mobile_navigation()
