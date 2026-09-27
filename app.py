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
# RENKLER
# ==================================================

NAVY = "#06152F"
NAVY_2 = "#0A2145"
BLUE = "#0878FF"
CYAN = "#08C8E8"
TURQUOISE = "#19E0C5"
WHITE = "#F7FBFF"
TEXT = "#F5F9FF"
MUTED = "#9EB3CC"
BORDER = "#164B7D"
CARD = "#091E3D"


# ==================================================
# KOYU TEMA TASARIMI
# ==================================================

st.markdown(
    dedent(
        f"""
        <style>
        /* =========================
           GLOBAL
        ========================= */

        .stApp {{
            background:
                radial-gradient(
                    circle at 82% 8%,
                    rgba(8,200,232,0.13) 0,
                    rgba(8,200,232,0) 25%
                ),
                radial-gradient(
                    circle at 10% 90%,
                    rgba(8,120,255,0.14) 0,
                    rgba(8,120,255,0) 28%
                ),
                linear-gradient(
                    135deg,
                    #041127 0%,
                    #06152F 45%,
                    #082746 100%
                );
            color: {TEXT};
        }}

        .main .block-container {{
            max-width: 1540px;
            padding-top: 1rem;
            padding-bottom: 3rem;
        }}

        header[data-testid="stHeader"] {{
            background: rgba(4,17,39,0.86);
        }}

        /* =========================
           SIDEBAR
        ========================= */

        section[data-testid="stSidebar"] {{
            background:
                radial-gradient(
                    circle at 80% 85%,
                    rgba(25,224,197,0.13) 0,
                    rgba(25,224,197,0) 28%
                ),
                linear-gradient(
                    180deg,
                    #031025 0%,
                    #061A38 60%,
                    #072B4D 100%
                );
            border-right: 1px solid #123E68;
        }}

        section[data-testid="stSidebar"] * {{
            color: #FFFFFF !important;
        }}

        section[data-testid="stSidebar"] .stCaption {{
            color: #AFC7DE !important;
        }}

        section[data-testid="stSidebar"] hr {{
            border-color: rgba(255,255,255,0.14) !important;
        }}

        /* =========================
           HERO
        ========================= */

        .hero {{
            position: relative;
            overflow: hidden;

            background:
                radial-gradient(
                    circle at 78% 38%,
                    rgba(8,200,232,0.16) 0,
                    rgba(8,200,232,0) 23%
                ),
                linear-gradient(
                    125deg,
                    #071A39 0%,
                    #082D59 58%,
                    #075C68 100%
                );

            border: 1px solid #0A68A5;
            border-radius: 28px;
            padding: 30px 34px;
            margin-bottom: 16px;

            box-shadow:
                0 18px 50px rgba(0,0,0,0.28);
        }}

        .hero::after {{
            content: "";
            position: absolute;
            width: 420px;
            height: 420px;
            right: -130px;
            top: -210px;
            border-radius: 50%;
            border: 1px solid rgba(8,200,232,0.18);
            box-shadow:
                0 0 0 35px rgba(8,120,255,0.04),
                0 0 0 75px rgba(8,120,255,0.025);
        }}

        .hero-copy {{
            position: relative;
            z-index: 2;
        }}

        .hero-small {{
            color: #25D7F2;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 1px;
        }}

        .hero-title {{
            color: #FFFFFF;
            font-size: 44px;
            font-weight: 850;
            letter-spacing: -1.8px;
            margin: 3px 0 5px;
        }}

        .hero-highlight {{
            background:
                linear-gradient(
                    90deg,
                    #0B7CFF,
                    #08C8E8,
                    #19E0C5
                );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .hero-description {{
            color: #D3E3F2;
            font-size: 16px;
        }}

        .hero-flow {{
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 18px;
        }}

        .hero-flow span {{
            color: #FFFFFF;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.16);
            border-radius: 18px;
            padding: 8px 13px;
            font-size: 12px;
            font-weight: 750;
            backdrop-filter: blur(8px);
        }}

        .hero-flow b {{
            color: #26DDF2;
        }}

        .hero-visual {{
            position: absolute;
            z-index: 1;
            right: 28px;
            top: 28px;
            width: 315px;
            height: 170px;
            padding: 16px;
            border-radius: 22px;
            background: rgba(4,20,48,0.38);
            border: 1px solid rgba(53,208,255,0.25);
        }}

        .mini-chart {{
            height: 112px;
            display: flex;
            align-items: flex-end;
            gap: 10px;
            padding: 14px 12px 0;
            border-radius: 16px;
            background: rgba(255,255,255,0.035);
        }}

        .mini-chart i {{
            flex: 1;
            display: block;
            border-radius: 8px 8px 3px 3px;
            background: linear-gradient(
                180deg,
                #08C8E8,
                #0878FF
            );
            box-shadow: 0 0 16px rgba(8,200,232,0.18);
        }}

        .hero-date {{
            float: right;
            color: #DCEEFF;
            font-size: 10px;
            font-weight: 700;
            padding: 5px 9px;
            border: 1px solid rgba(255,255,255,0.17);
            border-radius: 13px;
            background: rgba(255,255,255,0.06);
        }}

        /* =========================
           HEADINGS / TEXT
        ========================= */

        .main h1,
        .main h2,
        .main h3,
        .main h4,
        .main h5,
        .main h6,
        .main p,
        .main label,
        .main span,
        .main div {{
            color: inherit;
        }}

        .main h2,
        .main h3,
        .main h4 {{
            color: #FFFFFF !important;
            font-weight: 800 !important;
        }}

        .main [data-testid="stCaptionContainer"] {{
            color: #9EB3CC !important;
        }}

        /* =========================
           CONTAINER / CARDS
        ========================= */

        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background:
                linear-gradient(
                    145deg,
                    rgba(10,33,69,0.96),
                    rgba(5,24,49,0.96)
                );

            border: 1px solid #164B7D !important;
            border-radius: 22px !important;

            box-shadow:
                0 10px 30px rgba(0,0,0,0.20);
        }}

        /* =========================
           METRICS
        ========================= */

        div[data-testid="stMetric"] {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
        }}

        div[data-testid="stMetricLabel"] {{
            color: #9EB3CC !important;
        }}

        div[data-testid="stMetricValue"] {{
            color: #FFFFFF !important;
            font-weight: 850 !important;
        }}

        div[data-testid="stMetricDelta"] {{
            color: #19E0C5 !important;
        }}

        /* =========================
           INPUT
        ========================= */

        div[data-baseweb="input"] {{
            background: #071A34 !important;
            border: 1px solid #1A5A8F !important;
            border-radius: 15px !important;
        }}

        div[data-baseweb="input"]:focus-within {{
            border-color: #08C8E8 !important;
            box-shadow: 0 0 0 1px #08C8E8 !important;
        }}

        div[data-baseweb="input"] input {{
            color: #FFFFFF !important;
            background: #071A34 !important;
        }}

        div[data-baseweb="input"] input::placeholder {{
            color: #7894B0 !important;
        }}

        /* =========================
           ALERTS
        ========================= */

        div[data-testid="stAlert"] {{
            border-radius: 15px !important;
        }}

        /* =========================
           DATAFRAME
        ========================= */

        div[data-testid="stDataFrame"] {{
            border-radius: 18px;
            overflow: hidden;
            border: 1px solid #164B7D;
        }}

        /* =========================
           EXPANDER
        ========================= */

        div[data-testid="stExpander"] {{
            background: #081C39 !important;
            border: 1px solid #164B7D !important;
            border-radius: 18px !important;
        }}

        /* =========================
           AI PANEL
        ========================= */

        .ai-panel {{
            background:
                radial-gradient(
                    circle at 85% 20%,
                    rgba(25,224,197,0.15) 0,
                    rgba(25,224,197,0) 25%
                ),
                linear-gradient(
                    120deg,
                    #031027 0%,
                    #062452 54%,
                    #075E68 100%
                );

            border: 1px solid #0C7195;
            border-radius: 26px;
            padding: 28px 30px;

            box-shadow:
                0 18px 45px rgba(0,0,0,0.25);
        }}

        .ai-label {{
            color: #25D7F2 !important;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 1px;
        }}

        .ai-title {{
            color: #FFFFFF !important;
            font-size: 30px;
            font-weight: 850;
            margin-top: 4px;
        }}

        .ai-description {{
            color: #C9DDED !important;
            font-size: 14px;
            line-height: 1.55;
        }}

        .ai-chip {{
            display: inline-block;
            margin-top: 14px;
            margin-right: 7px;
            padding: 7px 12px;
            border-radius: 18px;
            border: 1px solid rgba(255,255,255,0.18);
            background: rgba(255,255,255,0.06);
            color: #FFFFFF !important;
            font-size: 11px;
        }}

        /* =========================
           FOOTER
        ========================= */

        .footer {{
            text-align: center;
            color: #7894B0 !important;
            font-size: 12px;
            padding: 30px 0 10px;
        }}

        /* =========================
           SCROLLBAR
        ========================= */

        ::-webkit-scrollbar {{
            width: 9px;
        }}

        ::-webkit-scrollbar-track {{
            background: #041127;
        }}

        ::-webkit-scrollbar-thumb {{
            background: #164B7D;
            border-radius: 10px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: #0878FF;
        }}
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

    st.caption("Yapay Zekâ Destekli İş Analitiği")

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

    st.info(
        "Satış verilerinizi yükleyerek "
        "DataPilot analizini başlatın."
    )


# ==================================================
# DOSYA YOKSA
# ==================================================

if uploaded_file is None:

    st.markdown(
        dedent(
            """
            <div class="hero">

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

                    <div class="mini-chart">
                        <i style="height:28%"></i>
                        <i style="height:45%"></i>
                        <i style="height:58%"></i>
                        <i style="height:38%"></i>
                        <i style="height:75%"></i>
                        <i style="height:92%"></i>
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
# SÜTUN KONTROLÜ
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

for column in ["Adet", "Birim_Fiyat", "Toplam_Satis"]:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    ).fillna(0)


# ==================================================
# TEMEL ANALİZLER
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
        "Oca", "Şub", "Mar", "Nis",
        "May", "Haz", "Tem", "Ağu",
        "Eyl", "Eki", "Kas", "Ara"
    ]

    return (
        f"{tarih.day:02d} "
        f"{aylar[tarih.month - 1]} "
        f"{tarih.year}"
    )


