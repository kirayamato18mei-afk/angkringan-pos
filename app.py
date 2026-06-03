import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(layout="wide")
st.title("🍱 Angkringan Pro-POS")

# Load data
df_m = pd.read_csv('data_menu.csv')
df_t = pd.read_csv('data_transaksi.csv')

menu = st.sidebar.radio("Navigasi:", ["Kasir", "Laporan", "Stok"])

if menu == "Kasir":
    st.subheader("🛒 Kasir")
    produk = st.selectbox("Menu", df_m['Nama'].tolist())
    qty = st.number_input("Jumlah", 1, 99)
    if st.button("Bayar"):
        idx = df_m[df_m['Nama'] == produk].index[0]
        df_m.at[idx, 'Stok'] -= qty
        new_row = {'Tanggal': datetime.now().strftime('%Y-%m-%d'), 'Nama': produk, 'Qty': qty, 
                   'TotalJual': qty*df_m.at[idx, 'HargaJual'], 'TotalModal': qty*df_m.at[idx, 'HargaModal']}
        df_t = pd.concat([df_t, pd.DataFrame([new_row])])
        df_t.to_csv('data_transaksi.csv', index=False)
        df_m.to_csv('data_menu.csv', index=False)
        st.success("Transaksi Sukses!")

elif menu == "Laporan":
    st.subheader("📊 Laporan")
    st.dataframe(df_t)
    st.metric("Keuntungan", f"Rp {(df_t['TotalJual'] - df_t['TotalModal']).sum():,}")

elif menu == "Stok":
    st.subheader("📦 Stok")
    st.dataframe(df_m)
