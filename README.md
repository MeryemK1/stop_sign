# stop_sign
# Stop Levhası Tespit Projesi

Bu proje, OpenCV ve NumPy kullanarak görüntülerdeki “STOP” trafik levhalarını tespit eden basit bir Python uygulamasıdır. Renk ve şekil filtrelemeleriyle kırmızı sekizgen stop levhası bulunur, tespit edilen levha etrafına dikdörtgen çizilir ve merkez koordinatı hesaplanır.

---

## İçindekiler

1. [Genel Bakış](#genel-bakış)  
2. [Özellikler](#özellikler)  
3. [Gereksinimler](#gereksinimler)  
4. [Parametreler ve Ayarlar](#parametreler-ve-ayarlar)  

---

## Genel Bakış

- Bu proje, “stop_sign_dataset” klasöründeki resimleri tarar, her bir resimde kırmızı renk filtresi ve kontur analizleri ile STOP levhasını arar.  
- Bulunan levha etrafına yeşil bir dikdörtgen çizilir ve merkez koordinatı (mavi nokta) hesaplanarak fotoğraf “output_images” klasörüne kaydedilir.  
- Konsola tespit edilen levha bilgileri (merkez koordinatı, alan, köşe sayısı, en/boy oranı) yazdırılır.

---

## Özellikler

- **Renk Temelli Maskeleme:** HSV renk uzayında iki aralıkla kırmızı renk filtresi (turn1, turn2).  
- **Morfolojik İşlemler:** Gürültüyü azaltmak için Open ve Close operasyonları (3×3 kernel, 2 iterasyon).  
- **Kontur Analizi:**  
  - Kontur alanı eşiği: `area < 1000` → küçük konturlar elenir.  
  - Sekizgen benzeri şekil filtresi: `6 ≤ n_corners ≤ 10`.  
  - En/boy oranı: `0.8 ≤ w/h ≤ 1.2`.  
- **Adaylar Arasından Seçim:**  
  - Alan ve merkezden uzaklık kriterine göre sıralama → en uygun aday seçilir.  
- **Çıktı Görseli:**  
  - Yeşil dikdörtgen (bounding box)  
  - Mavi dolgu daire (centroid)  
  - Çıktı fotoğrafı “output_images/detected_<orijinal_dosya_adı>” olarak kaydedilir.  
- **Konsol Mesajları (Türkçe):** Hata, uyarı ve bilgi mesajları.

---

## Gereksinimler

- Python 3.6 veya üstü  
- Aşağıdaki Python paketleri:
  ```bash
  pip install opencv-python numpy
