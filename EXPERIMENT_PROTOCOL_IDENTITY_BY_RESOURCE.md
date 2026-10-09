# Protokol: Kaynak Rejimi × Kimlik Geri Beslemesi

## Soru

`identity_feedback_strength` yükselmesi güveni ve çatışmayı değiştiriyor mu;
bu etki kapasite/yenilenme rejimine göre farklı mı?

## Gerekçe ve iddia sınırı

Önceki V6 yeniden sınamada (`REVALIDATION.md`) identity feedback 0.0→0.5
karşılaştırması varsayılan kaynak rejiminde `avg_trust`, `conflict_rate`,
`inequality_gini` ve popülasyonla ilişkiliydi. Eski mekanizma taramasındaki
monoton doz iddiası yalnızca beş seed'e dayanıyordu. Bu takip, seçilmiş uç
kontrastı daha önce incelenmiş 2×2 kaynak aralığına taşır. Kuramsal/keşifsel
ve model içi bir deneydir; dış geçerlilik veya insan davranışına dair nedensel
iddia hedeflemez.

## Önceden belirlenen tasarım

- Faktörler: kaynak kapasitesi 90/120; gıda ve su yenilenme oranı 0.016/0.019;
  `identity_feedback_strength` 0.0/0.5.
- 2×2×2 = 8 hücre; hücre başına 30 seed; toplam 240 simülasyon.
- Her seed tüm sekiz koşulda kullanılır (seed bloklu/eşleşik tasarım); seedler
  50000–50029. Aynı seed etiketi tam common-random-numbers garantisi değildir:
  mekanizma farklılaşınca paylaşılan RNG çekilişleri farklı dallara kayabilir.
- Her dünya 80 kurucu ajan ve 500 tick; food/water başlangıcı kapasitenin 2/3'ü.
- Güncelleme sırası sabit; `agent_rng_mode="shared"` mevcut varsayılanı
  koruyarak eski V6 sonuçlarıyla karşılaştırılabilirlik sağlar. RNG ve sıra
  belirsizlikleri bu tasarımın sınırlaması olarak kaydedilir.
- Birim: bir seed/koşul simülasyonu. Metrikler son 100 tick içinde seed başına
  ortalanır. Tickler bağımsız örnek sayılmaz.

## Sonuç ölçüleri ve analiz

Birincil ölçüler `avg_trust`, `conflict_rate` ve dar davranışsal vekil olan
`cooperation_rate`'tir. Birincil tahminler, her kaynak hücresinde kimlik geri
beslemesi 0.5 eksi 0.0 eşleşmiş seed farkı; ayrıca kaynak faktörlerinin kimlik
etkisini değiştirip değiştirmediğini gösteren identity×capacity,
identity×regen ve üçlü etkileşim kontrastlarıdır. %95 seed-block bootstrap
aralıkları 10.000 çekilişle ve kaydedilmiş analiz seed'iyle üretilir. P-değeri
yerine tahminler ve aralıklar raporlanır; sonuçları seçerek öne çıkarmamak için
tüm hücre ve birincil kontrastlar gösterilir.

İkincil ölçüler `true_scarcity`, `inequality_gini`, `population`,
`identity_formed_rate` ve `positive_relationship_rate`; keşifsel olarak
etiketlenir. Dış veriyle kalibrasyon/doğrulama yapılmadığından tüm yorumlar
mevcut model mekanizmalarıyla sınırlıdır.

## Durdurma ve raporlama

30 seed/hücre önceden belirlenmiş pilot/final örneklemidir; yeterlilik garantisi
değildir. Koşular başladıktan sonra sonuçlara bakarak örneklem/ölçü değiştirilmez.
Çıktılar `output/identity_resource_factorial/` içine seed özetleri, tam
zaman serisi ve konfigürasyonla yazılır.
