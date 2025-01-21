# Kopya Başı Takip Otomasyonu

Bu proje, makinelerin baskı sayıları, döviz kurları ve diğer önemli verilerin takip edilmesi ve işlenmesi için kullanılan bir otomasyon sistemidir. Kullanıcılar, makinelerin baskı sayılarından döviz kuru bilgilerine kadar bir dizi işlemi kolayca gerçekleştirebilir. 

## Kullanıcı Alanları

- **Şirket İsmi**: İşlem yapılan şirketin adını belirtir.
- **Makine Bilgisi**: Kullanılan makinenin adı veya model bilgisini belirtir.
- **Başlangıç Adeti**: Makinenin başlangıç baskı sayısı.
- **Bitiş Adeti**: Makinenin son baskı sayısı. Başlangıç ve bitiş adetleri arasındaki fark, makinenin aldığı toplam baskı sayısını hesaplamak için kullanılır.
- **Çekim Birimi**: Her bir baskı için alınacak ücreti belirtir.
- **Tarih**: Fatura kesim tarihini belirtir.
- **Dolar Kuru**: Dolar kuru.
- **Euro Kuru**: Euro kuru.

## Butonlar ve İşlemler

### Ürün Ekleme Butonu
Kullanıcı, gerekli alanları doldurduktan sonra yalnızca döviz kuru bilgisi girer (dolar veya euro) ve boş bırakılan alanlar otomatik olarak "Girilmedi" veya "0" olarak atanır. Bu işlem, yeni bir ürün kaydeder.

### Ürün Sil Butonu
Tabloya eklenen ürünlerden birini silmek için, tablonun sol tarafındaki numaralardan birine tıklanır ve o satır silinir.

### Ürün Güncelle Butonu
Tabloya eklenen bir ürünü güncellemek için, silmek istenilen ürünün numarasına tıklanır. Ürün bilgileri giriş alanlarına doldurulur. Ardından, ürünün eski kaydı silinir ve güncel bilgilerle ürün eklenir.

### Ürün Listele Butonu
Sistemdeki tüm kayıtlı bilgileri kullanıcıya listeleyerek, mevcut verilerin görüntülenmesini sağlar.

### Tablo Oluştur Butonu
Kullanıcı, tablonun sol tarafındaki numaralardan seçtiği satırı veya satırları, gerekli hesaplamaları yaparak Excel dosyasına kaydeder.

## Filtreleme

- **Şirket İsmi (Açılır Kutu)**: Seçilen şirket adına göre veriler filtrelenir.
  
- **Tarih (Açılır Kutu)**: Seçilen tarihe göre veriler filtrelenir. Ancak, **Şirket İsmi** ve **Tarih** filtreleri aynı anda sağlıklı çalışmaz.

## Teknolojiler

- Python
- PyQt
- SQLite
- Excel 