from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

def plot_charts(df):
    fig, ax = plt.subplots()
    ticket_type_counts = df['Ticket Tipe'].value_counts()

    # Plot diagram batang
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


@app.route('/', methods=['GET', 'POST'])
def index():
    bar_chart = None
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            return "No file uploaded"

        # Baca file dengan pandas
        if file.filename.endswith('csv'):
            df = pd.read_csv(file)
            bar_chart = plot_charts(df)
        elif file.filename.endswith(('xls', 'xlsx')):
            df = pd.read_excel(file)
            bar_chart = plot_charts(df)    
        else:
            return "Unsupported file format"
    
    
    return render_template('index.html', bar_chart=bar_chart)


if __name__ == '__main__':
    app.run(debug=True)