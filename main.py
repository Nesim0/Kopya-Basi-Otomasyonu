import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from Urun_ekle import *
import pandas as pd
from PyQt5.QtWidgets import QFileDialog
uygulama = QApplication(sys.argv)
pencere= QMainWindow()
ui= Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()
# Veritabanı İşlemleri
import sqlite3
baglanti = sqlite3.connect("urunler.db")
islem=baglanti.cursor()
table=islem.execute("create table if not exists urun (SirketIsmi text, MakineBilgisi text, BaslangicAdeti int, BitisAdeti int, CekimBirimi float, Tarih text, Dolar float, Euro float)")
baglanti.commit()

def urunekle():
    sirket_ismi = ui.lnsirketismi.text().strip() if ui.lnsirketismi.text().strip() else "Girilmedi"
    makine_bilgisi = ui.lnmakinebilgisi.text().strip() if ui.lnmakinebilgisi.text().strip() else "Girilmedi"
    baslangic_adet = ui.lnbaslangicadet.text().strip() if ui.lnbaslangicadet.text().strip() else "0"
    bitis_adeti = ui.lnbitisadet.text().strip() if ui.lnbitisadet.text().strip() else "0"
    cekim_birim = ui.lncekimbirimi.text().strip() if ui.lncekimbirimi.text().strip() else "0"
    tarih = ui.lntarih.text().strip() if ui.lntarih.text().strip() else "Girilmedi"
    dolar = ui.lndolar.text().strip() if ui.lndolar.text().strip() else "0"
    euro = ui.lneuro.text().strip() if ui.lneuro.text().strip() else "0"
    sirket_ismi_kategori = ui.combosirketismi.currentText()
    tarih_liste = ui.combotarih.currentText()
    dolar = float(dolar) if dolar else 0
    euro = float(euro) if euro else 0

    try:
        ekle= "insert into urun (SirketIsmi, MakineBilgisi, BaslangicAdeti, BitisAdeti, CekimBirimi,Tarih,Dolar,Euro) values(?,?,?,?,?,?,?,?)"
        islem.execute(ekle,(sirket_ismi, makine_bilgisi,baslangic_adet,bitis_adeti,cekim_birim,tarih,dolar,euro))
        kategorileri_yukle()
        baglanti.commit()
        ui.statusbar.showMessage("Kayıt ekleme işlemi başarılı", 3000)
        temizle()
        urun_listele()
        
    except Exception as error:
        ui.statusbar.showMessage("Kayıt ekleme işlemi sırasında hata meydana geldi!"+str(error), 3000)
        print(error)




def urun_listele():
    ui.tableWidget.clear()
    ui.tableWidget.setHorizontalHeaderLabels(("Şirket İsmi","Makine Bilgisi","Baslangıç Adeti","Bitiş Adeti","ÇekimBirimi","Tarih","Dolar","Euro"))
    # ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #Bu kısımdan tablo X ekseni scroll aç!
    sorgu= "select * from urun"
    islem.execute(sorgu)
    for indexSatir,kayitNumarasi in enumerate(islem):
        for indexSutun, kayıtSutun in enumerate (kayitNumarasi):
            ui.tableWidget.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayıtSutun)))

def urun_sil():
    secilen_urun = ui.tableWidget.selectedItems()
    
    if not secilen_urun:  
        ui.statusbar.showMessage("Lütfen silmek için bir ürün seçin!", 3000)
        return  # Fonksiyonu durdur
    
    # Silme onayı al
    silme_mesaj = QMessageBox.question(pencere, "Silme Onayı", "Silmek İstediğinizden Emin misiniz?", QMessageBox.Yes | QMessageBox.No)
    
    if silme_mesaj == QMessageBox.Yes:
        silinecek_urun_sirket_ismi = secilen_urun[0].text()
        silinecek_urun_makine_bilgisi = secilen_urun[1].text()
        
        sorgu = "Delete from urun where SirketIsmi = ? and MakineBilgisi = ?"
        try:
            islem.execute(sorgu, (silinecek_urun_sirket_ismi, silinecek_urun_makine_bilgisi,))
            baglanti.commit()
            ui.statusbar.showMessage("Kayıt Silme işlemi Başarıyla Gerçekleşti!", 3000)
            ui.combosirketismi.clear()
            kategorileri_yukle()
            urun_listele()
            temizle()
        except Exception as error:
            ui.statusbar.showMessage(f"Kayıt silme işlemi sırasında hata meydana geldi! {str(error)}", 3000)

    else:
        ui.statusbar.showMessage("Kayıt silme işlemi iptal edildi!", 3000)





