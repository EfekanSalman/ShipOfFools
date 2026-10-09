# Gerçek Yoksunluk × Karar Mimarisi — Sonuçlar

## Durum ve yorum düzeyi

**Koşu tamamlandı: 2026-10-09.** Protokol (`EXPERIMENT_PROTOCOL_DEPRIVATION.md`)
koşudan önce yazıldı ve commit edildi (`d0c9bda`). Model içi, kuramsal/keşifsel
analizdir; insan verisine kalibrasyon yoktur.

## Yöntem (özet)

- Kapasite 90/120 × yenilenme 0.004 (yoksun) / 0.010 (depo boş, ajanlar
  büyük ölçüde tok) × dört karar kolu = 16 hücre; 30 seed bloğu
  (94000–94029); 480 simülasyon.
- `agent_update_order="shuffled"` (ISSUE-016). 80 kurucu ajan, 500 tick,
  `agent_rng_mode="shared"`. Son 100 tick seed içinde ortalandı.
- Yenilenme kontrastı = 0.010 eksi 0.004 = **tok eksi yoksun**. Pozitif
  değer, ölçünün tok koşulda daha yüksek olduğunu gösterir.
- Köşeli parantezler 10.000 çekilişli seed-blok bootstrap %95 aralığıdır.

## Manipülasyon kontrolü

| Ölçü | `intact` | `provisions_only` | `scoring_only` | `need_based` |
|---|---:|---:|---:|---:|
| Yoksun pay — yenilenme kontrastı | −0.206 [−0.213, −0.199] | −0.214 [−0.223, −0.205] | −0.077 [−0.087, −0.068] | −0.236 [−0.243, −0.228] |
| Gerçek kıtlık — hücre ortalamaları | 1.000 | 0.998–1.000 | 0.991–1.000 | 0.984–1.000 |
| Kıtlık inancı — hücre ortalamaları | 0.990–0.991 | 0.982–0.990 | 0.982–0.986 | 0.976–0.985 |

Yoksunluk manipülasyonu dört kolda da geçti; depo göstergesi ve ona dair inanç
her hücrede doygun. İki yenilenme düzeyi arasındaki davranış farkı doğrudan
`scarcity_belief` terimlerinden gelemez. `scoring_only` kolunda kontrast
daha küçük, çünkü o kolun "tok" düzeyi de %13–19 yoksun.

## Birincil sonuçlar

Yenilenme kontrastı (tok eksi yoksun):

| Sonuç | `intact` | `provisions_only` | `scoring_only` | `need_based` |
|---|---:|---:|---:|---:|
| Çatışma (`steal` payı) | +0.048 [+0.045, +0.050] | +0.051 [+0.047, +0.054] | −0.006 [−0.009, −0.003] | −0.034 [−0.037, −0.032] |
| İşbirliği | +0.015 [+0.014, +0.017] | +0.020 [+0.018, +0.022] | −0.009 [−0.012, −0.006] | +0.020 [+0.017, +0.023] |

Çatışma kontrastının erzak × skor ayrışımı: erzak ana etkisi −0.012
[−0.015, −0.010], skor ana etkisi −0.069 [−0.073, −0.066], etkileşim −0.031
[−0.038, −0.025]. Etkileşim sıfırı dışladığı için, kural gereği ana etkiler
yerine dört kolun ayrı kontrastları esas alınır.

Önceden yazılan kurala göre: **özgün skorlu iki kolda yoksunluk `steal` payını
düşürüyor (4.8–5.1 puan), ihtiyaç temelli skorlu iki kolda artırıyor (0.6 ve
3.4 puan); dört aralık da sıfırı dışlıyor. Gerçek yoksunluğun çatışma
ölçüsüne etkisinin yönü karar kuralı varsayımına bağlıdır.**

Beklentilerle karşılaştırma:

