from datetime import datetime
import random
import streamlit as st

PROMOS = {"NOVA10": .10, "WELCOME15": .15}

def rupiah(value): return f"Rp {value:,.0f}".replace(",", ".")
def initialize_state():
    for key, value in {"page":"Beranda","cart":[],"promo":None,"selected_product":None,"order":None}.items(): st.session_state.setdefault(key, value)
def navigate(page, product_id=None):
    st.session_state.page = page
    if product_id: st.session_state.selected_product = product_id
    st.rerun()
def cart_count(): return sum(item["quantity"] for item in st.session_state.cart)
def order_totals(items=None):
    items = items if items is not None else st.session_state.cart
    subtotal = sum(item["price"] * item["quantity"] for item in items); discount = round(subtotal * PROMOS.get(st.session_state.promo, 0)); shipping = 25000 if subtotal and subtotal-discount < 500000 else 0
    return {"subtotal":subtotal,"discount":discount,"shipping":shipping,"total":subtotal-discount+shipping}
def add_item(product, size, color, quantity):
    for item in st.session_state.cart:
        if item["id"] == product["id"] and item["size"] == size and item["color"] == color:
            item["quantity"] = min(item["quantity"] + quantity, product["stock"]); return
    st.session_state.cart.append({key:product[key] for key in ("id","name","image","price","stock")} | {"size":size,"color":color,"quantity":quantity})
def create_order(customer, payment):
    order = {"id":f"NVA-{datetime.now():%Y%m%d}-{random.randint(100,999)}","date":datetime.now().strftime("%d %B %Y"),"customer":customer,"payment":payment,"items":[item.copy() for item in st.session_state.cart],**order_totals()}
    st.session_state.order=order; st.session_state.cart=[]; st.session_state.promo=None
    return order
