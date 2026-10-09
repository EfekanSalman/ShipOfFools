# Kimlik Geri Beslemesi × Kaynak Rejimi — Sonuçlar

## Durum ve kapsam

**Deney tamamlandı: 2026-10-05.** Bu, 2×2×2 faktöriyel model içi
keşifsel analizdir; insan verisine kalibrasyon veya ampirik doğrulama değildir.

## Yöntem

- 80 kurucu ajan, 500 tick; son 100 tick seed içinde ortalandı.
- Kaynak kapasitesi 90/120; gıda ve su yenilenmesi birlikte 0.016/0.019.
- `identity_feedback_strength` 0.0/0.5. Başlangıç food/water stoku tüm
  koşullarda kapasitenin 2/3'ü.
- 8 koşul hücresi × 30 seed = 240 simülasyon. Aynı 30 seed bütün sekiz
  hücrede kullanıldı (50000–50029), böylece seed bloklaması yapıldı.
- Sabit ajan sırası ve mevcut varsayılan `agent_rng_mode="shared"` kullanıldı.
  Müdahale yolları ayrıştıkça aynı seed etiketi RNG çekilişlerinin hizasını
  korumaz; eşleşme tam ortak-rastgele-sayı tasarımı değildir.
- Seed simülasyonu analiz birimidir. 10.000 paired seed-block bootstrap
  örneklemesi kullanıldı. P-değeriyle ikili karar veya çoklu-ölçü düzeltmesi
  yapılmadı.

## Birincil sonuçlar

Kimlik etkisi = `identity_feedback_strength=0.5` eksi `0.0`. Parantezler
%95 seed-bootstrap aralıklarıdır. İşbirliği dar vekil ölçüdür; `share` veya
`socialize` son eylemi payıdır. Çatışma `steal` son eylemi payıdır.

| Kaynak rejimi | Ortalama güven | Çatışma ölçüsü | İşbirliği ölçüsü |
|---|---:|---:|---:|
| 90 / 0.016 | −0.0182 [−0.0198, −0.0168] | +0.0579 [+0.0522, +0.0636] | −0.0314 [−0.0357, −0.0275] |
| 90 / 0.019 | −0.0165 [−0.0194, −0.0136] | +0.0430 [+0.0359, +0.0501] | −0.0192 [−0.0267, −0.0115] |
| 120 / 0.016 | −0.0138 [−0.0162, −0.0112] | +0.0273 [+0.0165, +0.0387] | −0.0102 [−0.0229, +0.0019] |
| 120 / 0.019 | −0.0126 [−0.0146, −0.0106] | +0.0175 [+0.0095, +0.0257] | +0.0014 [−0.0077, +0.0100] |

## Kimlik × kaynak kontrastları

Kontrastlar, kimlik geri beslemesinin 0.5–0.0 etkisinin yüksek kaynak faktörü
ile düşük kaynak faktörü arasındaki farkıdır. Üçlü terim, kapasiteye bağlı
kimlik etkisinin yenilenme düzeyine göre değişim farkıdır.

| Sonuç | Kimlik ortalama etkisi | Kimlik × kapasite | Kimlik × yenilenme | Üçlü etkileşim |
|---|---:|---:|---:|---:|
| Ortalama güven | −0.0152 [−0.0163, −0.0142] | +0.0042 [+0.0017, +0.0067] | +0.0015 [−0.0010, +0.0039] | −0.0006 [−0.0045, +0.0034] |
| Çatışma ölçüsü | +0.0364 [+0.0318, +0.0409] | −0.0280 [−0.0373, −0.0181] | −0.0123 [−0.0202, −0.0047] | +0.0050 [−0.0063, +0.0173] |
| İşbirliği ölçüsü | −0.0149 [−0.0195, −0.0101] | +0.0209 [+0.0105, +0.0304] | +0.0119 [+0.0036, +0.0210] | −0.0006 [−0.0144, +0.0122] |

Sonuçlar, bu modelde yüksek kimlik geri beslemesinin güveni düşürüp `steal`
oranını artırdığını destekliyor. Bu ilişki düşük kapasitede daha büyük çıktı.
İşbirliği ölçüsündeki düşüş düşük kapasite koşullarında belirgindi; yüksek
kapasite/yüksek yenilenmede aralık sıfırı kapsadı. Yenilenmenin kimlik etkisini
azaltması çatışma ve işbirliği ölçülerinde görülürken güven için aralık sıfırı
kapsıyor. Üçlü etkileşim aralıkları sıfırı kapsadı.

## İkincil keşifsel sonuçlar

Dört kaynak hücresindeki kimlik etkisinin ortalaması:

| Ölçü | Kimlik etkisi (%95 GA) |
|---|---:|
| Gerçek kıtlık | −0.0110 [−0.0421, +0.0193] |
| Gini eşitsizliği | +0.1106 [+0.1055, +0.1155] |
| Son nüfus | −10.51 [−12.35, −8.63] |
| Kimlik oluşum oranı | +0.0023 [+0.0014, +0.0033] |
| Pozitif ilişki oranı | −0.0360 [−0.0397, −0.0323] |

Gini, nüfus ve diğer ikincil ölçüler protokolde keşifsel olarak işaretlendi;
çoklu karşılaştırma düzeltmesi uygulanmadı. Özellikle Gini farkı büyük görünse
de, mekanizmanın ayrıştırılması ve alternatif yapısal varsayımlarla tekrarı
gerekir. Kimlik geri beslemesi kaynak kıtlığı ölçüsünü belirgin biçimde
değiştirmemiş görünüyor; kıtlık düzeyi bu deneyde bir sonuçtur, ayrıca deneysel
olarak sabitlenen aracı değişken değildir.

