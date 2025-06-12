import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("ascendant-timer-352404-a0a09f9e6e2a.json", scope)
client = gspread.authorize(creds)

sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Fx-4Y9O4mmcI2PbpEehipAacc3OXhgGQDUcO3KOkkI8/edit").sheet1

# Fetch product names
products = sheet.col_values(1)[1:]

st.title("📦 Product Dashboard")
st.markdown("Use this tool to update product inventory and calculate GST.")

# Two columns side-by-side
left_col, right_col = st.columns(2)

# Left: GST Reverse Calculator
with left_col:
    st.markdown("### 📊 GST Reverse Calculator")
    total_amount = st.number_input("Enter Total Amount (Including GST)", min_value=0.0, step=1.0, key="total_amount")
    gst_rate = st.selectbox("Select GST Rate (%)", [5, 12, 18, 28], key="gst_rate")

    if total_amount > 0:
        taxable_value = total_amount / (1 + gst_rate / 100)
        gst_amount = total_amount - taxable_value

        st.subheader("🧾 GST Breakdown")
        st.write(f"**Total Amount (with GST):** ₹ {total_amount:.2f}")
        st.write(f"**GST Amount ({gst_rate}%):** ₹ {gst_amount:.2f}")
        st.write(f"**Taxable Value (without GST):** ₹ {taxable_value:.2f}")

# Right: Product Entry Interface
with right_col:
    st.markdown("### 📝 Product Entry")
    selected_product = st.selectbox("Select Product", products)
    quantity = st.number_input("Add Quantity", min_value=0, step=1)
    cgst = st.number_input("CGST (%)", min_value=0.0, step=0.1)
    sgst = st.number_input("SGST (%)", min_value=0.0, step=0.1)
    price_wo_tax = st.number_input("Price Without Tax", min_value=0.0, step=0.1)
    price_w_tax = st.number_input("Price With Tax", min_value=0.0, step=0.1)

    if st.button("✅ Update Product"):
        try:
            cell = sheet.find(selected_product)
            row = cell.row

            existing_qty = sheet.cell(row, 2).value
            existing_qty = int(existing_qty) if existing_qty else 0
            new_qty = existing_qty + quantity

            sheet.update_cell(row, 2, new_qty)
            sheet.update_cell(row, 3, cgst)
            sheet.update_cell(row, 4, sgst)
            sheet.update_cell(row, 5, price_wo_tax)
            sheet.update_cell(row, 6, price_w_tax)

            st.success(f"✅ {selected_product} updated successfully!")
        except Exception as e:
            st.error(f"❌ Error: {e}")
