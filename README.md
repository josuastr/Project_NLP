# 💬 PLN Chatbot Asisten

![PLN Chatbot Hero](https://github.com/josuastr/Project_NLP/blob/main/static/tampilan%20chatbot.png?raw=1)

PLN Chatbot Asisten adalah aplikasi chatbot berbasis **Artificial Intelligence (AI)** yang dirancang untuk membantu pengguna mendapatkan informasi layanan PLN secara **real-time**, khususnya terkait pemadaman listrik. Sistem ini bertujuan untuk meningkatkan efisiensi layanan pelanggan serta memberikan pengalaman interaksi yang cepat, jelas, dan informatif.

---

## 📌 Latar Belakang
Sebagai penyedia layanan kelistrikan nasional, PLN memiliki kebutuhan akan sistem layanan informasi yang responsif dan mudah diakses oleh masyarakat. Chatbot ini dikembangkan sebagai solusi digital untuk menjawab pertanyaan umum pelanggan secara otomatis, sehingga dapat mengurangi ketergantungan pada layanan manual dan mempercepat penyampaian informasi kepada pengguna.

---

## 🧠 Cara Kerja Chatbot
Pengguna dapat mengajukan pertanyaan melalui antarmuka chat berbasis web. Sistem kemudian akan memproses pertanyaan tersebut menggunakan pendekatan **Natural Language Processing (NLP)** untuk menentukan respons yang paling relevan berdasarkan informasi layanan PLN.

### Contoh Percakapan

**Bot:**  
> Halo! Saya Asisten Virtual PLN.  
> Ada yang bisa saya bantu?

**Pengguna:**  
> Informasi mati lampu hari ini

**Bot:**  
> Informasi pemadaman listrik (terencana/insidental) dapat dicek di PLN Mobile (menu Info Pemadaman) atau situs resmi PLN. Detail wilayah terdampak, jadwal mulai/selesai, dan estimasi penormalan ditampilkan di aplikasi. Untuk keadaan darurat, hubungi 123.

Percakapan di atas ditampilkan secara konsisten pada implementasi antarmuka chatbot berbasis Flask.

---

## 🤖 Pendekatan AI yang Digunakan
Chatbot ini mengadopsi pendekatan **hybrid**, yaitu:

- **Intent Classification** menggunakan model **Bidirectional Long Short Term Memory (BiLSTM)** untuk memahami maksud pertanyaan pengguna.
- **TF-IDF Retrieval** sebagai mekanisme *fallback* apabila model klasifikasi tidak mencapai tingkat kepercayaan tertentu.
- **Pesan Default** sebagai respons akhir apabila pertanyaan tidak dapat ditangani oleh kedua mekanisme tersebut.

Pendekatan ini memungkinkan chatbot tetap memberikan respons yang relevan meskipun menghadapi variasi pertanyaan pengguna.

---

## 🚀 Fitur Utama
- 💬 Layanan informasi PLN berbasis chatbot  
- ⚡ Respons cepat terkait pemadaman listrik  
- 🤖 Pemrosesan bahasa alami berbasis AI  
- 🔁 Mekanisme fallback menggunakan TF-IDF  
- 🖥️ Antarmuka web modern dan user-friendly  
- 📘 Informasi terarah ke kanal resmi PLN  

---

## 🛠️ Teknologi yang Digunakan
- **Bahasa Pemrograman**: Python  
- **Framework Backend**: Flask  
- **Model AI**: BiLSTM (Intent Classification)  
- **Metode NLP**: Tokenization, Padding, TF-IDF Retrieval  
- **Frontend**: HTML, CSS, JavaScript  
- **Desain UI**: Mockup berbasis web (Desktop)  

---

## 🎯 Tujuan Pengembangan
- Meningkatkan kualitas dan kecepatan layanan informasi PLN  
- Menyediakan akses informasi yang akurat dan mudah dipahami  
- Mengurangi beban layanan pelanggan manual  
- Menjadi studi kasus penerapan AI dan NLP dalam layanan publik  

---

## 📷 Tampilan Aplikasi
Tampilan chatbot ditunjukkan pada hero image proyek yang menampilkan simulasi percakapan layanan pelanggan PLN pada perangkat desktop, sesuai dengan skenario penggunaan nyata.

## 📄 Catatan
Proyek ini dikembangkan untuk keperluan **pembelajaran, portofolio, dan demonstrasi sistem AI**, dan **bukan merupakan sistem resmi PLN**.

---

## 📜 Lisensi
Proyek ini bersifat non-komersial dan digunakan untuk tujuan akademik serta pembelajaran.
