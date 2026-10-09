# Ajan-Başı RNG ile Güncelleme Sırası Sağlamlığı

## Araştırma sorusu

Sabit ID sırasına göre eylem güncellemek, kaynak kapasitesi ve yenilenme
etkilerini değiştirdi mi? Önceki sağlamlık analizinde ajanların eylemleri tek
bir karar RNG'sini paylaşıyordu. Bu nedenle güncelleme sırası değiştiğinde bir
ajanın tükettiği rastgele çekiliş sayısı, sonraki ajanlara giden çekilişleri
kaydırabiliyordu. Bu takipte eylem/lifecycle çekilişleri ajan başına ayrı
akışlara ayrıldı.

## Tasarım

- 2×2 kaynak düzeni: kapasite 90/120, gıda ve su yenilenme oranı 0.016/0.019.
- Her hücrede aynı 30 seed hem sabit hem tick-başı karıştırılmış eylem sırasıyla
  çalıştırıldı: 4 hücre × 30 seed × 2 çizelge = 240 simülasyon.
- Her koşu 80 kurucu ajan ve 500 tick içerir; analiz son 100 tick'in seed içi
  ortalamasıdır.
- `agent_rng_mode="per_agent"` eylem kararları, algı gürültüsü, etkileşim hedefi,
  söylenti bozulması, yakalanma, yaşlanma ve doğum çekilişlerinde ajan-ID'den
  türetilen RNG kullanır. Tick başı sıralama ayrı scheduler RNG kullanır.
- Hücre içindeki eş seed farkları ve faktöriyel kontrast farkları için 10.000
  paired bootstrap örneklemesi yapıldı.

Bu, RNG aktarımını ajanlar arasında ayırır; tam ortak-rastgele-sayı/potansiyel
sonuç tasarımı değildir. Bir ajanın eylemi ve etkileşimleri değişince o ajanın
sonraki çekiliş sayısı/yolu da değişebilir. Çevre, ağ başlatma ve lider medya
çekilişleri ana simülasyon RNG'sini kullanmayı sürdürür. Bu koşular içinde her
seed/schedule tekrarlanabilir; per-agent mod, `shared` varsayılanını değiştirmez.

## Birincil faktöriyel sonuçlar

Kontrast yüksek düzey eksi düşük düzey; Δ karıştırılmış eylem sırası eksi sabit
sıra kontrastıdır. Parantezler Δ için paired seed bootstrap %95 aralığıdır.

| Sonuç / kontrast | Sabit | Karıştırılmış | Δ (%95 GA) |
|---|---:|---:|---:|
| İşbirliği — kapasite | +0.096 | +0.093 | −0.003 [−0.009, +0.003] |
| İşbirliği — yenilenme | +0.042 | +0.041 | −0.001 [−0.007, +0.006] |
| İşbirliği — etkileşim | +0.024 | +0.021 | −0.004 [−0.016, +0.009] |
| Çatışma — kapasite | −0.105 | −0.102 | +0.004 [−0.003, +0.011] |
| Çatışma — yenilenme | −0.042 | −0.043 | −0.001 [−0.008, +0.006] |
| Çatışma — etkileşim | −0.020 | −0.017 | +0.003 [−0.011, +0.017] |
| Kıtlık — kapasite | −0.560 | −0.554 | +0.006 [−0.041, +0.052] |
| Kıtlık — yenilenme | −0.231 | −0.228 | +0.003 [−0.043, +0.049] |
| Kıtlık — etkileşim | −0.176 | −0.190 | −0.014 [−0.107, +0.078] |

Dokuz fark aralığının tümü sıfırı içeriyor ve üç sonucun kapasite/yenilenme
ana etkileri iki çizelgede de aynı yönde. Bu analiz güncelleme sıralarının
eşdeğerliğini ispatlamaz; önceden belirlenmiş eşdeğerlik sınırı yoktur ve
seedler arası değişkenlik özellikle kıtlık/etkileşim tahminlerinde aralıkları
genişletir. Bununla birlikte önceki kaynak sonucu, ajanlar arası RNG çekiliş
kaymasına daha az bağlı bir tasarımda da yönünü korudu.

## Sonraki yöntem kararı

`shared` modu varsayılan olarak korundu; böylece eski deneyler değişmeden
tekrarlanabilir. Yeni araştırmalarda `per_agent` modunun varsayılan olup
olmayacağı, `shared` ve `per_agent` altında temel bulguların replikasyonu ve
ajan başına stream tasarımının metodolojik gerekçesi birlikte değerlendirilerek
seçilmelidir. Ortak dışsal olayları kimlik/tick bazında sabitleyen counter-based
RNG, daha güçlü eşleştirme için gelecekteki bir alternatif olabilir.

## Kapsam notu (2026-10-09)

Bu sonuç ajanların tok olduğu kaynak hücrelerine aittir; kıt rejimlerde
güncelleme sırası sonuçları değiştirir (ISSUE-016).

## Tekrar üretim

- `run_agent_rng_robustness.py` — 240 koşu ve ham zaman serileri.
- `analyze_agent_rng_robustness.py` — paired hücre ve faktöriyel bootstrap analizi.
- `output/agent_rng_robustness/experiment.json` — tasarım/seed metaverisi.
- `output/agent_rng_robustness/analysis.json` — sonuç tahminleri ve aralıklar.
- `output/agent_rng_robustness/seed_summaries.csv` — 240 seed/schedule özeti.
- `output/agent_rng_robustness/timeseries.csv` — 120.000 tick gözlemi.
