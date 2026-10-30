# Sıradaki Adımlar

Son güncelleme: 2026-10-30. Bu dosya kısa çalışma planıdır; ayrıntılı geçmiş
[TASK_GRAPH.md](TASK_GRAPH.md), açık sorunlar [KNOWN_ISSUES.md](KNOWN_ISSUES.md)
içindedir.

## Şu ana kadarki ana sonuç

Bu modelde kıtlık → çatışma ilişkisinin işareti iki şeye bağlıdır: kıtlığın
inanç mı yoksa gerçek yoksunluk mu olduğuna ve karar kuralına.

| Koşul | Karar kuralı | Elverişsiz koşulun `steal` payına etkisi |
|---|---|---|
| Depo boşalıyor, ajanlar tok (sabit sıra) | özgün | artırıyor (≈ +0.10) |
| | doğrudan terim kesilmiş | hafif azaltıyor (≈ −0.012) |
| | ihtiyaç temelli | hafif artırıyor (≈ +0.012) |
| Depo zaten boş, ajanlar yoksun (karışık sıra) | özgün | azaltıyor (≈ −0.048) |
| | ihtiyaç temelli | artırıyor (≈ +0.034) |

İki tasarım farklı güncelleme sırası kullanır; tablo yan yana okuma içindir,
doğrudan fark alınmamalıdır. Sonuçlar model içidir, gerçek toplumlar hakkında
iddia değildir. Raporlar: [SCARCITY_LINK_ABLATION_RESULTS.md](SCARCITY_LINK_ABLATION_RESULTS.md),
[NEED_BASED_DECISION_RESULTS.md](NEED_BASED_DECISION_RESULTS.md),
[PROVISION_SCORING_FACTORIAL_RESULTS.md](PROVISION_SCORING_FACTORIAL_RESULTS.md),
[DEPRIVATION_RESULTS.md](DEPRIVATION_RESULTS.md).

## Sıradaki işler (önerilen sıra)

1. [ ] **Güncelleme sırası tanısını 30 seed ile doğrulamak (ISSUE-016).**
   Sabit sırada yüksek kimlikli kurucuların açlıktan ölme oranı %100, karışık
   sırada %33 çıktı, ama bu 4 seed'e dayanıyor. Bundan sonraki deneylerin hangi
   sırayla koşulacağını belirler.
   - **Karar gerekiyor:** varsayılan sıra `shuffled` olsun mu? Eski deneylerin
     tekrarı için `fixed` seçeneği kalır.
2. [ ] **İhtiyaç temelli skordaki toplama zayıflığını düzeltmek.** Skor,
   toplamanın getirisini depo inancıyla çarpıyor; depo boş görününce ajan
   yoksunken de toplamıyor ve en çok açlık ölümü bu kollarda oluyor. Aday:
   ajan getiriyi kendi son toplama deneyiminden öğrensin. Ayrı protokol ve yeni
   seed bloğu gerekir.
3. [ ] **Gini için null model.** Yalnızca rastgele aktarım yapan ajanlarla aynı
   ölçüm; Gini bulgularının neye karşı okunacağını belirler
   ([REFERENCES.md](REFERENCES.md) #15).
4. [ ] **Kimlik bonusu ablasyonu.** Kaynak deneyinde yapılanın kimlik deneyindeki
   karşılığı (ISSUE-013); ayrıca Gini artışının nedeni için etiket bazında
   servet kaydı.
5. [ ] **Doğum oranı bulgusunu 30 seed ile yeniden sınamak** (ISSUE-007, ISSUE-012;
   şu an 10 seed).
6. [ ] **`provision_*` duyarlılığı.** Yalnızca yoksunluk rejiminde anlamlı;
   özellikle dayanaksız olan `provision_max_per_tick`.
7. [ ] **Makale iskeleti.** ODD+D taslağı, protokoller ve sonuç raporlarından
   derlenir. 1 ve 2 bitmeden ana iddia yazılmamalı.

## Daha sonra

- Epstein (2002) karar kuralıyla karşılaştırma ("docking") — [REFERENCES.md](REFERENCES.md) #10–11.
- Toplamada kütle korunumu (fazla toplanan kaynağın kaybolması).
- Uzun deneyleri birkaç çekirdeğe bölmek; sonuçlar seed'e bağlı olduğu için
  değişmez, süre kısalır.
- Dashboard'u gerçek tarayıcıda doğrulamak (ISSUE-010).

## Çalışma kuralları

Her deney için protokol koşudan önce yazılır ve commit edilir; yeni seed bloğu
kullanılır; katsayılar sonuca bakılarak değiştirilmez
([PROJECT_CONSTITUTION.md](PROJECT_CONSTITUTION.md)).