if pd.notna(min_date) and pd.notna(max_date):

    tarih_metni = (
        f"{turkce_tarih(min_date)} — "
        f"{turkce_tarih(max_date)}"
    )

else:

    tarih_metni = "Tarih aralığı bulunamadı"


# ==================================================
# HERO
# ==================================================

hero_html = f"""<div class="hero"><div class="hero-copy"><div class="hero-small">YAPAY ZEKÂ DESTEKLİ İŞ ANALİZİ</div><div class="hero-title">Merhaba, <span class="hero-highlight">DataPilot</span></div><div class="hero-description">Satış verilerinizden anlamlı iş içgörüleri keşfedin.</div><div class="hero-flow"><span>🗄️ Veri</span><b>→</b><span>📊 Analiz</span><b>→</b><span>💡 İçgörü</span><b>→</b><span>🎯 Karar</span></div></div><div class="hero-visual"><div class="hero-date">📅 {tarih_metni}</div><div class="mini-chart"><i style="height:28%"></i><i style="height:45%"></i><i style="height:58%"></i><i style="height:38%"></i><i style="height:75%"></i><i style="height:92%"></i></div></div></div>"""

st.markdown(
    hero_html,
    unsafe_allow_html=True
)

st.success(
    f"✓ {uploaded_file.name} başarıyla yüklendi."
)


