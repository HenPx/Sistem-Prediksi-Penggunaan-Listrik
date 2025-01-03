import streamlit as st
import pandas as pd
from utils.prophet_model import prepare_prophet_data, predict_future
from utils.visualizer import visualize_forecast, plot_forecast_with_capacity, plot_stacked_chart, plot_data_per_year
from components.option_menu import create_option_menu
import plotly.express as px
import folium
from streamlit_folium import st_folium
import streamlit_authenticator as stauth
import streamlit as st
import yaml
from yaml.loader import SafeLoader
import os

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

    
# Fungsi untuk memuat data default
def load_default_data():
    try:
        return pd.read_csv('BP_2024.csv')
    except FileNotFoundError:
        st.error("Data default 'BP_2024.csv' tidak ditemukan.")
        return None

# Fungsi untuk menyimpan data ke file CSV
def save_data(data, filename="Save_Data.csv"):
    data.to_csv(filename, index=False)
    st.success(f"Data berhasil diupload. Silahkan refresh website dan pilih data yang digunakan pada sidebar.")
# Judul utama aplikasi
st.markdown(
    """
    <h1 style="text-align: center; color: #fffff; font-size:30px;">SiPRELIS | Sistem Prediksi Penggunaan Listrik</h1>

    
    """, 
    unsafe_allow_html=True
)
col1, col2, col3 = st.columns([2,1,2])

with col1:
    st.write("")

with col2:
    st.image("images/logo_App.png", width=100)

with col3:
    st.write("")


st.markdown("---")