| Beklenti | Sonuç |
|---|---|
| Özgün skor: yoksunlukta `steal` daha düşük | Doğrulandı (+0.048, +0.051) |
| Özgün skor: yoksunlukta işbirliği daha düşük | Doğrulandı (+0.015, +0.020) |
| İhtiyaç temelli skor: yoksunlukta `steal` daha yüksek | Doğrulandı (−0.006, −0.034); `scoring_only`'de çok küçük |
| İhtiyaç temelli skor: yoksunlukta işbirliği daha düşük | `need_based`'de doğrulandı (+0.020); **`scoring_only`'de tutmadı** (−0.009: yoksunlukta işbirliği daha yüksek) |
| İhtiyaç temelli kollarda açlık ölümü daha fazla | Doğrulandı (aşağıda) |
| Erzak yoksun payı düşürür, birincil etkisi küçük ama öncekinden büyük | Kısmen: birincil kontrasta etkisi artık ayırt ediliyor ve skorla etkileşiyor; yoksun pay kapasiteye göre iki yönde değişiyor (aşağıda) |

## Hücre ortalamaları

Sütunlar: 90/0.004, 90/0.010, 120/0.004, 120/0.010.

| Ölçü | Kol | 90 yoksun | 90 tok | 120 yoksun | 120 tok |
|---|---|---:|---:|---:|---:|
| `steal` payı | `intact` | 0.268 | 0.318 | 0.280 | 0.325 |
| | `provisions_only` | 0.259 | 0.321 | 0.291 | 0.331 |
| | `scoring_only` | 0.218 | 0.219 | 0.219 | 0.206 |
| | `need_based` | 0.230 | 0.215 | 0.252 | 0.198 |
| `forage` payı | `intact` | 0.260 | 0.187 | 0.255 | 0.166 |
| | `provisions_only` | 0.295 | 0.181 | 0.239 | 0.163 |
| | `scoring_only` | 0.124 | 0.121 | 0.123 | 0.120 |
| | `need_based` | 0.139 | 0.123 | 0.127 | 0.123 |
| Yoksun pay | `intact` | 0.253 | 0.070 | 0.257 | 0.027 |
| | `provisions_only` | 0.319 | 0.027 | 0.146 | 0.011 |
| | `scoring_only` | 0.236 | 0.185 | 0.236 | 0.133 |
| | `need_based` | 0.259 | 0.067 | 0.321 | 0.042 |
| Açlık ölümü (toplam) | `intact` | 29.0 | 0.0 | 9.4 | 0.0 |
| | `provisions_only` | 12.7 | 0.0 | 0.0 | 0.0 |
| | `scoring_only` | 60.1 | 12.4 | 45.6 | 1.8 |
| | `need_based` | 48.0 | 0.0 | 13.8 | 0.0 |
| Nüfus | `intact` | 56.0 | 86.1 | 74.7 | 90.6 |
| | `provisions_only` | 73.9 | 86.4 | 84.6 | 89.4 |
| | `scoring_only` | 42.6 | 90.7 | 58.3 | 103.3 |
| | `need_based` | 56.7 | 103.9 | 86.3 | 107.7 |
| Ortalama servet | `intact` | 38.0 | 49.2 | 37.8 | 59.3 |
| | `provisions_only` | 1.0 | 42.6 | 7.0 | 57.5 |
| | `scoring_only` | 27.3 | 32.2 | 27.4 | 39.5 |
| | `need_based` | 1.5 | 19.3 | 1.2 | 32.7 |
| Stres | `intact` | 0.795 | 0.847 | 0.848 | 0.846 |
| | `provisions_only` | 0.545 | 0.837 | 0.770 | 0.846 |
| | `scoring_only` | 0.578 | 0.699 | 0.626 | 0.674 |
| | `need_based` | 0.415 | 0.653 | 0.560 | 0.608 |

## İkincil keşifsel sonuçlar

Mekanizma açıklamaları sınanmamış adaylardır.

- **Özgün skorda yoksunluk toplamaya yöneltiyor.** `intact` kolda `forage`
  payı yoksun koşulda 0.26, tok koşulda 0.17–0.19; boşalan pay `steal` ve
  `spread_belief`'ten geliyor. Protokolde öngörülen sıkıştırma budur.
