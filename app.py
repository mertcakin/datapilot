import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="DataPilot",
    page_icon="📊",
    layout="wide"
)

st.title("👋 Merhaba, DataPilot'a Hoş Geldiniz!")
st.subheader("📊 Yapay Zekâ Destekli İş Analiz Asistanı")

st.write(
    "Satış verilerinizi yükleyin, işletmenizin performansını "
    "analiz edin ve verilerinizden anlamlı içgörüler elde edin."
)

uploaded_file = st.file_uploader(
    "📂 Satış verilerinizi yükleyin",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    try:
        # Veriyi oku
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Tarih sütununu düzenle
        if "Tarih" in df.columns:
            df["Tarih"] = pd.to_datetime(df["Tarih"])

        st.success("✅ Verileriniz başarıyla yüklendi!")

        # KPI hesaplamaları
        toplam_satis = df["Toplam_Satis"].sum()
        toplam_adet = df["Adet"].sum()
        ortalama_satis = df["Toplam_Satis"].mean()
        musteri_segmenti = df["Musteri_Segmenti"].nunique()

        # KPI başlığı
        st.header("📊 Temel Performans Göstergeleri")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Toplam Satış",
            f"₺{toplam_satis:,.0f}"
        )

        col2.metric(
            "Toplam Ürün Adedi",
            f"{toplam_adet:,.0f}"
        )

        col3.metric(
            "Ortalama Satış",
            f"₺{ortalama_satis:,.0f}"
        )

        col4.metric(
            "Müşteri Segmenti",
            f"{musteri_segmenti}"
        )

        # Veri önizleme
        st.header("📋 Veri Önizleme")
        st.dataframe(
            df,
            use_container_width=True
        )

        # Aylık satış analizi
        st.header("📈 Aylık Satış Analizi")

        aylik_satis = (
            df.groupby(df["Tarih"].dt.to_period("M"))["Toplam_Satis"]
            .sum()
        )

        aylik_satis.index = aylik_satis.index.astype(str)

        st.bar_chart(aylik_satis)

        # Ürün analizi
        st.header("📦 Ürün Performansı")

        urun_satis = (
            df.groupby("Urun")["Toplam_Satis"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(urun_satis)

        # Segment analizi
        st.header("👥 Müşteri Segmenti Analizi")

        segment_satis = (
            df.groupby("Musteri_Segmenti")["Toplam_Satis"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(segment_satis)

        # Temel içgörü
        en_cok_satan_urun = urun_satis.idxmax()
        en_degerli_segment = segment_satis.idxmax()

        st.header("💡 İş İçgörüleri")

        st.info(
            f"📌 En yüksek satış yapan ürün: **{en_cok_satan_urun}**"
        )

        st.info(
            f"📌 En yüksek satış hacmine sahip müşteri segmenti: "
            f"**{en_degerli_segment}**"
        )

    except Exception as e:
        st.error(
            f"❌ Veriler analiz edilirken bir hata oluştu: {e}"
        )

else:
    st.info(
        "👆 Analize başlamak için yukarıdaki alandan "
        "CSV veya Excel dosyanızı yükleyin."
    )
