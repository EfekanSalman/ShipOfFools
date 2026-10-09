# Protokol: İhtiyaç Temelli Karar Mimarisi × Kaynak Rejimi

**Durum:** protokol koşudan önce yazıldı (2026-10-07). Sonuçlar ayrı
`NEED_BASED_DECISION_RESULTS.md` dosyasında raporlanır.

## Soru

Kıtlık inancı `steal`/`share` skorlarına doğrudan yazılmadığında, ama servet
yenebilir erzak olduğunda ve eylemler ajanın kendi ihtiyacına etkisiyle
puanlandığında, kaynak rejimi çatışma ve işbirliği ölçülerini değiştiriyor mu?

## Gerekçe

Ablasyon (`SCARCITY_LINK_ABLATION_RESULTS.md`) kaynak rejiminin çatışma
ölçüsüne etkisinin `decision.py` içindeki doğrudan terime bağlı olduğunu
gösterdi (ISSUE-013). Bunun altında yapısal bir eksik var (ISSUE-014): servet
hiçbir ihtiyacı karşılamıyor, yani çalmak açlığı gideremiyor. Bu deney o bağı
kurar ve ilişkinin katsayı olmadan ortaya çıkıp çıkmadığını sınar.

## Mekanizma (`decision_architecture="need_based"`)

Varsayılan (`"heuristic"`) değişmez ve eski yörüngeleri bit-bit korur.

1. **Servet = erzak.** Bir ajanın yiyecek veya su ihtiyacı
   `provision_eat_threshold` (0.4) altındaysa, o tick en fazla
   `provision_max_per_tick` (1.0) servet yer; her birim iki ihtiyacı
   `provision_need_per_wealth` (0.1) kadar yükseltir.
2. **Sonuca dayalı skor.** `steal` ve `share` skorlarındaki doğrudan
   `scarcity_belief` terimleri kaldırılır. Yerine, aciliyet
   `u = 1.2(1−food) + 1.2(1−water)` (mevcut `forage` skorundaki terim) ile:
   - `forage` −= `u × scarcity_belief` (ajan depoları boş sanıyorsa toplamak
     daha az kazandırır),
   - `steal` += `u × g`, `share` −= `u × g`.
   `g`, bir hırsızlığın getirdiği erzakın bir temel toplamaya oranıdır ve
   mevcut sabitlerden türetilir: `(2.0 × 0.1) / (forage_base_amount / 10) = 0.4`.

Parametre dayanakları: 0.1 oranı, motorda çocuğa yapılan paylaşımın zaten
kullandığı orandır (2.0 servet → +0.2 yiyecek ve su). 0.4 eşiği, stres
formülünde kıtlık baskısının başladığı düzeydir. 1.0 üst sınırı yeni bir
tasarım seçimidir ve duyarlılığı sınanmamıştır.

Skorlar hâlâ elle yazılmıştır. Fark şudur: varsayım "kıtlık inancı çalmayı
artırır" yerine "ajan eylemi kendi ihtiyacına getirisiyle tartar" olur;
kıtlık → çalma yönü formülde yer almaz.

## Tasarım

- Kaynak faktörleri öncekilerle aynı: kapasite 90/120; food ve water
  yenilenmesi 0.016/0.019; başlangıç stoku kapasitenin 2/3'ü.
- Mimari faktörü, iki kol: `intact` (heuristic, varsayılan) ve `need_based`.
- 2×2×2 = 8 hücre; 30 seed bloğu (70000–70029) her hücrede; 240 simülasyon.
  Seed aralığı daha önce kullanılmadı. Aynı seed etiketi tam
  ortak-rastgele-sayı tasarımı değildir.
- 80 kurucu ajan, 500 tick, sabit sıra, `agent_rng_mode="shared"`. Son 100
  tick seed içinde ortalanır; seed analiz birimidir.

Koşudan önce görülen tek `need_based` çıktısı, varsayılan konfigürasyonda
seed 42 ile yapılan bir duman testidir (deney hücrelerinden ve seed'lerinden
biri değil).

## Ölçüler ve analiz

**Birincil:** `need_based` kolu içinde `conflict_rate` ve `cooperation_rate`
için kapasite ve yenilenme ana etkileri ile etkileşim.

**Manipülasyon kontrolü:** `true_scarcity`, `avg_scarcity_belief`.

**İkincil (keşifsel):** eylem payları, `avg_stress`, `avg_trust`,
`inequality_gini`, `avg_wealth`, `population`, `helping_norm`, kimlik etiketi
payları; `need_based` eksi `intact` kontrast farkları ve oranları.

Belirsizlik: 10.000 çekilişli seed-blok bootstrap, %95 yüzdelik aralık.
P-değeri veya çoklu karşılaştırma düzeltmesi yok; tüm hücreler raporlanır.

## Önceden yazılan beklenti ve yorum kuralları

Beklenti: elverişsiz kaynak koşulunda toplama daha az kazandırır, ihtiyaçlar
düşer, aciliyet yükselir; bu `steal` payını artırıp `share` payını azaltmalı.
Yani `need_based` kolda da çatışma için negatif, işbirliği için pozitif
kapasite etkisi beklenir. Beklentiyi bozabilecek kanallar: erzakı tükenen
nüfusta çalınacak şey kalmaması, `forage` payının diğer eylemleri sıkıştırması,
yenen erzakın ihtiyaçları koruyup aciliyeti bastırması.

- `need_based` kolda kontrast sıfırı dışlıyor ve işaret `intact` ile aynıysa:
  ilişki doğrudan katsayı olmadan, ihtiyaç kanalından da çıkıyor. Bu, ilişkinin
  "emergent" olduğunu kanıtlamaz; karar kuralındaki daha zayıf bir varsayımdan
  türediğini gösterir.
- Aralık sıfırı kapsıyorsa: bu örneklemde ayırt edilebilir etki yok.
- İşaret tersse: ihtiyaç temelli kural altında kaynak bolluğu çalmayı
  artırıyor; mekanizma eylem payları üzerinden incelenir.
- Manipülasyon kontrolü `need_based` kolda geçmezse birincil kontrastlar
  yorumlanmaz.
- Sonuca bakarak `provision_*` parametreleri veya skor terimleri değiştirilmez
  (ilke 9). Değişiklik gerekiyorsa yeni protokol ve yeni seed bloğu.

## Sınırlar

- `need_based` kol erzak yemeyi de ekler; iki kol aynı kıtlık düzeyinde
  çalışmaz. Karşılaştırma "karar kuralı + erzak" paketinedir.
- Toplamada kazanılan servet ihtiyaç kazancına ek olarak yazılır (motorun
  mevcut hâli); erzak olarak yenebildiğinde bu, toplama veriminin yaklaşık
  %10'u kadar ek besin demektir. Kütle korunumu tam değildir.
- Dış veriyle kalibrasyon yok; yorumlar model içidir.

## Uygulama

```
py run_scarcity_link_ablation.py --arms intact,need_based --seed-start 70000 \
   --out-dir output/need_based_decision --protocol EXPERIMENT_PROTOCOL_NEED_BASED_DECISION.md
py analyze_scarcity_link_ablation.py --dir output/need_based_decision
```
