# Deney Protokolü: Kaynak Rejimi, İşbirliği ve Çatışma

**Durum:** protokol final koşudan önce sabitlendi; final koşu 2026-10-04'te
tamamlandı. Kalibrasyon/pilot seed'leri final sonuçlara dahil edilmedi. Sonuçlar
ayrı [RESOURCE_STRESS_RESULTS.md](RESOURCE_STRESS_RESULTS.md) dosyasında.

## Araştırma sorusu

Modelde kaynak kapasitesi ve kaynak yenilenme oranları, nüfusun kıtlık,
işbirliği ve çatışma yörüngelerini nasıl değiştiriyor? Etkiler seed'ler arasında
ne kadar değişiyor ve kapasite ile yenilenme birbirini etkiliyor mu?

Bu, **model içi** müdahale sorusudur. Sonuçlar gerçek toplumlar hakkında doğrudan
nedensel iddia sayılmaz.

## Gerekçe ve tasarım

İlk kıtlık pilotunda `resource_capacity_per_agent=90, regen=0.019` ayarı ilk
seed grubunda orta kıtlık verdi, fakat yeni 20-seed grubunda ortalama kıtlık
0.853 oldu. `120 / 0.016` koşulu yeni grupta ortalama 0.582 verdi; ancak
seedlerin yalnızca 11/20'sinde son-pencere ortalaması 0.30–0.60 bandındaydı.
Bu nedenle tek bir “orta kıtlık” parametresi seçip bütün seed'lerin benzer
davranacağını varsaymıyoruz. Rejimler arası ve seedler arası dağılımı birlikte
inceliyoruz.

2×2 faktöriyel koşullar:

| Hücre | Kapasite/kurucu | Food ve water regen/tick |
|---|---:|---:|
| C90-R016 | 90 | 0.016 |
| C90-R019 | 90 | 0.019 |
| C120-R016 | 120 | 0.016 |
| C120-R019 | 120 | 0.019 |

Başlangıç kaynak stoku tüm hücrelerde kapasitenin aynı oranında tutulur:
başlangıç food ve water ayrı ayrı `2/3 × capacity`. Diğer parametreler
`Config` varsayılanlarında sabit kalır. Koşu: 80 kurucu ajan, 500 tick.

## Hipotezler

- **H1 — manipülasyon kontrolü:** kapasite veya yenilenme artışı, son dönem
  gerçek kıtlığını azaltır.
- **H2 — davranışsal sonuç:** daha elverişli kaynak koşulları, son dönemdeki
  işbirliği ölçüsünü artırır ve çatışma ölçüsünü azaltır.
- **H3 — etkileşim:** yenilenme oranının etkisi, kapasite düzeyine göre
  değişebilir.

H1, H2 ve H3 model içindeki sonuçlar olarak sınanacaktır. Belirsizlik aralığı
sıfırı kapsarsa sonuç “etki yok” diye kesinlenmeyecek; tahmin ve belirsizlik
raporlanacaktır.

## Sonuç ölçüleri

**Birincil sonuçlar:** her seed'in son 100 tick'i üzerindeki ortalama
`cooperation_rate` ve `conflict_rate`.

- `cooperation_rate`: yaşayan ajanların son eylemi `share` veya `socialize`
  olanların oranı.
- `conflict_rate`: yaşayan ajanların son eylemi `steal` olanların oranı.

Bunlar geniş “işbirliği” ve “çatışma” kavramlarının sınırlı operasyonel
tanımlarıdır; örneğin güven, paylaşım miktarı veya şiddet olarak
yorumlanmamalıdır.

**Manipülasyon kontrolü ve ikincil sonuçlar:** `true_scarcity`, `avg_stress`,
`avg_trust`, `inequality_gini`, `population`, `avg_health`. Son dönem
ortalamaları ve her seed için tam zaman serisi saklanır.

Her tick bağımsız gözlem sayılmaz. Bir simülasyon seed'i deney birimidir;
son-100-tick ortalaması seed düzeyindeki özet değerdir. Böylece tick'leri
bağımsız örnek sayan yapay örneklem büyüklüğünden kaçınılır.

## Seed ve örneklem planı

- 30 seed/hücre başlangıç final örneklemi; toplam 120 simülasyon.
- Final seed aralığı 30000–30119; her hücreye kesişmeyen 30'luk aralık verilir.
- Pilot seed aralıkları 10000–10063 ve 20000–20079'dur; final analizde
  kullanılmaz.
- Koşullar arasında aynı seed'in kullanıldığı iddia edilmeyecek. Mevcut
  simülasyonun ortak RNG akışı davranışlar ayrıştıktan sonra ortak şokları
  hizalamayı garanti etmez.
- 30 seed evrensel bir yeterlilik garantisi değildir. Seed düzeyi tahminler ve
  belirsizlik aralıkları raporlanır; sonuçların hassasiyeti sınırlıysa ek
  seed'ler ayrı, belgeli bir genişletme olarak eklenir.

## Analiz

- Hücre ortalamaları, seedler arası standart sapma ve %95 bootstrap güven
  aralığı raporlanır.
- Kapasite ana etkisi, yenilenme ana etkisi ve 2×2 farkların-farkı etkileşimi
  seed düzeyindeki özetlerden hesaplanır. Her hücre seedleri ayrı yeniden
  örneklenir; 10.000 bootstrap çekilişi, sabit ve kaydedilen analiz seed'i ile
  yapılır.
- Birincil sonuçlar iki sonuç ölçüsü ve üç faktöriyel kontrasttır; p-değerine
  göre ikili karar yerine tahmin ve güven aralıkları yorumlanır. Keşifsel
  ikincil ölçüler açıkça etiketlenir.
- Tam zaman serileri betimleyici ve dinamik değerlendirme için sunulur; tick
  düzeyi satırlar çıkarımsal örneklem sayısını büyütmek için kullanılmaz.
- Ham seed özetleri, zaman serileri, konfigürasyon, seed atama kuralı, Python
  sürümü ve analiz kodu birlikte saklanır.

## Yorum sınırları

- Final faktöriyel çalışmada ajanlar sabit list/ID sırasında ve anında etkilerle
  hareket etti. Tick başında karıştırılmış sırayla yapılan takip karşılaştırması
  `SCHEDULE_ROBUSTNESS_RESULTS.md` içinde raporlanır.
- Kaynak, yenilenme ve stres arasındaki geri besleme doğrusal olmayabilir;
  ortalamalar seed dağılımını saklayabileceği için tüm seed sonuçları da
  raporlanır.
- İnsan verisi ile kalibrasyon/doğrulama yapılmadığından sonuçlar gemi
  simülasyonunun iç dinamiklerine aittir.

## Uygulama

Deney `run_resource_factorial.py` ile 30 seed/hücre ayarında çalıştırıldı.
Ham sonuçlar `output/resource_factorial/` içinde. Protokol değişikliğiyle yeni
bir koşu yapılırsa bu çalışmanın yerine geçmemeli; ayrı sürüm ve seed aralığıyla
kaydedilmelidir.
