import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# Judul aplikasi
st.title('Impor Data dari CSV atau XLS')

# Unggah file CSV atau XLS
file = st.file_uploader("Unggah file", type=['csv', 'xls', 'xlsx'])

if file is not None:
    try:
        # Baca file dengan pandas
        if file.name.endswith('csv'):
            df = pd.read_csv(file)
        elif file.name.endswith(('xls', 'xlsx')):
            df = pd.read_excel(file)
        else:
            st.error("Format file tidak didukung.")
            st.stop()
        st.write(df)
        st.bar_chart(df['Ticket Tipe'].value_counts())
        fig, ax = plt.subplots()
        df['Ticket Tipe'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
        st.pyplot(fig)

        options = st.multiselect(
            'What are your favorite colors',
            df['Ticket Tipe'].unique(),
            [])
        df_filtered = df[df['Ticket Tipe'].isin(options)]
        st.write(df_filtered)
        fig, ax = plt.subplots()
        df_filtered['Ticket Tipe'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
        st.pyplot(fig)


    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {str(e)}")