## Yorum sınırları ve sonraki adım

- `identity_feedback_strength` 0.0/0.5 uç değerleri test edildi; doz-cevap
  eğrisi bu yeni rejimlerde yeniden incelenmedi.
- Seed bootstrap belirsizliği özetler; mekanizma, parametre ve ölçüm tanımı
  belirsizliğini içermez.
- Kimlik oluşum oranı yüksek olabilir; ortalama kimlik etkisi, bütün kimlik
  etiketlerinin veya davranış yollarının ayrı ayrı açıklandığı anlamına gelmez.
- Sonraki adım, öncelikle Gini/nüfus etkisini ayrıştırmak için seed düzeyindeki
  yörüngeleri ve kimlik etiketlerini incelemek; ardından kaynak rejimlerinde
  ara dozları ancak önceden tanımlı hipotezle test etmektir.

## Ek (2026-10-07): etiket ve eylem payları — post hoc, keşifsel

İlk koşu kimlik etiketi paylarını ve eylemlerin ayrı paylarını kaydetmemişti.
`run_identity_label_followup.py` aynı 240 dünyayı aynı seed'lerle yeniden koştu;
240 koşunun tamamında `mean_conflict_rate` orijinal seed özetleriyle eşleşti
(fark ≤ 1e−12). Bu analiz protokolde yoktu; sonuçlar görüldükten sonra
eklenmiştir ve aralık/çoklu karşılaştırma düzeltmesi içermez. Değerler son 100
tick'in 30 seed ortalamasıdır; ok `identity_feedback_strength` 0.0 → 0.5.

| Kaynak rejimi | `benefactor` payı | `opportunist` payı | `survivor` payı | `steal` payı | `share` payı | Gini |
|---|---:|---:|---:|---:|---:|---:|
| 90 / 0.016 | 0.078 → 0.063 | 0.523 → 0.488 | 0.394 → 0.445 | 0.285 → 0.343 | 0.093 → 0.074 | 0.351 → 0.462 |
| 90 / 0.019 | 0.264 → 0.217 | 0.409 → 0.422 | 0.314 → 0.353 | 0.267 → 0.310 | 0.105 → 0.098 | 0.347 → 0.451 |
| 120 / 0.016 | 0.439 → 0.339 | 0.305 → 0.387 | 0.240 → 0.262 | 0.217 → 0.244 | 0.140 → 0.142 | 0.351 → 0.465 |
| 120 / 0.019 | 0.526 → 0.406 | 0.250 → 0.357 | 0.206 → 0.220 | 0.171 → 0.189 | 0.176 → 0.189 | 0.362 → 0.475 |

Gözlemler:

- **Etiket bileşimi kaynak rejimine bağlı.** Geri besleme kapalıyken bile
  `opportunist` payı en kıt rejimde 0.52, en bol rejimde 0.25; `benefactor`
  payı 0.08'e karşı 0.53. "Kimlik etkisi" her rejimde farklı bir etiket
  karışımına uygulanıyor.
- **`steal` artışı en büyük olduğu yerde `opportunist` payı artmıyor.**
  90/0.016'da `steal` +0.058 artarken `opportunist` payı 0.523'ten 0.488'e
  iniyor (30 seed'in 5'inde artış). Buradaki artış, etiket dönüşümünden değil,
  zaten nüfusun yarısı olan `opportunist` ajanların `steal` skoruna eklenen
  doğrudan bonustan (`decision.py`) geliyor görünüyor. Yani düşük kapasitede
  daha büyük çıkan çatışma etkisi büyük ölçüde "başlangıçtaki `opportunist`
  payı × sabit bonus" ile uyumlu (ISSUE-013).
- **Yüksek kapasitede mekanizma farklı.** `benefactor` payı 0.10–0.12 düşüp
  `opportunist` payı 0.08–0.11 artıyor (30 seed'in 28–29'unda); buna rağmen
  `share` payı düşmüyor, hafif artıyor. Geri besleme burada etiket
  bileşimini değiştiriyor ama kalan `benefactor` ajanların bonusu `share`
  payını koruyor.
- **Gini artışı rejimden bağımsız.** Dört hücrede +0.104 ile +0.114 arasında
  ve 120 seed çiftinin tamamında pozitif. `steal` artışı rejime göre üç kat
  değişirken Gini artışı değişmiyor; dolayısıyla Gini farkı yalnızca çalma
  oranıyla açıklanamaz. Aday açıklamalar (sınanmadı): `survivor` etiketinin
  `forage` bonusu tek gelir kaynağını belirli ajanlarda yoğunlaştırıyor olabilir;
  `forage` payı dört hücrede de artıyor. Etiket bazında servet kaydı
  gerektirir.
- `socialize` ve `spread_belief` payları dört hücrede de düşüyor; işbirliği
  ölçüsündeki düşüşün düşük kapasitede `share` + `socialize`, yüksek
  kapasitede yalnızca `socialize` kaynaklı olduğu görülüyor.

Dosyalar: `output/identity_label_followup/seed_summaries.csv`, `summary.json`.

## Tekrar üretim dosyaları

- Protokol: `EXPERIMENT_PROTOCOL_IDENTITY_BY_RESOURCE.md`.
- Koşu betiği: `run_identity_resource_factorial.py`.
- Analiz: `analyze_identity_resource_factorial.py`.
- Tasarım metaverisi ve analiz JSON'u: `output/identity_resource_factorial/experiment.json`, `analysis.json`.
- Seed özetleri: `output/identity_resource_factorial/seed_summaries.csv` (240 satır).
- Tam zaman serisi: `output/identity_resource_factorial/timeseries.csv` (120.000 tick satırı).
