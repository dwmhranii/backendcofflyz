document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    let formData = new FormData();
    formData.append('file', document.getElementById('image').files[0]);

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Mengecek apakah prediksi berhasil
        if (data.predicted_class !== undefined) {
            // Menampilkan hasil prediksi
            document.getElementById('prediction').textContent = `Prediksi Penyakit: ${data.predicted_class}`;
            document.getElementById('confidence').textContent = `Tingkat Kepercayaan: ${data.confidence.toFixed(2)}%`;

            // Menampilkan deskripsi penyakit
            document.getElementById('disease-description').textContent = `Deskripsi: ${data.disease_description}`;

            // Menampilkan gambar yang diunggah
            const uploadedImage = document.getElementById('uploaded-image');
            uploadedImage.src = data.image_url;  // Mengatur sumber gambar yang diunggah
            uploadedImage.style.display = 'block';  // Menampilkan gambar
        } else {
            // Menangani kasus kesalahan
            document.getElementById('prediction').textContent = 'Terjadi kesalahan saat memproses gambar.';
            document.getElementById('confidence').textContent = '';
            document.getElementById('disease-description').textContent = '';  // Kosongkan deskripsi
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('prediction').textContent = 'Terjadi kesalahan.';
        document.getElementById('confidence').textContent = '';
        document.getElementById('disease-description').textContent = '';  // Kosongkan deskripsi
    });
});