def kategorileri_yukle():
    try:
        # Şirket isimlerini çek
        sirket_sorgu = "SELECT DISTINCT SirketIsmi FROM urun"
        islem.execute(sirket_sorgu)
        sirket_kategoriler = islem.fetchall()

        mevcut_sirketler = [ui.combosirketismi.itemText(i) for i in range(ui.combosirketismi.count())]
        for kategori in sirket_kategoriler:
            if kategori[0] not in mevcut_sirketler:
                ui.combosirketismi.addItem(kategori[0])

        # Tarih bilgilerini çek
        tarih_sorgu = "SELECT DISTINCT Tarih FROM urun"
        islem.execute(tarih_sorgu)
        tarih_kategoriler = islem.fetchall()

        mevcut_tarihler = [ui.combotarih.itemText(i) for i in range(ui.combotarih.count())]
        for tarih in tarih_kategoriler:
            if tarih[0] not in mevcut_tarihler:
                ui.combotarih.addItem(tarih[0])

    except Exception as error:
        print(f"Kategorileri yüklerken bir hata oluştu: {error}")

def filtrele():
    listelenecek_sirket= ui.combosirketismi.currentText()
    sorgu = "SELECT * from urun where SirketIsmi = ? "
    islem.execute(sorgu,(listelenecek_sirket,))
    ui.tableWidget.clear()
    for indexSatir,kayitNumarasi in enumerate(islem):
        for indexSutun, kayıtSutun in enumerate (kayitNumarasi):
            ui.tableWidget.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayıtSutun)))
    listelenecek_tarih= ui.combotarih.currentText()
    tarih_sorgu = "SELECT * from urun where Tarih = ? "
    islem.execute(tarih_sorgu,(listelenecek_tarih,))
    for indexSatir,kayitNumarasi in enumerate(islem):
        for indexSutun, kayıtSutun in enumerate (kayitNumarasi):
            ui.tableWidget.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayıtSutun)))
    ui.combotarih.setCurrentIndex(-1)
    ui.combosirketismi.setCurrentIndex(-1) 


def tablo_olustur():
    secilen_satirlar = ui.tableWidget.selectedItems()
    
    if not secilen_satirlar:  # Eğer hiç seçim yapılmamışsa
        ui.statusbar.showMessage("Lütfen Güncellemek için bir ürün seçin!", 3000)
        return  # Fonksiyonu durdur, başka işlem yapılmasın
    tum_veriler = []
    
    
    for i in range(0, len(secilen_satirlar), 8): #0'dan başla kaç öğe seçildiyse oraya kadar git ama 8'er 8'er atlayarak git!
        sirket_Adi = secilen_satirlar[i].text()
        makine_Bilgisi = secilen_satirlar[i + 1].text()
        baslangic_Adeti = int(secilen_satirlar[i + 2].text())
        bitis_Adeti = int(secilen_satirlar[i + 3].text())
        cekim_Birimi = secilen_satirlar[i + 4].text()
        tarih = secilen_satirlar[i + 5].text()
        dolar = float(secilen_satirlar[i + 6].text())
        euro = float(secilen_satirlar[i + 7].text())

        fark = bitis_Adeti - baslangic_Adeti
        hesap = fark * float(cekim_Birimi)
        dolar_hesap = hesap * dolar
        euro_hesap = hesap * euro

        if euro_hesap == 0:
            data = {
                "Şirket Adı": sirket_Adi,
                "Makine Bilgisi": makine_Bilgisi,
                "Başlangıç Adeti": baslangic_Adeti,
                "Bitiş Adeti": bitis_Adeti,
                "Çekilen Miktar": fark,
                "Çekim Birimi": cekim_Birimi,
                "Fiyat": dolar_hesap,
                "Tarih": tarih,
                "Dolar Kuru": dolar
            }
        else:
            data = {
                "Şirket Adı": sirket_Adi,
                "Makine Bilgisi": makine_Bilgisi,
                "Başlangıç Adeti": baslangic_Adeti,
                "Bitiş Adeti": bitis_Adeti,
                "Çekilen Miktar": fark,
                "Çekim Birimi": cekim_Birimi,
                "Fiyat": euro_hesap,
                "Tarih": tarih,
                "Euro Kuru": euro
            }
        
        tum_veriler.append(data)

    # Tüm verileri bir DataFrame'e dönüştürüyoruz
    df = pd.DataFrame(tum_veriler)

    # Dosya yolunu alıyoruz
    dosya_yolu, _ = QFileDialog.getSaveFileName(None, "Dosyayı Kaydet", "", "Excel Files (*.xlsx)")

    if dosya_yolu:
        try:
            # Tüm DataFrame'i Excel dosyasına yazıyoruz
            with pd.ExcelWriter(dosya_yolu, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="Hesaplar", index=False)
            ui.statusbar.showMessage(f"Veriler '{dosya_yolu}' dosyasına başarıyla kaydedildi!", 3000)
        except Exception as e:
            ui.statusbar.showMessage(f"Excel'e yazma sırasında bir hata oluştu: {str(e)}", 3000)
            print(e)


