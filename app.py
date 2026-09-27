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

st.info(
    "Başlamak için aşağıdaki alandan CSV veya Excel formatındaki "
    "satış verilerinizi yükleyebilirsiniz."
)

uploaded_file = st.file_uploader(
    "📂 Satış verilerinizi yükleyin",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ Verileriniz başarıyla yüklendi!")

        st.subheader("📋 Veri Önizleme")
        st.dataframe(df, use_container_width=True)

        st.subheader("📈 Temel İstatistikler")
        st.write(df.describe(include="all"))

    except Exception as e:
        st.error(f"❌ Veriler yüklenirken bir hata oluştu: {e}")