# ==================================================
# KPI
# ==================================================

st.markdown("## 📊 İşletme Performansı")

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    with st.container(border=True):
        st.markdown("### 💰")
        st.metric(
            "Toplam Satış",
            f"₺{toplam_satis:,.0f}"
        )
        st.caption("Toplam satış hacmi")

with k2:
    with st.container(border=True):
        st.markdown("### 📦")
        st.metric(
            "Toplam Adet",
            f"{toplam_adet:,.0f}"
        )
        st.caption("Satılan toplam ürün")

with k3:
    with st.container(border=True):
        st.markdown("### 🧾")
        st.metric(
            "İşlem Sayısı",
            f"{toplam_islem:,}"
        )
        st.caption("Toplam satış işlemi")

with k4:
    with st.container(border=True):
        st.markdown("### 💳")
        st.metric(
            "Ortalama Satış",
            f"₺{ortalama_satis:,.0f}"
        )
        st.caption("İşlem başına ortalama")

with k5:
    with st.container(border=True):
        st.markdown("### 👥")
        st.metric(
            "En Değerli Segment",
            en_degerli_segment
        )
        st.caption("En yüksek satış hacmi")


# ==================================================
# AYLIK VERİ
# ==================================================

tarih_df = df.dropna(
    subset=["Tarih"]
).copy()

