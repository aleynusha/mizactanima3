import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Mizaç Tespiti", layout="centered")

# Logo ve başlık
st.image("logo.png", width=120)
st.title("🧭 Mizaç Tespiti Aracı")
st.markdown("Klasik tıp anlayışına göre **temel ve ikincil mizaç** tespiti")

# Türkiye illeri
iller = [
    "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Aksaray", "Amasya", "Ankara", "Antalya",
    "Ardahan", "Artvin", "Aydın", "Balıkesir", "Bartın", "Batman", "Bayburt", "Bilecik", "Bingöl",
    "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır",
    "Düzce", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun",
    "Gümüşhane", "Hakkâri", "Hatay", "Iğdır", "Isparta", "İstanbul", "İzmir", "Kahramanmaraş",
    "Karabük", "Karaman", "Kars", "Kastamonu", "Kayseri", "Kırıkkale", "Kırklareli", "Kırşehir",
    "Kilis", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla",
    "Muş", "Nevşehir", "Niğde", "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun", "Şanlıurfa",
    "Siirt", "Sinop", "Şırnak", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Uşak",
    "Van", "Yalova", "Yozgat", "Zonguldak"
]

col1, col2 = st.columns(2)
with col1:
    tarih = st.date_input("Doğum Tarihi")
with col2:
    il = st.selectbox("Doğum Yeri (İl)", iller)

saat = st.number_input("Doğum Saati (0-23)", min_value=0, max_value=23)
dakika = st.number_input("Doğum Dakikası (0-59)", min_value=0, max_value=59)

def ezan_vakitlerini_getir(tarih, il):
    t_str = tarih.strftime("%Y-%m-%d")
    url = f"https://api.aladhan.com/v1/timingsByCity/{t_str}?city={il}&country=Turkey&method=13"
    response = requests.get(url)
    data = response.json()
    vakitler = data["data"]["timings"]
    return {
        "Fajr": vakitler["Fajr"],
        "Dhuhr": vakitler["Dhuhr"],
        "Asr": vakitler["Asr"],
        "Isha": vakitler["Isha"]
    }

def saat_to_minutes(zaman):
    h, m = map(int, zaman.split(":"))
    return h * 60 + m

def temel_mizac_belirle(dakika_toplam, vakitler):
    sabah = saat_to_minutes(vakitler["Fajr"])
    ogle = saat_to_minutes(vakitler["Dhuhr"])
    ikindi = saat_to_minutes(vakitler["Asr"])
    yatsi = saat_to_minutes(vakitler["Isha"])

    if sabah <= dakika_toplam < ogle - 120:  # 11:30'dan önce
        return "Sevdavi (Soğuk - Kuru)", "Düşünceye yatkın, düzen sever, sabırlıdır."
    elif ogle - 120 <= dakika_toplam < ikindi:
        return "Safravi (Sıcak - Kuru)", "Hızlı, atılgan, kararlı ve enerjiktir."
    elif ikindi <= dakika_toplam < yatsi:
        return "Demevi (Sıcak - Nemli)", "Sosyal, konuşkan, neşeli ve yaratıcıdır."
    else:
        return "Balgami (Soğuk - Nemli)", "Sakin, uyumlu, yavaş ama sabit yapılıdır."

def mevsim_mizaci(ay):
    if ay in [3, 4, 5]:
        return "Demevi (Sıcak - Nemli)", "İlkbaharda doğanlar sosyal ve canlı yapıdadır."
    elif ay in [6, 7, 8]:
        return "Safravi (Sıcak - Kuru)", "Yaz doğumlular enerjik ve rekabetçidir."
    elif ay in [9, 10, 11]:
        return "Sevdavi (Soğuk - Kuru)", "Sonbaharda doğanlar derin düşüncelidir."
    else:
        return "Balgami (Soğuk - Nemli)", "Kış doğanlar daha sakin ve içe dönüktür."

if st.button("Mizaçları Göster"):
    try:
        vakitler = ezan_vakitlerini_getir(tarih, il)
        dakika_toplam = saat * 60 + dakika
        temel, temel_aciklama = temel_mizac_belirle(dakika_toplam, vakitler)
        ikincil, ikincil_aciklama = mevsim_mizaci(tarih.month)

        st.subheader("🔍 Sonuçlar")
        st.markdown(f"**Temel Mizaç:** {temel}  \n_{temel_aciklama}_")
        st.markdown(f"**İkincil Mizaç:** {ikincil}  \n_{ikincil_aciklama}_")
    except:
        st.error("Ezan vakitleri alınırken bir hata oluştu. İnternet bağlantınızı ve ili kontrol edin.")

# WhatsApp butonu
st.markdown("---")
st.markdown("📞 [**Mizaca göre beslenme danışmanlığı için bize ulaşabilirsiniz**](https://wa.me/message/OKQCC7SH7FEHO1)")
