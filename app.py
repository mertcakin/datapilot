import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from ai_assistant import create_business_summary, answer_question


# ==================================================
# SAYFA AYARLARI
# ==================================================

st.set_page_config(
    page_title="DataPilot | İş Analizi",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# RENKLER
# ==================================================

NAVY = "#071A3A"
DARK_NAVY = "#041127"
BLUE = "#0B63CE"
LIGHT_BLUE = "#38BDF8"
TURQUOISE = "#18D5C0"
CYAN = "#06B6D4"
WHITE = "#FFFFFF"
LIGHT_BG = "#F4F8FC"
TEXT = "#10213F"
MUTED = "#64748B"


# ==================================================
# CSS TASARIM
# ==================================================

st.markdown(
    f"""
    <style>

    /* GENEL */

    .stApp {{
        background:
            linear-gradient(
                135deg,
                #F7FBFF 0%,
                #EEF8FF 55%,
                #F2FFFD 100%
            );
        color: {TEXT};
    }}

    .main {{
        padding-top: 1rem;
    }}

    /* SIDEBAR */

    section[data-testid="stSidebar"] {{
        background:
            linear-gradient(
                180deg,
                {DARK_NAVY} 0%,
                {NAVY} 55%,
                #063B63 100%
            );
    }}

    section[data-testid="stSidebar"] * {{
        color: white !important;
    }}

    .sidebar-logo {{
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }}

    .sidebar-subtitle {{
        font-size: 13px;
        color: #A9C7E8 !important;
        margin-bottom: 30px;
    }}

    .sidebar-box {{
        margin-top: 25px;
        padding: 20px;
        border-radius: 22px;
        border: 1px solid rgba(255,255,255,0.22);
        background: rgba(255,255,255,0.07);
        text-align: center;
    }}

    /* HEADER */

    .hero {{
        padding: 30px 35px;
        border-radius: 28px;
        margin-bottom: 25px;
        background:
            linear-gradient(
                115deg,
                #FFFFFF 0%,
                #F4FAFF 48%,
                #DFFBFA 100%
            );
        border: 1px solid #D9EAF7;
        box-shadow: 0 12px 35px rgba(7,26,58,0.08);
        position: relative;
        overflow: hidden;
    }}

    .hero::after {{
        content: "";
        position: absolute;
        width: 430px;
        height: 180px;
        right: -80px;
        top: -70px;
        background:
            linear-gradient(
                135deg,
                rgba(6,182,212,0.15),
                rgba(24,213,192,0.20)
            );
        border-radius: 50%;
    }}

    .hero-title {{
        font-size: 42px;
        font-weight: 800;
        color: {NAVY};
        letter-spacing: -1.5px;
        margin-bottom: 5px;
    }}

    .hero-title span {{
        background:
            linear-gradient(
                90deg,
                {BLUE},
                {TURQUOISE}
            );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .hero-subtitle {{
        color: {MUTED};
        font-size: 17px;
        margin-bottom: 15px;
    }}

    .hero-tagline {{
        color: {NAVY};
        font-weight: 700;
        font-size: 14px;
    }}

    /* SECTION */

    .section-title {{
        color: {NAVY};
        font-size: 24px;
        font-weight: 800;
        margin-top: 30px;
        margin-bottom: 15px;
    }}

    /* KPI CARDS */

    .kpi-card {{
        background:
            linear-gradient(
                145deg,
                #FFFFFF 0%,
                #F8FCFF 70%,
                #E8FFFC 100%
            );
        border: 1px solid #DDEBF5;
        border-radius: 24px;
        padding: 23px;
        min-height: 150px;
        box-shadow: 0 10px 30px rgba(7,26,58,0.07);
        position: relative;
        overflow: hidden;
    }}

    .kpi-card::after {{
        content: "";
        position: absolute;
        width: 95px;
        height: 95px;
        right: -30px;
        bottom: -35px;
        border-radius: 50%;
        background:
            linear-gradient(
                135deg,
                rgba(56,189,248,0.18),
                rgba(24,213,192,0.24)
            );
    }}

    .kpi-icon {{
        width: 45px;
        height: 45px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        background:
            linear-gradient(
                135deg,
                #DFF6FF,
                #D9FFFA
            );
        font-size: 21px;
        margin-bottom: 13px;
    }}

    .kpi-label {{
        color: {MUTED};
        font-size: 13px;
        font-weight: 600;
    }}

    .kpi-value {{
        color: {NAVY};
        font-size: 25px;
        font-weight: 800;
        margin-top: 4px;
    }}

    .kpi-description {{
        color: #718096;
        font-size: 11px;
        margin-top: 5px;
    }}

    /* CHART CARDS */

    .chart-card {{
        background: #FFFFFF;
        border: 1px solid #E2ECF5;
        border-radius: 24px;
        padding: 18px 20px 10px 20px;
        box-shadow: 0 10px 30px rgba(7,26,58,0.055);
        margin-bottom: 18px;
    }}

    .chart-title {{
        color: {NAVY};
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 4px;
    }}

    .chart-subtitle {{
        color: {MUTED};
        font-size: 12px;
        margin-bottom: 8px;
    }}

    /* AI PANEL */

    .ai-panel {{
        background:
            linear-gradient(
                120deg,
                {DARK_NAVY} 0%,
                #082B57 48%,
                #006B78 100%
            );
        border-radius: 30px;
        padding: 32px;
        margin-top: 35px;
        margin-bottom: 25px;
        box-shadow: 0 20px 45px rgba(4,17,39,0.20);
        color: white;
    }}

    .ai-label {{
        color: #55E6D8;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1px;
    }}

    .ai-title {{
        font-size: 31px;
        font-weight: 800;
        margin-top: 5px;
    }}

    .ai-description {{
        color: #C5D9EC;
        font-size: 14px;
        max-width: 600px;
        line-height: 1.6;
    }}

    .question-chip {{
        display: inline-block;
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.18);
        color: white;
        border-radius: 30px;
        padding: 8px 15px;
        margin: 5px 5px 5px 0;
        font-size: 12px;
    }}

    /* INSIGHTS */

    .insight-card {{
        padding: 20px;
        border-radius: 22px;
        background:
            linear-gradient(
                135deg,
                #FFFFFF,
                #F0FCFF
            );
        border: 1px solid #DCECF5;
        box-shadow: 0 8px 24px rgba(7,26,58,0.05);
        min-height: 125px;
    }}

    .insight-title {{
        font-weight: 800;
        color: {NAVY};
        margin-bottom: 8px;
    }}

    .insight-text {{
        color: {MUTED};
        font-size: 13px;
        line-height: 1.5;
    }}

    /* DATAFRAME */

    div[data-testid="stDataFrame"] {{
        border-radius: 18px;
        overflow: hidden;
        border: 1px solid #DCE8F2;
    }}

    /* FILE UPLOADER */

    div[data-testid="stFileUploader"] {{
        background: rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 5px;
    }}

    /* INPUT */

    div[data-baseweb="input"] {{
        border-radius: 16px !important;
    }}

    /* BUTTON */

    .stButton > button {{
        border-radius: 14px;
        border: none;
        font-weight: 700;
        background:
            linear-gradient(
                90deg,
                {BLUE},
                {TURQUOISE}
            );
        color: white;
    }}

    /* DIVIDER */

    hr {{
        border-color: #DCEAF4;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-logo">📊 DataPilot</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">Yapay Zekâ Destekli İş Analitiği</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 🧭 Menü")

    st.markdown("📊 Genel Bakış")
    st.markdown("📦 Ürün Analizi")
    st.markdown("👥 Müşteri Analizi")
    st.markdown("📈 Zaman Analizi")
    st.markdown("🤖 AI Asistan")

    st.markdown("---")

    st.markdown("### 📂 Veri Yükle")

    uploaded_file = st.file_uploader(
        "CSV veya Excel dosyanızı yükleyin",
        type=["csv", "xlsx"],
        label_visibility="visible"
    )

    st.markdown(
        """
        <div class="sidebar-box">
            <div style="font-size:32px;">☁️</div>
            <div style="font-weight:700; margin-top:8px;">
                Verinizi Analiz Edin
            </div>
            <div style="font-size:12px; color:#A9C7E8 !important; margin-top:5px;">
                CSV veya Excel dosyanızı yükleyerek
                analiz ekranını başlatın.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# DOSYA YÜKLENMEDİ
# ==================================================

if uploaded_file is None:

    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">
                Data<span>Pilot</span>
            </div>
            <div class="hero-subtitle">
                Yapay zekâ destekli satış ve iş analizi platformu
            </div>
            <div class="hero-tagline">
                Veri → Analiz → İçgörü → Karar
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            background:white;
            border-radius:28px;
            padding:50px;
            text-align:center;
            border:1px solid #DDEAF4;
            box-shadow:0 12px 35px rgba(7,26,58,0.07);
        ">
            <div style="font-size:55px;">📂</div>
            <h2 style="color:#071A3A;">
                Analize Başlayın
            </h2>
            <p style="color:#64748B;">
                Sol menüden CSV veya Excel satış verinizi yükleyin.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# ==================================================
# VERİYİ OKU
# ==================================================

try:

    if uploaded_file.name.endswith(".csv"):

        df = pd.read_csv(uploaded_file)

    else:

        df = pd.read_excel(uploaded_file)

except Exception as e:

    st.error(
        f"❌ Dosya okunurken bir hata oluştu: {e}"
    )

    st.stop()


# ==================================================
# GEREKLİ SÜTUNLAR
# ==================================================

gerekli_sutunlar = [
    "Tarih",
    "Urun",
    "Musteri_Segmenti",
    "Adet",
    "Birim_Fiyat",
    "Toplam_Satis"
]

eksik_sutunlar = [
    sutun
    for sutun in gerekli_sutunlar
    if sutun not in df.columns
]

if eksik_sutunlar:

    st.error(
        "❌ Dosyada gerekli sütunlar bulunamadı: "
        + ", ".join(eksik_sutunlar)
    )

    st.stop()


# ==================================================
# TARİH
# ==================================================

df["Tarih"] = pd.to_datetime(
    df["Tarih"],
    errors="coerce"
)


# ==================================================
# TEMEL HESAPLAMALAR
# ==================================================

toplam_satis = df["Toplam_Satis"].sum()

toplam_adet = df["Adet"].sum()

ortalama_satis = df["Toplam_Satis"].mean()

toplam_islem = len(df)

urun_sayisi = df["Urun"].nunique()

segment_sayisi = df["Musteri_Segmenti"].nunique()


# ==================================================
# ÜRÜN ANALİZİ
# ==================================================

urun_satis = (
    df.groupby("Urun")["Toplam_Satis"]
    .sum()
    .sort_values(ascending=False)
)

urun_adet = (
    df.groupby("Urun")["Adet"]
    .sum()
    .sort_values(ascending=False)
)

en_cok_satan_urun = urun_satis.idxmax()

en_cok_satan_urun_tutari = urun_satis.max()


# ==================================================
# SEGMENT ANALİZİ
# ==================================================

segment_satis = (
    df.groupby("Musteri_Segmenti")["Toplam_Satis"]
    .sum()
    .sort_values(ascending=False)
)

en_degerli_segment = segment_satis.idxmax()

en_degerli_segment_tutari = segment_satis.max()


# ==================================================
# AYLIK SATIŞ
# ==================================================

aylik_satis = (
    df.dropna(subset=["Tarih"])
    .groupby(
        df.dropna(subset=["Tarih"])["Tarih"].dt.to_period("M")
    )["Toplam_Satis"]
    .sum()
)

aylik_satis.index = aylik_satis.index.astype(str)


# ==================================================
# AYLIK ADET
# ==================================================

aylik_adet = (
    df.dropna(subset=["Tarih"])
    .groupby(
        df.dropna(subset=["Tarih"])["Tarih"].dt.to_period("M")
    )["Adet"]
    .sum()
)

aylik_adet.index = aylik_adet.index.astype(str)


# ==================================================
# BAŞLIK
# ==================================================

st.markdown(
    f"""
    <div class="hero">

        <div class="hero-title">
            Merhaba, <span>DataPilot</span>
        </div>

        <div class="hero-subtitle">
            Satış verilerinizden anlamlı iş içgörüleri keşfedin.
        </div>

        <div class="hero-tagline">
            Veri → Analiz → İçgörü → Karar
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


st.success(
    f"✅ {uploaded_file.name} başarıyla yüklendi."
)


# ==================================================
# KPI'LAR
# ==================================================

st.markdown(
    '<div class="section-title">📊 İşletme Performansı</div>',
    unsafe_allow_html=True
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">💰</div>

            <div class="kpi-label">
                Toplam Satış
            </div>

            <div class="kpi-value">
                ₺{toplam_satis:,.0f}
            </div>

            <div class="kpi-description">
                Toplam satış hacmi
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with kpi2:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">📦</div>

            <div class="kpi-label">
                Toplam Adet
            </div>

            <div class="kpi-value">
                {toplam_adet:,.0f}
            </div>

            <div class="kpi-description">
                Satılan toplam ürün
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with kpi3:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">🧾</div>

            <div class="kpi-label">
                İşlem Sayısı
            </div>

            <div class="kpi-value">
                {toplam_islem:,}
            </div>

            <div class="kpi-description">
                Toplam satış işlemi
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with kpi4:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-icon">👥</div>

            <div class="kpi-label">
                En Değerli Segment
            </div>

            <div class="kpi-value">
                {en_degerli_segment}
            </div>

            <div class="kpi-description">
                En yüksek satış hacmine sahip
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# ANA GRAFİKLER
# ==================================================

st.markdown(
    '<div class="section-title">📈 Satış Analizi</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([1.65, 1])


# --------------------------------------------------
# AYLIK SATIŞ
# --------------------------------------------------

with col1:

    st.markdown(
        """
        <div class="chart-card">
            <div class="chart-title">
                📈 Aylık Satış Trendi
            </div>
            <div class="chart-subtitle">
                Aylara göre toplam satış performansı
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=aylik_satis.index,
            y=aylik_satis.values,
            name="Aylık Satış",
            marker=dict(
                color=aylik_satis.values,
                colorscale=[
                    [0, "#0B63CE"],
                    [0.5, "#18BFD1"],
                    [1, "#18D5C0"]
                ]
            ),
            hovertemplate="Satış: ₺%{y:,.0f}<extra></extra>"
        )
    )

    fig.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=TEXT),
        showlegend=False,
        xaxis=dict(
            title=None,
            showgrid=False
        ),
        yaxis=dict(
            title=None,
            gridcolor="#E8F0F6",
            tickprefix="₺",
            tickformat=","
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# --------------------------------------------------
# ÜRÜN DAĞILIMI
# --------------------------------------------------

with col2:

    st.markdown(
        """
        <div class="chart-card">
            <div class="chart-title">
                📦 Ürün Satış Dağılımı
            </div>
            <div class="chart-subtitle">
                Ürünlerin toplam satış içindeki payı
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    fig = px.pie(
        names=urun_satis.index,
        values=urun_satis.values,
        hole=0.62
    )

    fig.update_traces(
        marker=dict(
            colors=[
                "#0B63CE",
                "#18D5C0",
                "#38BDF8",
                "#4F8EF7",
                "#64748B"
            ],
            line=dict(
                color="white",
                width=3
            )
        ),
        textinfo="percent",
        hovertemplate="%{label}<br>₺%{value:,.0f}<extra></extra>"
    )

    fig.update_layout(
        height=350,
        margin=dict(l=5, r=5, t=5, b=5),
        paper_bgcolor="white",
        showlegend=True,
        legend=dict(
            orientation="h",
            y=-0.08
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# ==================================================
# İKİNCİ GRAFİK SATIRI
# ==================================================

col1, col2 = st.columns(2)


# --------------------------------------------------
# ÜRÜN PERFORMANSI
# --------------------------------------------------

with col1:

    st.markdown(
        """
        <div class="chart-card">
            <div class="chart-title">
                🏆 Ürün Performansı
            </div>
            <div class="chart-subtitle">
                Ürün bazında satış tutarları
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    fig = px.bar(
        x=urun_satis.values,
        y=urun_satis.index,
        orientation="h"
    )

    fig.update_traces(
        marker=dict(
            color=[
                "#0B63CE",
                "#159BD7",
                "#18BFD1",
                "#18D5C0",
                "#73E6DB"
            ]
        ),
        hovertemplate="₺%{x:,.0f}<extra></extra>"
    )

    fig.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(
            title=None,
            gridcolor="#E8F0F6",
            tickprefix="₺"
        ),
        yaxis=dict(
            title=None
        ),
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# --------------------------------------------------
# SEGMENT ANALİZİ
# --------------------------------------------------

with col2:

    st.markdown(
        """
        <div class="chart-card">
            <div class="chart-title">
                👥 Müşteri Segmenti Analizi
            </div>
            <div class="chart-subtitle">
                Segmentlere göre satış hacmi
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    fig = px.bar(
        x=segment_satis.values,
        y=segment_satis.index,
        orientation="h"
    )

    fig.update_traces(
        marker=dict(
            color=[
                "#0B63CE",
                "#18BFD1",
                "#18D5C0",
                "#4F8EF7",
                "#73E6DB"
            ]
        ),
        hovertemplate="₺%{x:,.0f}<extra></extra>"
    )

    fig.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(
            title=None,
            gridcolor="#E8F0F6",
            tickprefix="₺"
        ),
        yaxis=dict(
            title=None
        ),
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# ==================================================
# ZAMAN ANALİZİ
# ==================================================

st.markdown(
    '<div class="section-title">📅 Zaman Analizi</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


# --------------------------------------------------
# AYLIK ADET
# --------------------------------------------------

with col1:

    st.markdown(
        """
        <div class="chart-card">
            <div class="chart-title">
                📦 Aylık Ürün Adedi
            </div>
            <div class="chart-subtitle">
                Aylara göre satılan ürün miktarı
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=aylik_adet.index,
            y=aylik_adet.values,
            mode="lines+markers",
            line=dict(
                color=TURQUOISE,
                width=4
            ),
            marker=dict(
                size=9,
                color=BLUE
            ),
            hovertemplate="%{y:,.0f} adet<extra></extra>"
        )
    )

    fig.update_layout(
        height=330,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(
            showgrid=False
        ),
        yaxis=dict(
            gridcolor="#E8F0F6"
        ),
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# --------------------------------------------------
# SATIŞ + ADET KARŞILAŞTIRMASI
# --------------------------------------------------

with col2:

    st.markdown(
        """
        <div class="chart-card">
            <div class="chart-title">
                🔄 Satış ve Adet Karşılaştırması
            </div>
            <div class="chart-subtitle">
                Aylık satış ve ürün miktarı
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=aylik_satis.index,
            y=aylik_satis.values,
            mode="lines+markers",
            name="Satış",
            line=dict(
                color=BLUE,
                width=4
            ),
            marker=dict(size=8),
            hovertemplate="₺%{y:,.0f}<extra></extra>"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=aylik_adet.index,
            y=aylik_adet.values,
            mode="lines+markers",
            name="Adet",
            line=dict(
                color=TURQUOISE,
                width=4
            ),
            marker=dict(size=8),
            yaxis="y2",
            hovertemplate="%{y:,.0f} adet<extra></extra>"
        )
    )

    fig.update_layout(
        height=330,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        yaxis=dict(
            title="Satış",
            tickprefix="₺",
            gridcolor="#E8F0F6"
        ),
        yaxis2=dict(
            title="Adet",
            overlaying="y",
            side="right"
        ),
        legend=dict(
            orientation="h",
            y=1.12
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# ==================================================
# OTOMATİK İŞ İÇGÖRÜLERİ
# ==================================================

st.markdown(
    '<div class="section-title">💡 Otomatik İş İçgörüleri</div>',
    unsafe_allow_html=True
)

urun_payi = (
    en_cok_satan_urun_tutari / toplam_satis * 100
    if toplam_satis > 0
    else 0
)


insight1, insight2, insight3 = st.columns(3)


with insight1:

    st.markdown(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                🏆 Ürün Performansı
            </div>

            <div class="insight-text">
                <b>{en_cok_satan_urun}</b>,
                toplam satışların yaklaşık
                <b>%{urun_payi:.1f}</b>'ini oluşturuyor.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with insight2:

    st.markdown(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                👥 Müşteri Analizi
            </div>

            <div class="insight-text">
                En yüksek satış hacmine sahip segment
                <b>{en_degerli_segment}</b>.
                Toplam satış:
                <b>₺{en_degerli_segment_tutari:,.0f}</b>.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with insight3:

    st.markdown(
        f"""
        <div class="insight-card">

            <div class="insight-title">
                💳 Ortalama İşlem
            </div>

            <div class="insight-text">
                İşlem başına ortalama satış tutarı
                <b>₺{ortalama_satis:,.0f}</b>.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# ÜRÜN TABLOSU
# ==================================================

st.markdown(
    '<div class="section-title">📋 Ürün Performans Tablosu</div>',
    unsafe_allow_html=True
)

urun_tablosu = (
    df.groupby("Urun")
    .agg(
        Toplam_Satis=("Toplam_Satis", "sum"),
        Adet=("Adet", "sum"),
        Ortalama_Fiyat=("Birim_Fiyat", "mean")
    )
    .sort_values(
        "Toplam_Satis",
        ascending=False
    )
    .reset_index()
)

urun_tablosu.columns = [
    "Ürün",
    "Toplam Satış",
    "Adet",
    "Ortalama Fiyat"
]

st.dataframe(
    urun_tablosu,
    use_container_width=True,
    hide_index=True
)


# ==================================================
# AI ASİSTAN
# ==================================================

st.markdown(
    """
    <div class="ai-panel">

        <div class="ai-label">
            ✦ YAPAY ZEKÂ ASİSTANI
        </div>

        <div class="ai-title">
            DataPilot AI
        </div>

        <div class="ai-description">
            Satış verilerinizi analiz edin,
            sorularınızı yazın ve verilerinizden
            anında anlamlı cevaplar alın.
        </div>

        <div style="margin-top:20px;">

            <span class="question-chip">
                En çok satan ürün hangisi?
            </span>

            <span class="question-chip">
                Toplam satış ne kadar?
            </span>

            <span class="question-chip">
                En değerli müşteri segmenti hangisi?
            </span>

            <span class="question-chip">
                En çok hangi ay satış yapıldı?
            </span>

            <span class="question-chip">
                Laptop satışları nasıl?
            </span>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


soru = st.text_input(
    "💬 DataPilot'a sorun",
    placeholder="Örneğin: En değerli müşteri segmenti hangisi?",
    key="ai_question"
)


if soru:

    cevap = answer_question(
        df,
        soru
    )

    st.markdown(
        f"""
        <div style="
            background:
                linear-gradient(
                    135deg,
                    #071A3A,
                    #063B63
                );
            color:white;
            border-radius:22px;
            padding:25px;
            margin-top:15px;
            box-shadow:0 10px 30px rgba(7,26,58,0.15);
        ">

            <div style="
                color:#55E6D8;
                font-size:13px;
                font-weight:700;
                margin-bottom:10px;
            ">
                🤖 DATAPILOT
            </div>

            <div style="
                font-size:16px;
                line-height:1.7;
            ">
                {cevap}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# VERİ ÖZETİ
# ==================================================

st.markdown(
    '<div class="section-title">📌 Veri Özeti</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Veri Satırı",
        f"{len(df):,}"
    )


with col2:

    st.metric(
        "Ürün Sayısı",
        f"{urun_sayisi:,}"
    )


with col3:

    st.metric(
        "Müşteri Segmenti",
        f"{segment_sayisi:,}"
    )


# ==================================================
# VERİ ÖNİZLEME
# ==================================================

with st.expander("📄 Ham Veriyi Görüntüle"):

    st.dataframe(
        df,
        use_container_width=True,
        height=350
    )


# ==================================================
# FOOTER
# ==================================================

st.markdown(
    """
    <div style="
        text-align:center;
        padding:35px 10px 20px 10px;
        color:#64748B;
        font-size:12px;
    ">
        <b style="color:#071A3A;">DataPilot</b>
        • Satış Verileri Analiz ve İş İçgörü Platformu
        <br>
        Veri → Analiz → İçgörü → Karar
    </div>
    """,
    unsafe_allow_html=True
)
