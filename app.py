import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from textwrap import dedent

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
TEXT = "#10213F"
MUTED = "#64748B"


# ==================================================
# TASARIM
# ==================================================

st.markdown(
    dedent(
        """
        <style>
        /* ==================================================
           ANA ARKA PLAN
        ================================================== */

        .stApp {
            background:
                radial-gradient(
                    circle at 92% 7%,
                    rgba(165, 240, 238, 0.24) 0,
                    rgba(165, 240, 238, 0) 27%
                ),
                radial-gradient(
                    circle at 7% 88%,
                    rgba(250, 225, 177, 0.17) 0,
                    rgba(250, 225, 177, 0) 25%
                ),
                linear-gradient(
                    120deg,
                    #FBF6EC 0%,
                    #F8FAFC 46%,
                    #EAFBF8 100%
                );
        }

        .main .block-container {
            max-width: 1510px;
            padding-top: 1rem;
            padding-bottom: 2.5rem;
        }

        header[data-testid="stHeader"] {
            background: rgba(255,255,255,0.70);
            backdrop-filter: blur(12px);
        }


        /* ==================================================
           SIDEBAR
        ================================================== */

        section[data-testid="stSidebar"] {
            width: 235px !important;

            background:
                radial-gradient(
                    circle at 80% 82%,
                    rgba(24,213,192,0.16) 0,
                    rgba(24,213,192,0) 28%
                ),
                linear-gradient(
                    180deg,
                    #041127 0%,
                    #071A3A 58%,
                    #0A4566 100%
                );

            border-right: 1px solid rgba(255,255,255,0.08);
        }

        section[data-testid="stSidebar"] * {
            color: #FFFFFF !important;
        }

        section[data-testid="stSidebar"] .stCaption,
        section[data-testid="stSidebar"] small {
            color: #BFD5E8 !important;
        }

        section[data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.16) !important;
        }


        /* ==================================================
           HERO
        ================================================== */

        .hero-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 30px;

            background:
                linear-gradient(
                    118deg,
                    #FFFCF6 0%,
                    #F9FBFD 47%,
                    #E1FAF7 100%
                );

            border: 1px solid #D7E7F0;

            border-radius: 28px;

            padding: 28px 32px;

            margin-bottom: 12px;

            box-shadow:
                0 14px 34px rgba(7,26,58,0.07);

            overflow: hidden;

            position: relative;
        }

        .hero-container::before {
            content: "";
            position: absolute;

            width: 320px;
            height: 320px;

            right: -125px;
            top: -170px;

            border-radius: 50%;

            background:
                rgba(24,213,192,0.09);
        }

        .hero-copy {
            flex: 1;
            position: relative;
            z-index: 1;
        }

        .hero-small {
            color: #6B9DC4;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.9px;
            margin-bottom: 2px;
        }

        .hero-title {
            color: #071A3A;
            font-size: 42px;
            font-weight: 850;
            letter-spacing: -1.8px;
            margin: 0;
        }

        .hero-highlight {
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

        .hero-description {
            color: #64748B;
            font-size: 15px;
            margin-top: 7px;
        }

        .hero-flow {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;

            margin-top: 17px;

            color: #173556;

            font-size: 13px;
            font-weight: 750;
        }

        .hero-flow span {
            padding: 7px 11px;

            border-radius: 13px;

            background:
                rgba(255,255,255,0.74);

            border: 1px solid #E0ECF3;
        }

        .hero-flow b {
            color: #5A7A98;
        }

        .hero-visual {
            width: 295px;
            min-width: 295px;
            height: 168px;

            border-radius: 24px;

            padding: 15px 19px;

            background:
                linear-gradient(
                    145deg,
                    rgba(235,249,255,0.92),
                    rgba(205,249,243,0.96)
                );

            border: 1px solid #CDE8F0;

            position: relative;
            z-index: 1;

            box-shadow:
                inset 0 1px 0 rgba(255,255,255,0.75);
        }

        .hero-date {
            display: inline-block;

            float: right;

            margin-bottom: 9px;

            padding: 6px 10px;

            border-radius: 14px;

            background:
                rgba(255,255,255,0.86);

            border: 1px solid #D5E5EE;

            color: #35546E;

            font-size: 10px;

            font-weight: 750;
        }

        .hero-visual-top {
            text-align: right;

            color: #2A91C9;

            font-size: 16px;

            font-weight: 800;
        }

        .mini-chart {
            height: 92px;

            display: flex;
            align-items: flex-end;

            gap: 10px;

            padding: 8px 10px 0 10px;

            border-radius: 16px;

            background:
                rgba(255,255,255,0.58);

            border:
                1px solid rgba(255,255,255,0.7);
        }

        .mini-chart i {
            display: block;

            flex: 1;

            border-radius:
                8px 8px 3px 3px;

            background:
                linear-gradient(
                    180deg,
                    #0B63CE,
                    #18D5C0
                );

            box-shadow:
                0 4px 9px rgba(11,99,206,0.12);
        }

        .hero-visual-bottom {
            margin-top: 7px;

            color: #7AAFC4;

            font-size: 11px;

            letter-spacing: 5px;
        }


        /* ==================================================
           TARİH PİLİ
        ================================================== */

        .date-pill {
            display: inline-block;

            width: 100%;

            box-sizing: border-box;

            padding: 10px 14px;

            text-align: center;

            border-radius: 18px;

            background:
                rgba(255,255,255,0.84);

            border: 1px solid #D6E6F0;

            color: #294661;

            font-size: 12px;

            font-weight: 700;

            box-shadow:
                0 6px 18px rgba(7,26,58,0.04);
        }


        /* ==================================================
           KARTLAR
        ================================================== */

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background:
                rgba(255,255,255,0.90);

            border:
                1px solid #DCEAF4 !important;

            border-radius:
                22px !important;

            box-shadow:
                0 9px 26px rgba(7,26,58,0.055);
        }


        /* ==================================================
           METRİKLER
        ================================================== */

        div[data-testid="stMetric"] {
            background:
                transparent !important;

            border:
                none !important;

            box-shadow:
                none !important;

            padding:
                0 !important;
        }

        div[data-testid="stMetricLabel"] {
            color:
                #64748B !important;

            font-size:
                0.78rem !important;
        }

        div[data-testid="stMetricValue"] {
            color:
                #071A3A !important;

            font-weight:
                850 !important;

            letter-spacing:
                -0.5px;
        }

        div[data-testid="stMetricDelta"] {
            font-size:
                0.72rem !important;
        }


        /* ==================================================
           GENEL YAZILAR
        ================================================== */

        .main h1,
        .main h2,
        .main h3,
        .main h4,
        .main h5,
        .main h6,
        .main p,
        .main label {
            color:
                #10213F;
        }

        .main h2,
        .main h3,
        .main h4 {
            font-weight:
                800 !important;
        }

        .main [data-testid="stCaptionContainer"] {
            color:
                #64748B !important;
        }


        /* ==================================================
           INPUT
        ================================================== */

        div[data-baseweb="input"] {
            background:
                #FFFFFF !important;

            border:
                1px solid #C9DDEA !important;

            border-radius:
                15px !important;
        }

        div[data-baseweb="input"] input {
            color:
                #10213F !important;

            background:
                #FFFFFF !important;
        }

        div[data-baseweb="input"] input::placeholder {
            color:
                #8A9AAF !important;
        }


        /* ==================================================
           TABLO
        ================================================== */

        div[data-testid="stDataFrame"] {
            border-radius:
                18px;

            overflow:
                hidden;

            border:
                1px solid #DCEAF4;
        }


        /* ==================================================
           EXPANDER
        ================================================== */

        div[data-testid="stExpander"] {
            background:
                rgba(255,255,255,0.90);

            border:
                1px solid #DCEAF4;

            border-radius:
                18px;
        }


        /* ==================================================
           ALERT
        ================================================== */

        div[data-testid="stAlert"] {
            border-radius:
                15px !important;
        }


        /* ==================================================
           AI
        ================================================== */

        .ai-panel {
            background:
                linear-gradient(
                    115deg,
                    #041127 0%,
                    #082B57 52%,
                    #0A6D72 100%
                );

            border-radius:
                26px;

            padding:
                28px 30px;

            color:
                white;

            box-shadow:
                0 16px 38px rgba(7,26,58,0.16);
        }

        .ai-label {
            color:
                #55E6D8;

            font-size:
                12px;

            font-weight:
                800;

            letter-spacing:
                1px;
        }

        .ai-title {
            color:
                #FFFFFF;

            font-size:
                30px;

            font-weight:
                850;

            margin-top:
                4px;
        }

        .ai-description {
            color:
                #C7D9EA;

            font-size:
                14px;

            line-height:
                1.55;

            margin-top:
                6px;
        }

        .ai-chip {
            display:
                inline-block;

            margin-top:
                14px;

            margin-right:
                8px;

            padding:
                7px 12px;

            border-radius:
                18px;

            border:
                1px solid rgba(255,255,255,0.20);

            background:
                rgba(255,255,255,0.08);

            color:
                #FFFFFF;

            font-size:
                11px;
        }


        /* ==================================================
           FOOTER
        ================================================== */

        .footer {
            text-align:
                center;

            color:
                #64748B;

            font-size:
                12px;

            padding:
                28px 0 8px 0;
        }

        </style>
        """
    ),
    unsafe_allow_html=True
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown("# 📊 DataPilot")

    st.caption(
        "Yapay Zekâ Destekli İş Analitiği"
    )

    st.markdown("### 🧭 Menü")

    st.markdown("📊 Genel Bakış")
    st.markdown("📦 Ürün Analizi")
    st.markdown("👥 Müşteri Analizi")
    st.markdown("📈 Zaman Analizi")
    st.markdown("🤖 AI Asistan")

    st.divider()

    st.markdown("### 📂 Veri Yükle")

    uploaded_file = st.file_uploader(
        "CSV veya Excel dosyanızı yükleyin",
        type=["csv", "xlsx"]
    )

    st.caption(
        "Satış verilerinizi yükleyerek "
        "DataPilot analizini başlatın."
    )


# ==================================================
# DOSYA YÜKLENMEDİ
# ==================================================

if uploaded_file is None:

    st.markdown(
        dedent(
            """
            <div class="hero-container">
                <div class="hero-copy">
                    <div class="hero-small">YAPAY ZEKÂ DESTEKLİ İŞ ANALİZİ</div>
                    <div class="hero-title">Merhaba, <span class="hero-highlight">DataPilot</span></div>
                    <div class="hero-description">Satış verilerinizden anlamlı iş içgörüleri keşfedin.</div>
                    <div class="hero-flow">
                        <span>🗄️ Veri</span>
                        <b>→</b>
                        <span>📊 Analiz</span>
                        <b>→</b>
                        <span>💡 İçgörü</span>
                        <b>→</b>
                        <span>🎯 Karar</span>
                    </div>
                </div>

                <div class="hero-visual">
                    <div class="hero-visual-top">
                        ↗ &nbsp; 📈 &nbsp; ◔
                    </div>

                    <div class="mini-chart">
                        <i style="height:28%"></i>
                        <i style="height:45%"></i>
                        <i style="height:58%"></i>
                        <i style="height:38%"></i>
                        <i style="height:75%"></i>
                        <i style="height:92%"></i>
                    </div>

                    <div class="hero-visual-bottom">
                        ▰ &nbsp; ▰▰ &nbsp; • • •
                    </div>
                </div>
            </div>
            """
        ),
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
        f"Dosya okunurken hata oluştu: {e}"
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
        "Dosyada gerekli sütunlar bulunamadı: "
        + ", ".join(eksik_sutunlar)
    )

    st.stop()


# ==================================================
# VERİ TEMİZLİĞİ
# ==================================================

df["Tarih"] = pd.to_datetime(
    df["Tarih"],
    errors="coerce"
)

df["Adet"] = pd.to_numeric(
    df["Adet"],
    errors="coerce"
).fillna(0)

df["Birim_Fiyat"] = pd.to_numeric(
    df["Birim_Fiyat"],
    errors="coerce"
).fillna(0)

df["Toplam_Satis"] = pd.to_numeric(
    df["Toplam_Satis"],
    errors="coerce"
).fillna(0)


# ==================================================
# HESAPLAMALAR
# ==================================================

toplam_satis = df["Toplam_Satis"].sum()

toplam_adet = df["Adet"].sum()

ortalama_satis = df["Toplam_Satis"].mean()

toplam_islem = len(df)

urun_sayisi = df["Urun"].nunique()

segment_sayisi = df["Musteri_Segmenti"].nunique()


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

segment_satis = (
    df.groupby("Musteri_Segmenti")["Toplam_Satis"]
    .sum()
    .sort_values(ascending=False)
)

en_cok_satan_urun = urun_satis.idxmax()

en_cok_satan_urun_tutari = urun_satis.max()

en_degerli_segment = segment_satis.idxmax()

en_degerli_segment_tutari = segment_satis.max()


# ==================================================
# TARİH
# ==================================================

min_date = df["Tarih"].min()

max_date = df["Tarih"].max()


def turkce_tarih(tarih):

    aylar = [
        "Oca",
        "Şub",
        "Mar",
        "Nis",
        "May",
        "Haz",
        "Tem",
        "Ağu",
        "Eyl",
        "Eki",
        "Kas",
        "Ara"
    ]

    return (
        f"{tarih.day:02d} "
        f"{aylar[tarih.month - 1]} "
        f"{tarih.year}"
    )


if pd.notna(min_date) and pd.notna(max_date):

    tarih_metni = (
        f"📅 {turkce_tarih(min_date)} — "
        f"{turkce_tarih(max_date)}"
    )

else:

    tarih_metni = (
        "📅 Tarih aralığı bulunamadı"
    )


# ==================================================
# HERO
# ==================================================

st.markdown(
    dedent(
        f"""
        <div class="hero-container">

            <div class="hero-copy">

                <div class="hero-small">
                    YAPAY ZEKÂ DESTEKLİ İŞ ANALİZİ
                </div>

                <div class="hero-title">
                    Merhaba,
                    <span class="hero-highlight">
                        DataPilot
                    </span>
                </div>

                <div class="hero-description">
                    Satış verilerinizden anlamlı iş içgörüleri keşfedin.
                </div>

                <div class="hero-flow">

                    <span>
                        🗄️ Veri
                    </span>

                    <b>→</b>

                    <span>
                        📊 Analiz
                    </span>

                    <b>→</b>

                    <span>
                        💡 İçgörü
                    </span>

                    <b>→</b>

                    <span>
                        🎯 Karar
                    </span>

                </div>

            </div>


            <div class="hero-visual">

                <div class="hero-date">
                    {tarih_metni}
                </div>

                <div class="hero-visual-top">
                    ↗ &nbsp; 📈 &nbsp; ◔
                </div>

                <div class="mini-chart">

                    <i style="height:28%"></i>

                    <i style="height:45%"></i>

                    <i style="height:58%"></i>

                    <i style="height:38%"></i>

                    <i style="height:75%"></i>

                    <i style="height:92%"></i>

                </div>

                <div class="hero-visual-bottom">
                    ▰ &nbsp; ▰▰ &nbsp; • • •
                </div>

            </div>

        </div>
        """
    ),
    unsafe_allow_html=True
)


st.markdown(
    "**Veri → Analiz → İçgörü → Karar**"
)


st.success(
    f"✅ {uploaded_file.name} başarıyla yüklendi."
)


# ==================================================
# KPI
# ==================================================

st.markdown(
    "## 📊 İşletme Performansı"
)

k1, k2, k3, k4, k5 = st.columns(5)


with k1:

    with st.container(border=True):

        st.markdown("### 💰")

        st.metric(
            "Toplam Satış",
            f"₺{toplam_satis:,.0f}"
        )

        st.caption(
            "Toplam satış hacmi"
        )


with k2:

    with st.container(border=True):

        st.markdown("### 📦")

        st.metric(
            "Toplam Adet",
            f"{toplam_adet:,.0f}"
        )

        st.caption(
            "Satılan toplam ürün"
        )


with k3:

    with st.container(border=True):

        st.markdown("### 🧾")

        st.metric(
            "İşlem Sayısı",
            f"{toplam_islem:,}"
        )

        st.caption(
            "Toplam satış işlemi"
        )


with k4:

    with st.container(border=True):

        st.markdown("### 💳")

        st.metric(
            "Ortalama Satış",
            f"₺{ortalama_satis:,.0f}"
        )

        st.caption(
            "İşlem başına ortalama"
        )


with k5:

    with st.container(border=True):

        st.markdown("### 👥")

        st.metric(
            "En Değerli Segment",
            en_degerli_segment
        )

        st.caption(
            "En yüksek satış hacmine sahip"
        )


# ==================================================
# AYLIK VERİ
# ==================================================

aylik_df = df.dropna(
    subset=["Tarih"]
).copy()


if not aylik_df.empty:

    aylik_df["Ay"] = (
        aylik_df["Tarih"]
        .dt.to_period("M")
        .astype(str)
    )

    aylik_satis = (
        aylik_df
        .groupby("Ay")["Toplam_Satis"]
        .sum()
    )

    aylik_adet = (
        aylik_df
        .groupby("Ay")["Adet"]
        .sum()
    )

else:

    aylik_satis = pd.Series(
        dtype=float
    )

    aylik_adet = pd.Series(
        dtype=float
    )


def turkce_ay(ay):

    try:

        yil, ay_no = ay.split("-")

        isimler = [
            "Oca",
            "Şub",
            "Mar",
            "Nis",
            "May",
            "Haz",
            "Tem",
            "Ağu",
            "Eyl",
            "Eki",
            "Kas",
            "Ara"
        ]

        return (
            f"{isimler[int(ay_no) - 1]} "
            f"{yil}"
        )

    except Exception:

        return ay


aylik_labels = [
    turkce_ay(x)
    for x in aylik_satis.index
]


# ==================================================
# SATIŞ ANALİZİ
# ==================================================

st.markdown(
    "## 📈 Satış Analizi"
)


col1, col2 = st.columns(
    [1.65, 1]
)


# ==================================================
# AYLIK SATIŞ TRENDİ
# ==================================================

with col1:

    with st.container(border=True):

        st.subheader(
            "📈 Aylık Satış Trendi"
        )

        st.caption(
            "Aylara göre toplam satış performansı"
        )

        fig = go.Figure()


        if not aylik_satis.empty:

            fig.add_trace(
                go.Bar(
                    x=aylik_labels,
                    y=aylik_satis.values,

                    marker=dict(
                        color=aylik_satis.values,

                        colorscale=[
                            [0.0, BLUE],
                            [0.55, CYAN],
                            [1.0, TURQUOISE]
                        ]
                    ),

                    hovertemplate=
                    "%{x}<br>"
                    "₺%{y:,.0f}"
                    "<extra></extra>"
                )
            )


        fig.update_layout(

            height=360,

            margin=dict(
                l=5,
                r=5,
                t=8,
                b=5
            ),

            paper_bgcolor="white",

            plot_bgcolor="white",

            showlegend=False,

            xaxis=dict(
                showgrid=False
            ),

            yaxis=dict(
                title=None,

                gridcolor="#E7EFF5",

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


# ==================================================
# ÜRÜN DAĞILIMI
# ==================================================

with col2:

    with st.container(border=True):

        st.subheader(
            "📦 Ürün Satış Dağılımı"
        )

        st.caption(
            "Ürünlerin toplam satış içindeki payı"
        )


        pie_data = urun_satis.copy()


        if len(pie_data) > 6:

            top_products = (
                pie_data.head(5)
            )

            other_value = (
                pie_data.iloc[5:].sum()
            )

            pie_data = pd.concat(
                [
                    top_products,
                    pd.Series(
                        {
                            "Diğer":
                            other_value
                        }
                    )
                ]
            )


        fig = px.pie(

            names=
            pie_data.index,

            values=
            pie_data.values,

            hole=0.64
        )


        fig.update_traces(

            marker=dict(

                colors=[
                    BLUE,
                    CYAN,
                    TURQUOISE,
                    "#5C8FF7",
                    "#7A8FA8",
                    "#B7C5D4"
                ],

                line=dict(
                    color="white",
                    width=3
                )
            ),

            textinfo="percent",

            hovertemplate=
            "%{label}<br>"
            "₺%{value:,.0f}"
            "<extra></extra>"
        )


        fig.update_layout(

            height=360,

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
# ÜRÜN + SEGMENT
# ==================================================

col1, col2 = st.columns(2)


with col1:

    with st.container(border=True):

        st.subheader(
            "🏆 Ürün Performansı"
        )

        st.caption(
            "Ürün bazında toplam satış"
        )


        fig = px.bar(

            x=urun_satis.values,

            y=urun_satis.index,

            orientation="h"
        )


        fig.update_traces(

            marker_color=BLUE,

            hovertemplate=
            "₺%{x:,.0f}"
            "<extra></extra>"
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

            plot_bgcolor="white",

            xaxis=dict(

                title=None,

                gridcolor="#E7EFF5",

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

        st.subheader(
            "👥 Müşteri Segmenti Analizi"
        )

        st.caption(
            "Segmentlere göre satış hacmi"
        )


        fig = px.bar(

            x=segment_satis.values,

            y=segment_satis.index,

            orientation="h"
        )


        fig.update_traces(

            marker_color=TURQUOISE,

            hovertemplate=
            "₺%{x:,.0f}"
            "<extra></extra>"
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

            plot_bgcolor="white",

            xaxis=dict(

                title=None,

                gridcolor="#E7EFF5",

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
    "## 📅 Zaman Analizi"
)


col1, col2 = st.columns(2)


with col1:

    with st.container(border=True):

        st.subheader(
            "📦 Aylık Ürün Adedi"
        )

        st.caption(
            "Aylara göre satılan toplam ürün"
        )


        fig = go.Figure()


        if not aylik_adet.empty:

            fig.add_trace(

                go.Scatter(

                    x=aylik_labels,

                    y=aylik_adet.values,

                    mode="lines+markers",

                    line=dict(
                        color=TURQUOISE,
                        width=4
                    ),

                    marker=dict(
                        color=BLUE,
                        size=8
                    ),

                    fill="tozeroy",

                    fillcolor=
                    "rgba(24,213,192,0.10)",

                    hovertemplate=
                    "%{x}<br>"
                    "%{y:,.0f} adet"
                    "<extra></extra>"
                )
            )


        fig.update_layout(

            height=330,

            margin=dict(
                l=5,
                r=5,
                t=8,
                b=5
            ),

            paper_bgcolor="white",

            plot_bgcolor="white",

            xaxis=dict(
                showgrid=False
            ),

            yaxis=dict(
                gridcolor="#E7EFF5"
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

        st.subheader(
            "🔄 Satış ve Adet Karşılaştırması"
        )

        st.caption(
            "Aylık satış tutarı ve ürün adedi"
        )


        fig = go.Figure()


        if not aylik_satis.empty:

            fig.add_trace(

                go.Scatter(

                    x=aylik_labels,

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
                    "%{x}<br>"
                    "₺%{y:,.0f}"
                    "<extra></extra>"
                )
            )


            fig.add_trace(

                go.Scatter(

                    x=aylik_labels,

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
                    "%{x}<br>"
                    "%{y:,.0f} adet"
                    "<extra></extra>"
                )
            )


        fig.update_layout(

            height=330,

            margin=dict(
                l=5,
                r=5,
                t=8,
                b=5
            ),

            paper_bgcolor="white",

            plot_bgcolor="white",

            yaxis=dict(

                title="Satış",

                gridcolor="#E7EFF5",

                tickprefix="₺",

                tickformat=","
            ),

            yaxis2=dict(

                title="Adet",

                overlaying="y",

                side="right"
            ),

            legend=dict(
                orientation="h",
                y=1.08
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
    "## 💡 Otomatik İş İçgörüleri"
)


urun_payi = (

    (
        en_cok_satan_urun_tutari
        / toplam_satis
    )
    * 100

    if toplam_satis > 0

    else 0
)


i1, i2, i3 = st.columns(3)


with i1:

    with st.container(border=True):

        st.subheader(
            "🏆 Ürün Performansı"
        )

        st.metric(
            "En yüksek satış yapan ürün",
            en_cok_satan_urun
        )

        st.write(
            f"Toplam satışların yaklaşık "
            f"**%{urun_payi:.1f}**'ini oluşturuyor."
        )

        st.caption(
            f"Satış tutarı: "
            f"₺{en_cok_satan_urun_tutari:,.0f}"
        )


with i2:

    with st.container(border=True):

        st.subheader(
            "👥 Müşteri Analizi"
        )

        st.metric(
            "En yüksek satış segmenti",
            en_degerli_segment
        )

        st.write(
            "En yüksek satış hacmine sahip "
            "müşteri segmentidir."
        )

        st.caption(
            f"Satış tutarı: "
            f"₺{en_degerli_segment_tutari:,.0f}"
        )


with i3:

    with st.container(border=True):

        st.subheader(
            "💳 Ortalama İşlem"
        )

        st.metric(
            "Ortalama satış",
            f"₺{ortalama_satis:,.0f}"
        )

        st.write(
            "İşlem başına gerçekleşen "
            "ortalama satış tutarıdır."
        )


# ==================================================
# ÜRÜN PERFORMANS TABLOSU
# ==================================================

st.markdown(
    "## 📋 Ürün Performans Tablosu"
)


urun_tablosu = (

    df.groupby("Urun")

    .agg(

        Toplam_Satis=(
            "Toplam_Satis",
            "sum"
        ),

        Adet=(
            "Adet",
            "sum"
        ),

        Ortalama_Fiyat=(
            "Birim_Fiyat",
            "mean"
        )
    )

    .sort_values(
        "Toplam_Satis",
        ascending=False
    )

    .reset_index()
)


urun_tablosu["Satis_Payi"] = (

    urun_tablosu["Toplam_Satis"]
    / toplam_satis
    * 100

    if toplam_satis > 0

    else 0
)


urun_tablosu.columns = [

    "Ürün",

    "Toplam Satış",

    "Adet",

    "Ortalama Fiyat",

    "Satış Payı"
]


urun_tablosu["Toplam Satış"] = (

    urun_tablosu[
        "Toplam Satış"
    ].round(0)
)


urun_tablosu["Ortalama Fiyat"] = (

    urun_tablosu[
        "Ortalama Fiyat"
    ].round(0)
)


urun_tablosu["Satış Payı"] = (

    urun_tablosu[
        "Satış Payı"
    ]
    .round(1)
    .map(
        lambda x:
        f"%{x:.1f}"
    )
)


st.dataframe(

    urun_tablosu,

    use_container_width=True,

    hide_index=True
)


# ==================================================
# DATAPILOT AI
# ==================================================

st.markdown(
    "## 🤖 DataPilot AI"
)


st.markdown(
    dedent(
        """
        <div class="ai-panel">

            <div class="ai-label">
                YAPAY ZEKÂ ASİSTANI
            </div>

            <div class="ai-title">
                DataPilot AI
            </div>

            <div class="ai-description">
                Satış verilerinizi analiz edin,
                sorularınızı yazın ve verilerinizden
                anlamlı cevaplar alın.
            </div>

            <span class="ai-chip">
                En çok satan ürün hangisi?
            </span>

            <span class="ai-chip">
                Toplam satış ne kadar?
            </span>

            <span class="ai-chip">
                En değerli müşteri segmenti hangisi?
            </span>

            <span class="ai-chip">
                Genel performans nasıl?
            </span>

        </div>
        """
    ),
    unsafe_allow_html=True
)


soru = st.text_input(

    "💬 DataPilot'a sorun",

    placeholder=
    "Örneğin: En değerli müşteri segmenti hangisi?",

    key="ai_question"
)


if soru:

    cevap = answer_question(
        df,
        soru
    )

    with st.container(border=True):

        st.markdown(
            "### 🤖 DataPilot'ın Cevabı"
        )

        st.info(
            cevap
        )


# ==================================================
# VERİ ÖZETİ
# ==================================================

st.markdown(
    "## 📌 Veri Özeti"
)


o1, o2, o3 = st.columns(3)


with o1:

    with st.container(border=True):

        st.metric(
            "Veri Satırı",
            f"{len(df):,}"
        )


with o2:

    with st.container(border=True):

        st.metric(
            "Ürün Sayısı",
            f"{urun_sayisi:,}"
        )


with o3:

    with st.container(border=True):

        st.metric(
            "Müşteri Segmenti",
            f"{segment_sayisi:,}"
        )


# ==================================================
# HAM VERİ
# ==================================================

with st.expander(
    "📄 Ham Veriyi Görüntüle"
):

    st.dataframe(

        df,

        use_container_width=True,

        height=350
    )


# ==================================================
# FOOTER
# ==================================================

st.markdown(

    "<div class='footer'>"
    "<b>DataPilot</b> • "
    "Satış Verileri Analiz ve İş İçgörü Platformu"
    "<br>"
    "Veri → Analiz → İçgörü → Karar"
    "</div>",

    unsafe_allow_html=True
)
