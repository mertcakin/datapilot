import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from ai_assistant import answer_question


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
# RENK PALETİ
# ==================================================

NAVY = "#071A3A"
DARK_NAVY = "#041127"
BLUE = "#0B63CE"
CYAN = "#06B6D4"
TURQUOISE = "#18D5C0"
LIGHT_BLUE = "#38BDF8"
WHITE = "#FFFFFF"
LIGHT_BG = "#F4F8FC"
TEXT = "#10213F"
MUTED = "#64748B"


# ==================================================
# CSS
# ==================================================

st.markdown(
    """
    <style>

    /* ==============================
       GENEL
    ============================== */

    .stApp {
        background:
            linear-gradient(
                135deg,
                #F7FBFF 0%,
                #EFF8FF 55%,
                #F1FFFD 100%
            );
    }

    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }


    /* ==============================
       SIDEBAR
    ============================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #041127 0%,
                #071A3A 55%,
                #063B63 100%
            );
    }

    section[data-testid="stSidebar"] * {
        color: #FFFFFF;
    }

    .sidebar-title {
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 3px;
    }

    .sidebar-subtitle {
        color: #AFC8E4 !important;
        font-size: 12px;
        margin-bottom: 25px;
    }

    .sidebar-divider {
        height: 1px;
        background: rgba(255,255,255,0.16);
        margin: 20px 0;
    }


    /* ==============================
       HERO
    ============================== */

    .hero-box {
        background:
            linear-gradient(
                120deg,
                #FFFFFF 0%,
                #F5FBFF 48%,
                #DDFBF8 100%
            );
        border: 1px solid #D9EAF5;
        border-radius: 28px;
        padding: 30px 34px;
        margin-bottom: 24px;
        box-shadow:
            0 12px 35px rgba(7,26,58,0.08);
    }

    .hero-title {
        font-size: 39px;
        font-weight: 800;
        color: #071A3A;
        letter-spacing: -1.5px;
        margin-bottom: 5px;
    }

    .hero-gradient {
        background:
            linear-gradient(
                90deg,
                #0B63CE,
                #06B6D4,
                #18D5C0
            );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        color: #64748B;
        font-size: 16px;
        margin-bottom: 12px;
    }

    .hero-tagline {
        color: #071A3A;
        font-size: 14px;
        font-weight: 700;
    }


    /* ==============================
       SECTION BAŞLIKLARI
    ============================== */

    .section-title {
        color: #071A3A;
        font-size: 23px;
        font-weight: 800;
        margin-top: 30px;
        margin-bottom: 14px;
    }


    /* ==============================
       KPI
    ============================== */

    div[data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                #FFFFFF,
                #F8FCFF
            );
        border: 1px solid #DCEAF4;
        border-radius: 22px;
        padding: 18px;
        box-shadow:
            0 8px 25px rgba(7,26,58,0.06);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748B !important;
    }

    div[data-testid="stMetricValue"] {
        color: #071A3A !important;
        font-weight: 800;
    }


    /* ==============================
       GRAFİK CONTAINER
    ============================== */

    .chart-header {
        color: #071A3A;
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 2px;
    }

    .chart-description {
        color: #64748B;
        font-size: 12px;
        margin-bottom: 8px;
    }


    /* ==============================
       INSIGHT
    ============================== */

    .insight-title {
        color: #071A3A;
        font-size: 17px;
        font-weight: 800;
    }

    .insight-value {
        color: #0B63CE;
        font-size: 21px;
        font-weight: 800;
        margin: 8px 0;
    }

    .insight-description {
        color: #64748B;
        font-size: 13px;
        line-height: 1.5;
    }


    /* ==============================
       AI
    ============================== */

    .ai-label {
        color: #55E6D8;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    .ai-title {
        color: #FFFFFF;
        font-size: 30px;
        font-weight: 800;
        margin-top: 3px;
    }

    .ai-description {
        color: #C7D9EA;
        font-size: 14px;
        line-height: 1.6;
    }


    /* ==============================
       DOSYA YÜKLEME
    ============================== */

    div[data-testid="stFileUploader"] {
        border-radius: 18px;
    }


    /* ==============================
       INPUT
    ============================== */

    div[data-baseweb="input"] {
        border-radius: 15px !important;
    }


    /* ==============================
       BUTTON
    ============================== */

    .stButton > button {
        border-radius: 14px;
        border: none;
        background:
            linear-gradient(
                90deg,
                #0B63CE,
                #18D5C0
            );
        color: #FFFFFF;
        font-weight: 700;
    }


    /* ==============================
       TABLE
    ============================== */

    div[data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
        border: 1px solid #DCEAF4;
    }


    /* ==============================
       EXPANDER
    ============================== */

    div[data-testid="stExpander"] {
        border-radius: 18px;
        border: 1px solid #DCEAF4;
        background: #FFFFFF;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown(
        "📊 **DataPilot**",
        unsafe_allow_html=False
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

    st.markdown(
        '<div class="sidebar-divider"></div>',
        unsafe_allow_html=True
    )

    st.markdown("### 📂 Veri Yükle")

    uploaded_file = st.file_uploader(
        "CSV veya Excel dosyanızı yükleyin",
        type=["csv", "xlsx"]
    )

    st.markdown(
        """
        <div style="
            padding:18px;
            margin-top:15px;
            border-radius:20px;
            background:rgba(255,255,255,0.08);
            border:1px solid rgba(255,255,255,0.15);
            text-align:center;
        ">
            ☁️
            <br><br>
            <b>Verinizi Analiz Edin</b>
            <br>
            <span style="
                color:#AFC8E4;
                font-size:12px;
            ">
            CSV veya Excel dosyanızı yükleyin.
            </span>
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
        <div class="hero-box">

            <div class="hero-title">
                Merhaba, 
                <span class="hero-gradient">
                    DataPilot
                </span>
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

    st.info(
        "👈 Analize başlamak için sol menüden "
        "CSV veya Excel dosyanızı yükleyin."
    )

    st.stop()


# ==================================================
# VERİ OKUMA
# ==================================================

try:

    if uploaded_file.name.lower().endswith(".csv"):

        df = pd.read_csv(uploaded_file)

    else:

        df = pd.read_excel(uploaded_file)

except Exception as e:

    st.error(
        f"❌ Dosya okunurken hata oluştu: {e}"
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
        "❌ Eksik sütunlar: "
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

tarih_df = df.dropna(
    subset=["Tarih"]
).copy()

if not tarih_df.empty:

    aylik_satis = (
        tarih_df.groupby(
            tarih_df["Tarih"].dt.to_period("M")
        )["Toplam_Satis"]
        .sum()
    )

    aylik_adet = (
        tarih_df.groupby(
            tarih_df["Tarih"].dt.to_period("M")
        )["Adet"]
        .sum()
    )

    aylik_satis.index = aylik_satis.index.astype(str)

    aylik_adet.index = aylik_adet.index.astype(str)

else:

    aylik_satis = pd.Series(dtype="float64")

    aylik_adet = pd.Series(dtype="float64")


# ==================================================
# HERO
# ==================================================

st.markdown(
    """
    <div class="hero-box">

        <div class="hero-title">
            Merhaba,
            <span class="hero-gradient">
                DataPilot
            </span>
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
# KPI
# ==================================================

st.markdown(
    '<div class="section-title">📊 İşletme Performansı</div>',
    unsafe_allow_html=True
)

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)


with kpi1:

    st.metric(
        "💰 Toplam Satış",
        f"₺{toplam_satis:,.0f}"
    )


with kpi2:

    st.metric(
        "📦 Toplam Adet",
        f"{toplam_adet:,.0f}"
    )


with kpi3:

    st.metric(
        "🧾 İşlem Sayısı",
        f"{toplam_islem:,}"
    )


with kpi4:

    st.metric(
        "💳 Ortalama Satış",
        f"₺{ortalama_satis:,.0f}"
    )


with kpi5:

    st.metric(
        "👥 En Değerli Segment",
        en_degerli_segment
    )


# ==================================================
# SATIŞ TRENDİ + ÜRÜN DAĞILIMI
# ==================================================

st.markdown(
    '<div class="section-title">📈 Satış Analizi</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([1.6, 1])


# --------------------------------------------------
# AYLIK SATIŞ
# --------------------------------------------------

with col1:

    with st.container(border=True):

        st.markdown(
            '<div class="chart-header">📈 Aylık Satış Trendi</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="chart-description">'
            'Aylara göre toplam satış performansı'
            '</div>',
            unsafe_allow_html=True
        )

        if not aylik_satis.empty:

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=aylik_satis.index,
                    y=aylik_satis.values,
                    marker=dict(
                        color=aylik_satis.values,
                        colorscale=[
                            [0, "#0B63CE"],
                            [0.5, "#06B6D4"],
                            [1, "#18D5C0"]
                        ]
                    ),
                    hovertemplate=
                    "Satış: ₺%{y:,.0f}<extra></extra>"
                )
            )

            fig.update_layout(
                height=350,
                margin=dict(
                    l=10,
                    r=10,
                    t=10,
                    b=10
                ),
                paper_bgcolor="white",
                plot_bgcolor="white",
                showlegend=False,
                xaxis=dict(
                    showgrid=False
                ),
                yaxis=dict(
                    gridcolor="#E8F0F6",
                    tickprefix="₺",
                    tickformat=","
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )


# --------------------------------------------------
# ÜRÜN DAĞILIMI
# --------------------------------------------------

with col2:

    with st.container(border=True):

        st.markdown(
            '<div class="chart-header">📦 Ürün Satış Dağılımı</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="chart-description">'
            'Ürünlerin toplam satış içindeki payı'
            '</div>',
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
                    "#06B6D4",
                    "#18D5C0",
                    "#38BDF8",
                    "#64748B"
                ],
                line=dict(
                    color="white",
                    width=3
                )
            ),
            textinfo="percent",
            hovertemplate=
            "%{label}<br>₺%{value:,.0f}<extra></extra>"
        )

        fig.update_layout(
            height=350,
            margin=dict(
                l=5,
                r=5,
                t=5,
                b=5
            ),
            paper_bgcolor="white",
            showlegend=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )


# ==================================================
# ÜRÜN + SEGMENT GRAFİKLERİ
# ==================================================

col1, col2 = st.columns(2)


with col1:

    with st.container(border=True):

        st.markdown(
            '<div class="chart-header">🏆 Ürün Performansı</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="chart-description">'
            'Ürün bazında toplam satış'
            '</div>',
            unsafe_allow_html=True
        )

        fig = px.bar(
            x=urun_satis.values,
            y=urun_satis.index,
            orientation="h"
        )

        fig.update_traces(
            marker_color="#0B63CE",
            hovertemplate=
            "₺%{x:,.0f}<extra></extra>"
        )

        fig.update_layout(
            height=350,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis=dict(
                gridcolor="#E8F0F6",
                tickprefix="₺",
                tickformat=","
            ),
            yaxis=dict(
                title=None
            ),
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )


with col2:

    with st.container(border=True):

        st.markdown(
            '<div class="chart-header">👥 Müşteri Segmenti Analizi</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="chart-description">'
            'Segmentlere göre satış hacmi'
            '</div>',
            unsafe_allow_html=True
        )

        fig = px.bar(
            x=segment_satis.values,
            y=segment_satis.index,
            orientation="h"
        )

        fig.update_traces(
            marker_color="#18D5C0",
            hovertemplate=
            "₺%{x:,.0f}<extra></extra>"
        )

        fig.update_layout(
            height=350,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis=dict(
                gridcolor="#E8F0F6",
                tickprefix="₺",
                tickformat=","
            ),
            yaxis=dict(
                title=None
            ),
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )


# ==================================================
# ZAMAN ANALİZİ
# ==================================================

st.markdown(
    '<div class="section-title">📅 Zaman Analizi</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


with col1:

    with st.container(border=True):

        st.markdown(
            '<div class="chart-header">📦 Aylık Ürün Adedi</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="chart-description">'
            'Aylara göre satılan toplam ürün'
            '</div>',
            unsafe_allow_html=True
        )

        if not aylik_adet.empty:

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
                        color=BLUE,
                        size=9
                    ),
                    fill="tozeroy",
                    fillcolor="rgba(24,213,192,0.10)",
                    hovertemplate=
                    "%{y:,.0f} adet<extra></extra>"
                )
            )

            fig.update_layout(
                height=330,
                margin=dict(
                    l=10,
                    r=10,
                    t=10,
                    b=10
                ),
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
                config={
                    "displayModeBar": False
                }
            )


with col2:

    with st.container(border=True):

        st.markdown(
            '<div class="chart-header">🔄 Satış ve Adet Karşılaştırması</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="chart-description">'
            'Aylık satış tutarı ve ürün adedi'
            '</div>',
            unsafe_allow_html=True
        )

        if not aylik_satis.empty:

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
                    marker=dict(
                        size=8
                    ),
                    hovertemplate=
                    "₺%{y:,.0f}<extra></extra>"
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
                    marker=dict(
                        size=8
                    ),
                    yaxis="y2",
                    hovertemplate=
                    "%{y:,.0f} adet<extra></extra>"
                )
            )

            fig.update_layout(
                height=330,
                margin=dict(
                    l=10,
                    r=10,
                    t=10,
                    b=10
                ),
                paper_bgcolor="white",
                plot_bgcolor="white",
                yaxis=dict(
                    title="Satış",
                    tickprefix="₺",
                    tickformat=",",
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
                config={
                    "displayModeBar": False
                }
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

    with st.container(border=True):

        st.markdown(
            '<div class="insight-title">🏆 Ürün Performansı</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="insight-value">'
            f'{en_cok_satan_urun}'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="insight-description">
                Toplam satışların yaklaşık
                <b>%{urun_payi:.1f}</b>'ini
                oluşturuyor.
                <br><br>
                Satış tutarı:
                <b>₺{en_cok_satan_urun_tutari:,.0f}</b>
            </div>
            """,
            unsafe_allow_html=True
        )


with insight2:

    with st.container(border=True):

        st.markdown(
            '<div class="insight-title">👥 Müşteri Analizi</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="insight-value">'
            f'{en_degerli_segment}'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="insight-description">
                En yüksek satış hacmine sahip
                müşteri segmentidir.
                <br><br>
                Satış tutarı:
                <b>₺{en_degerli_segment_tutari:,.0f}</b>
            </div>
            """,
            unsafe_allow_html=True
        )


with insight3:

    with st.container(border=True):

        st.markdown(
            '<div class="insight-title">💳 Ortalama İşlem</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="insight-value">'
            f'₺{ortalama_satis:,.0f}'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="insight-description">
                İşlem başına gerçekleşen
                ortalama satış tutarıdır.
            </div>
            """,
            unsafe_allow_html=True
        )


# ==================================================
# ÜRÜN PERFORMANS TABLOSU
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
    '<div class="section-title">🤖 DataPilot AI</div>',
    unsafe_allow_html=True
)

with st.container(border=True):

    st.markdown(
        '<div class="ai-label">YAPAY ZEKÂ ASİSTANI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="ai-title">DataPilot AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="ai-description">'
        'Satış verilerinizi analiz edin, sorularınızı yazın '
        've verilerinizden anlamlı cevaplar alın.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("")

    st.markdown(
        "**💬 Örnek sorular**"
    )

    q1, q2, q3 = st.columns(3)

    with q1:
        st.caption("• En çok satan ürün hangisi?")
        st.caption("• Toplam satış ne kadar?")

    with q2:
        st.caption("• En değerli müşteri segmenti hangisi?")
        st.caption("• En çok hangi ay satış yapıldı?")

    with q3:
        st.caption("• Laptop satışları nasıl?")
        st.caption("• Genel performans nasıl?")


# ==================================================
# AI SORU ALANI
# ==================================================

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

    st.markdown("### 🤖 DataPilot'ın Cevabı")

    with st.container(border=True):

        st.info(
            cevap
        )


# ==================================================
# VERİ ÖZETİ
# ==================================================

st.markdown(
    '<div class="section-title">📌 Veri Özeti</div>',
    unsafe_allow_html=True
)

ozet1, ozet2, ozet3 = st.columns(3)


with ozet1:

    st.metric(
        "Veri Satırı",
        f"{len(df):,}"
    )


with ozet2:

    st.metric(
        "Ürün Sayısı",
        f"{urun_sayisi:,}"
    )


with ozet3:

    st.metric(
        "Müşteri Segmenti",
        f"{segment_sayisi:,}"
    )


# ==================================================
# HAM VERİ
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

st.divider()

st.caption(
    "DataPilot • Satış Verileri Analiz ve İş İçgörü Platformu • "
    "Veri → Analiz → İçgörü → Karar"
)
