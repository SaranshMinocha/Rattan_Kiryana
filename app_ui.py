import streamlit as st
import requests
from datetime import datetime
import os

API_URL = os.getenv("API_URL","https://shelfsense-backend-cg19.onrender.com")

st.set_page_config(
    page_title="ShelfSense",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 1.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }

    /* Interactive button hovers & transitions */
    div.stButton > button {
        border-radius: 10px;
        font-weight: 700;
        letter-spacing: 0.3px;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid #334155;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(56, 189, 248, 0.28);
        border-color: #38bdf8 !important;
        color: #38bdf8 !important;
    }

    div.stButton > button:active {
        transform: translateY(0px);
    }

    /* Branded product showcase cards */
    .pos-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 8px;
        transition: border-color 0.2s ease;
    }

    .pos-card:hover {
        border-color: #38bdf8;
    }

    .card-category-tag {
        display: inline-block;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #38bdf8;
        background: rgba(56, 189, 248, 0.12);
        padding: 2px 7px;
        border-radius: 5px;
        margin-bottom: 6px;
    }

    .card-title {
        font-size: 18px;
        font-weight: 800;
        color: #f8fafc;
        margin: 0;
    }

    .card-meta {
        font-size: 13px;
        color: #94a3b8;
        margin-top: 4px;
    }

    .card-price {
        color: #4ade80;
        font-weight: 800;
    }

    /* Thermal receipt box */
    .bill-receipt-box {
        background: linear-gradient(145deg, #022c22, #064e3b);
        border: 2px solid #22c55e;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 0 20px rgba(34, 197, 94, 0.25);
    }
</style>
""", unsafe_allow_html=True)


# Helper functions to talk to backend
def fetch_data(endpoint):
    try:
        r = requests.get(f"{API_URL}/{endpoint}", timeout=3)
        return r.json() if r.status_code == 200 else []
    except Exception:
        return []


products = fetch_data("products")
sales = fetch_data("sales")

if not products:
    st.error("Backend offline. Run `uvicorn main:app --reload` in your terminal.")
    st.stop()

st.title("⚡ ShelfSense--Inventory Manager")

today_str = datetime.now().strftime("%Y-%m-%d")


todays_sales = [
    s for s in sales
    if s.get("SaleTimestamp", "").startswith(today_str)
]

total_revenue = sum(s.get("TotalAmount", 0) for s in todays_sales)
bills_count = len(todays_sales)
low_stock_items = [p for p in products if p.get("Stock", 0) <= 5]

m1, m2, m3 = st.columns(3)
with m1:
    st.metric(f"Today's Revenue ({today_str})", f"₹{total_revenue:,.2f}")
with m2:
    st.metric("Today's Bills Cleared", f"{bills_count} bills")
with m3:
    st.metric("Low Stock Items (≤5)", f"{len(low_stock_items)} items", delta_color="inverse")

st.divider()


tab_counter, tab_restock, tab_add, tab_register = st.tabs([
    "⚡ Billing Counter",
    "📦 Restock Shelf",
    "➕ Add New Product",
    "📜 Today's Register"
])


with tab_counter:
    categories = sorted(list({p.get("Category", "General") for p in products}))
    if "active_cat" not in st.session_state:
        st.session_state["active_cat"] = categories[0]

    # Category Bar
    cat_cols = st.columns(len(categories))
    for i, cat in enumerate(categories):
        is_active = st.session_state["active_cat"] == cat
        if cat_cols[i].button(
                f"● {cat.upper()}",
                key=f"cat_{cat}",
                type="primary" if is_active else "secondary",
                width="stretch"
        ):
            st.session_state["active_cat"] = cat
            st.session_state["active_brand"] = None
            st.session_state.pop("last_bill", None)
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    col_shelf, col_dock = st.columns([1.6, 1.0], gap="large")

    with col_shelf:
        current_cat = st.session_state["active_cat"]
        shelf_items = [p for p in products if p.get("Category", "General") == current_cat]
        brands = sorted(list({p.get("Brand") for p in shelf_items}))

        st.caption(f"SHELF: **{current_cat.upper()}** — {len(brands)} BRANDS AVAILABLE")

        GRID = 2
        for r in range(0, len(brands), GRID):
            row_cols = st.columns(GRID)
            for idx, brand in enumerate(brands[r:r + GRID]):
                variants = [p for p in shelf_items if p.get("Brand") == brand]
                min_price = min(v.get("Price", 0) for v in variants)
                total_stock = sum(v.get("Stock", 0) for v in variants)

                with row_cols[idx]:
                    st.markdown(f"""
                    <div class="pos-card">
                        <span class="card-category-tag">{current_cat}</span>
                        <div class="card-title">{brand}</div>
                        <div class="card-meta">
                            From <span class="card-price">₹{min_price}</span> • Shelf Stock: <strong>{total_stock}</strong>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    is_chosen = st.session_state.get("active_brand") == brand
                    btn_label = "SELECTED" if is_chosen else f"BILL {brand.upper()}"

                    if st.button(btn_label, key=f"btn_{brand}", type="primary" if is_chosen else "secondary",
                                 width="stretch"):
                        st.session_state["active_brand"] = brand
                        st.session_state.pop("last_bill", None)
                        st.rerun()

    with col_dock:
        if "last_bill" in st.session_state:
            b = st.session_state["last_bill"]
            st.markdown(f"""
            <div class="bill-receipt-box">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:12px; font-weight:800; color:#86efac;">RECEIPT PRINTED</span>
                    <span style="font-size:11px; color:#cbd5e1;">{b['time']}</span>
                </div>
                <div style="font-size:26px; font-weight:800; color:#ffffff; margin:6px 0;">
                    ₹{b['total']:.2f}
                </div>
                <div style="font-size:13px; color:#f1f5f9;">
                    Item: <strong>{b['brand']}</strong> ({b['size']}) × {b['qty']}
                </div>
                <div style="font-size:12px; color:#67e8f9; font-weight:700; margin-top:4px;">
                    Shelf Remaining: {b['remaining']} units
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("✕ NEXT ORDER", key="dismiss_bill_btn", width="stretch"):
                st.session_state.pop("last_bill", None)
                st.rerun()
            st.divider()

        st.markdown("### ⚡ **Counter Checkout**")
        brand = st.session_state.get("active_brand")

        if not brand:
            st.info("👈 Tap **BILL [BRAND]** on any card to prepare receipt.")
        else:
            brand_items = [p for p in shelf_items if p.get("Brand") == brand]
            st.markdown(f"Charging: **{brand}**")

            def variant_formatter(v):
                sz = f"{v.get('SizeValue', '')}{v.get('SizeUnit', '')}".strip() or "Standard"
                return f"{sz} — ₹{v['Price']} (In Stock: {v['Stock']})"

            v_lookup = {variant_formatter(v): v for v in brand_items}
            chosen_variant = st.selectbox("Pack Size / Variant", list(v_lookup.keys()))
            target = v_lookup[chosen_variant]

            stock = target.get("Stock", 0)
            price = target.get("Price", 0)

            if stock <= 0:
                st.error("❌ Out of stock!")
            else:
                q_col, tot_col = st.columns([1, 1])
                with q_col:
                    qty = st.number_input("Qty", min_value=1, max_value=int(stock), value=1, step=1)
                with tot_col:
                    total_due = price * qty
                    st.metric("Payable", f"₹{total_due}")

                if st.button("CHARGE & CUT BILL", type="primary", width="stretch"):
                    try:
                        res = requests.post(
                            f"{API_URL}/products/{target['ProductID']}/sell?quantity={qty}",
                            timeout=5
                        )
                        if res.status_code == 200:
                            st.session_state["last_bill"] = {
                                "brand": brand,
                                "size": f"{target.get('SizeValue', '')}{target.get('SizeUnit', '')}",
                                "qty": qty,
                                "total": total_due,
                                "remaining": stock - qty,
                                "time": datetime.now().strftime("%I:%M:%S %p")
                            }
                            st.rerun()
                        else:
                            st.error("Sale rejected by backend.")
                    except Exception as e:
                        st.error(f"Error: {e}")


with tab_restock:
    st.subheader("📦 Add Inward Inventory from Suppliers")

    prod_options = {
        f"{p['Brand']} ({p.get('Category', '')} {p.get('SizeValue', '')}{p.get('SizeUnit', '')}) — Shelf Stock: {p['Stock']}": p
        for p in products
    }

    selected_label = st.selectbox("Select Item to Refill:", options=list(prod_options.keys()))
    restock_target = prod_options[selected_label]

    col_inward_qty, col_inward_btn = st.columns([1, 1])
    with col_inward_qty:
        incoming_qty = st.number_input("Boxes / Packets Received", min_value=1, value=12, step=1)

    if st.button("Update Shelf Inventory", type="primary", width="stretch"):
        try:
            res = requests.post(f"{API_URL}/products/{restock_target['ProductID']}/restock?quantity={incoming_qty}")
            if res.status_code == 200:
                st.success(
                    f"Added {incoming_qty} units to {restock_target['Brand']}. New Stock: {restock_target['Stock'] + incoming_qty}")
                st.rerun()
            else:
                st.error("Failed to restock item.")
        except Exception as e:
            st.error(f"Error: {e}")


with tab_add:
    st.subheader("➕ Register New Product Line")
    with st.form("new_product_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            new_cat = st.text_input("Category (e.g., Tea, Soap, Dal, Oil)")
            new_brand = st.text_input("Brand Name (e.g., Surf Excel, Parle-G)")
            new_size_val = st.number_input("Size Value", min_value=0, value=1)
        with c2:
            new_size_unit = st.selectbox("Unit", ["g", "kg", "ml", "L", "pcs", "pack"])
            new_price = st.number_input("Selling Price (₹)", min_value=1, value=20, step=1)
            new_stock = st.number_input("Initial Shelf Stock", min_value=0, value=10, step=1)

        if st.form_submit_button("Save New Product to Database", width="stretch"):
            if not new_cat or not new_brand:
                st.warning("Category and Brand cannot be blank.")
            else:
                payload = {
                    "category": new_cat.strip().capitalize(),
                    "brand": new_brand.strip(),
                    "size_value": int(new_size_val),
                    "size_unit": new_size_unit,
                    "price": int(new_price),
                    "stock": int(new_stock)
                }
                res = requests.post(f"{API_URL}/products", json=payload)
                if res.status_code == 200:
                    st.success(f"Added {new_brand} to {new_cat}!")
                    st.rerun()
                else:
                    st.error("Failed to insert product.")


with tab_register:
    st.subheader(f"📜 Today's Sales Log ({today_str})")
    if todays_sales:
        st.dataframe(
            todays_sales,
            column_order=["SaleID", "Brand", "Category", "SizeValue", "SizeUnit", "Quantity", "TotalAmount",
                          "SaleTimestamp"],
            width="stretch",
            hide_index=True
        )
    else:
        st.info("No sales recorded yet today.")