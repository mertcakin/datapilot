import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from ai_assistant import answer_question


# ==================================================
# SAYFA
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
CYAN = "#06B6D4"
TURQUOISE = "#18D5C0"
TEXT = "#10213F"
MUTED = "#64748B"


# ==================================================
# GLOBAL TASARIM
# ==================================================

st.markdown(
    """
<style>

/* ==================================================
   ANA SAYFA
================================================== */

.stApp {
    background:
        linear-gradient(
            135deg,
            #FFFFFF 0%,
            #F7FBFF 48%,
            #ECFBFA 100%
        );
}

.main .block-container {
    max-width: 1500px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}


/* ==================================================
   TÜM ANA YAZILAR
================================================== */

.main .stMarkdown,
.main .stMarkdown p,
.main .stMarkdown span,
.main .stMarkdown label,
.main .stCaption,
.main label {
    color: #10213F;
}

h1,
h2,
h3,
h4,
h5,
h6 {
    color: #071A3A !important;
}


/* ==================================================
   SIDEBAR
================================================== */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #041127 0%,
            #071A3A 52%,
            #07516A 100%
        );
}

section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] .stCaption {
    color: #B9D4EA !important;
}


/* ==================================================
   HERO
================================================== */

.hero-container {
    background:
        linear-gradient(
            120deg,
            #FFFFFF 0%,
            #F6FBFF 55%,
            #E1FAF7 100%
        );

    border: 1px solid #D7E8F2;

    border-radius: 28px;

    padding: 32px 36px;

    margin-bottom: 24px;

    box-shadow:
        0 12px 35px rgba(7,26,58,0.07);
}

.hero-small {
    color: #64748B;
    font-size: 14px;
    font-weight: 600;
}

.hero-title {
    color: #071A3A;
    font-size: 42px;
    font-weight: 850;
    letter-spacing: -1.5px;
    margin: 4px 0;
}

.hero-highlight {
    color: #0B63CE;
}

.hero-description {
    color: #64748B;
    font-size: 16px;
    margin-top: 8px;
}

.hero-tagline {
    color: #071A3A;
    font-weight: 750;
    font-size: 14px;
    margin-top: 16px;
}


/* ==================================================
   SECTION BAŞLIKLARI
================================================== */

.section-title {
    color: #071A3A !important;
    font-size: 23px;
    font-weight: 800;
    margin-top: 30px;
    margin-bottom: 14px;
}


/* ==================================================
   METRIC KARTLARI
================================================== */

div[data-testid="stMetric"] {
    background:
        linear-gradient(
            145deg,
            #FFFFFF 0%,
            #F8FCFF 70%,
            #EDFFFD 100%
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
    font-weight: 850;
}


/* ==================================================
   GRAFİK KARTLARI
================================================== */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background:
        rgba(255,255,255,0.92);

    border:
        1px solid #DCEAF4 !important;

    border-radius:
        22px !important;

    box-shadow:
        0 8px 25px rgba(7,26,58,0.045);
}


/* ==================================================
   INPUT
================================================== */

div[data-baseweb="input"] {
    background: #FFFFFF !important;
    border-radius: 15px !important;
    border: 1px solid #CBDDEB !important;
}

div[data-baseweb="input"] input {
    color: #10213F !important;
    background: #FFFFFF !important;
}

div[data-baseweb="input"] input::placeholder {
    color: #8A9AAF !important;
}


/* ==================================================
   TEXT AREA
================================================== */

textarea {
    color: #10213F !important;
    background: #FFFFFF !important;
}


/* ==================================================
   INFO
================================================== */

div[data-testid="stAlert"] {
    border-radius: 16px;
}


/* ==================================================
   DATAFRAME
================================================== */

div[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid #DCEAF4;
}


/* ==================================================
   EXPANDER
================================================== */

div[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid #DCEAF4;
    border-radius: 18px;
}


/* ==================================================
   FOOTER
================================================== */

.footer {
    text-align: center;
    color: #64748B;
    font-size: 12px;
    padding: 30px 0 10px 0;
}


/* ==================================================
   BUTON
================================================== */

.stButton > button {
    background:
        linear-gradient(
            90deg,
            #0B63CE,
            #06B6D4,
            #18D5C0
        );

    color: white !important;

    border: none;

    border-radius: 14px;

    font-weight: 750;
}

</style>
""",
    unsafe_allow_html=True
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("📊 DataPilot")

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

    st.info(
        "Satış verinizi yükleyerek "
        "DataPilot analizini başlatın."
    )


# ==================================================
# DOSYA YOK
# ==================================================

if uploaded_file is None:

    st.markdown(
        """
        <div class="hero-container">

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
                Satış verilerinizi analiz edin,
                performansınızı ölçün ve
                verilerinizden anlamlı iş içgörüleri elde edin.
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
# KPI HESAPLARI
# ==================================================

toplam_satis = df["Toplam_Satis"].sum()

toplam_adet = df["Adet"].sum()

ortalama_satis = df["Toplam_Satis"].mean()

toplam_islem = len(df)

urun_sayisi = df["Urun"].nunique()

segment_sayisi = df["Musteri_Segmenti"].nunique()


# ==================================================
# ÜRÜN
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
# SEGMENT
# ==================================================

segment_satis = (
    df.groupby("Musteri_Segmenti")["Toplam_Satis"]
    .sum()
    .sort_values(ascending=False)
)

en_degerli_segment = segment_satis.idxmax()

en_degerli_segment_tutari = segment_satis.max()


# ==================================================
# AYLIK
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
    <div class="hero-container">

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

k1, k2, k3, k4, k5 = st.columns(5)


with k1:

    st.metric(
        "💰 Toplam Satış",
        f"₺{toplam_satis:,.0f}"
    )


with k2:

    st.metric(
        "📦 Toplam Adet",
        f"{toplam_adet:,.0f}"
    )


with k3:

    st.metric(
        "🧾 İşlem Sayısı",
        f"{toplam_islem:,}"
    )


with k4:

    st.metric(
        "💳 Ortalama Satış",
        f"₺{ortalama_satis:,.0f}"
    )


with k5:

    st.metric(
        "👥 En Değerli Segment",
        en_degerli_segment
    )


# ==================================================
# SATIŞ ANALİZİ
# ==================================================

st.markdown(
    '<div class="section-title">📈 Satış Analizi</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([1.6, 1])


with col1:

    with st.container(border=True):

        st.subheader("📈 Aylık Satış Trendi")

        st.caption(
            "Aylara göre toplam satış performansı"
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


with col2:

    with st.container(border=True):

        st.subheader("📦 Ürün Satış Dağılımı")

        st.caption(
            "Ürünlerin toplam satış içindeki payı"
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
            textinfo="percent"
        )

        fig.update_layout(
            height=350,
            margin=dict(
                l=5,
                r=5,
                t=5,
                b=5
            ),
            paper_bgcolor="white"
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
            marker_color="#0B63CE"
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

        st.subheader("👥 Müşteri Segmentleri")

        st.caption(
            "Segmentlere göre satış hacmi"
        )

        fig = px.bar(
            x=segment_satis.values,
            y=segment_satis.index,
            orientation="h"
        )

        fig.update_traces(
            marker_color="#18D5C0"
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

        st.subheader("📦 Aylık Ürün Adedi")

        st.caption(
            "Aylara göre satılan toplam ürün"
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
                    fillcolor="rgba(24,213,192,0.10)"
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

        st.subheader("🔄 Satış ve Adet")

        st.caption(
            "Aylık satış tutarı ve ürün adedi"
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
                    )
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
                    yaxis="y2"
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
                    orientation="h"
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
            f"Satış tutarı: ₺{en_cok_satan_urun_tutari:,.0f}"
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
            f"Satış tutarı: ₺{en_degerli_segment_tutari:,.0f}"
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
            "ortalama satış tutarı."
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
# DATAPILOT AI
# ==================================================

st.markdown(
    '<div class="section-title">🤖 DataPilot AI</div>',
    unsafe_allow_html=True
)

with st.container(border=True):

    st.markdown(
        "### 🤖 DataPilot AI"
    )

    st.markdown(
        "**YAPAY ZEKÂ ASİSTANI**"
    )

    st.write(
        "Satış verilerinizi analiz edin, sorularınızı yazın "
        "ve verilerinizden anlamlı cevaplar alın."
    )

    st.markdown("#### 💬 Örnek Sorular")

    q1, q2, q3 = st.columns(3)

    with q1:

        st.write(
            "• En çok satan ürün hangisi?"
        )

        st.write(
            "• Toplam satış ne kadar?"
        )

    with q2:

        st.write(
            "• En değerli müşteri segmenti hangisi?"
        )

        st.write(
            "• En çok hangi ay satış yapıldı?"
        )

    with q3:

        st.write(
            "• Laptop Pro satışları nasıl?"
        )

        st.write(
            "• Genel performans nasıl?"
        )


# ==================================================
# AI SORU
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

    st.markdown(
        "### 🤖 DataPilot'ın Cevabı"
    )

    st.success(
        cevap
    )


# ==================================================
# VERİ ÖZETİ
# ==================================================

st.markdown(
    '<div class="section-title">📌 Veri Özeti</div>',
    unsafe_allow_html=True
)

o1, o2, o3 = st.columns(3)


with o1:

    st.metric(
        "Veri Satırı",
        f"{len(df):,}"
    )


with o2:

    st.metric(
        "Ürün Sayısı",
        f"{urun_sayisi:,}"
    )


with o3:

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
