import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page to fullscreen
st.set_page_config("Streamlit Components Hub", "🎪", layout="wide")
file = st.file_uploader("Unggah file", type=['csv', 'xls', 'xlsx'])

if file is not None:
    try:
        # Read file using pandas
        if file.name.endswith('csv'):
            df = pd.read_csv(file)
        elif file.name.endswith(('xls', 'xlsx')):
            df = pd.read_excel(file)
        else:
            st.error("Format file tidak didukung.")
            st.stop()

        df['Created'] = pd.to_datetime(df['Created'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
        filter_unique = st.multiselect(
                'Select filter',
                df['Ticket Tipe'].unique(),
                df['Ticket Tipe'].unique())
        df_filtered = df[df['Ticket Tipe'].isin(filter_unique)]
        st.write(df_filtered)
        
        col6, col7 = st.columns([2,2])
        with col6:
            st.bar_chart(df['Ticket Tipe'].value_counts())
        
        with col7:
            ticket_counts = df.groupby([df['Created'].dt.date, 'Ticket Tipe']).size().unstack(fill_value=0)
            st.line_chart(ticket_counts, use_container_width=True)

        col1, col2, col3, col4 = st.columns([1,1,1,1])        
        with col1:
            # Pie Chart with transparent background
            df_filtered = df[df['Ticket Tipe'].isin(filter_unique)]
            fig, ax = plt.subplots()
            ticket_type_counts = df_filtered['Ticket Tipe'].value_counts()
            pie_data = ticket_type_counts.plot.pie(ax=ax, autopct=None, startangle=90, shadow=True, labels=None)
            ax.set_title('Distribution (Pie Chart)')
            ax.set_ylabel('')
            ax.set_xlabel('')
            plt.tight_layout()
            labels = [f"{label} ({percentage})" for label, percentage in zip(ticket_type_counts.index, ticket_type_counts.values)]
            plt.legend(labels, loc="best")
            # Set the background color to transparent
            fig.patch.set_alpha(0)
            plt.setp(pie_data, alpha=0.7)  # Adjust transparency of pie chart patches
            st.pyplot(fig)
        
        with col2:    
            # Pie Chart with transparent background
            df_filtered = df[df['Ticket Tipe'].isin(filter_unique)]
            fig, ax = plt.subplots()
            ticket_type_counts = df_filtered['Status'].value_counts()
            pie_data = ticket_type_counts.plot.pie(ax=ax, autopct=None, startangle=90, shadow=True, labels=None)
            ax.set_title('Distribution (Pie Chart)')
            ax.set_ylabel('')
            ax.set_xlabel('')
            plt.tight_layout()
            labels = [f"{label} ({percentage})" for label, percentage in zip(ticket_type_counts.index, ticket_type_counts.values)]
            plt.legend(labels, loc="best")
            # Set the background color to transparent
            fig.patch.set_alpha(0)
            plt.setp(pie_data, alpha=0.7)  # Adjust transparency of pie chart patches
            st.pyplot(fig)
        
        with col3:    
            # Pie Chart with transparent background
            df_filtered = df[df['Ticket Tipe'].isin(filter_unique)]
            fig, ax = plt.subplots()
            ticket_type_counts = df_filtered['Source'].value_counts()
            pie_data = ticket_type_counts.plot.pie(ax=ax, autopct=None, startangle=90, shadow=True, labels=None)
            ax.set_title('Distribution (Pie Chart)')
            ax.set_ylabel('')
            ax.set_xlabel('')
            plt.tight_layout()
            labels = [f"{label} ({percentage})" for label, percentage in zip(ticket_type_counts.index, ticket_type_counts.values)]
            plt.legend(labels, loc="best")
            # Set the background color to transparent
            fig.patch.set_alpha(0)
            plt.setp(pie_data, alpha=0.7)  # Adjust transparency of pie chart patches
            st.pyplot(fig)
        
        with col4:    
            # Pie Chart with transparent background
            df_filtered = df[df['Ticket Tipe'].isin(filter_unique)]
            fig, ax = plt.subplots()
            ticket_type_counts = df_filtered['Responsible'].value_counts()
            pie_data = ticket_type_counts.plot.pie(ax=ax, autopct=None, startangle=90, shadow=True, labels=None)
            ax.set_title('Distribution (Pie Chart)')
            ax.set_ylabel('')
            ax.set_xlabel('')
            plt.tight_layout()
            labels = [f"{label} ({percentage})" for label, percentage in zip(ticket_type_counts.index, ticket_type_counts.values)]
            plt.legend(labels, loc="best")
            # Set the background color to transparent
            fig.patch.set_alpha(0)
            plt.setp(pie_data, alpha=0.7)  # Adjust transparency of pie chart patches
            st.pyplot(fig)
            
            

    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {str(e)}")
