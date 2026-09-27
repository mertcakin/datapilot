import pandas as pd


# ==================================================
# DATA PILOT - İŞ ANALİZ FONKSİYONLARI
# ==================================================


def create_business_summary(df):
    """
    Satış verilerinden otomatik iş özeti oluşturur.
    """

    if df is None or df.empty:
        return "Analiz edilecek veri bulunamadı."

    toplam_satis = df["Toplam_Satis"].sum()
    toplam_adet = df["Adet"].sum()
    ortalama_satis = df["Toplam_Satis"].mean()

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
    en_degerli_segment = segment_satis.idxmax()

    return (
        f"Toplam satış ₺{toplam_satis:,.0f}. "
        f"Toplam {toplam_adet:,.0f} adet ürün satıldı. "
        f"İşlem başına ortalama satış ₺{ortalama_satis:,.0f}. "
        f"En yüksek satış yapan ürün {en_cok_satan_urun}. "
        f"En yüksek satış hacmine sahip müşteri segmenti "
        f"{en_degerli_segment}."
    )


# ==================================================
# SORU ANALİZİ
# ==================================================


def answer_question(df, question):
    """
    Kullanıcının satış verileriyle ilgili sorusunu analiz eder.
    """

    if df is None or df.empty:
        return "Analiz edilecek veri bulunamadı."

    if not question or not question.strip():
        return "Lütfen bir soru yazın."

    soru = question.lower().strip()

    # ==================================================
    # TEMEL HESAPLAMALAR
    # ==================================================

    toplam_satis = df["Toplam_Satis"].sum()
    toplam_adet = df["Adet"].sum()
    ortalama_satis = df["Toplam_Satis"].mean()
    islem_sayisi = len(df)
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

    en_az_satan_urun = urun_satis.idxmin()
    en_az_satan_urun_tutari = urun_satis.min()

    en_cok_satilan_urun = urun_adet.idxmax()
    en_cok_satilan_adet = urun_adet.max()

    # ==================================================
    # MÜŞTERİ SEGMENTİ ANALİZİ
    # ==================================================

    segment_satis = (
        df.groupby("Musteri_Segmenti")["Toplam_Satis"]
        .sum()
        .sort_values(ascending=False)
    )

    en_degerli_segment = segment_satis.idxmax()
    en_degerli_segment_tutari = segment_satis.max()

    en_dusuk_segment = segment_satis.idxmin()
    en_dusuk_segment_tutari = segment_satis.min()

    # ==================================================
    # AYLIK ANALİZ
    # ==================================================

    df_analiz = df.copy()

    df_analiz["Tarih"] = pd.to_datetime(
        df_analiz["Tarih"],
        errors="coerce"
    )

    tarihli_df = df_analiz.dropna(
        subset=["Tarih"]
    )

    if not tarihli_df.empty:

        aylik_satis = (
            tarihli_df.groupby(
                tarihli_df["Tarih"].dt.to_period("M")
            )["Toplam_Satis"]
            .sum()
            .sort_values(ascending=False)
        )

    else:

        aylik_satis = pd.Series(dtype="float64")

    if not aylik_satis.empty:

        en_yuksek_ay = aylik_satis.idxmax()
        en_yuksek_ay_tutari = aylik_satis.max()

        en_dusuk_ay = aylik_satis.idxmin()
        en_dusuk_ay_tutari = aylik_satis.min()

    else:

        en_yuksek_ay = None
        en_yuksek_ay_tutari = 0

        en_dusuk_ay = None
        en_dusuk_ay_tutari = 0

    # ==================================================
    # TOPLAM SATIŞ
    # ==================================================

    if (
        "toplam satış" in soru
        or "toplam ciro" in soru
        or "ciro ne kadar" in soru
        or "ne kadar satış" in soru
    ):

        return (
            f"Toplam satış tutarı ₺{toplam_satis:,.0f}."
        )

    # ==================================================
    # TOPLAM ADET
    # ==================================================

    if (
        "kaç adet" in soru
        or "toplam adet" in soru
        or "kaç ürün" in soru
        or "ürün sayısı" in soru
    ):

        return (
            f"Toplam {toplam_adet:,.0f} adet ürün satışı gerçekleşti."
        )

    # ==================================================
    # ORTALAMA SATIŞ
    # ==================================================

    if (
        "ortalama satış" in soru
        or "ortalama tutar" in soru
        or "ortalama ciro" in soru
    ):

        return (
            f"İşlem başına ortalama satış tutarı "
            f"₺{ortalama_satis:,.0f}."
        )

    # ==================================================
    # EN ÇOK SATAN ÜRÜN
    # ==================================================

    if (
        "en çok satan ürün" in soru
        or "en fazla satan ürün" in soru
        or "en başarılı ürün" in soru
        or "hangi ürün daha çok satıyor" in soru
    ):

        return (
            f"En yüksek satış cirosuna sahip ürün "
            f"{en_cok_satan_urun}. "
            f"Toplam satış tutarı "
            f"₺{en_cok_satan_urun_tutari:,.0f}."
        )

    # ==================================================
    # EN ÇOK SATILAN ADET
    # ==================================================

    if (
        "en çok satılan" in soru
        or "en fazla adet" in soru
        or "adet olarak en çok" in soru
    ):

        return (
            f"Adet bazında en çok satılan ürün "
            f"{en_cok_satilan_urun}. "
            f"Toplam {en_cok_satilan_adet:,.0f} adet satıldı."
        )

    # ==================================================
    # EN AZ SATAN ÜRÜN
    # ==================================================

    if (
        "en az satan" in soru
        or "en düşük satan" in soru
        or "en az satış" in soru
    ):

        return (
            f"En düşük satış cirosuna sahip ürün "
            f"{en_az_satan_urun}. "
            f"Toplam satış tutarı "
            f"₺{en_az_satan_urun_tutari:,.0f}."
        )

    # ==================================================
    # EN DEĞERLİ MÜŞTERİ SEGMENTİ
    # ==================================================

    if (
        "en değerli segment" in soru
        or "en değerli müşteri segmenti" in soru
        or "en değerli müşteri" in soru
        or "en iyi müşteri segmenti" in soru
        or "hangi müşteri segmenti" in soru
        or "hangi segment" in soru
        or "en çok alışveriş yapan segment" in soru
        or "en çok alışveriş yapan müşteri segmenti" in soru
        or "en çok satış yapan segment" in soru
        or "en çok satış yapan müşteri segmenti" in soru
    ):

        return (
            f"En yüksek satış hacmine sahip müşteri segmenti "
            f"{en_degerli_segment}. "
            f"Toplam satış tutarı "
            f"₺{en_degerli_segment_tutari:,.0f}."
        )

    # ==================================================
    # EN DÜŞÜK SATIŞLI MÜŞTERİ SEGMENTİ
    # ==================================================

    if (
        "en düşük segment" in soru
        or "en az satış yapan segment" in soru
        or "en düşük satış yapan segment" in soru
        or "en az alışveriş yapan segment" in soru
        or "en düşük müşteri segmenti" in soru
    ):

        return (
            f"En düşük satış hacmine sahip müşteri segmenti "
            f"{en_dusuk_segment}. "
            f"Toplam satış tutarı "
            f"₺{en_dusuk_segment_tutari:,.0f}."
        )

    # ==================================================
    # AYLIK SATIŞ
    # ==================================================

    if (
        "en yüksek ay" in soru
        or "en iyi ay" in soru
        or "hangi ay" in soru
        or "en çok satış hangi ay" in soru
        or "en yüksek satış hangi ay" in soru
    ):

        if en_yuksek_ay is not None:

            return (
                f"En yüksek satış yapılan ay "
                f"{en_yuksek_ay}. "
                f"Toplam satış "
                f"₺{en_yuksek_ay_tutari:,.0f}."
            )

        return "Tarih bilgileri analiz için uygun değil."

    # ==================================================
    # İŞLEM SAYISI
    # ==================================================

    if (
        "kaç işlem" in soru
        or "işlem sayısı" in soru
        or "kaç satış" in soru
    ):

        return (
            f"Toplam {islem_sayisi:,} satış işlemi bulunuyor."
        )

    # ==================================================
    # ÜRÜN SAYISI
    # ==================================================

    if (
        "kaç farklı ürün" in soru
        or "kaç ürün var" in soru
        or "farklı ürün" in soru
    ):

        return (
            f"Veri setinde {urun_sayisi} farklı ürün bulunuyor."
        )

    # ==================================================
    # SEGMENT SAYISI
    # ==================================================

    if (
        "kaç segment" in soru
        or "kaç müşteri segmenti" in soru
        or "segment sayısı" in soru
    ):

        return (
            f"Veri setinde {segment_sayisi} farklı müşteri segmenti bulunuyor."
        )

    # ==================================================
    # GENEL ÖZET
    # ==================================================

    if (
        "özet" in soru
        or "genel durum" in soru
        or "genel analiz" in soru
        or "performans" in soru
        or "nasıl gidiyor" in soru
    ):

        return create_business_summary(df)

    # ==================================================
    # YARDIM
    # ==================================================

    if (
        "ne sorabilirim" in soru
        or "yardım" in soru
        or "neler yapabilirsin" in soru
        or "hangi soruları" in soru
    ):

        return (
            "Şunları sorabilirsiniz:\n\n"
            "• En çok satan ürün hangisi?\n"
            "• Toplam satış ne kadar?\n"
            "• En değerli müşteri segmenti hangisi?\n"
            "• En düşük satış yapan segment hangisi?\n"
            "• En çok hangi ay satış yapıldı?\n"
            "• Toplam kaç adet ürün satıldı?\n"
            "• Ortalama satış tutarı ne kadar?\n"
            "• Genel performans nasıl?"
        )

    # ==================================================
    # ÜRÜN ADI ÜZERİNDEN ANALİZ
    # ==================================================

    for urun in df["Urun"].dropna().unique():

        urun_adi = str(urun).lower()

        if urun_adi in soru:

            urun_verisi = df[
                df["Urun"].astype(str).str.lower()
                == urun_adi
            ]

            urun_toplam_satis = (
                urun_verisi["Toplam_Satis"].sum()
            )

            urun_toplam_adet = (
                urun_verisi["Adet"].sum()
            )

            urun_ortalama = (
                urun_verisi["Toplam_Satis"].mean()
            )

            return (
                f"{urun} için toplam satış "
                f"₺{urun_toplam_satis:,.0f}. "
                f"Toplam {urun_toplam_adet:,.0f} adet satıldı. "
                f"Ortalama işlem tutarı "
                f"₺{urun_ortalama:,.0f}."
            )

    # ==================================================
    # SEGMENT ADI ÜZERİNDEN ANALİZ
    # ==================================================

    for segment in df["Musteri_Segmenti"].dropna().unique():

        segment_adi = str(segment).lower()

        if segment_adi in soru:

            segment_verisi = df[
                df["Musteri_Segmenti"].astype(str).str.lower()
                == segment_adi
            ]

            segment_toplam_satis = (
                segment_verisi["Toplam_Satis"].sum()
            )

            segment_toplam_adet = (
                segment_verisi["Adet"].sum()
            )

            return (
                f"{segment} segmentinin toplam satış tutarı "
                f"₺{segment_toplam_satis:,.0f}. "
                f"Toplam {segment_toplam_adet:,.0f} adet "
                f"ürün satıldı."
            )

    # ==================================================
    # ANLAŞILMAYAN SORU
    # ==================================================

    return (
        "Bu soruyu mevcut analiz fonksiyonlarıyla "
        "yorumlayamadım.\n\n"
        "Örneğin şunları sorabilirsiniz:\n"
        "• En çok satan ürün hangisi?\n"
        "• Toplam satış ne kadar?\n"
        "• En değerli müşteri segmenti hangisi?\n"
        "• En düşük satış yapan segment hangisi?\n"
        "• En çok hangi ay satış yapıldı?\n"
        "• Ortalama satış tutarı ne kadar?"
    )
