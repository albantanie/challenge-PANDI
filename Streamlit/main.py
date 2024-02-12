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

        option = st.selectbox(
        'Select Column',
        (df.columns))

        st.bar_chart(df[option].value_counts())

        fileter_unique = st.multiselect(
            'Select filter',
            df[option].unique(),
            [])
        
        df_filtered = df[df[option].isin(fileter_unique)]
        st.write(df_filtered)

    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {str(e)}")

