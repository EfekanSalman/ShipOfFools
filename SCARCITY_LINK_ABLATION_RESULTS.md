# Kıtlık İnancı → Eylem Skoru Ablasyonu — Sonuçlar

## Durum ve yorum düzeyi

**Koşu tamamlandı: 2026-10-07.** Protokol
(`EXPERIMENT_PROTOCOL_SCARCITY_LINK_ABLATION.md`) koşudan önce yazıldı ve
koşu sırasında değiştirilmedi. Model içi, kuramsal/keşifsel analizdir; insan
verisine kalibrasyon veya ampirik doğrulama değildir.

## Yöntem (özet)

- 2×2 kaynak (kapasite 90/120; food+water yenilenme 0.016/0.019) × 3 bağlantı
  kolu = 12 hücre; 30 seed bloğu (60000–60029) her hücrede; 360 simülasyon.
- Kollar: `intact` (varsayılan); `zero` (`steal_scarcity_weight` ve
  `share_scarcity_weight` = 0); `fixed` (`action_scarcity_reference=0.5`).
- 80 kurucu ajan, 500 tick, sabit sıra, `agent_rng_mode="shared"`. Son 100
  tick seed içinde ortalandı; seed analiz birimidir.
- Köşeli parantezler 10.000 çekilişli seed-blok bootstrap %95 aralığıdır.
  P-değeri veya çoklu karşılaştırma düzeltmesi yok.

## Birincil sonuçlar

Kontrast = yüksek düzey eksi düşük düzey. Kalan pay = kol kontrastı / `intact`
kontrastı.

| Sonuç / kontrast | `intact` | `zero` | `fixed` | Kalan pay `zero` | Kalan pay `fixed` |
|---|---:|---:|---:|---:|---:|
| Çatışma — kapasite | −0.101 [−0.108, −0.093] | +0.012 [+0.011, +0.014] | +0.014 [+0.012, +0.016] | −0.12 [−0.14, −0.11] | −0.14 [−0.17, −0.11] |
| Çatışma — yenilenme | −0.042 [−0.047, −0.037] | +0.004 [+0.003, +0.005] | +0.008 [+0.005, +0.010] | −0.09 [−0.13, −0.06] | −0.18 [−0.25, −0.12] |
| Çatışma — etkileşim | −0.033 [−0.046, −0.021] | +0.002 [−0.002, +0.006] | −0.011 [−0.014, −0.007] | — | — |
| İşbirliği — kapasite | +0.095 [+0.087, +0.102] | +0.023 [+0.021, +0.026] | +0.013 [+0.011, +0.015] | +0.25 [+0.21, +0.28] | +0.14 [+0.11, +0.16] |
| İşbirliği — yenilenme | +0.044 [+0.039, +0.049] | +0.008 [+0.005, +0.010] | +0.007 [+0.004, +0.009] | +0.18 [+0.12, +0.24] | +0.15 [+0.10, +0.20] |
| İşbirliği — etkileşim | +0.033 [+0.022, +0.044] | +0.007 [+0.002, +0.012] | −0.008 [−0.012, −0.004] | — | — |

`intact` kolu, farklı seed'lerle yapılan ilk kaynak deneyini yeniden üretti
(çatışma kapasite etkisi orada −0.099, burada −0.101; işbirliği +0.090 ve
+0.095).

Önceden yazılan yorum kurallarına göre:

- **Çatışma ölçüsü:** iki ablasyon kolunda da kapasite ve yenilenme
  kontrastları sıfırı dışlıyor ve işaretleri `intact` kolunun **tersi**.
  Doğrudan terim kesildiğinde elverişli kaynak koşulu `steal` payını azaltmıyor,
  hafifçe artırıyor (yaklaşık sekizde biri büyüklükte). Kural gereği: dolaylı
  kanallar doğrudan terimin tersine çalışıyor; `intact` sonucu doğrudan terimin
  baskınlığını yansıtıyor.
- **İşbirliği ölçüsü:** kontrastlar sıfırı dışlıyor ve işaret aynı; etkinin
  %14–25'i doğrudan terimden bağımsız. Kalan kısım çoğunlukla `socialize`
  payından geliyor (aşağıda).

İki ablasyon kolu ana etkilerde aynı sonucu veriyor; yalnızca etkileşim
terimlerinde ayrışıyorlar (aşağıdaki düzey notuna bakın).

## Manipülasyon kontrolü

| Sonuç / kontrast | `intact` | `zero` | `fixed` |
|---|---:|---:|---:|
| Gerçek kıtlık — kapasite | −0.562 [−0.609, −0.513] | −0.461 [−0.519, −0.404] | −0.655 [−0.700, −0.610] |
| Gerçek kıtlık — yenilenme | −0.234 [−0.266, −0.203] | −0.243 [−0.279, −0.206] | −0.302 [−0.348, −0.256] |
| Kıtlık inancı — kapasite | −0.510 [−0.559, −0.459] | −0.405 [−0.458, −0.354] | −0.587 [−0.628, −0.548] |
| Kıtlık inancı — yenilenme | −0.218 [−0.248, −0.188] | −0.227 [−0.261, −0.193] | −0.262 [−0.302, −0.222] |

