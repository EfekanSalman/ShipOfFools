# Protokol: Yenebilir Erzak × İhtiyaç Temelli Skor × Kaynak Rejimi

**Durum:** protokol koşudan önce yazıldı (2026-10-09). Sonuçlar ayrı
`PROVISION_SCORING_FACTORIAL_RESULTS.md` dosyasında raporlanır.

## Soru

`NEED_BASED_DECISION_RESULTS.md`'de `need_based` kol iki şeyi birden
değiştiriyordu: servetin yenebilir olması ve `forage`/`steal`/`share`
skorlarının ihtiyaç aciliyeti × getiri ile hesaplanması. Kaynak rejiminin
çatışma ve işbirliği ölçülerine etkisindeki değişim bu iki parçadan hangisine
ait, ve birbirlerine bağlılar mı?

## Tasarım

- Kaynak faktörleri öncekilerle aynı: kapasite 90/120; food ve water
  yenilenmesi 0.016/0.019; başlangıç stoku kapasitenin 2/3'ü.
- Karar tarafında 2×2, dört kol:

  | Kol | Yenebilir erzak | İhtiyaç temelli skor | `Config` |
  |---|---|---|---|
  | `intact` | hayır | hayır | varsayılan |
  | `provisions_only` | evet | hayır | `provisions_edible=True` |
  | `scoring_only` | hayır | evet | `need_based_scoring=True` |
  | `need_based` | evet | evet | `decision_architecture="need_based"` |

- 2×2×4 = 16 hücre; 30 seed bloğu (80000–80029) her hücrede; 480 simülasyon.
  Seed aralığı daha önce kullanılmadı. Aynı seed etiketi tam
  ortak-rastgele-sayı tasarımı değildir.
- 80 kurucu ajan, 500 tick, sabit sıra, `agent_rng_mode="shared"`. Son 100
  tick seed içinde ortalanır; seed analiz birimidir.
- `provision_*` değerleri önceki deneydekiyle aynıdır ve değiştirilmez.

İki ara kolun anlamı:

- `provisions_only`: özgün skorlar (doğrudan `scarcity_belief` terimleri
  dahil) korunur; ajanlar aç kaldıklarında servetlerinden yer.
- `scoring_only`: skorlar aciliyet × getiri ile hesaplanır ama servet
  yenemez. Bu kolda `steal` skorundaki getiri terimi motorda karşılığı olmayan
  bir kazancı varsayar; ajanın değerlemesi fiilen yanlıştır. Kol, skor
  biçiminin etkisini erzak dinamiğinden ayırmak için vardır.

## Ölçüler ve analiz

**Birincil:** `conflict_rate` ve `cooperation_rate` için kapasite ve yenilenme
ana etkileri, her kolda; ve bu kontrastların karar tarafındaki 2×2 ayrışımı:

- erzak ana etkisi = ((`provisions_only` − `intact`) + (`need_based` −
  `scoring_only`)) / 2,
- skor ana etkisi = ((`scoring_only` − `intact`) + (`need_based` −
  `provisions_only`)) / 2,
- erzak × skor etkileşimi = (`need_based` − `scoring_only`) −
  (`provisions_only` − `intact`).

**Manipülasyon kontrolü:** `true_scarcity`, `avg_scarcity_belief`.

**İkincil (keşifsel):** eylem payları, `avg_stress`, `avg_trust`,
`inequality_gini`, `avg_wealth`, `population`, `helping_norm`, kimlik etiketi
payları.

Belirsizlik: 10.000 çekilişli seed-blok bootstrap, %95 yüzdelik aralık.
P-değeri veya çoklu karşılaştırma düzeltmesi yok; tüm hücreler raporlanır.

## Koşudan önce bilinenler ve beklenti

`intact` ve `need_based` kolları farklı seed bloklarında daha önce koşuldu
(çatışma kapasite etkisi sırasıyla ≈ −0.10 ve −0.012); bu deneyde yeniden
koşulurlar. `provisions_only` ve `scoring_only` kolları hiç koşulmadı.

Beklenti (zayıf):

- Çatışma ölçüsündeki farkın büyük kısmı **skor** faktörüne aittir, çünkü
  doğrudan terimi kaldıran odur; ablasyonda terim kalkınca etki −0.10'dan
  +0.012'ye gitmişti.
- `provisions_only` kolda kapasite etkisi `intact`'e yakın kalır; erzak
  ihtiyaçları tamponladığı için bir miktar küçülebilir.
- `scoring_only` ile `need_based` arasındaki fark, yani erzakın skor açıkken
  etkisi, işaret bakımından belirsizdir. Erzak yoksa hırsızlık ihtiyacı
  gidermez ve aciliyet yüksek kalır; bu `steal` payını her hücrede yükseltip
  kaynak kontrastını büyütebilir veya düzleştirebilir.

## Yorum kuralları

- Ayrışımdaki bir ana etkinin aralığı sıfırı dışlıyorsa o faktör kaynak
  etkisini değiştiriyor; kapsıyorsa bu örneklemde ayırt edilemiyor.
- Etkileşim aralığı sıfırı dışlıyorsa iki parça birbirinden bağımsız
  yorumlanamaz; ana etkiler yerine dört kolun ayrı kontrastları esas alınır.
- `intact` ve `need_based` kollarının bu deneydeki kontrastları önceki
  deneylerdekilerle aynı yönde ve benzer büyüklükte değilse bu ayrıca
  raporlanır.
- Manipülasyon kontrolü geçmeyen kolun birincil kontrastları yorumlanmaz.
- Sonuca bakarak `provision_*` değerleri veya skor terimleri değiştirilmez
  (ilke 9).

## Sınırlar

Önceki protokoldekilerle aynı: kollar aynı kıtlık düzeyinde çalışmaz;
toplamada kütle korunumu tam değildir; dış veriyle kalibrasyon yoktur.

## Uygulama

```
py run_scarcity_link_ablation.py --arms intact,provisions_only,scoring_only,need_based \
   --seed-start 80000 --out-dir output/provision_scoring_factorial \
   --protocol EXPERIMENT_PROTOCOL_PROVISION_SCORING_FACTORIAL.md
py analyze_scarcity_link_ablation.py --dir output/provision_scoring_factorial \
   --factorial provisions_only,scoring_only,need_based
```
