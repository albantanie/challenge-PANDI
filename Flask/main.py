from flask import Flask, render_template, request, send_file
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if not file:
        return "No file uploaded"

    # Baca file dengan pandas
    if file.filename.endswith('csv'):
        df = pd.read_csv(file)
    elif file.filename.endswith(('xls', 'xlsx')):
        df = pd.read_excel(file)    
    else:
        return "Unsupported file format"

    # Visualisasi data
    plt.figure(figsize=(8,6))
    df['Ticket Tipe'].value_counts().plot.bar()
    plt.title('Pie Chart Ticket Tipe')
    plt.axis('equal')

    # Simpan gambar sebagai objek byte
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Hapus plot dari memori
    plt.clf()
    plt.close()

    # Tampilkan gambar di halaman web
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
