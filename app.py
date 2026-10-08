import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Hava Durumu ve Seyahat Asistanı", page_icon="✈️", layout="wide"
)

# Kesin Çözüm: Karanlık Tema ve Okunabilirlik İçin Özel CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #38BDF8 !important;
    }
    p, label, span, div {
        color: #E2E8F0 !important;
    }
    .metric-card {
        background-color: #1E293B;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border: 1px solid #334155;
        text-align: center;
    }
    .stSelectbox label {
        color: #38BDF8 !important;
        font-weight: bold;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Başlık
st.markdown(
    "✈️ 🌍 **Hava Durumu ve Seyahat Asistanı**", unsafe_allow_html=True
)
st.markdown(
    "Seçtiğiniz şehirlerin anlık hava durumunu öğrenin, akıllı giyim önerileri alın ve rotanızı planlayın."
)
st.markdown("---")

# Kenar Çubuğu (Seyahat Planlayıcı Girişleri)
st.sidebar.header("🗺️ Rota ve Konum Seçimi")
secilen_sehir = st.sidebar.selectbox(
    "Hedef Şehir Seçin",
    [
        "İstanbul",
        "Ankara",
        "İzmir",
        "Antalya",
        "Erzurum",
        "Trabzon",
        "London",
        "Paris",
    ],
)
seyahat_turu = st.sidebar.selectbox(
    "Seyahat Amacı", ["Tatil / Gezi", "İş Toplantısı", "Doğa Yürüyüşü / Kamp"]
)

# Örnek Şehir Verileri
sehir_koordinatlari = {
    "İstanbul": {"lat": 41.0082, "lon": 28.9784, "sicaklik": 18, "durum": "Parçalı Bulutlu", "nem": 65, "ruzgar": 15},
    "Ankara": {"lat": 39.9334, "lon": 32.8597, "sicaklik": 14, "durum": "Açık ve Güneşli", "nem": 45, "ruzgar": 10},
    "İzmir": {"lat": 38.4192, "lon": 27.1287, "sicaklik": 22, "durum": "Güneşli", "nem": 50, "ruzgar": 12},
    "Antalya": {"lat": 36.8969, "lon": 30.7133, "sicaklik": 26, "durum": "Sıcak ve Güneşli", "nem": 60, "ruzgar": 8},
    "Erzurum": {"lat": 39.9043, "lon": 41.2679, "sicaklik": 5, "durum": "Soğuk / Karlı", "nem": 75, "ruzgar": 20},
    "Trabzon": {"lat": 41.0015, "lon": 39.7178, "sicaklik": 16, "durum": "Yağmurlu", "nem": 85, "ruzgar": 25},
    "London": {"lat": 51.5074, "lon": -0.1278, "sicaklik": 12, "durum": "Sisli", "nem": 80, "ruzgar": 18},
    "Paris": {"lat": 48.8566, "lon": 2.3522, "sicaklik": 15, "durum": "Bulutlu", "nem": 70, "ruzgar": 14},
}

data = sehir_koordinatlari[secilen_sehir]

# Ana Ekran Metrikleri
st.subheader(f"📍 {secilen_sehir} İçin Anlık Hava Durumu Analizi")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Sıcaklık", f"{data['sicaklik']}°C")
with col2:
    st.metric("Hava Durumu", data["durum"])
with col3:
    st.metric("Nem Oranı", f"%{data['nem']}")
with col4:
    st.metric("Rüzgar Hızı", f"{data['ruzgar']} km/s")

st.markdown("---")

# Akıllı Giyim ve Seyahat Önerisi
col_giysi, col_rota = st.columns(2)

with col_giysi:
    st.markdown("### 🧥 Akıllı Giyim Önerisi")
    if data["sicaklik"] < 10:
        tavsiye = "Hava oldukça soğuk! Kalın mont, atkı, bere ve eldiven almayı unutmayın."
    elif 10 <= data["sicaklik"] < 20:
        tavsiye = "Hava serin. Yanınıza hırka, ceket veya hafif bir trençkot almanız iyi olacaktır."
    else:
        tavsiye = "Hava sıcak ve ferah! Tişört ve hafif kıyafetler tercih edebilirsiniz."

    if "Yağmur" in data["durum"] or "Sisli" in data["durum"]:
        tavsiye += " ☔ Ayrıca yanınızda şemsiye bulundurmanızda fayda var."

    st.info(tavsiye)

with col_rota:
    st.markdown("### 🎒 Seyahat İpucu")
    if seyahat_turu == "Doğa Yürüyüşü / Kamp":
        st.info("Doğa yürüyüşü için sağlam tabanlı botlar ve su geçirmez kıyafetler tercih edin.")
    elif seyahat_turu == "İş Toplantısı":
        st.info("Kurumsal kombinler ve yanınızda şık bir evrak çantası ideal olacaktır.")
    else:
        st.info("Şehir turu için rahat yürüyüş ayakkabıları ve güneş gözlüğü şart!")

st.markdown("---")

# Harita ve Konum Görselleştirme
st.markdown("### 🗺️ Rota ve Harita Konumu")
df_map = pd.DataFrame(
    [[data["lat"], data["lon"], secilen_sehir]], columns=["lat", "lon", "Sehir"]
)
st.map(df_map, zoom=6)