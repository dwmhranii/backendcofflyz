import os
import numpy as np
from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

app = Flask(__name__)

# Memuat model dari file .h5
model = load_model('model/Cendekia-pest-81.11.h5')

# Fungsi untuk memproses gambar dan menyesuaikan dengan input model
def prepare_image(image_path):
    img = Image.open(image_path)  # Membuka gambar
    img = img.resize((299, 299))  # Ubah ukuran menjadi 299x299 untuk model
    img_array = np.array(img)  # Mengubah gambar menjadi array numpy
    img_array = np.expand_dims(img_array, axis=0)  # Menambahkan dimensi batch
    img_array = img_array / 255.0  # Normalisasi jika diperlukan
    return img_array

# Fungsi untuk prediksi penyakit tanaman kopi
def predict_disease(image_path):
    img_array = prepare_image(image_path)
    prediction = model.predict(img_array)  # Melakukan prediksi
    predicted_class = np.argmax(prediction, axis=1)  # Kelas dengan skor tertinggi
    confidence = np.max(prediction)  # Skor tingkat kepercayaan tertinggi

    # Menentukan nama kelas penyakit
    class_names = ['healthy', 'phoma', 'rust']
    predicted_class_name = class_names[predicted_class[0]]

    # Deskripsi untuk setiap kelas
    class_descriptions = {
        'rust': """Ciri-ciri penyakit Rust pada daun kopi:
                    - Bercak berwarna kuning pucat hingga oranye cerah
                    - Bercak dapat berukuran kecil hingga besar, terlihat seperti karat pada permukaan daun
                    - Penyakit ini menyebabkan daun menguning dan kering jika tidak ditangani""",
        'phoma': """Ciri-ciri penyakit Phoma pada daun kopi:
                    - Bintik-bintik coklat atau kehitaman dengan batas yang jelas
                    - Bintik bisa berukuran kecil hingga sedang
                    - Pada beberapa kasus, daun juga menguning di sekitar bintik""",
        'healthy': """Ciri-ciri daun kopi yang sehat:
                      - Warna hijau cerah dan daun memiliki tekstur halus
                      - Tidak ada bercak atau perubahan warna pada permukaan daun
                      - Daun sehat menunjukkan pertumbuhan yang baik dan kuat"""
    }

    disease_description = class_descriptions.get(predicted_class_name, "Deskripsi tidak ditemukan")

    return predicted_class_name, confidence, disease_description

# Halaman utama (form upload gambar)
@app.route('/')
def index():
    return render_template('index.html')

# Menangani upload gambar dan melakukan prediksi
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    # Simpan file gambar sementara
    file_path = os.path.join('static', file.filename)
    file.save(file_path)
    
    try:
        # Lakukan prediksi
        predicted_class, confidence, disease_description = predict_disease(file_path)
        
        # Kembalikan hasil prediksi, convert predicted_class to native string
        return jsonify({
            'predicted_class': predicted_class,  # Nama kelas penyakit
            'confidence': float(confidence),  # Tingkat kepercayaan
            'disease_description': disease_description,  # Deskripsi penyakit
            'image_url': file_path  # URL gambar yang diunggah
        })
    except Exception as e:
        # Tangani error saat prediksi
        print(f"Error during prediction: {e}")
        return jsonify({'error': 'Error during prediction'})

if __name__ == '__main__':
    app.run(debug=True)
