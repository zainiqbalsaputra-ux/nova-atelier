import streamlit as st
from utils.store import cart_count, navigate, rupiah

BRAND = {"name": "NOVA ATELIER", "tagline": "Pakaian sehari-hari dengan bentuk yang sederhana dan nyaman dipakai."}

def inject_css():
    st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
.stApp{background:#f5f5f5;color:#222;font-family:'DM Sans',sans-serif}#MainMenu,footer,header{visibility:hidden}.block-container{max-width:1360px;padding:.4rem 4.5vw 4rem}h1,h2,h3{font-family:'DM Sans',sans-serif!important;letter-spacing:-.02em}h1{font-size:1.7rem!important;line-height:1.2}.eyebrow{font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;color:#777;font-weight:600}.muted{color:#666}.brand{font-weight:700;font-size:1.1rem;letter-spacing:.12em;white-space:nowrap;color:#d8602b}.topline,.line{height:1px;background:#e5e5e5;margin:.8rem 0}.promo{background:#fff3ed;color:#b34a20;text-align:center;padding:.5rem;font-size:.76rem;margin:0 -4.5vw .7rem}.hero-copy{padding:1.8rem 1.8rem}.hero-copy h1{margin:.25rem 0 .65rem;font-size:2rem!important}.hero-copy p{line-height:1.55;color:#666}.hero-image img{height:255px!important;object-fit:cover}.product-image img{height:255px!important;object-fit:cover;background:#eee}.product-name{font-weight:500;margin-top:.55rem;line-height:1.35;height:2.7em;overflow:hidden}.product-meta{font-size:.72rem;color:#777;margin-top:.18rem}.product-price{font-weight:700;color:#d35420;margin-top:.35rem}.old-price{font-size:.72rem;color:#999;text-decoration:line-through}.discount{font-size:.7rem;color:#d35420;margin-left:.35rem}.label{font-size:.62rem;background:#e85b28;color:#fff;padding:.2rem .35rem;display:inline-block;margin-top:.45rem}.summary{background:#fff;border:1px solid #e5e5e5;padding:1.15rem}.empty{text-align:center;padding:3rem 1rem;background:#fff;border:1px solid #e5e5e5}.footer{font-size:.78rem;color:#666;padding:1.4rem 0 0}.timeline{border-left:1px solid #ccc;padding:0 0 1.1rem 1.25rem;margin-left:.5rem;position:relative}.timeline:before{content:'✓';position:absolute;left:-.53rem;top:0;width:1rem;height:1rem;border-radius:50%;background:#e05b27;color:#fff;text-align:center;font-size:.65rem;line-height:1rem}.pending:before{content:'○';background:#f5f5f5;color:#777;font-size:.95rem;line-height:.88rem}.stButton>button[kind="primary"]{background:#e05b27;border:1px solid #e05b27;border-radius:3px;color:#fff;font-size:.8rem;font-weight:600;padding:.58rem .9rem}.stButton>button[kind="tertiary"]{color:#444;padding:.28rem .1rem;border-radius:0;font-size:.8rem;font-weight:500}.stButton>button[kind="tertiary"]:hover{color:#d35420}.stTextInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"]>div{background:#fff!important;border-radius:4px!important;border-color:#ddd!important}.stTextInput input{padding:.55rem!important}.market-banner{background:#fff1e8;border:1px solid #f1d5c7;padding:1.8rem 2rem;height:255px}.category-icon{height:46px;width:46px;border-radius:50%;background:#fff1e8;color:#d35420;display:flex;align-items:center;justify-content:center;font-weight:700;margin:auto}.category-name{text-align:center;font-size:.75rem;margin-top:.4rem}.bottom-nav{display:none}@media(max-width:780px){.block-container{padding:.4rem .8rem 5.2rem}.promo{margin-left:-.8rem;margin-right:-.8rem}.hero-copy{padding:1.3rem}.hero-copy h1{font-size:1.55rem!important}.hero-image img{height:185px!important}.product-image img{height:190px!important}.brand{font-size:.9rem}.bottom-nav{display:block;position:fixed;z-index:1000;bottom:0;left:0;right:0;background:#fff;border-top:1px solid #ddd;padding:.5rem .4rem}.bottom-nav div{text-align:center;font-size:.65rem;color:#666}.bottom-nav b{display:block;color:#d35420;font-size:1rem;line-height:1.15}}
/* Mobile-only layout repairs: keep commerce content compact and horizontal. */
.category-rail{display:flex;gap:.75rem;overflow-x:auto;padding:.25rem 0 .45rem;scrollbar-width:none}.category-rail::-webkit-scrollbar{display:none}.category-shortcut{flex:0 0 64px;text-align:center;color:#333}
@media(max-width:780px){
 .block-container{padding:.35rem .7rem 5.7rem}.promo{margin-left:-.7rem;margin-right:-.7rem}.hero-copy{padding:1.1rem}.hero-copy h1{font-size:1.45rem!important}.hero-image img{height:170px!important}.market-banner{height:170px;padding:1.1rem}.market-banner h1{font-size:1.35rem!important;margin:.25rem 0}.market-banner p{font-size:.8rem;margin:.25rem 0 .55rem}.product-image img{height:180px!important}.product-name{font-size:.82rem}.product-meta{font-size:.65rem}.product-price{font-size:.88rem}.old-price,.discount{font-size:.64rem}
 .st-key-site-header [data-testid="stHorizontalBlock"]{flex-wrap:nowrap!important;gap:.35rem!important;align-items:center}.st-key-site-header [data-testid="stHorizontalBlock"]>div{min-width:0!important}.st-key-site-header [data-testid="stHorizontalBlock"]>div:nth-child(1){flex:0 0 82px!important}.st-key-site-header [data-testid="stHorizontalBlock"]>div:nth-child(2){flex:1 1 auto!important}.st-key-site-header [data-testid="stHorizontalBlock"]>div:nth-child(5){flex:0 0 28px!important}.st-key-site-header .st-key-nav_help,.st-key-site-header .st-key-nav_order{display:none}.st-key-site-header .st-key-nav_cart button{padding:0!important;white-space:nowrap!important}
 .st-key-home-hero [data-testid="stHorizontalBlock"]>div:nth-child(2){display:none!important}.st-key-home-hero .stButton>button{width:100%;margin-top:.45rem}
 div[class*="st-key-home-grid"] [data-testid="stHorizontalBlock"],.st-key-catalog-grid [data-testid="stHorizontalBlock"]{flex-wrap:wrap!important;gap:.55rem!important}div[class*="st-key-home-grid"] [data-testid="stHorizontalBlock"]>div,.st-key-catalog-grid [data-testid="stHorizontalBlock"]>div{flex:0 0 calc(50% - .28rem)!important;width:calc(50% - .28rem)!important;min-width:0!important}
 .bottom-nav{display:block;position:fixed;z-index:1000;bottom:0;left:0;width:100vw;box-sizing:border-box;background:#fff;border-top:1px solid #ddd;padding:.5rem .25rem env(safe-area-inset-bottom)}.bottom-nav div{box-sizing:border-box;text-align:center;font-size:.62rem;color:#666;min-width:0}.bottom-nav b{display:block;color:#d35420;font-size:.95rem;line-height:1.15}.footer{padding-bottom:.4rem}
}
</style>""", unsafe_allow_html=True)

def navigation():
    with st.container(key="site-header"):
        brand, search, help_col, order, cart = st.columns([1.4,4.2,.85,.85,1.1])
        with brand: st.markdown(f'<div class="brand">{BRAND["name"]}</div>', unsafe_allow_html=True)
        with search:
            term=st.text_input("Pencarian",placeholder="Cari produk, kategori, atau brand...",label_visibility="collapsed",key="global_search")
            if term:
                st.session_state.catalog_query=term; navigate("Koleksi")
        with help_col:
            if st.button("Bantuan",key="nav_help",type="tertiary"): navigate("Bantuan")
        with order:
            if st.button("Pesanan",key="nav_order",type="tertiary"): navigate("Status")
        with cart:
            if st.button("🛒",key="nav_cart",type="tertiary",help=f"Keranjang ({cart_count()})"): navigate("Keranjang")
    st.markdown('<div class="topline"></div>',unsafe_allow_html=True)

def product_card(product, key):
    st.markdown('<div class="product-image">',unsafe_allow_html=True); st.image(product["image"],use_container_width=True); st.markdown('</div>',unsafe_allow_html=True)
    if product["label"]: st.markdown(f'<span class="label">{product["label"]}</span>',unsafe_allow_html=True)
    original=round(product["price"]*1.15/1000)*1000
    st.markdown(f'<div class="product-name">{product["name"]}</div><div class="product-meta">★ {product["rating"]} · {product["stock"]*17} terjual</div><div class="product-price">{rupiah(product["price"])}</div><span class="old-price">{rupiah(original)}</span><span class="discount">-13%</span><div class="product-meta">Jakarta</div>',unsafe_allow_html=True)
    if st.button("Lihat detail",key=f"{key}_{product['id']}",type="tertiary"): navigate("Produk",product["id"])

def footer():
    st.markdown(f'<div class="footer"><div class="line" style="margin-top:2.5rem"></div><b>{BRAND["name"]}</b><br>{BRAND["tagline"]}<br><br>Tentang Kami &nbsp; · &nbsp; Koleksi &nbsp; · &nbsp; Bantuan &nbsp; · &nbsp; Kebijakan Pengiriman &nbsp; · &nbsp; Kebijakan Pengembalian<br><br>© 2026 {BRAND["name"]}</div>',unsafe_allow_html=True)

def mobile_navigation():
    st.markdown('<div class="bottom-nav"><div style="display:flex;justify-content:space-around"><div><b>⌂</b>Beranda</div><div><b>▦</b>Kategori</div><div><b>□</b>Pesanan</div><div><b>🛒</b>Keranjang</div><div><b>◯</b>Akun</div></div></div>',unsafe_allow_html=True)