Kaynak manipülasyonu üç kolda da gerçek kıtlığı ve ajanların kıtlık inancını
değiştirmeye devam ediyor; birincil kontrastlar yorumlanabilir. Ablasyon
inancı değil, yalnızca inancın `share`/`steal` skorlarına girişini kesti.

## Hücre ortalamaları

Sütunlar: 90/0.016, 90/0.019, 120/0.016, 120/0.019.

| Ölçü | Kol | 90/0.016 | 90/0.019 | 120/0.016 | 120/0.019 |
|---|---|---:|---:|---:|---:|
| `steal` payı (çatışma) | `intact` | 0.321 | 0.295 | 0.237 | 0.178 |
| | `zero` | 0.120 | 0.123 | 0.132 | 0.136 |
| | `fixed` | 0.218 | 0.231 | 0.238 | 0.240 |
| `share` payı | `intact` | 0.083 | 0.103 | 0.141 | 0.192 |
| | `zero` | 0.217 | 0.219 | 0.228 | 0.235 |
| | `fixed` | 0.128 | 0.134 | 0.137 | 0.139 |
| `socialize` payı | `intact` | 0.088 | 0.096 | 0.109 | 0.118 |
| | `zero` | 0.109 | 0.111 | 0.118 | 0.122 |
| | `fixed` | 0.101 | 0.105 | 0.108 | 0.109 |
| `forage` payı | `intact` | 0.163 | 0.154 | 0.161 | 0.169 |
| | `zero` | 0.207 | 0.195 | 0.171 | 0.168 |
| | `fixed` | 0.184 | 0.170 | 0.170 | 0.170 |
| Gerçek kıtlık | `intact` | 0.982 | 0.880 | 0.552 | 0.186 |
| | `zero` | 1.000 | 0.991 | 0.773 | 0.296 |
| | `fixed` | 0.978 | 0.504 | 0.151 | 0.022 |
| Stres | `intact` | 0.843 | 0.783 | 0.652 | 0.516 |
| | `zero` | 0.422 | 0.417 | 0.394 | 0.399 |
| | `fixed` | 0.704 | 0.700 | 0.710 | 0.706 |
| Ortalama güven | `intact` | −0.035 | −0.017 | 0.001 | 0.017 |
| | `zero` | 0.035 | 0.034 | 0.034 | 0.035 |
| | `fixed` | −0.013 | −0.014 | −0.013 | −0.013 |
| Nüfus | `intact` | 93.4 | 107.0 | 113.3 | 118.8 |
| | `zero` | 108.9 | 126.3 | 129.0 | 129.0 |
| | `fixed` | 92.1 | 93.5 | 94.8 | 93.2 |
| `benefactor` etiketi payı | `intact` | 0.079 | 0.278 | 0.384 | 0.480 |
| | `zero` | 0.663 | 0.658 | 0.667 | 0.665 |
| | `fixed` | 0.121 | 0.119 | 0.121 | 0.126 |

## İkincil keşifsel sonuçlar

Kapasite kontrastı (yüksek eksi düşük):

| Ölçü | `intact` | `zero` | `fixed` |
|---|---:|---:|---:|
| Stres | −0.229 [−0.247, −0.212] | −0.023 [−0.032, −0.013] | +0.006 [−0.002, +0.015] |
| Ortalama güven | +0.035 [+0.033, +0.037] | −0.000 [−0.001, +0.001] | +0.000 [−0.001, +0.001] |
| `helping_norm` | +0.096 [+0.090, +0.103] | +0.024 [+0.022, +0.026] | +0.012 [+0.010, +0.014] |
| `benefactor` etiketi payı | +0.254 [+0.234, +0.273] | +0.005 [−0.008, +0.018] | +0.004 [−0.006, +0.014] |
| `opportunist` etiketi payı | −0.112 [−0.123, −0.100] | +0.012 [+0.002, +0.021] | −0.003 [−0.017, +0.011] |
| `forage` payı | +0.006 [+0.002, +0.010] | −0.032 [−0.035, −0.028] | −0.007 [−0.010, −0.004] |
| `share` payı | +0.073 [+0.067, +0.080] | +0.013 [+0.011, +0.016] | +0.007 [+0.005, +0.008] |
| `socialize` payı | +0.021 [+0.020, +0.023] | +0.010 [+0.009, +0.011] | +0.006 [+0.005, +0.007] |
| Gini | +0.013 [+0.005, +0.021] | −0.028 [−0.037, −0.020] | −0.006 [−0.014, +0.003] |
| Nüfus | +15.9 [+13.5, +18.3] | +11.3 [+8.8, +13.9] | +1.2 [−0.4, +2.9] |

