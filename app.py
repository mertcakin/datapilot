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
# RENKLER
# ==================================================

NAVY = "#071A3A"
DARK_NAVY = "#041127"
BLUE = "#0B63CE"
CYAN = "#06B6D4"
TURQUOISE = "#18D5C0"
LIGHT_BLUE = "#38BDF8"
TEXT = "#10213F"
MUTED = "#64748B"


# ==================================================
# TASARIM
# ==================================================

st.markdown(
    """
<style>

/* ================================
   GENEL
================================ */

.stApp {
    background:
        linear-gradient(
            135deg,
            #F7FBFF 0%,
            #EEF8FF 55%,
            #F1FFFD 100%
        );
}

.main .block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}


/* ================================
   SIDEBAR
================================ */

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
    color: white;
}

.sidebar-subtitle {
    color: #AFC8E4 !important;
    font-size: 12px;
    margin-bottom: 25px;
}


/* ================================
   HERO CONTAINER
================================ */

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 24px !important;
    border-color: #DCEAF4 !important;
    background: rgba(255,255,255,0.82);
}


/* ================================
   METRIC KARTLARI
================================ */

div[data-testid="stMetric"] {
    background:
        linear-gradient(
            145deg,
            #FFFFFF,
            #F5FBFF
        );
    border: 1px solid #DCEAF4;
    border-radius: 20px;
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


/* ================================
   BAŞLIKLAR
================================ */

.section-title {
    color: #071A3A;
    font-size: 23px;
    font-weight: 800;
    margin-top: 30px;
    margin-bottom: 15px;
}


/* ================================
   TABLO
================================ */

div[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid #DCEAF4;
}


/* ================================
   EXPANDER
================================ */

div[data-testid="stExpander"] {
    border-radius: 18px;
    border: 1px solid #DCEAF4;
    background: white;
}


/* ================================
   INPUT
================================ */

div[data-baseweb="input"] {
    border-radius: 15px !important;
}


/* ================================
   FOOTER
================================ */

.footer-text {
    color: #64748B;
    text-align: center;
    font-size: 12px;
    padding: 25px 0;
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

    st.markdown(
        '<div class="sidebar-subtitle">'
        'Yapay Zekâ Destekli İş Analitiği'
        '</div>',
        unsafe_allow_html=True
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
        "CSV veya Excel satış verinizi yükleyerek "
        "analizi başlatabilirsiniz."
    )


# ==================================================
# DOSYA YÜKLENMEDİ
# ==================================================

if uploaded_file is None:

    with st.container(border=True):

        st.markdown("## 👋 Merhaba,")

        st.markdown(
            "# :blue[DataPilot]"
        )

        st.markdown(
            "### Yapay zekâ destekli satış ve iş analizi platformu"
        )

        st.write(
            "Satış verilerinizi yükleyin, performansınızı analiz edin "
            "ve verilerinizden anlamlı iş içgörüleri elde edin."
        )

        st.markdown(
            "**Veri → Analiz → İçgörü → Karar**"
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
# AYLIK ANALİZ
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

with st.container(border=True):

    st.markdown("## 👋 Merhaba,")

    st.markdown(
        "# :blue[DataPilot]"
    )

    st.markdown(
        "### Yapay zekâ destekli satış ve iş analizi platformu"
    )

    st.write(
        "Satış verilerinizden anlamlı iş içgörüleri keşfedin."
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
# SATIŞ ANALİZİ
# ==================================================

st.markdown(
    '<div class="section-title">📈 Satış Analizi</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([1.6, 1])


# ==================================================
# AYLIK SATIŞ
# ==================================================

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


# ==================================================
# ÜRÜN DAĞILIMI
# ==================================================

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
# ÜRÜN VE SEGMENT
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

        st.subheader("🔄 Satış ve Adet Karşılaştırması")

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


with insight2:

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


with insight3:

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
# DATAPILOT AI
# ==================================================

st.markdown(
    '<div class="section-title">🤖 DataPilot AI</div>',
    unsafe_allow_html=True
)

with st.container(border=True):

    st.markdown("### 🤖 DataPilot AI")

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

        st.caption(
            "• En çok satan ürün hangisi?"
        )

        st.caption(
            "• Toplam satış ne kadar?"
        )

    with q2:

        st.caption(
            "• En değerli müşteri segmenti hangisi?"
        )

        st.caption(
            "• En çok hangi ay satış yapıldı?"
        )

    with q3:

        st.caption(
            "• Laptop satışları nasıl?"
        )

        st.caption(
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

    st.markdown("### 🤖 DataPilot'ın Cevabı")

    with st.container(border=True):

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

st.markdown(
    '<div class="footer-text">'
    'DataPilot • Satış Verileri Analiz ve İş İçgörü Platformu'
    '<br>'
    'Veri → Analiz → İçgörü → Karar'
    '</div>',
    unsafe_allow_html=True
)