if not tarih_df.empty:

    tarih_df["Ay"] = (
        tarih_df["Tarih"]
        .dt.to_period("M")
        .astype(str)
    )

    aylik_satis = (
        tarih_df
        .groupby("Ay")["Toplam_Satis"]
        .sum()
    )

    aylik_adet = (
        tarih_df
        .groupby("Ay")["Adet"]
        .sum()
    )

else:

    aylik_satis = pd.Series(dtype=float)
    aylik_adet = pd.Series(dtype=float)


def turkce_ay(ay):

    try:

        yil, ay_no = ay.split("-")

        isimler = [
            "Oca", "Şub", "Mar", "Nis",
            "May", "Haz", "Tem", "Ağu",
            "Eyl", "Eki", "Kas", "Ara"
        ]

        return f"{isimler[int(ay_no) - 1]} {yil}"

    except Exception:

        return ay


aylik_labels = [
    turkce_ay(x)
    for x in aylik_satis.index
]


# ==================================================
# SATIŞ ANALİZİ
# ==================================================

st.markdown("## 📈 Satış Analizi")

col1, col2 = st.columns([1.65, 1])


with col1:

    with st.container(border=True):

        st.subheader("📈 Aylık Satış Trendi")

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
                            [0.5, CYAN],
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
            margin=dict(l=5, r=5, t=8, b=5),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT),
            showlegend=False,
            xaxis=dict(
                showgrid=False,
                color=MUTED
            ),
            yaxis=dict(
                gridcolor="#173B61",
                color=MUTED,
                tickprefix="₺",
                tickformat=","
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )


with col2:

    with st.container(border=True):

        st.subheader("📦 Ürün Satış Dağılımı")

        st.caption(
            "Ürünlerin toplam satış içindeki payı"
        )

        pie_data = urun_satis.copy()

        if len(pie_data) > 6:

            top_products = pie_data.head(5)
            other_value = pie_data.iloc[5:].sum()

            pie_data = pd.concat(
                [
                    top_products,
                    pd.Series({"Diğer": other_value})
                ]
            )

        fig = px.pie(
            names=pie_data.index,
            values=pie_data.values,
            hole=0.64
        )

        fig.update_traces(
            marker=dict(
                colors=[
                    BLUE,
                    CYAN,
                    TURQUOISE,
                    "#3C8DFF",
                    "#6EA8FF",
                    "#8BA8C5"
                ],
                line=dict(
                    color=NAVY,
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
            margin=dict(l=5, r=5, t=5, b=5),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT),
            legend=dict(
                font=dict(color=TEXT)
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )


# ==================================================
# ÜRÜN + SEGMENT
# ==================================================

col1, col2 = st.columns(2)


with col1:

    with st.container(border=True):

        st.subheader("🏆 Ürün Performansı")

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
            margin=dict(l=5, r=5, t=5, b=5),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT),
            xaxis=dict(
                gridcolor="#173B61",
                color=MUTED,
                tickprefix="₺",
                tickformat=","
            ),
            yaxis=dict(
                title=None,
                color=TEXT
            ),
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )


