Hand-Gesture Controlled Environment-Aware Car

Özetle, el hareketleri kullanılarak araca ileri, geri, sağ, sol manevraları yaptırılabilmekte veya araç durdurulabilmektedir. Araç üzerinde bulunan sensörler sayesinde, aracın dört cephesindeki mesafeler santimetre cinsinden el istasyonuna anlık olarak iletilmektedir. Buna ek olarak, aynı sensörler aracılığıyla anlık sıcaklık ve nem değerleri de el istasyonunda görüntülenebilmektedir. El istasyonu, belirli aralıklarla ekrandaki bu değerleri güncellemektedir.

El hareketleri Python ile algılanarak Arduino’ya gönderilmektedir. Arduino, aldığı komut doğrultusunda dört motorun kontrolünü bağımsız şekilde sağlayabilmektedir. Motorlar, gelen komuta karşılık önceden belirlenmiş hareketleri 1 saniye boyunca gerçekleştirmektedir.

Bilgisayar ile araç arasındaki iletişim HC-06 modülü, araç ile el istasyonu arasındaki iletişim ise HC-05 kablosuz haberleşme modülü aracılığıyla sağlanmaktadır.

Proje ile ilgili tüm ayrıntılar PDF dosyasında yer almaktadır.
