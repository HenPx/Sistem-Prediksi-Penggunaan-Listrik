import streamlit as st
from streamlit_option_menu import option_menu

def create_option_menu():
    # Tampilkan logo PLN di sidebar
    st.markdown(
        """
        <style>
            [data-testid=stSidebar] {
                background-color: #D6E4FF;  /* Warna latar belakang sidebar */
                padding: 10px;  /* Tambahkan padding jika diperlukan */
                
            }
            [data-testid=stSidebar] [data-testid=stImage]{
                text-align: center;
                margin-left: auto;
                margin-right: auto;
                max-width: 70%;
            }
            .st-emotion-cache-1mi2ry5 {
                padding: 0;
            }
        </style>
        """, unsafe_allow_html=True
    )
    with st.sidebar:
        st.image("images/logo_App.png")
 
    # Tambahkan tulisan di samping logo
    st.sidebar.markdown("<p style='font-size: 25px; text-align: center; font-weight: bold; color: #000000;'>SiPRELIS</p>", unsafe_allow_html=True)

    selected = option_menu(
        menu_title="Menu",
        options=["Beranda", "Analisis", "Prediksi", "FAQ"],
        icons=["house", "graph-up", "clipboard2-data", "question-circle"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
        styles={
            "menu-title": {"font-size": "20px"},
            "nav-link": {"font-size": "15px"},
        }
    )
    return selected