with col2:

    with st.container(border=True):

        st.subheader("👥 Müşteri Segmenti Analizi")

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
            margin=dict(l=5, r=5, t=5, b=5),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT),
            xaxis=dict(
                gridcolor="#173B61",
                color=MUTED,
                tickprefix="₺",
                tickformat=","
            ),
            yaxis=dict(
                title=None,
                color=TEXT
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

st.markdown("## 📅 Zaman Analizi")

col1, col2 = st.columns(2)


with col1:

    with st.container(border=True):

        st.subheader("📦 Aylık Ürün Adedi")

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
                        color=CYAN,
                        size=8
                    ),
                    fill="tozeroy",
                    fillcolor="rgba(25,224,197,0.08)",
                    hovertemplate=
                    "%{x}<br>"
                    "%{y:,.0f} adet"
                    "<extra></extra>"
                )
            )

        fig.update_layout(
            height=330,
            margin=dict(l=5, r=5, t=8, b=5),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT),
            xaxis=dict(
                showgrid=False,
                color=MUTED
            ),
            yaxis=dict(
                gridcolor="#173B61",
                color=MUTED
            ),
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )


with col2:

    with st.container(border=True):

        st.subheader("🔄 Satış ve Adet Karşılaştırması")

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
                    marker=dict(size=8),
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
                    marker=dict(size=8),
                    yaxis="y2",
                    hovertemplate=
                    "%{x}<br>"
                    "%{y:,.0f} adet"
                    "<extra></extra>"
                )
            )

        fig.update_layout(
            height=330,
            margin=dict(l=5, r=5, t=8, b=5),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT),
            yaxis=dict(
                title="Satış",
                gridcolor="#173B61",
                color=MUTED,
                tickprefix="₺",
                tickformat=","
            ),
            yaxis2=dict(
                title="Adet",
                overlaying="y",
                side="right",
                color=MUTED
            ),
            legend=dict(
                orientation="h",
                font=dict(color=TEXT)
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

st.markdown("## 💡 Otomatik İş İçgörüleri")

urun_payi = (
    en_cok_satan_urun_tutari / toplam_satis * 100
    if toplam_satis > 0
    else 0
)

i1, i2, i3 = st.columns(3)


with i1:

    with st.container(border=True):

        st.subheader("🏆 Ürün Performansı")

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

        st.subheader("👥 Müşteri Analizi")

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

        st.subheader("💳 Ortalama İşlem")

        st.metric(
            "Ortalama satış",
            f"₺{ortalama_satis:,.0f}"
        )

        st.write(
            "İşlem başına gerçekleşen "
            "ortalama satış tutarıdır."
        )


# ==================================================
# ÜRÜN TABLOSU
# ==================================================

st.markdown("## 📋 Ürün Performans Tablosu")

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
    urun_tablosu["Toplam Satış"].round(0)
)

urun_tablosu["Ortalama Fiyat"] = (
    urun_tablosu["Ortalama Fiyat"].round(0)
)

urun_tablosu["Satış Payı"] = (
    urun_tablosu["Satış Payı"]
    .round(1)
    .map(lambda x: f"%{x:.1f}")
)

st.dataframe(
    urun_tablosu,
    use_container_width=True,
    hide_index=True
)


# ==================================================
# AI PANELİ
# ==================================================

st.markdown("## 🤖 DataPilot AI")

ai_html = """<div class="ai-panel"><div class="ai-label">YAPAY ZEKÂ ASİSTANI</div><div class="ai-title">DataPilot AI</div><div class="ai-description">Satış verilerinizi analiz edin, sorularınızı yazın ve verilerinizden anlamlı cevaplar alın.</div><span class="ai-chip">En çok satan ürün hangisi?</span><span class="ai-chip">Toplam satış ne kadar?</span><span class="ai-chip">En değerli müşteri segmenti hangisi?</span><span class="ai-chip">Genel performans nasıl?</span></div>"""

st.markdown(
    ai_html,
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

    with st.container(border=True):

        st.markdown(
            "### 🤖 DataPilot'ın Cevabı"
        )

        st.info(cevap)


# ==================================================
# VERİ ÖZETİ
# ==================================================

st.markdown("## 📌 Veri Özeti")

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
    <div class="footer">
        <b>DataPilot</b>
        • Satış Verileri Analiz ve İş İçgörü Platformu
        <br>
        Veri → Analiz → İçgörü → Karar
    </div>
    """,
    unsafe_allow_html=True
)
