# Kaynak Rejimi Deneyi — Sonuçlar

## Durum ve yorum düzeyi

**Final koşu tamamlandı: 2026-10-04.** Bu, sabitlenmiş 2×2 kaynak rejimi
deneyinin simülasyon içi sonucudur; gerçek toplum verisine kalibrasyon veya
ampirik doğrulama değildir.

## Yöntem

- 80 kurucu ajan, 500 tick; `Config` varsayılanları dışında kapasite ve food /
  water yenilenme oranları değiştirildi.
- Kapasite 90/120; food ve water yenilenme oranı birlikte 0.016/0.019.
- Başlangıç food ve water stoku her koşulda kapasitenin 2/3'ü.
- 30 seed/hücre, 4 hücre, toplam 120 simülasyon. Seed aralığı 30000–30119;
  hücre seed blokları ayrık. Koşullar eşleşmiş-seed tasarımı değildir.
- Son 100 tick seed içinde ortalandı. Seed simülasyon birimidir; tick'ler
  bağımsız örnek olarak sayılmadı.
- Tablolardaki güven aralıkları seed düzeyindeki 10.000 çekilişli bootstrap
  %95 **marginal** aralıklarıdır. P-değeri veya familywise düzeltme
  uygulanmadı; yorumlar etki büyüklüğü ve aralıklarına dayanır.

## Birincil sonuçlar

Hücre başına son 100 tick ortalaması; köşeli parantez %95 bootstrap GA, `SD`
seedler arası standart sapmadır.

| Kapasite / regen | İşbirliği ölçüsü | Çatışma ölçüsü | Gerçek kıtlık |
|---|---:|---:|---:|
| 90 / 0.016 | 0.174 [0.172, 0.177], SD 0.007 | 0.320 [0.316, 0.324], SD 0.011 | 0.978 [0.963, 0.992], SD 0.042 |
| 90 / 0.019 | 0.206 [0.199, 0.214], SD 0.022 | 0.287 [0.278, 0.295], SD 0.026 | 0.803 [0.744, 0.860], SD 0.165 |
| 120 / 0.016 | 0.252 [0.244, 0.261], SD 0.024 | 0.231 [0.222, 0.241], SD 0.027 | 0.493 [0.431, 0.555], SD 0.178 |
| 120 / 0.019 | 0.308 [0.300, 0.315], SD 0.022 | 0.178 [0.171, 0.184], SD 0.018 | 0.169 [0.123, 0.221], SD 0.140 |

### Faktöriyel kontrastlar

Etki = yüksek düzey eksi düşük düzey. Etkileşim = kapasite farklarının
yenilenme düzeyleri arasındaki farkı.

| Sonuç | Kapasite etkisi | Yenilenme etkisi | Kapasite × yenilenme |
|---|---:|---:|---:|
| İşbirliği ölçüsü | +0.090 [0.083, 0.097] | +0.044 [0.036, 0.051] | +0.023 [0.009, 0.037] |
| Çatışma ölçüsü | −0.099 [−0.107, −0.091] | −0.043 [−0.051, −0.036] | −0.020 [−0.035, −0.005] |
| Gerçek kıtlık | −0.560 [−0.610, −0.510] | −0.249 [−0.299, −0.199] | −0.149 [−0.249, −0.046] |

İşbirliği ve çatışma için kontrast aralıklarının tümü model içinde beklenen
yönde yer aldı: yüksek kapasite/yenilenme koşullarında `share`/`socialize`
eylemlerinin oranı yükseldi, `steal` oranı düştü. Kaynak manipülasyonu da
kıtlık ölçüsünde açık bir değişim üretti. Bu, manipüle edilen konfigürasyonların
simülasyon içindeki etkisidir; tek başına kıtlığın insan toplumlarında bu
sonuçlara neden olduğunu göstermez.

## Seed değişkenliği ve ikinci düzey bulgular

`120 / 0.016` koşulunun ortalama kıtlığı orta bantta olsa da seedler benzer
seyir izlemedi: son-pencere seed ortalaması 17/30 seed'de 0.30–0.60 aralığında
kaldı; aralık 0.085–0.819 idi. Dolayısıyla “orta ortalama”, her koşunun orta
kıtlıkta kaldığı anlamına gelmiyor. Kıtlık yörüngelerinin değişkenliği önemli
bir araştırma konusu.

Diğer son-pencere ortalamaları:

| Kapasite / regen | Stres | Ortalama güven | Gini | Nüfus |
|---|---:|---:|---:|---:|
| 90 / 0.016 | 0.842 | −0.034 | 0.412 | 93.1 |
| 90 / 0.019 | 0.763 | −0.015 | 0.403 | 105.0 |
| 120 / 0.016 | 0.653 | 0.002 | 0.415 | 111.5 |
| 120 / 0.019 | 0.518 | 0.016 | 0.427 | 117.3 |

Stres ve güven daha elverişli kaynak koşullarında beklenen yönde değişirken,
Gini düşmedi; yüksek kapasite düzeyinde biraz daha yüksek çıktı. Bu, modelde
kaynak bolluğunun eşitsizliği otomatik azaltmadığını gösteren keşifsel bir
bulgudur. Gini için seed aralıkları ve mekanizma etkileşimleri ayrıca
incelenmelidir.

## Ölçü tanımları ve sınırlar

- `cooperation_rate`, yaşayan ajanların son eylemi `share` **veya** `socialize`
  olanların payıdır. İşbirliği davranışının dar bir vekil ölçüsüdür.
- `conflict_rate`, yaşayan ajanların son eylemi `steal` olanların payıdır;
  fiziksel şiddet ölçüsü değildir.
- `true_scarcity` fiziksel food/water stoklarının kapasiteye oranından türetilir.
  Ajanların inançları bu gerçek değerle aynı şey değildir.
- Ajanlar tick içinde sabit liste sırasıyla ve anında etkilerle işliyor.
  Karıştırılmış sıra ve ajan-başı RNG ile takip karşılaştırmaları sonradan
  yapıldı: `SCHEDULE_ROBUSTNESS_RESULTS.md`, `AGENT_RNG_ROBUSTNESS_RESULTS.md`.
- İşbirliği/çatışma kontrastları karar formülündeki doğrudan `scarcity_belief`
  terimlerine bağlıdır (ISSUE-013); ayrıştırma `SCARCITY_LINK_ABLATION_RESULTS.md`
  içindedir.
- Deney kaynak parametrelerini manipüle etti; kıtlığı ayrıca izole bir müdahale
  olarak atamadı. Aracı/mediatör iddiaları için yeni bir deney tasarımı gerekir.
- Seed bazlı bootstrap aralıkları seed belirsizliğini özetler; model yapısı,
  seçilen mekanizma ve parametre varsayımlarındaki belirsizliği kapsamaz.

## Tekrar üretim dosyaları

- [Tam sonuç JSON'u](output/resource_factorial/results.json): konfigürasyon,
  seed ataması, hücre istatistikleri ve tüm faktöriyel kontrastlar.
- [Seed özetleri CSV](output/resource_factorial/seed_summaries.csv): 120 seed'in
  her birinde son 100 tick ortalamaları.
- [Tam zaman serisi CSV](output/resource_factorial/timeseries.csv): her seed'in
  tüm tick'leri ve metrikleri (60.000 satır).
- Kod ve önceden yazılmış yöntem: `run_resource_factorial.py`,
  `EXPERIMENT_PROTOCOL_RESOURCE_STRESS.md`.