- **İhtiyaç temelli skorda ajanlar yoksunken de toplamıyor.** `forage` payı
  dört hücrede 0.12–0.14'te sabit. Skor, toplamanın getirisini depo inancıyla
  çarpıyor; inanç ≈1 olduğunda aciliyet terimi sıfırlanıyor. Sonuç: en çok
  açlık ölümü bu kollarda (`scoring_only` 60 ve 46; `intact` 29 ve 9).
  **Bu, mekanizmanın tasarım zayıflığıdır:** depo göstergesi boşken bile her
  tick yenilenen bir akış var ve toplayan ajan ondan pay alıyor; ajanın
  "depo boş, toplamak boşuna" inancı fiilen yanlış. Skor biçimi bu sonuca
  bakılarak değiştirilmedi (ilke 9); düzeltme ayrı bir protokol ister.
- **Erzak yoksunlukta işe yarıyor.** Özgün skorla açlık ölümü 29 → 13
  (kapasite 90) ve 9.4 → 0.03 (kapasite 120); yoksun hücrelerde servet
  neredeyse tamamen yeniyor (38 → 1). Tok rejimlerdeki etkisizliğin nedeni
  açlığın oluşmamasıydı (ISSUE-015); bu deney onu doğruluyor.
- **Erzak kollarında yoksun pay tek yönlü değişmiyor** (kapasite 90'da 0.25 →
  0.32, 120'de 0.26 → 0.15). Olası neden hayatta kalma seçilimi: erzak
  olmadan ölecek ajanlar hayatta ve yoksun kalıyor. Ölçü yaşayanlar
  üzerinden hesaplanır.
- **Servet tükenince stres düşüyor.** `provisions_only`, 90/yoksun hücresinde
  stres 0.55 (`intact` 0.80), `steal` payı ise benzer (0.26). Motorda hırsızlık
  ancak kurbanın serveti 1'in üzerindeyse gerçekleşir ve kurbana stres ekler;
  servet ≈1 iken girişimler boşa çıkıyor olabilir. Ablasyondaki "stres
  çalmayı izliyor" adayıyla uyumlu.
- Kapasitenin birincil ölçülere etkisi küçük (mutlak değeri ≤ 0.021).

## Kaynak deneyleriyle birlikte okuma

| Koşul | Karar kuralı | Elverişsiz koşulun `steal` payına etkisi |
|---|---|---|
| Depo boşalıyor, ajanlar tok (sabit sıra) | özgün | artırıyor (≈ +0.10) |
| | terim kesilmiş | hafif azaltıyor (≈ −0.012) |
| | ihtiyaç temelli | hafif artırıyor (≈ +0.012) |
| Depo zaten boş, ajanlar yoksun (karışık sıra) | özgün | azaltıyor (≈ −0.048) |
| | ihtiyaç temelli | artırıyor (≈ +0.034) |

Özgün karar kuralında "kıtlık çatışmayı artırır" sonucu yalnızca inanç
kanalıyla ve ajanlar tokken ortaya çıkıyor; ajanlar gerçekten yoksun
kaldığında aynı kural tersini veriyor. Modelden çıkarılabilecek sağlam sonuç
bir işaret ya da büyüklük değil, şudur: kıtlık → çatışma ilişkisi, (a) kıtlığın
inanç mı yoksa yoksunluk mu olduğuna ve (b) karar kuralına bağlıdır.

## Yorum sınırları

- Hücreler arasında nüfus çok farklı (43–108); paylar yaşayanlar üzerinden
  hesaplanır ve açlıktan ölenler ölçümden çıkar (hayatta kalma seçilimi).
- "Tok" düzey tam tok değil (yoksun pay 0.01–0.19, kola göre).
- Önceki deneyler sabit sırayla, bu deney karıştırılmış sırayla koşuldu;
  yukarıdaki tablo iki tasarımı yan yana koyar, doğrudan fark alınmamalıdır.
- Karşılaştırma düzeyini seçen ikinci kural pilot görüldükten sonra yazıldı.
- `provision_*` değerleri ve skor terimleri sınanmadı/değiştirilmedi; toplamada
  kütle korunumu tam değil; dış veriyle kalibrasyon yok.

## Tekrar üretim dosyaları

- Protokol ve komutlar: `EXPERIMENT_PROTOCOL_DEPRIVATION.md`.
- Pilot: `run_deprivation_pilot.py`, `output/deprivation_pilot.json` (sabit
  sıra), `output/deprivation_pilot_shuffled.json`.
- `output/deprivation/experiment.json`, `analysis.json`, `seed_summaries.csv`
  (480 satır); `timeseries.csv` git dışında.
