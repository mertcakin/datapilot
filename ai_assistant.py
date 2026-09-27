import pandas as pd


def create_business_summary(df):
    toplam_satis = df["Toplam_Satis"].sum()
    toplam_adet = df["Adet"].sum()

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

    urun_adet = (
        df.groupby("Urun")["Adet"]
        .sum()
        .sort_values(ascending=False)
    )

    return {
        "toplam_satis": toplam_satis,
        "toplam_adet": toplam_adet,
        "ortalama_satis": df["Toplam_Satis"].mean(),
        "en_cok_satan_urun": urun_satis.idxmax(),
        "en_az_satan_urun": urun_satis.idxmin(),
        "en_cok_satan_urun_tutari": urun_satis.max(),
        "en_az_satan_urun_tutari": urun_satis.min(),
        "en_cok_satilan_adet_urun": urun_adet.idxmax(),
        "en_az_satilan_adet_urun": urun_adet.idxmin(),
        "en_degerli_segment": segment_satis.idxmax(),
        "en_dusuk_segment": segment_satis.idxmin(),
        "urun_sayisi": df["Urun"].nunique(),
        "segment_sayisi": df["Musteri_Segmenti"].nunique()
    }


def answer_question(df, question):

    soru = question.lower().strip()

    analiz = create_business_summary(df)

    toplam_satis = analiz["toplam_satis"]
    toplam_adet = analiz["toplam_adet"]
    ortalama_satis = analiz["ortalama_satis"]

    en_cok = analiz["en_cok_satan_urun"]
    en_az = analiz["en_az_satan_urun"]

    en_cok_tutar = analiz["en_cok_satan_urun_tutari"]
    en_az_tutar = analiz["en_az_satan_urun_tutari"]

    en_cok_adet = analiz["en_cok_satilan_adet_urun"]
    en_az_adet = analiz["en_az_satilan_adet_urun"]

    en_degerli_segment = analiz["en_degerli_segment"]
    en_dusuk_segment = analiz["en_dusuk_segment"]

    # ---------------------------------------------
    # EN ÇOK SATAN ÜRÜN
    # ---------------------------------------------

    if (
        "en çok satan" in soru
        or "en cok satan" in soru
        or "en fazla satan" in soru
        or "en iyi satan" in soru
        or "en yüksek satış" in soru
        or "en yuksek satis" in soru
    ):

        return (
            f"🏆 En yüksek satış yapan ürün **{en_cok}**. "
            f"Bu ürünün toplam satış tutarı "
            f"**₺{en_cok_tutar:,.0f}**."
        )

    # ---------------------------------------------
    # EN AZ SATAN ÜRÜN
    # ---------------------------------------------

    elif (
        "en az satan" in soru
        or "en düşük satış" in soru
        or "en dusuk satis" in soru
        or "en az satış" in soru
        or "en az satis" in soru
    ):

        return (
            f"📉 En düşük satış yapan ürün **{en_az}**. "
            f"Bu ürünün toplam satış tutarı "
            f"**₺{en_az_tutar:,.0f}**."
        )

    # ---------------------------------------------
    # EN ÇOK ADET SATAN
    # ---------------------------------------------

    elif (
        "en çok adet" in soru
        or "en cok adet" in soru
        or "en fazla adet" in soru
        or "en çok ürün" in soru
        or "en cok urun" in soru
    ):

        adet = df.groupby("Urun")["Adet"].sum()

        return (
            f"📦 Adet bazında en fazla satılan ürün "
            f"**{en_cok_adet}**. "
            f"Toplam **{adet[en_cok_adet]:,.0f} adet** satılmış."
        )

    # ---------------------------------------------
    # EN AZ ADET SATAN
    # ---------------------------------------------

    elif (
        "en az adet" in soru
        or "en düşük adet" in soru
        or "en dusuk adet" in soru
    ):

        adet = df.groupby("Urun")["Adet"].sum()

        return (
            f"📉 Adet bazında en az satılan ürün "
            f"**{en_az_adet}**. "
            f"Toplam **{adet[en_az_adet]:,.0f} adet** satılmış."
        )

    # ---------------------------------------------
    # TOPLAM SATIŞ / CİRO
    # ---------------------------------------------

    elif (
        "toplam satış" in soru
        or "toplam satis" in soru
        or "ciro" in soru
        or "gelir" in soru
        or "kazanç" in soru
        or "kazanc" in soru
    ):

        return (
            f"💰 Toplam satış hacmi "
            f"**₺{toplam_satis:,.0f}**."
        )

    # ---------------------------------------------
    # TOPLAM ADET
    # ---------------------------------------------

    elif (
        "kaç ürün" in soru
        or "kaç adet" in soru
        or "kac urun" in soru
        or "kac adet" in soru
        or "toplam ürün" in soru
        or "toplam urun" in soru
    ):

        return (
            f"📦 Toplam **{toplam_adet:,.0f} adet** ürün satılmış."
        )

    # ---------------------------------------------
    # ORTALAMA SATIŞ
    # ---------------------------------------------

    elif (
        "ortalama satış" in soru
        or "ortalama satis" in soru
        or "ortalama" in soru
        or "ortalama tutar" in soru
    ):

        return (
            f"📊 İşlem başına ortalama satış tutarı "
            f"**₺{ortalama_satis:,.0f}**."
        )

    # ---------------------------------------------
    # EN DEĞERLİ SEGMENT
    # ---------------------------------------------

    elif (
        "en değerli müşteri" in soru
        or "en degerli musteri" in soru
        or "en iyi müşteri" in soru
        or "en iyi musteri" in soru
        or "en çok hangi müşteri" in soru
        or "en cok hangi musteri" in soru
        or "en yüksek segment" in soru
        or "en yuksek segment" in soru
    ):

        return (
            f"👥 En yüksek satış hacmine sahip müşteri segmenti "
            f"**{en_degerli_segment}**."
        )

    # ---------------------------------------------
    # EN DÜŞÜK SEGMENT
    # ---------------------------------------------

    elif (
        "en az müşteri" in soru
        or "en az musteri" in soru
        or "en düşük segment" in soru
        or "en dusuk segment" in soru
        or "en kötü segment" in soru
        or "en kotu segment" in soru
    ):

        return (
            f"📉 En düşük satış hacmine sahip müşteri segmenti "
            f"**{en_dusuk_segment}**."
        )

    # ---------------------------------------------
    # KAÇ FARKLI ÜRÜN
    # ---------------------------------------------

    elif (
        "kaç farklı ürün" in soru
        or "kaç ürün var" in soru
        or "kac farkli urun" in soru
        or "kaç çeşit ürün" in soru
        or "kac cesit urun" in soru
    ):

        return (
            f"📦 Veri setinde **{analiz['urun_sayisi']} farklı ürün** bulunuyor."
        )

    # ---------------------------------------------
    # KAÇ SEGMENT
    # ---------------------------------------------

    elif (
        "kaç segment" in soru
        or "kaç müşteri segmenti" in soru
        or "kac segment" in soru
        or "kac musteri segmenti" in soru
    ):

        return (
            f"👥 Veri setinde **{analiz['segment_sayisi']} farklı "
            f"müşteri segmenti** bulunuyor."
        )

    # ---------------------------------------------
    # GENEL ÖZET
    # ---------------------------------------------

    elif (
        "özet" in soru
        or "ozet" in soru
        or "genel durum" in soru
        or "veriler ne söylüyor" in soru
        or "veriler ne soyluyor" in soru
        or "analiz et" in soru
    ):

        return (
            f"📊 **Genel Veri Özeti**\n\n"
            f"• Toplam satış: **₺{toplam_satis:,.0f}**\n\n"
            f"• Toplam ürün adedi: **{toplam_adet:,.0f}**\n\n"
            f"• Ortalama satış: **₺{ortalama_satis:,.0f}**\n\n"
            f"• En yüksek satış yapan ürün: **{en_cok}**\n\n"
            f"• En düşük satış yapan ürün: **{en_az}**\n\n"
            f"• En yüksek satış yapan segment: **{en_degerli_segment}**"
        )

    # ---------------------------------------------
    # ANLAŞILMAYAN SORU
    # ---------------------------------------------

    else:

        return (
            "🤖 Bu soruyu tam olarak anlayamadım.\n\n"
            "Şunlardan birini deneyebilirsin:\n\n"
            "• En çok satan ürün hangisi?\n"
            "• En az satan ürün hangisi?\n"
            "• Toplam cirom ne kadar?\n"
            "• Kaç ürün sattım?\n"
            "• Ortalama satış ne kadar?\n"
            "• En değerli müşteri segmenti hangisi?\n"
            "• Kaç farklı ürün var?\n"
            "• Verileri özetle."
        )