def guncelle():
    secilen_satir = ui.tableWidget.selectedItems()
    
    if not secilen_satir:  
        ui.statusbar.showMessage("Lütfen Güncellemek için bir ürün seçin!", 3000)
        return  # Fonksiyonu durdur
    sirket_ismi=secilen_satir[0].text()
    makine_bilgisi=secilen_satir[1].text()
    baslangic_adeti=secilen_satir[2].text()
    bitis_adeti=secilen_satir[3].text()
    cekim_birimi=secilen_satir[4].text()
    tarih=secilen_satir[5].text()
    dolar=secilen_satir[6].text()
    euro=secilen_satir[7].text()
    ui.lnsirketismi.setText(sirket_ismi)  
    ui.lnmakinebilgisi.setText(makine_bilgisi)  
    ui.lnbaslangicadet.setText(baslangic_adeti)  
    ui.lnbitisadet.setText(bitis_adeti)  
    ui.lncekimbirimi.setText(cekim_birimi) 
    ui.lntarih.setText(tarih) 
    ui.lndolar.setText(dolar)  
    ui.lneuro.setText(euro)
    sorgu= "Delete from urun where SirketIsmi = ? and MakineBilgisi = ? and BaslangicAdeti = ? and BitisAdeti = ? and CekimBirimi = ? and Tarih = ? and Dolar = ? and Euro = ?"
    try:
            islem.execute(sorgu,(sirket_ismi,makine_bilgisi,baslangic_adeti,bitis_adeti,cekim_birimi,tarih,dolar,euro,))
            baglanti.commit()
            ui.statusbar.showMessage("Kayıt Silme işlemi Başarıyla Gerçekleşti! ",3000)
            ui.combosirketismi.clear()
            kategorileri_yukle()
    except Exception as error:
            ui.statusbar.showMessage("Kayıt ekleme işlemi sırasında hata meydana geldi! "+str(error), 3000)





def temizle():
    ui.lnsirketismi.clear() 
    ui.lnmakinebilgisi.clear()
    ui.lnbaslangicadet.clear()
    ui.lnbitisadet.clear()
    ui.lncekimbirimi.clear()
    ui.lntarih.clear()
    ui.lndolar.clear()
    ui.lneuro.clear()


def baslat():
    urun_listele()
    kategorileri_yukle()
    pencere.show
    ui.combosirketismi.setCurrentIndex(-1)
    ui.combotarih.setCurrentIndex(-1)

baslat()

#butonlar
ui.btnekle.clicked.connect(urunekle)
ui.btnlistele.clicked.connect(urun_listele)
ui.btnkategorilistele.clicked.connect(filtrele)
ui.btnsil.clicked.connect(urun_sil)
ui.btntabloolustur.clicked.connect(tablo_olustur)
ui.btnguncelle.clicked.connect(guncelle)

sys.exit(uygulama.exec_())