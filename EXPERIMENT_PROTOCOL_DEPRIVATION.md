# Protokol: Gerçek Yoksunluk × Karar Mimarisi

**Durum:** protokol koşudan önce yazıldı (2026-10-09). Sonuçlar ayrı
`DEPRIVATION_RESULTS.md` dosyasında raporlanır.

## Soru

Önceki kaynak deneyleri ajanların tok olduğu rejimlerde koşuldu; ölçülen şey
depo göstergesine dair inanca tepkiydi (ISSUE-015). Depo göstergesi sabitken
(boş) ajanlar gerçekten yoksun kaldığında çatışma ve işbirliği ölçüleri
değişiyor mu, ve bu değişim karar mimarisine bağlı mı?

## Pilot ve rejim seçimi

`run_deprivation_pilot.py`, kapasite 90/120 × dokuz yenilenme düzeyi × 4 seed
taradı. Seçim kuralı koşudan önce betiğe yazıldı: iki kapasitede de
son-pencere `need_deficit_rate` ortalaması ≥ 0.20 olan ve hiçbir pilot
seed'inde nüfusu 20'nin altına düşmeyen en yüksek yenilenme düzeyi. Kural
yalnızca ihtiyaç ve nüfusa bakar; işbirliği/çatışma sonuçlarına bakmaz.

- **Sabit ajan sırası (varsayılan), seed 91000–91071:** hiçbir düzey kuralı
  geçmedi. Kıtlık, kalıcı yoksunluk yerine açlık ölümü üretiyor; hayatta
  kalanlar tok kalıyor (son pencerede yoksun pay %2–8). Nedeni ISSUE-016:
  sabit sırada depoya önce düşük kimlikli ajanlar ulaşıyor.
- **Karıştırılmış sıra, seed 93000–93071:** 0.003 ve 0.004 kuralı geçti;
  **seçilen düzey 0.004** (yoksun pay kapasite 90'da 0.25, 120'de 0.27).

Karşılaştırma düzeyi için ikinci kural pilot görüldükten sonra yazıldı ve
yalnızca depo göstergesine bakar: iki kapasitede de ortalama `true_scarcity`
≥ 0.99 olan en yüksek yenilenme düzeyi. Bu **0.010**'dur (yoksun pay 0.06 ve
0.03). Böylece iki düzeyde de depo boş görünür; fark yoksunluktadır. Pilotta
işbirliği/çatışma ölçülerine bakılmadı.

Ayrıca, özet kodunun nüfus sıfırlanırsa bozulup bozulmayacağını görmek için
seçilen yoksunluk hücresinde `scoring_only` ve `need_based` kolları iki seed
ile (92010–92011) koşuldu ve **yalnızca nüfusa** bakıldı (38–85; yok oluş yok).

## Tasarım

- Kapasite 90/120; food ve water yenilenmesi birlikte **0.004 (yoksun) /
  0.010 (boş depo, tok)**; başlangıç stoku kapasitenin 2/3'ü.
- Karar tarafında 2×2, dört kol: `intact`, `provisions_only`, `scoring_only`,
  `need_based` (tanımlar `EXPERIMENT_PROTOCOL_PROVISION_SCORING_FACTORIAL.md`).
- **`agent_update_order="shuffled"`.** Sabit sıra bu rejimde kimliğe göre
  öncelik üretiyor (ISSUE-016) ve kalıcı yoksunluk oluşturmuyor; bu deney onu
  kullanmaz. Sonuçlar önceki (sabit sıralı) deneylerle doğrudan
  karşılaştırılmamalıdır.
- 2×2×4 = 16 hücre; 30 seed bloğu (94000–94029) her hücrede; 480 simülasyon.
  Seed aralığı daha önce kullanılmadı.
- 80 kurucu ajan, 500 tick, `agent_rng_mode="shared"`. Son 100 tick seed
  içinde ortalanır; seed analiz birimidir. `provision_*` değerleri değişmez.

## Ölçüler ve analiz

