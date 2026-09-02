from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

# Mobil ekran boyutunu simüle edelim (Bilgisayarda test ederken işe yarar)
Window.size = (360, 640)

# Etiket renk kodları (Kırmızı, Mavi, Sarı, Yeşil)
RENKLER = {
    "KIRMIZI": [0.8, 0.1, 0.1, 1],
    "MAVİ": [0.1, 0.4, 0.8, 1],
    "SARI": [0.9, 0.8, 0.1, 1],
    "YEŞİL": [0.2, 0.7, 0.2, 1]
}

# Excel dosyasından alınan başlangıç verileri
VERILER = [
    {"bina": "BEYZA SİTESİ", "tarih": "2026-07-15", "renk": "MAVİ"},
    {"bina": "AYDINLAR APT.", "tarih": "2026-07-22", "renk": "KIRMIZI"}
]

class EtiketKaydi(BoxLayout):
    def __init__(self, bina, tarih, baslangic_rengi, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 100
        self.spacing = 10
        self.padding = 10

        # Sol taraf: Bina Adı ve Tarih
        sol_panel = BoxLayout(orientation='vertical', size_hint_x=0.6)
        sol_panel.add_widget(Label(text=bina, bold=True, font_size='18sp'))
        sol_panel.add_widget(Label(text=tarih, font_size='14sp'))
        self.add_widget(sol_panel)

        # Sağ taraf: Tıklanabilir Renk Butonu
        self.renk_listesi = list(RENKLER.keys())
        self.guncel_index = self.renk_listesi.index(baslangic_rengi) if baslangic_rengi in self.renk_listesi else 0
        
        self.renk_butonu = Button(
            text=self.renk_listesi[self.guncel_index], 
            size_hint_x=0.4, 
            bold=True,
            background_normal='',
            background_color=RENKLER[self.renk_listesi[self.guncel_index]]
        )
        self.renk_butonu.bind(on_press=self.renk_degistir)
        self.add_widget(self.renk_butonu)

    def renk_degistir(self, instance):
        # Renkler arasında geçiş yap
        self.guncel_index = (self.guncel_index + 1) % len(self.renk_listesi)
        yeni_renk = self.renk_listesi[self.guncel_index]
        
        self.renk_butonu.text = yeni_renk
        self.renk_butonu.background_color = RENKLER[yeni_renk]

class EtiketTakipUygulamasi(App):
    def build(self):
        ana_ekran = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Üst Başlık
        baslik = Label(text="Etiket Durumları", size_hint_y=None, height=50, bold=True, font_size='22sp')
        ana_ekran.add_widget(baslik)

        # Kaydırılabilir Liste
        kaydirma_alani = ScrollView(size_hint=(1, 1))
        self.liste = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.liste.bind(minimum_height=self.liste.setter('height'))

        # Excel verilerini arayüze ekle
        for kayit in VERILER:
            satir = EtiketKaydi(kayit["bina"], kayit["tarih"], kayit["renk"])
            self.liste.add_widget(satir)

        kaydirma_alani.add_widget(self.liste)
        ana_ekran.add_widget(kaydirma_alani)

        return ana_ekran

if __name__ == '__main__':
    EtiketTakipUygulamasi().run()