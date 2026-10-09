# İhtiyaç Temelli Karar Mimarisi × Kaynak Rejimi — Sonuçlar

## Durum ve yorum düzeyi

**Koşu tamamlandı: 2026-10-09.** Protokol
(`EXPERIMENT_PROTOCOL_NEED_BASED_DECISION.md`) 2026-10-07'de koşudan önce
yazıldı ve değiştirilmedi. İlk koşu 240 dünyanın 50'sinde oturum kapanınca
kesildi; özet veya analiz dosyası üretmemişti ve sonuçlarına bakılmadı. Deney
aynı seed'lerle baştan koşuldu. Model içi, kuramsal/keşifsel analizdir.

## Yöntem (özet)

- 2×2 kaynak (kapasite 90/120; food+water yenilenme 0.016/0.019) × 2 mimari
  (`intact` = varsayılan heuristic; `need_based`) = 8 hücre; 30 seed bloğu
  (70000–70029) her hücrede; 240 simülasyon.
- 80 kurucu ajan, 500 tick, sabit sıra, `agent_rng_mode="shared"`. Son 100
  tick seed içinde ortalandı; seed analiz birimidir.
- Köşeli parantezler 10.000 çekilişli seed-blok bootstrap %95 aralığıdır.
  P-değeri veya çoklu karşılaştırma düzeltmesi yok.

## Birincil sonuçlar

Kontrast = yüksek düzey eksi düşük düzey. Oran = `need_based` / `intact`.

| Sonuç / kontrast | `intact` | `need_based` | Oran |
|---|---:|---:|---:|
| Çatışma — kapasite | −0.098 [−0.105, −0.090] | −0.012 [−0.013, −0.010] | 0.12 [0.10, 0.14] |
| Çatışma — yenilenme | −0.042 [−0.047, −0.038] | −0.007 [−0.008, −0.005] | 0.15 [0.12, 0.19] |
| Çatışma — etkileşim | −0.024 [−0.040, −0.009] | +0.008 [+0.004, +0.011] | — |
| İşbirliği — kapasite | +0.092 [+0.084, +0.099] | +0.016 [+0.014, +0.018] | 0.17 [0.15, 0.20] |
| İşbirliği — yenilenme | +0.045 [+0.040, +0.050] | +0.008 [+0.006, +0.010] | 0.18 [0.13, 0.23] |
| İşbirliği — etkileşim | +0.024 [+0.011, +0.036] | −0.009 [−0.014, −0.005] | — |

Önceden yazılan kurala göre: `need_based` kolda dört ana etki kontrastı da
sıfırı dışlıyor ve işaretleri `intact` ile aynı. **İlişki doğrudan katsayı
olmadan, ihtiyaç kanalından da çıkıyor; ama büyüklüğü `intact` koldakinin
yaklaşık sekizde biri ile altıda biri arasında.** Protokoldeki beklenti işaret
bakımından doğrulandı. Kuralın kendi kaydı geçerlidir: bu, ilişkinin
"emergent" olduğunu kanıtlamaz; karar kuralındaki daha zayıf bir varsayımdan
da türediğini gösterir.

`intact` kolu üçüncü bağımsız seed bloğunda da aynı sonucu verdi (çatışma
kapasite etkisi −0.099, −0.101, −0.098).

Etkileşim terimleri iki kolda ters işaretli; `need_based` kolda kaynak
faktörleri birbirini güçlendirmek yerine doyuma gidiyor.

## Manipülasyon kontrolü

| Sonuç / kontrast | `intact` | `need_based` |
|---|---:|---:|
| Gerçek kıtlık — kapasite | −0.560 [−0.611, −0.507] | −0.527 [−0.563, −0.490] |
| Gerçek kıtlık — yenilenme | −0.250 [−0.283, −0.217] | −0.265 [−0.306, −0.222] |
| Kıtlık inancı — kapasite | −0.508 [−0.560, −0.456] | −0.498 [−0.532, −0.465] |
| Kıtlık inancı — yenilenme | −0.226 [−0.256, −0.195] | −0.243 [−0.279, −0.205] |