**Manipülasyon kontrolü:** `need_deficit_rate` ve `avg_min_need` yenilenme
kontrastı (yüksek eksi düşük = tok eksi yoksun) her kolda sıfırı dışlamalı;
`true_scarcity` her hücrede ≈ 1 olmalı. Bir kolda yoksunluk kontrastı sıfırı
kapsıyorsa o kolun birincil kontrastları yorumlanmaz.

**Birincil:** `conflict_rate` ve `cooperation_rate` için yenilenme ana etkisi
(tok eksi yoksun), her kolda; ve bu kontrastın erzak × skor ayrışımı.

**İkincil (keşifsel):** eylem payları, `avg_stress`, `avg_trust`,
`inequality_gini`, `avg_wealth`, `population`, `cumulative_deaths_starvation`,
kimlik etiketi payları; kapasite kontrastları.

Belirsizlik: 10.000 çekilişli seed-blok bootstrap, %95 yüzdelik aralık.
P-değeri veya çoklu karşılaştırma düzeltmesi yok; tüm hücreler raporlanır.

## Önceden yazılan beklentiler

İnanç iki düzeyde de doygun (≈1) olduğundan doğrudan `scarcity_belief`
terimleri iki düzey arasında fark üretmemeli; farklar ihtiyaç, stres ve ölüm
kanallarından gelir.

- **`intact` ve `provisions_only`:** `steal` skorunda ihtiyaç terimi yok.
  Yoksunlukta `forage` skoru yükselir ve diğer eylemleri sıkıştırır. Beklenti:
  yoksun koşulda `steal` payı **daha düşük** (çatışma kontrastı pozitif),
  işbirliği payı da daha düşük (işbirliği kontrastı pozitif).
- **`scoring_only` ve `need_based`:** `steal` skoru aciliyetle artar, `share`
  azalır; `forage` skorundaki aciliyet terimi doygun inançla neredeyse
  sıfırlanır (ajan depoyu boş sandığı için toplamaya yönelmez). Beklenti:
  yoksun koşulda `steal` payı **daha yüksek** (çatışma kontrastı negatif),
  işbirliği daha düşük (kontrast pozitif). Bu kollarda toplama azaldığı için
  yoksunluk ve açlık ölümü `intact`'ten fazla olabilir.
- **Erzak:** ajanlar artık eşiğin altına düştüğü için yeme tetiklenir.
  Beklenti: erzak yoksun payı düşürür; birincil kontrastlara etkisi küçük
  ama önceki deneydekinden büyük.

## Yorum kuralları

- İki mimari grubunda çatışma kontrastı ters işaretliyse ve aralıklar sıfırı
  dışlıyorsa: gerçek yoksunluğun çatışmaya etkisinin **yönü** karar kuralı
  varsayımına bağlıdır.
- Bir kolda aralık sıfırı kapsıyorsa: bu örneklemde ayırt edilebilir etki yok.
- Beklentilerle uyuşmayan sonuç olduğu gibi raporlanır; skor terimleri veya
  `provision_*` değerleri sonuca bakılarak değiştirilmez (ilke 9).

## Sınırlar

- Yoksunluk kalıcı ama nüfus da düşer; hücreler arasında nüfus farklıdır ve
  oranlar farklı büyüklükte nüfuslar üzerinden hesaplanır.
- Karşılaştırma düzeyi (0.010) tam tok değildir (yoksun pay 0.03–0.06).
- İkinci seçim kuralı pilot görüldükten sonra yazıldı.
- Karıştırılmış sıra da bir zamanlama varsayımıdır; eşzamanlı güncelleme
  sınanmadı. Toplamada kütle korunumu tam değil; dış veriyle kalibrasyon yok.

## Uygulama

```
py run_scarcity_link_ablation.py --arms intact,provisions_only,scoring_only,need_based \
   --capacities 90,120 --regen-rates 0.004,0.010 --order shuffled --seed-start 94000 \
   --out-dir output/deprivation --protocol EXPERIMENT_PROTOCOL_DEPRIVATION.md
py analyze_scarcity_link_ablation.py --dir output/deprivation \
   --factorial provisions_only,scoring_only,need_based
```
