# sibelemniyet.com

Sibel Emniyet'in (Uzm. Psikolojik Danışman – Eğitim Danışmanı, Bursa) kişisel sitesi. Türkçe, tek sayfa.

Sayfanın tamamı tek bir gökyüzüdür: kaydırdıkça gün sabahtan geceye ilerler, rüzgâr her bölümde yön değiştirir, bir kâğıt uçak okura eşlik eder. Misty bölümünde sis basar, rüzgâr dağıtır ve güneş Misty'nin küresine dönüşür.

## Adresler

| Adres | İçerik | Arama motorları |
|---|---|---|
| `sibelemniyet.com`, `www` | Yapım aşamasında sayfası (`yapim.html`) | açık |
| `demo.sibelemniyet.com` | Sitenin tamamı (`index.html`) | kapalı |
| `*.up.railway.app` | Sitenin tamamı | kapalı |

## Dosyalar

- `index.html`: sitenin tamamı. HTML, CSS ve JavaScript tek dosyada; derleme adımı ve paket yok.
- `yapim.html`: yapım aşamasında sayfası. `index.html`'in açılış sahnesinden türetildi; stil ve gökyüzü kodu aynıdır.
- `server.py`: Python standart kütüphanesiyle yazılmış küçük sunucu. Alan adına bakıp hangi sayfayı sunacağına karar verir, başka hiçbir dosyayı dışarı açmaz.
- `Dockerfile`: Railway bu dosyayla derler.

## Yerelde çalıştırma

```bash
python3 server.py
```

`http://localhost:8080` sitenin tamamını, `http://localhost:8080/yapim` yapım aşamasında sayfasını gösterir. Farklı bir port için `PORT` değişkenini verin.

## Yayın

Railway bu depoya bağlıdır; `main` dalına gelen her push yeniden yayınlanır. Tek servis iki alan adına da hizmet eder.

Ortam değişkenleri (hepsi isteğe bağlı):

| Değişken | Ne işe yarar |
|---|---|
| `PORT` | Dinlenecek port. Railway kendisi verir. |
| `UMAMI_WEBSITE_ID` | Ana alan adının Umami kimliği. Varsayılanı `server.py` içindedir. |
| `UMAMI_DEMO_WEBSITE_ID` | Verilirse demo da ölçülür. Boşsa demo ölçülmez. |
| `UMAMI_SRC` | Umami betiğinin adresi. |

## Ölçüm

Umami betiği kaynak dosyalarda yoktur; `server.py` sayfayı sunarken ekler. Bağlantılardaki `data-umami-event` öznitelikleri tıklamaları olay olarak kaydeder.

## Dış kaynaklar

- Google Fonts: Newsreader ve Figtree.
- Misty bölümündeki üç telefon görseli şimdilik doğrudan humindx.com'dan yüklenir. Kalıcı yayından önce depoya alınmalıdır.

## Siteyi ana alan adına almak

`server.py` içindeki yönlendirmede `demo` koşulunu tersine çevirmek yeterlidir: ana alan adı `index.html`'i sunar, `X-Robots-Tag: noindex` başlığı kaldırılır. Öncesinde tamamlanması gerekenler:

- E-posta, telefon ve fotoğraf yer tutucuları
- Telefon görsellerinin depoya alınması

## Tasarım notları

- Hareketi azaltma tercihi açıksa sahne sabit çizilir, harfler ve uçak yerinde durur.
- Gökyüzü tek bir Canvas 2D tuvalidir; kitaplık kullanılmaz.
