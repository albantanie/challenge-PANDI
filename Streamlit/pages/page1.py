import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Membuat dataframe dengan data spam
data = {
    'Kategori': ['Pembayaran Pendaftaran dan Perpanjangan nama domain', 'Notifikasi', 'Abuse', 'Insiden', 'Business Strategic', 'Call', 'Deposit'],
    'Frekuensi': [100, 80, 50, 30, 70, 60, 40]  # Angka ini bisa diganti dengan data sesungguhnya
}

df = pd.DataFrame(data)

# Memilih jenis visualisasi
jenis_visualisasi = st.sidebar.selectbox(
    'Pilih Jenis Visualisasi:',
    ('Diagram Batang', 'Diagram Lingkaran')
)

# Menampilkan visualisasi sesuai pilihan
if jenis_visualisasi == 'Diagram Batang':
    st.write("### Diagram Batang Frekuensi Spam")
    plt.figure(figsize=(10, 6))
    plt.bar(df['Kategori'], df['Frekuensi'])
    plt.xlabel('Kategori')
    plt.ylabel('Frekuensi')
    plt.xticks(rotation=45)
    st.pyplot()

elif jenis_visualisasi == 'Diagram Lingkaran':
    st.write("### Diagram Lingkaran Frekuensi Spam")
    plt.figure(figsize=(8, 8))
    plt.pie(df['Frekuensi'], labels=df['Kategori'], autopct='%1.1f%%')
    plt.axis('equal')
    st.pyplot()

# Menampilkan data dalam bentuk tabel
st.write("### Data Spam")
st.dataframe(df)