Gözlemler (keşifsel; mekanizma açıklamaları sınanmamış adaylardır):

- **Aşağı akış etkileri de aynı terime bağlı.** Kaynak rejiminin güven, stres,
  yardım normu ve kimlik etiketi bileşimi üzerindeki etkileri ablasyon
  kollarında ya kayboluyor ya da onda bire iniyor. Bu etkiler `intact` kolda
  ayrı bulgular değil, `steal`/`share` skorlarındaki doğrudan terimin
  sonuçlarıdır.
- **Stres, kaynak yokluğundan çok çalmayı izliyor.** `fixed` kolda gerçek
  kıtlık 0.98'den 0.02'ye inerken stres 0.70'te sabit kalıyor; `steal` payı da
  o kolda sabit (~0.23). `zero` kolda `steal` payı düşük (~0.13) ve stres
  düşük (~0.40), kıtlık yüksek olsa bile. Motorda çalınan ajana doğrudan
  +0.2 stres eklenir; aday açıklama budur.
- **Nüfus, kaynak bolluğuyla değil stresle hareket ediyor görünüyor.** `fixed`
  kolda en bol hücrede kıtlık 0.02 iken nüfus 93'te kalıyor (`intact` 119).
  Doğum annenin stresinin 0.6 altında olmasını gerektirir ve bu kolda
  ortalama stres 0.70'tir. Aday açıklama: bu modelde nüfus artışını kaynak
  miktarı değil, çalma kaynaklı stres sınırlıyor.
- **Ters işaretin adayı: `forage` sıkışması.** Ablasyon kollarında elverişli
  koşulda `forage` payı düşüyor (`zero` −0.032), boşalan pay diğer eylemlere
  dağılıyor; `steal` de bundan pay alıyor. Protokolde öngörülen iki yönden
  biri buydu.

## Yorum sınırları

- **Düzey farkı.** `zero` kolu `steal` skorunu genel olarak düşürür (pay
  ~0.13), `fixed` kolu kabaca korur (~0.23). İki kol ana etkilerde aynı
  sonucu verse de etkileşim terimleri farklıdır; `fixed` kolda en bol hücre
  kıtlık tabanına (0.02), `zero` kolda en kıt hücre tavanına (1.00) yapışıyor.
  Etkileşim kontrastları bu yüzden kollar arasında karşılaştırılmamalıdır.
- Ablasyon kıtlık düzeyini de değiştiriyor (`fixed` kolda daha az, `zero`
  kolda daha çok kıtlık); kollar "aynı kıtlıkta farklı karar kuralı"
  karşılaştırması değildir.
- `fixed` kolundaki 0.5 araştırmacı seçimidir; başka bir sabit farklı düzey
  verir.
- Yalnızca `share`/`steal` skorlarındaki terim kesildi. `spread_belief`
  skorundaki `scarcity_belief` terimi ve stresin algı yanlılığı yerinde.
- Seed bootstrap seed belirsizliğini özetler; mekanizma ve parametre
  belirsizliğini kapsamaz. Aynı seed etiketi tam ortak-rastgele-sayı tasarımı
  değildir.

## Sonuç ve raporlama kararı

`RESOURCE_STRESS_RESULTS.md`'deki H2 sonucu ("elverişli kaynak koşulu → daha
az çatışma, daha çok işbirliği") bu modelde `decision.py` içindeki iki
katsayının sonucudur. Emergent bir bulgu olarak sunulmamalı; "karar kuralına
yazılan kıtlık duyarlılığının nüfus düzeyinde beklenen yönde ortaya çıktığı"
bir doğrulama (verification) sonucu olarak raporlanmalıdır. Doğrudan terim
olmadan kaynak rejiminin çatışma ölçüsüne etkisi küçük ve ters yönlüdür.

Varsayılan katsayılar bu sonuca bakılarak değiştirilmedi (ilke 9).

## Tekrar üretim dosyaları

- Protokol: `EXPERIMENT_PROTOCOL_SCARCITY_LINK_ABLATION.md`.
- Koşu: `run_scarcity_link_ablation.py`; analiz: `analyze_scarcity_link_ablation.py`.
- `output/scarcity_link_ablation/experiment.json` — tasarım ve seed metaverisi.
- `output/scarcity_link_ablation/analysis.json` — tüm ölçüler için hücre
  ortalamaları, kontrastlar, kol farkları ve kalan paylar.
- `output/scarcity_link_ablation/seed_summaries.csv` — 360 seed/hücre özeti.
- `output/scarcity_link_ablation/timeseries.csv` — 180.000 tick gözlemi.
