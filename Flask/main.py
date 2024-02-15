from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

def plot_bar_chart(df):
    fig, ax = plt.subplots()
    ticket_type_counts = df['Ticket Tipe'].value_counts()
    # Plot diagram batang
    ax.set_title('Ticket Type Distribution (Bar Chart)')
    ticket_type_counts.plot.bar()
    # Tambahkan nilai di atas setiap batang
    for i, count in enumerate(ticket_type_counts):
        ax.text(i, count + 0.1, str(count), ha='center')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return graphic

def plot_pie_chart(df):
    fig, ax = plt.subplots()
    ticket_type_counts = df['Ticket Tipe'].value_counts()
    pie_data = ticket_type_counts.plot.pie(ax=ax, autopct=None, startangle=90, shadow=True, labels=None)
    ax.set_title('Ticket Type Distribution (Pie Chart)')
    ax.set_ylabel('')
    ax.set_xlabel('')
    plt.tight_layout()
    labels = [f"{label} ({percentage})" for label, percentage in zip(ticket_type_counts.index, ticket_type_counts.values)]
    
    # Set legend
    plt.legend(labels, loc="best")
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return graphic

@app.route('/', methods=['GET', 'POST'])
def index():
    bar_chart = None
    pie_chart = None
    # df_table = None  # Initialize df_table here
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            return "No file uploaded"

        # Baca file dengan pandas
        if file.filename.endswith('csv'):
            df = pd.read_csv(file)
            # df_table = df.to_html(classes='data', header="true")
            bar_chart = plot_bar_chart(df)
            pie_chart = plot_pie_chart(df)
        elif file.filename.endswith(('xls', 'xlsx')):
            df = pd.read_excel(file)
            # df_table = df.to_html(classes='data', header="true")
            bar_chart = plot_bar_chart(df)
            pie_chart = plot_pie_chart(df)    
        else:
            return "Unsupported file format"
    
    return render_template('index.html', bar_chart=bar_chart, pie_chart=pie_chart)



if __name__ == '__main__':
    app.run(debug=True)
