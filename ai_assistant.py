def create_business_summary(df):
    toplam_satis = df["Toplam_Satis"].sum()
    toplam_adet = df["Adet"].sum()

    en_cok_satan_urun = (
        df.groupby("Urun")["Toplam_Satis"]
        .sum()
        .idxmax()
    )

    en_degerli_segment = (
        df.groupby("Musteri_Segmenti")["Toplam_Satis"]
        .sum()
        .idxmax()
    )

    return {
        "toplam_satis": toplam_satis,
        "toplam_adet": toplam_adet,
        "en_cok_satan_urun": en_cok_satan_urun,
        "en_degerli_segment": en_degerli_segment
    }
