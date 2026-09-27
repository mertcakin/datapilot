import streamlit as st
import pandas as pd
from ai_assistant import create_business_summary

# --------------------------------------------------
# SAYFA AYARLARI
# --------------------------------------------------

st.set_page_config(
    page_title="DataPilot | İş Analizi",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# ÖZEL TASARIM
# --------------------------------------------------

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    color: #8b949e;
    margin-bottom: 30px;
}

.section-title {
    font-size: 25px;
    font-weight: 650;
    margin-top: 35px;
    margin-bottom: 15px;
}

.insight-box {
    padding: 18px;
    border-radius: 10px;
    background-color: #172033;
    border-left: 4px solid #4da3ff;
    margin-bottom: 12px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# BAŞLIK
# --------------------------------------------------

st.markdown(
    '<div class="main-title">👋 Merhaba, DataPilot\'a Hoş Geldiniz!</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">📊 Yapay Zekâ Destekli İş Analiz Asistanı</div>',
    unsafe_allow_html=True
)

st.write(
    "Satış verilerinizi yükleyin, işletmenizin performansını "
    "tek ekrandan analiz edin ve önemli iş içgörülerini keşfedin."
)

# --------------------------------------------------
# DOSYA YÜKLEME
# --------------------------------------------------

st.markdown(
    '<div class="section-title">📂 Veri Yükleme</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "CSV veya Excel satış dosyanızı yükleyin",
    type=["csv", "xlsx"]
)

# --------------------------------------------------
# DOSYA YÜKLENDİYSE
# --------------------------------------------------

if uploaded_file is not None:

    try:

        # --------------------------------------------------
        # VERİYİ OKU
        # --------------------------------------------------

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # --------------------------------------------------
        # TARİH
        # --------------------------------------------------

        if "Tarih" in df.columns:
            df["Tarih"] = pd.to_datetime(df["Tarih"])

        # --------------------------------------------------
        # GEREKLİ SÜTUNLAR
        # --------------------------------------------------

        gerekli_sutunlar = [
            "Tarih",
            "Urun",
            "Musteri_Segmenti",
            "Adet",
            "Birim_Fiyat",
            "Toplam_Satis"
        ]

        eksik_sutunlar = [
            sutun for sutun in gerekli_sutunlar
            if sutun not in df.columns
        ]

        if eksik_sutunlar:

            st.error(
                "❌ Dosyada gerekli sütunlar bulunamadı: "
                + ", ".join(eksik_sutunlar)
            )

            st.stop()

        st.success("✅ Verileriniz başarıyla yüklendi!")

        # --------------------------------------------------
        # HESAPLAMALAR
        # --------------------------------------------------

        toplam_satis = df["Toplam_Satis"].sum()

        toplam_adet = df["Adet"].sum()

        ortalama_satis = df["Toplam_Satis"].mean()

        toplam_islem = len(df)

        en_cok_satan_urun = (
            df.groupby("Urun")["Toplam_Satis"]
            .sum()
            .idxmax()
        )

        en_cok_satan_urun_tutari = (
            df.groupby("Urun")["Toplam_Satis"]
            .sum()
            .max()
        )

        en_degerli_segment = (
            df.groupby("Musteri_Segmenti")["Toplam_Satis"]
            .sum()
            .idxmax()
        )

        # --------------------------------------------------
        # KPI DASHBOARD
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">🎯 İşletme Performansı</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "💰 Toplam Ciro",
                f"₺{toplam_satis:,.0f}"
            )

        with col2:
            st.metric(
                "📦 Toplam Ürün",
                f"{toplam_adet:,.0f}"
            )

        with col3:
            st.metric(
                "🧾 İşlem Sayısı",
                f"{toplam_islem:,.0f}"
            )

        with col4:
            st.metric(
                "💳 Ortalama Satış",
                f"₺{ortalama_satis:,.0f}"
            )

        # --------------------------------------------------
        # İKİNCİ KPI SATIRI
        # --------------------------------------------------

        col5, col6, col7 = st.columns(3)

        with col5:
            st.metric(
                "🏆 En Çok Satan Ürün",
                en_cok_satan_urun
            )

        with col6:
            st.metric(
                "💰 Ürün Satış Tutarı",
                f"₺{en_cok_satan_urun_tutari:,.0f}"
            )

        with col7:
            st.metric(
                "👥 En Değerli Segment",
                en_degerli_segment
            )

        # --------------------------------------------------
        # VERİ ÖNİZLEME
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">📋 Veri Önizleme</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            df,
            use_container_width=True,
            height=350
        )

        # --------------------------------------------------
        # AYLIK SATIŞ
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">📈 Aylık Satış Analizi</div>',
            unsafe_allow_html=True
        )

        aylik_satis = (
            df.groupby(df["Tarih"].dt.to_period("M"))["Toplam_Satis"]
            .sum()
        )

        aylik_satis.index = aylik_satis.index.astype(str)

        st.line_chart(aylik_satis)

        # --------------------------------------------------
        # ÜRÜN ANALİZİ
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">📦 Ürün Performansı</div>',
            unsafe_allow_html=True
        )

        urun_satis = (
            df.groupby("Urun")["Toplam_Satis"]
            .sum()
            .sort_values(ascending=False)
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Ürünlere Göre Toplam Satış**")

            st.bar_chart(urun_satis)

        with col2:

            st.write("**Ürün Satış Tablosu**")

            urun_tablosu = urun_satis.reset_index()

            urun_tablosu.columns = [
                "Ürün",
                "Toplam Satış"
            ]

            st.dataframe(
                urun_tablosu,
                use_container_width=True,
                hide_index=True
            )

        # --------------------------------------------------
        # MÜŞTERİ SEGMENTİ
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">👥 Müşteri Segmenti Analizi</div>',
            unsafe_allow_html=True
        )

        segment_satis = (
            df.groupby("Musteri_Segmenti")["Toplam_Satis"]
            .sum()
            .sort_values(ascending=False)
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Segmentlere Göre Satış**")

            st.bar_chart(segment_satis)

        with col2:

            st.write("**Segment Satış Dağılımı**")

            segment_tablosu = segment_satis.reset_index()

            segment_tablosu.columns = [
                "Müşteri Segmenti",
                "Toplam Satış"
            ]

            st.dataframe(
                segment_tablosu,
                use_container_width=True,
                hide_index=True
            )

        # --------------------------------------------------
        # OTOMATİK İŞ İÇGÖRÜLERİ
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">💡 Otomatik İş İçgörüleri</div>',
            unsafe_allow_html=True
        )

        urun_payi = (
            en_cok_satan_urun_tutari / toplam_satis
        ) * 100

        st.markdown(
            f"""
            <div class="insight-box">
            🏆 <b>Ürün Performansı:</b><br>
            {en_cok_satan_urun}, toplam satışların yaklaşık
            <b>%{urun_payi:.1f}</b>'ini oluşturuyor.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="insight-box">
            👥 <b>Müşteri Analizi:</b><br>
            En yüksek satış hacmine sahip müşteri segmenti
            <b>{en_degerli_segment}</b>.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="insight-box">
            💰 <b>Satış Performansı:</b><br>
            İşlem başına ortalama satış tutarı
            <b>₺{ortalama_satis:,.0f}</b>.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="insight-box">
            📦 <b>Satış Hacmi:</b><br>
            Toplam <b>{toplam_adet:,.0f}</b> adet ürün satışı
            gerçekleşmiş durumda.
            </div>
            """,
            unsafe_allow_html=True
        )

        # --------------------------------------------------
        # VERİ ÖZETİ
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">📌 Veri Özeti</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(
                f"**Veri Satırı:** {len(df):,}"
            )

        with col2:
            st.write(
                f"**Ürün Sayısı:** {df['Urun'].nunique():,}"
            )

        with col3:
            st.write(
                f"**Müşteri Segmenti:** {df['Musteri_Segmenti'].nunique():,}"
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

    st.markdown("---")

    st.subheader("🚀 DataPilot ile neler yapabilirsiniz?")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("### 📊 Analiz")
        st.write(
            "Satış verilerinizi hızlıca analiz edin."
        )

    with col2:
        st.write("### 📈 Görselleştirme")
        st.write(
            "Satış trendlerini ve ürün performansını görüntüleyin."
        )

    with col3:
        st.write("### 🤖 Yapay Zekâ")
        st.write(
            "Verilerinizden otomatik iş içgörüleri elde edin."
        )