def main():
    # Sidebar menu
    with st.sidebar:
        selected = create_option_menu()


    # Inisialisasi session state untuk data jika belum ada
    if 'data' not in st.session_state:
        st.session_state['data'] = load_default_data()

    # Pilihan untuk menggunakan data default atau yang sudah disimpan
    data_option = st.sidebar.selectbox(
        "Pilih data yang ingin digunakan:",
        ["Data Default", "Data Upload"]
    )

    # Memuat dataset sesuai pilihan pengguna
    if data_option == "Data Default":
        st.session_state['data'] = load_default_data()
    elif data_option == "Data Upload":
        try:
            st.session_state['data'] = pd.read_csv("Save_Data.csv")
        except FileNotFoundError:
            st.error("Belum ada data yang di upload. Silahkan upload pada menu Beranda.")
    
    with st.sidebar:
        if os.path.exists('Save_Data.csv'):
            st.info("Sebelum keluar dari website, silahkan hapus data pribadi terlebih dahulu.")

            if st.button("Hapus Data Pribadi"):

                os.remove('Save_Data.csv')
                st.success("Data pribadi telah dihapus. Silahkan refresh ulang website.")
        else:
            authenticator.logout('Logout', 'sidebar')
            
        footer_html = """<div style='text-align: center;'>
        <p>© 2025 SiPRELIS. All rights reserved.</p>
        </div>"""
        st.markdown(footer_html, unsafe_allow_html=True)



    # Beranda
    if selected == "Beranda":
        st.header("Selamat Datang! 👋🏻")
        st.write("Aplikasi ini dirancang untuk membantu Anda menganalisis data beban penggunaan listrik dan memprediksi tren yang akan datang. Dengan wawasan yang tepat, Anda dapat mengambil keputusan yang lebih baik dalam pengelolaan sumber daya listrik.")
        st.write("Kami berharap aplikasi ini akan memberikan informasi yang berguna dan mendukung Anda dalam merencanakan kebutuhan energi yang lebih efisien. Selamat menggunakan aplikasi ini!")
        st.subheader("Data yang digunakan per hari ini di Nusa Penida:  📊")

        # Tampilkan data default atau yang telah diunggah pengguna
        if st.session_state['data'] is not None:
            st.write("Saat ini, kami menampilkan data yang anda gunakan pada sidebar. Jika Anda ingin mengeksplorasi data lainnya, jangan ragu untuk mengunggah (upload) file di bawah ini.")
            st.dataframe(st.session_state['data'])
        else:
            st.error("Tidak ada data yang tersedia.")

        # Unggah file untuk mengganti data
        st.header("Anda ingin menggunakan data pribadi?")
        st.subheader("Cek ketentuan datanya dulu, yuk! 📋")
        st.markdown(
            """
            <ul>
                <li><strong>Kolom 1:</strong> Tanggal dengan format <em>dd-mm-yyyy</em>, pastikan untuk mengikuti format ini agar data dapat diproses dengan benar.</li>
                <li><strong>Kolom 2:</strong> Beban Puncak (BP) merupakan total penggunaan listrik terbesar per-harinya dalam kilo watt (kW). Ditulis dengan format numerik/angka, harap masukkan angka tanpa simbol atau karakter lain.</li>
                <li><strong>Penting:</strong> Semakin banyak data historis, semakin baik prediksi kedepannya. Untuk menghasilkan prediksi yang maksimal, minimal memiliki data 2 tahun.</li>
            </ul>
            """,
            unsafe_allow_html=True
        )
        uploaded_file = st.file_uploader("Upload data Anda (format CSV)", type="csv")
        if uploaded_file is not None:
            # Load data dari file yang diunggah
            st.session_state['data'] = pd.read_csv(uploaded_file)
            st.write("Berikut adalah data yang Anda upload:")
            st.dataframe(st.session_state['data'])

            # Tombol untuk menyimpan data
            if st.button("Simpan Data"):
                save_data(st.session_state['data'])
        
        
                
        st.subheader("Lokasi Data Default📍")
        
        # Koordinat Nusa Penida
        nusa_penida_coords = [-8.675239286389026, 115.55320582997335]

        # Membuat peta dengan folium
        map_nusa_penida = folium.Map(location=nusa_penida_coords, zoom_start=12)

        # Link ke Google Maps
        google_maps_link = "https://maps.app.goo.gl/Zuq9yziHAMmnzHGh6"

        # Tambahkan marker dengan link ke Google Maps di popup
        folium.Marker(
            nusa_penida_coords,
            popup=f'<a href="{google_maps_link}" target="_blank">SiPRELIS</a>',
            icon=folium.Icon(color="red")
        ).add_to(map_nusa_penida)

        # Tampilkan peta di Streamlit
        st_folium(map_nusa_penida, width=700, height=500)


    # Analysis Page
    elif selected == "Analysis":
        if st.session_state['data'] is None:
            st.error("Tidak ada data yang tersedia untuk dianalisis. Silakan kembali ke halaman Beranda dan upload data atau gunakan data default.")
        else:
            st.header("Analisis Data  📈")
            st.write("Analisis data dapat membantu Anda memahami pola penggunaan energi secara mendalam. Melalui visualisasi data yang mudah dipahami, Anda dapat melihat fluktuasi penggunaan energi. Layanan ini dirancang untuk mendukung keputusan yang lebih baik dalam manajemen energi, perencanaan kapasitas, dan strategi optimalisasi penggunaan energi.")
            
            # Mengonversi kolom 'Date' menjadi datetime dan mengatur sebagai index
            try:
                st.session_state['data']['Date'] = pd.to_datetime(st.session_state['data']['Date'], dayfirst=True, errors='coerce')
                st.session_state['data'].set_index('Date', inplace=True)
            except KeyError:
                st.error("Kolom 'Date' tidak ditemukan di dataset.")

            # Data Wrangling Section
            st.markdown("## Cek Data ⌛")
            st.subheader("Data yang Digunakan")
            st.write("Berikut adalah data yang Anda gunakan. Untuk mengubah data, silakan pergi ke menu Beranda.")
            
            st.dataframe(st.session_state['data'])

            st.subheader("Penilaian Kualitas Data")

            st.write("Proses menilai kualitas data meliputi pencarian nilai yang hilang dan data duplikat.")
            missing_values = st.session_state['data'].isnull().sum()
            
            if 'BP' in st.session_state['data'].columns and 'Year' in st.session_state['data'].columns:
                drop_colum = st.session_state['data'].drop(['BP', 'Year'], axis=1)
            elif 'BP' in st.session_state['data'].columns:
                drop_colum = st.session_state['data'].drop('BP', axis=1)
            else:
                drop_colum = st.session_state['data']  # Jika tidak ada kolom 'BP', biarkan DataFrame tetap utuh

            duplicate_data = drop_colum.duplicated().sum()
            st.write(f"Jumlah nilai yang hilang per kolom:\n{missing_values}")
            st.write(f"Jumlah data duplikat: {duplicate_data}")

            st.subheader("Pembersihan Data")
            st.write("Proses membersihkan data dengan memperbaiki atau menghapus data yang tidak konsisten, hilang, atau duplikat untuk meningkatkan kualitas dan akurasi dataset.")
            if missing_values.any() or duplicate_data > 0:
                    st.session_state['data'] = st.session_state['data'].drop_duplicates()
                    st.session_state['data'] = st.session_state['data'].interpolate()   
                    st.write("Data berhasil dibersihkan.")
            else:
                st.write("Data sudah bersih.")

            # Fungsi untuk memvisualisasikan semua data dalam satu grafik
            def plot_all_data(data):
                daily_data = data['BP'].resample('D').mean()
                fig = px.line(daily_data, title='Data Beban Puncak Semua Tahun',
                            labels={'index': 'Tanggal', 'value': 'Beban Puncak'})
                return fig

            # Menampilkan visualisasi berdasarkan pilihan
            st.markdown("## Eksplor dan Cermati Data Anda! 📊")
            st.write("Pada bagian ini, Anda dapat memilih untuk menampilkan grafik data beban puncak per tahun atau semua data sekaligus.")

           # Menambahkan opsi pilihan visualisasi sebagai dropdown
            eda_option = st.selectbox("Pilih jenis visualisasi:", ['Pertahun', 'Semua Data'])

            
            # Logika kondisi untuk menampilkan visualisasi berdasarkan pilihan
            if eda_option == 'Pertahun':
                st.plotly_chart(plot_data_per_year(st.session_state['data']), use_container_width=True)
                st.markdown(
                    """
                    <ul>
                        <li> Legends ditandakan dengan beberapa warna yang melambangkan tiap tahun, untuk keterangan tiap warna dapat dilihat di sebelah kanan grafik. </li>
                        <li> Selain memilih grafik tiap tahun, Anda juga dapat melihat hubungan antar 2 tahun atau lebih, sesuai dengan tahun yang Anda pilih. </li>
                    </ul>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.plotly_chart(plot_all_data(st.session_state['data']), use_container_width=True)
                st.markdown(
                    """
                    <ul>
                        <li> Grafik menunjukkan data gabungan dari setiap tahun. </li>
                        <li> Jika Anda ingin melihat data beban puncak untuk tiap tahunnya, silahkan kembali memilih jenis visualisasi, lalu pilih pertahun. </li>
                    </ul>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("## Rata-Rata Beban ➗")

            plot_stacked_chart(st.session_state['data'])
    
    
    # Prediksi Page
    elif selected == "Prediksi":
        st.header("Cek prediksi di sini, yuk! 📈")
        st.write("Prediksi penggunaan listrik membantu mengidentifikasi pola penggunaan energi di masa depan. Dengan memanfaatkan data historis, prediksi ini memberikan wawasan mengenai fluktuasi dan tren penggunaan energi. Melalui pendekatan ini, Anda dapat membuat keputusan yang lebih baik dalam manajemen energi, perencanaan kapasitas, dan strategi optimalisasi, sehingga meningkatkan efisiensi penggunaan energi dan mengurangi risiko kelebihan penggunaan energi listrik.")
        st.subheader("Catatan:")
        st.markdown(
            """
            <ul>
                <li> Anda dapat menggeser garis di bawah untuk menentukan jangka waktu prediksi yang Anda inginkan. </li>
                <li> Prediksi dibuat dengan menggunakan algoritma Prophet. </li>
                <li> Terdapat 2 jenis prediksi, yaitu <em>historical</em> (digunakan untuk melihat rerata penggunaan listrik berdasarkan data) dan <em>future</em> (hasil prediksi dari data historis). </li>
            </ul>
            """,
            unsafe_allow_html=True
        )

        # Tentukan jumlah periode untuk prediksi (misalnya, 30 hari ke depan)
        periods = st.slider('Pilih jumlah hari untuk prediksi:', min_value=1, max_value=365, value=30)
        # Tampilkan nilai prediksi
        st.subheader(f"⚡Tren untuk {periods} Hari Terakhir⚡")
        # Siapkan data untuk Prophet
        df_prophet = prepare_prophet_data(st.session_state['data'])
        
        # Prediksi masa depan
        model, forecast = predict_future(df_prophet, periods)
        
        # Visualisasi prediksi
        visualize_forecast(model, forecast, df_prophet, periods)
            
        st.subheader('Masukan Batas Pemasukan Listrik')

        # Input batas kapasitas maksimal listrik
        total_capacity = st.number_input(
            'Masukkan batas kapasitas maksimal listrik (dalam kW):',
            min_value=0.0, 
            step=100.0,
            value=10000.0
        )

        # Visualisasi prediksi dengan batas kapasitas listrik
        plot_forecast_with_capacity(forecast, total_capacity)
    
            
authenticator.login()
    
if st.session_state['authentication_status']:
    main()
    
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
         # Hapus file save_data.csv jika ada
    
elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')