Kaynak manipülasyonu iki kolda da benzer büyüklükte kıtlık farkı üretiyor;
birincil kontrastlar yorumlanabilir.

## Hücre ortalamaları

| Ölçü | Kol | 90/0.016 | 90/0.019 | 120/0.016 | 120/0.019 |
|---|---|---:|---:|---:|---:|
| `steal` payı (çatışma) | `intact` | 0.319 | 0.289 | 0.234 | 0.179 |
| | `need_based` | 0.192 | 0.181 | 0.176 | 0.173 |
| `share` payı | `intact` | 0.084 | 0.108 | 0.143 | 0.191 |
| | `need_based` | 0.168 | 0.180 | 0.186 | 0.190 |
| `forage` payı | `intact` | 0.162 | 0.154 | 0.161 | 0.170 |
| | `need_based` | 0.126 | 0.139 | 0.153 | 0.168 |
| Gerçek kıtlık | `intact` | 0.992 | 0.837 | 0.527 | 0.182 |
| | `need_based` | 0.898 | 0.644 | 0.383 | 0.106 |
| Stres | `intact` | 0.844 | 0.765 | 0.657 | 0.522 |
| | `need_based` | 0.583 | 0.549 | 0.528 | 0.520 |
| Ortalama servet | `intact` | 60.9 | 56.2 | 49.7 | 49.1 |
| | `need_based` | 38.6 | 44.9 | 46.5 | 48.4 |
| Gini | `intact` | 0.416 | 0.409 | 0.420 | 0.433 |
| | `need_based` | 0.448 | 0.441 | 0.428 | 0.421 |
| Nüfus | `intact` | 94.3 | 106.9 | 115.7 | 117.8 |
| | `need_based` | 110.8 | 114.1 | 116.1 | 115.7 |

En bol hücrede (120/0.019) iki mimari neredeyse aynı davranış paylarını
veriyor; ayrışma kıtlık arttıkça büyüyor.

## İkincil keşifsel sonuçlar

Kapasite kontrastı (yüksek eksi düşük):

| Ölçü | `intact` | `need_based` |
|---|---:|---:|
| Ortalama servet | −9.1 [−10.3, −7.9] | +5.8 [+4.6, +6.9] |
| Gini | +0.015 [+0.007, +0.022] | −0.020 [−0.027, −0.013] |
| `forage` payı | +0.007 [+0.005, +0.010] | +0.028 [+0.026, +0.030] |
| `share` payı | +0.071 [+0.065, +0.078] | +0.014 [+0.012, +0.016] |
| `socialize` payı | +0.020 [+0.018, +0.022] | +0.002 [+0.001, +0.003] |
| `spread_belief` payı | −0.016 [−0.019, −0.013] | −0.039 [−0.042, −0.037] |
| Stres | −0.215 [−0.231, −0.200] | −0.042 [−0.051, −0.033] |
| Ortalama güven | +0.034 [+0.032, +0.035] | +0.003 [+0.002, +0.004] |
| Nüfus | +16.2 [+13.1, +19.2] | +3.4 [+0.9, +6.0] |
| `benefactor` etiketi payı | +0.234 [+0.215, +0.253] | +0.018 [+0.001, +0.035] |

Gözlemler (keşifsel; mekanizma açıklamaları sınanmamış adaylardır):

