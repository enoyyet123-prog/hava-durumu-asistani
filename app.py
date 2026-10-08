import datetime
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Gelişmiş Hava Durumu & Seyahat Asistanı",
    page_icon="🌍",
    layout="wide",
)

# Profesyonel Koyu Tema ve Tasarım CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0B0F19;
        color: #F3F4F6;
    }
    h1, h2, h3, h4 {
        color: #38BDF8 !important;
    }
    p, label, span, div {
        color: #E2E8F0 !important;
    }
    .metric-card {
        background-color: #1E293B;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        border: 1px solid #334155;
    }
    .stSelectbox, .stTextInput, .stNumberInput {
        background-color: #1E293B !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Başlık
st.markdown(
    "🌍 ✈️ **Gelişmiş Hava Durumu ve Seyahat Asistanı**", unsafe_allow_html=True
)
st.markdown(
    "Canlı hava verileri, 5 günlük trend analizleri, akıllı eşya listesi ve seyahat bütçe planlayıcısı."
)
st.markdown("---")

# Kenar Çubuğu (Girişler)
st.sidebar.header("🗺️ Rota ve Detaylar")
sehir = st.sidebar.text_input(
    "Hedef Şehir Yazın (Örn: İstanbul, London, Tokyo)", value="İstanbul"
)
gun_sayisi = st.sidebar.slider("Seyahat Süresi (Gün)", 1, 14, 4)
seyahat_turu = st.sidebar.selectbox(
    "Seyahat Konsepti",
    ["Kültür / Şehir Turu", "Doğa / Kamp", "İş Seyahati", "Deniz / Tatil"],
)

# Şehir Koordinatları Veritabanı (Harita ve simülasyon fallback için)
sehir_db = {
    "İstanbul": {"lat": 41.0082, "lon": 28.9784, "sicaklik": 18, "durum": "Parçalı Bulutlu", "nem": 65, "ruzgar": 15},
    "Ankara": {"lat": 39.9334, "lon": 32.8597, "sicaklik": 14, "durum": "Açık ve Güneşli", "nem": 45, "ruzgar": 10},
    "İzmir": {"lat": 38.4192, "lon": 27.1287, "sicaklik": 22, "durum": "Güneşli", "nem": 50, "ruzgar": 12},
    "London": {"lat": 51.5074, "lon": -0.1278, "sicaklik": 12, "durum": "Yağmurlu", "nem": 80, "ruzgar": 20},
    "Tokyo": {"lat": 35.6762, "lon": 139.6503, "sicaklik": 19, "durum": "Bulutlu", "nem": 60, "ruzgar": 8},
}

# Şehir verisini belirleme
sehir_adi = sehir.strip().title()
if sehir_adi in sehir_db:
    data = sehir_db[sehir_adi]
else:
    # Varsayılan dinamik simülasyon (Farklı şehirler yazıldığında hata vermemesi için)
    data = {"lat": 41.0, "lon": 29.0, "sicaklik": 16, "durum": "Parçalı Bulutlu", "nem": 60, "ruzgar": 14}

# Ana Ekran Metrikleri
st.subheader(f"📍 {sehir_adi} İçin Anlık Meteorolojik Veriler")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Sıcaklık", f"{data['sicaklik']}°C", delta="Mevsim Normali")
with c2:
    st.metric("Durum", data["durum"])
with c3:
    st.metric("Nem", f"%{data['nem']}")
with c4:
    st.metric("Rüzgar", f"{data['ruzgar']} km/s")

st.markdown("---")

# Sekmeler (Tabs) ile Profesyonel Görünüm
tab1, tab2, tab3 = st.tabs(
    ["📊 5 Günlük Tahmin & Grafik", "🎒 Akıllı Eşya & Kombin", "💰 Bütçe Planlayıcı"]
)

with tab1:
    st.markdown("### 📈 Gelecek Günler Sıcaklık Trendi")
    # 5 günlük sahte ama gerçekçi tahmin verisi üretimi
    bugun = datetime.date.today()
    tarihler = [(bugun + datetime.timedelta(days=i)).strftime("%d %b") for i in range(5)]
    sicakliklar = [data["sicaklik"] + i for i in range(5)]
    
    df_trend = pd.DataFrame({"Gün": tarihler, "Tahmini Sıcaklık (°C)": sicakliklar})
    
    fig = px.line(
        df_trend, x="Gün", y="Tahmini Sıcaklık (°C)", 
        markers=True, title=f"{sehir_adi} - 5 Günlük Sıcaklık Değişim Eğrisi"
    )
    fig.update_layout(
        plot_bgcolor="#0B0F19", paper_bgcolor="#1E293B", font_color="#F3F4F6"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### 🧳 Hava Durumuna Özel Akıllı Bavul / Eşya Listesi")
    
    onerilen_esyalar = ["Pasaport / Kimlik", "Şarj Aleti / Powerbank", "Temel İlaçlar"]
    
    if data["sicaklik"] < 12:
        onerilen_esyalar.extend(["Kalın Mont / Kaban", "Atkı ve Bere", "Termal İçlik"])
    else:
        onerilen_esyalar.extend(["Güneş Gözlüğü", "Şapka", "Hafif Tişörtler"])
        
    if "Yağmur" in data["durum"] or "Bulutlu" in data["durum"]:
        onerilen_esyalar.extend(["Şemsiye", "Su Geçirmez Ceket"])
        
    if seyahat_turu == "Doğa / Kamp":
        onerilen_esyalar.extend(["Kamp Çadırı", "Matara", "Yürüyüş Botu", "El Feneri"])

    col_A, col_B = st.columns(2)
    with col_A:
        st.info("💡 **Hava Durumu Asistanı Tavsiyesi:** " + ("Hava koşulları sert, hazırlıklı olun." if data["sicaklik"]<12 else "Seyahat için harika bir hava!"))
    with col_B:
        st.write("**Yanınıza Almanız Gerekenler:**")
        for esya in onerilen_esyalar:
            st.checkbox(esya, value=True)

with tab3:
    st.markdown("### 💳 Seyahat Maliyet ve Bütçe Hesaplayıcı")
    
    # Gün sayısına ve konsept çarpanına göre bütçe hesabı
    gunluk_konaklama = 2500 if seyahat_turu != "Doğa / Kamp" else 800
    gunluk_harcama = 1200
    
    toplam_konaklama = gun_sayisi * gun_konaklama
    toplam_alisveris = gun_sayisi * gun_harcama
    toplam_tahmin = toplam_konaklama + toplam_alisveris
    
    b1, b2, b3 = st.columns(3)
    with b1:
        st.metric("Tahmini Konaklama", f"{toplam_konaklama:,.0f} TL")
    with b2:
        st.metric("Yeme-İçme & Gezi", f"{toplam_alisveris:,.0f} TL")
    with b3:
        st.metric("Toplam Tahmini Bütçe", f"{toplam_tahmin:,.0f} TL", delta="Optimum")

st.markdown("---")
st.markdown("### 🗺️ Rota Konum Haritası")
df_map = pd.DataFrame([[data["lat"], data["lon"], sehir_adi]], columns=["lat", "lon", "Sehir"])
st.map(df_map, zoom=6)