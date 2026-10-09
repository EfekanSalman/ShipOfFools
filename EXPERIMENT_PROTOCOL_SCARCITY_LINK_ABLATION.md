# Protokol: Kıtlık İnancı → Eylem Skoru Bağlantısının Ablasyonu

**Durum:** protokol koşudan önce yazıldı (2026-10-07). Sonuçlar ayrı
`SCARCITY_LINK_ABLATION_RESULTS.md` dosyasında raporlanır.

## Soru

Kaynak deneyindeki (`RESOURCE_STRESS_RESULTS.md`) "elverişli kaynak koşulu →
daha az `steal`, daha çok `share`/`socialize`" sonucu ne ölçüde karar
formülündeki doğrudan terimlerden geliyor?

## Gerekçe

`cognition/decision.py` içinde `steal` skoru `+0.9 × scarcity_belief`, `share`
skoru `−0.5 × scarcity_belief` içerir. `scarcity_belief` gerçek kıtlığın
gürültülü bir okumasıdır; `conflict_rate` son eylemi `steal` olanların payıdır.
Dolayısıyla H2 sonucu, en azından kısmen, formüle elle yazılmış bir ilişkinin
geri okunmasıdır (ISSUE-013). Bu deney doğrudan bağlantıyı keser ve kaynak
etkisinin dolaylı kanallardan (ihtiyaçlar, stres, normlar, kimlik, nüfus)
ne kadarının kaldığını ölçer. `ACADEMIC_RESEARCH_PLAN.md` ilke 7 ve Aşama 5
kapsamındadır. Model içi, kuramsal/keşifsel bir analizdir.

## Tasarım

- Kaynak faktörleri önceki deneylerle aynı: kapasite 90/120; food ve water
  yenilenmesi birlikte 0.016/0.019; başlangıç stoku kapasitenin 2/3'ü.
- Bağlantı faktörü, üç kol:
  - `intact` — varsayılan (`steal_scarcity_weight=0.9`,
    `share_scarcity_weight=0.5`).
  - `zero` — iki ağırlık da 0. Doğrudan terim tamamen kalkar; `steal` skorunun
    genel düzeyi düşer, `share` skorununki yükselir.
  - `fixed` — `action_scarcity_reference=0.5`. `share`/`steal` skorları ajanın
    inancı yerine sabit 0.5 okur; ağırlıklar yerinde kalır, böylece skor
    düzeyi kabaca korunur ama kaynak koşuluna bağlı değişim kesilir. 0.5
    ölçeğin orta noktasıdır ve araştırmacı seçimidir.
- İki ablasyon kolu birlikte raporlanır; biri diğerinin yerine seçilmez.
  Softmax doğrusal olmadığından kontrastlar skor düzeyine bağlı olabilir; iki
  kolun ayrışması bu bağımlılığın göstergesidir.
- Ablasyon yalnızca `share` ve `steal` skorlarındaki terimi keser.
  `spread_belief` skorundaki `+0.3 × scarcity_belief`, inancın kendisi,
  `needs.safety` ve stres yanlılığı değişmez.
- 2×2×3 = 12 hücre; hücre başına 30 seed; toplam 360 simülasyon. Aynı 30 seed
  (60000–60029) bütün hücrelerde kullanılır (seed bloklu). Bu seed aralığı
  daha önce kullanılmadı. Aynı seed etiketi tam ortak-rastgele-sayı tasarımı
  değildir.
- 80 kurucu ajan, 500 tick; sabit ajan sırası; `agent_rng_mode="shared"`
  (önceki kaynak deneyleriyle karşılaştırılabilirlik için).
- Birim: bir seed/hücre simülasyonu. Metrikler son 100 tick içinde seed başına
  ortalanır. Tick'ler bağımsız örnek sayılmaz.

## Ölçüler

**Birincil:** `conflict_rate` ve `cooperation_rate`.

**Manipülasyon kontrolü:** `true_scarcity` ve `avg_scarcity_belief`. Kaynak
manipülasyonu her kolda kıtlığı değiştirmeye devam etmelidir; etmiyorsa o kolun
birincil kontrastları yorumlanmaz.

**İkincil (keşifsel):** altı eylemin ayrı payları (`action_*_rate`),
`avg_stress`, `avg_trust`, `inequality_gini`, `population`, `helping_norm`,
dört kimlik etiketi payı. Eylem payları, bir eylem azaldığında hangisinin
arttığını göstermek içindir.

## Analiz

- Her kol içinde kapasite ana etkisi, yenilenme ana etkisi ve kapasite ×
  yenilenme etkileşimi (yüksek eksi düşük), seed düzeyi özetlerden.
- Her ablasyon kolu için kontrast farkı: kol eksi `intact`.
- Birincil ölçülerde kapasite ve yenilenme ana etkileri için **kalan pay**:
  kol kontrastı / `intact` kontrastı.
- Belirsizlik: 10.000 çekilişli seed-blok bootstrap, %95 yüzdelik aralık,
  kaydedilmiş analiz seed'i. P-değeri veya çoklu karşılaştırma düzeltmesi
  yok; tüm hücreler ve tüm birincil kontrastlar raporlanır.

## Önceden yazılan yorum kuralları

Kalan etkinin yönü için tahmin yapılmıyor. Dolaylı kanallar iki yönde de
çalışabilir: kıtlıkta ihtiyaçlar düşer, `forage` skoru yükselir ve softmax
içinde hem `steal` hem `share` payını sıkıştırabilir; öte yandan stres ve
norm geri beslemesi `steal` lehine çalışabilir.

- Kol içi kontrast aralığı sıfırı kapsıyorsa: bu örneklemde dolaylı kanallardan
  ayırt edilebilir etki yok. "Etki yok" diye kesinlenmez.
- Aralık sıfırı dışlıyor ve işaret `intact` ile aynıysa: etkinin bir kısmı
  doğrudan terimden bağımsızdır; büyüklüğü kalan payla verilir.
- Aralık sıfırı dışlıyor ve işaret tersse: dolaylı kanallar doğrudan terimin
  tersine çalışıyor; `intact` sonucu doğrudan terimin baskınlığını yansıtır.
- Sonuç ne çıkarsa çıksın varsayılan katsayılar bu deneye bakılarak
  değiştirilmez (ilke 9).

## Durdurma ve raporlama

30 seed/hücre önceden belirlenmiştir; koşu başladıktan sonra sonuçlara bakarak
örneklem, ölçü veya kol değiştirilmez. Çıktılar
`output/scarcity_link_ablation/` içine yazılır: `experiment.json`,
`seed_summaries.csv`, `timeseries.csv`, `analysis.json`. Betikler:
`run_scarcity_link_ablation.py`, `analyze_scarcity_link_ablation.py`.