- **Servet iki mimaride ters yönde hareket ediyor.** `intact` kolda en kıt
  hücre en zengin hücredir (60.9'a karşı 49.1): servet hiçbir işe yaramadığı
  için birikir. `need_based` kolda kıtlıkta servet azalır (38.6'ya karşı
  48.4), çünkü yenir. Bu, ISSUE-014'ün veride görünen hâlidir.
- **Gini'nin kaynak rejimine tepkisi işaret değiştiriyor.** `intact` kolda
  bolluk Gini'yi hafif artırıyordu (ilk kaynak deneyindeki beklenmedik bulgu);
  `need_based` kolda bolluk Gini'yi düşürüyor. İlk bulgu, servetin yenemeyen
  bir sayı olmasına bağlı görünüyor; Gini üzerine çıkarımlar mimariye
  duyarlıdır.
- **Nüfus kıtlığa daha dayanıklı.** En kıt hücrede nüfus 94 yerine 111.
  Olası nedenler: erzakın ihtiyaç tamponu olması ve daha düşük `steal` payıyla
  daha düşük stres (0.58'e karşı 0.84). Ablasyondaki "nüfusu çalma kaynaklı
  stres sınırlıyor" adayıyla uyumlu, ama bu deney onu ayrıştırmaz.
- **Kıtlıkta boşalan `forage` payı `steal`'e değil çoğunlukla
  `spread_belief`'e gidiyor.** `spread_belief` skorundaki stres ve
  `scarcity_belief` terimleri bu mimaride de yerinde.
- Seed'ler arası değişkenlik `need_based` kolda çatışma ölçüsü için çok
  küçük (SD 0.006; `intact` kolda 0.012–0.029).

## Üç deneyin birlikte okunması

Çatışma ölçüsünde kapasite etkisi (ayrı seed blokları; kollar arası doğrudan
fark alınmamalı):

| Karar kuralı | Kapasite etkisi | Kaynak |
|---|---:|---|
| Doğrudan kıtlık inancı terimi (varsayılan) | −0.098 ile −0.101 | üç deney |
| Terim yok (`zero`) | +0.012 | ablasyon |
| Terim sabit (`fixed`) | +0.014 | ablasyon |
| İhtiyaç temelli, yenebilir erzak | −0.012 | bu deney |

Kaynak rejimi → çatışma ilişkisinin **yönü** iki farklı karar kuralında
aynı, üçüncüsünde ters; **büyüklüğü** karar kuralına göre yaklaşık sekiz kat
değişiyor. Bu modelden "kıtlık çatışmayı şu kadar artırır" türünde bir
büyüklük iddiası çıkarılamaz. Savunulabilir iddia yapısal belirsizliğin
kendisidir: sonucu kaynak dinamiği değil, bireysel karar kuralı varsayımı
belirliyor.

## Yorum sınırları

- `need_based` kol erzak yemeyi de ekler; iki kol aynı kıtlık düzeyinde
  çalışmaz (bu kolda kıtlık her hücrede biraz daha düşük). Karşılaştırma
  "karar kuralı + erzak" paketinedir; ikisi ayrıştırılmadı.
- Etkinin küçük çıkmasının nedeni sınanmadı. Adaylar: ortalama servet
  39–48 olduğundan ajanların erzakı nadiren tükeniyor ve aciliyet bastırılıyor;
  bir hırsızlığın getirisi (`g = 0.4`) toplamaya göre düşük.
- `provision_max_per_tick` ve diğer `provision_*` değerlerine duyarlılık
  sınanmadı. Bu sonuca bakılarak değiştirilmediler (ilke 9); duyarlılık ayrı
  protokol ve yeni seed bloğu gerektirir.
- Toplamada kütle korunumu tam değil (protokol, Sınırlar).
- Seed bootstrap seed belirsizliğini özetler; yukarıdaki tablo tam da bunun
  kapsamadığı model belirsizliğini gösteriyor.

## Tekrar üretim dosyaları

- Protokol: `EXPERIMENT_PROTOCOL_NEED_BASED_DECISION.md`.
- Koşu ve analiz komutları protokolün "Uygulama" bölümünde.
- `output/need_based_decision/experiment.json`, `analysis.json`,
  `seed_summaries.csv` (240 satır); `timeseries.csv` (120.000 tick gözlemi,
  git dışında).
