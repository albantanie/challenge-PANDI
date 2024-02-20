from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

def plot_bar_chart(df):
    fig, ax = plt.subplots()
    ticket_type_counts = df.value_counts()
    ax.set_title('Distribution (Bar Chart)')
    ticket_type_counts.plot.bar()
    for i, count in enumerate(ticket_type_counts):
        ax.text(i, count + 0.1, str(count), ha='center')
    buffer = BytesIO()
    plt.savefig(buffer, format='png', transparent=True)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return graphic

def plot_pie_chart(df):
    fig, ax = plt.subplots()
    ticket_type_counts = df.value_counts()
    pie_data = ticket_type_counts.plot.pie(ax=ax, autopct=None, startangle=90, shadow=True, labels=None)
    ax.set_title('Distribution (Pie Chart)')
    ax.set_ylabel('')
    ax.set_xlabel('')
    plt.tight_layout()
    labels = [f"{label} ({percentage})" for label, percentage in zip(ticket_type_counts.index, ticket_type_counts.values)]
    plt.legend(labels, loc="best")
    buffer = BytesIO()
    plt.savefig(buffer, format='png', transparent=True)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return graphic

@app.route('/', methods=['GET'])

def index():
    return render_template('index.html')

@app.route('/dashboard', methods=['POST'])

def dashboard():
    if 'file' not in request.files:
        return "No file uploaded"
    
    file = request.files['file']
    if not file:
        return "No file uploaded"
    
    if file.filename.endswith('csv'):
        df = pd.read_csv(file)
    elif file.filename.endswith(('xls', 'xlsx')):
        df = pd.read_excel(file)
    else:
        return "Unsupported file format"
    
    bar_chart = plot_bar_chart(df['Ticket Tipe'])
    pie_chart = plot_pie_chart(df['Ticket Tipe'])
    pie_chart2 = plot_pie_chart(df['Status'])
    pie_chart3 = plot_pie_chart(df['Source'])
    pie_chart4 = plot_pie_chart(df['Responsible'])

    return render_template('dashboard.html', bar_chart=bar_chart, pie_chart=pie_chart, pie_chart2=pie_chart2, pie_chart3=pie_chart3, pie_chart4=pie_chart4)

if __name__ == '__main__':
    app.run(debug=True)
