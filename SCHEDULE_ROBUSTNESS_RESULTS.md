# Ajan Güncelleme Sırası Sağlamlık Analizi

## Amaç ve tasarım

İlk kaynak deneyi ajanları sabit ID/list sırasıyla çalıştırmıştı. Bu analiz,
aynı 2×2 kaynak koşullarında aynı 120 seed-koşul çiftini tick başına bir kez
karıştırılmış ajan sırasıyla karşılaştırır. Sabit sıra değerleri önceki final
deneyinden alındı; 120 koşu karıştırılmış sırayla yeniden çalıştırıldı. Her
seed'in son 100 tick ortalaması analiz birimidir.

Sıra permütasyonu karar RNG'sinden ayrı bir scheduler RNG ile üretilir. Buna
karşın karar RNG'si ajanlar arasında ortaktır; sıralama değişince rastgele
karar çekilişlerinin hangi ajana gittiği ayrışabilir. Aynı seed etiketleri
eşleştirilmiştir ama bu tam common-random-numbers tasarımı değildir.

## Birincil kaynak faktöriyel kontrastlar

Kontrast = yüksek düzey eksi düşük düzey. `Δ` karıştırılmış sıra eksi sabit
sıra faktöriyel etki farkıdır. Parantez içleri, hücre içinde seed çiftleri
yeniden örneklenerek elde edilen bootstrap %95 aralıklarıdır.

| Sonuç / kontrast | Sabit sıra | Karıştırılmış sıra | Δ (%95 GA) |
|---|---:|---:|---:|
| İşbirliği — kapasite | +0.090 | +0.086 | −0.004 [−0.013, +0.004] |
| İşbirliği — yenilenme | +0.044 | +0.044 | −0.000 [−0.008, +0.008] |
| İşbirliği — etkileşim | +0.023 | +0.020 | −0.003 [−0.020, +0.013] |
| Çatışma — kapasite | −0.099 | −0.096 | +0.003 [−0.006, +0.012] |
| Çatışma — yenilenme | −0.043 | −0.045 | −0.002 [−0.011, +0.007] |
| Çatışma — etkileşim | −0.020 | −0.015 | +0.005 [−0.012, +0.023] |
| Kıtlık — kapasite | −0.560 | −0.527 | +0.033 [−0.025, +0.091] |
| Kıtlık — yenilenme | −0.249 | −0.269 | −0.019 [−0.077, +0.039] |
| Kıtlık — etkileşim | −0.149 | −0.160 | −0.011 [−0.128, +0.103] |

Bu örneklemde dokuz Δ aralığının tümü sıfırı kapsıyor. Kapasite ve yenilenme
etkilerinin yönleri iki çizelgede de aynı; etki büyüklükleri yakın. Bu sonuç,
güncelleme sırasının etkisizliğini kanıtlamaz: eşdeğerlik sınırı tanımlanmadı,
model belirsizliği ölçülmedi ve 30 seed/hücre ile tespit gücü sınırlı olabilir.
Özellikle kıtlık ve etkileşim kontrastları için belirsizlik daha geniştir.

## Hücre düzeyinde gözlem

Karıştırılmış-sıra eksi sabit-sıra birincil sonuç ortalama farkları dört hücrede
de küçüktür. En büyük nokta farkı kıtlıkta 120 kapasite / 0.016 yenilenme
hücresinde yaklaşık +0.051'dir (%95 eşleşmiş bootstrap aralığı −0.019 ile
+0.118); bu hücrede seedler arası değişkenlik yüksektir. Hücrelerin tüm metrik
ayrıntıları ve seed bazlı değerleri sonuç JSON'unda ve CSV dosyalarında yer alır.

## Yorum

İlk kaynak deneyi bulguları, test edilen **sabit sıra ile tick başına
karıştırılmış sıra** arasında yön bakımından dayanıklı görünüyor. Sonuçlar
farklı eşzamanlı/senkron eylem semantiğine, başka ajan seçimi kurallarına,
farklı parametrelere veya insan davranışına genellenemez. Bir sonraki
sağlamlık adımı karar RNG'lerini ajan başına ayırma veya aynı dışsal şokları
ajan kimliklerine sabitleme tasarımını ayrıca değerlendirmek olabilir.

## Kapsam notu (2026-10-09)

Bu karşılaştırmadaki dört kaynak hücresinde ajanlar toktu (ISSUE-015).
Yenilenme ihtiyacın altına indirildiğinde sabit sıra kimliğe göre öncelik
üretiyor ve sonuçları büyük ölçüde değiştiriyor (ISSUE-016). Buradaki
sağlamlık sonucu kıt rejimlere genellenmemelidir.

## Tekrar üretim

- `run_schedule_robustness.py`: 120 karıştırılmış koşuyu ve zaman serilerini üretir.
- `analyze_schedule_robustness.py`: eşleşmiş hücre-seed verilerinden faktöriyel Δ aralıklarını hesaplar.
- `output/schedule_robustness/results.json`: hücre farkları ve tam faktöriyel karşılaştırmalar.
- `output/schedule_robustness/shuffled_seed_summaries.csv`: 120 seed özeti.
- `output/schedule_robustness/shuffled_timeseries.csv`: 60.000 tick gözlemi.
- Sabit sıra eşleşmeleri: `output/resource_factorial/seed_summaries.csv` ve `timeseries.csv`.
