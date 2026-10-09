# REVALIDATION — eski bulguların formal istatistikle yeniden sınanması

Bu dosya `run_revalidation.py` çıktısından (`output/revalidation_results.json`)
üretildi; sayılar elle aktarılmadı. Amaç: daha önce "bakınca ayrışıyor" diye
raporladığım 4 bulguyu gerçek bir anlamlılık testinden geçirmek.

## Yöntem
- Her koşul **30 seed**, iki koşulda **aynı seed'ler**; n_agents=60, 300 tick.
- Metrik = her koşunun son 50 tick'inin ortalaması.
- Welch t-testi (eşit-varyans varsayımı yok — bazı metrikler bir koşulda tavana
  yapışıyor), %95 güven aralığı (Student t), Cohen d.
- **Çoklu karşılaştırma:** 4 karşılaştırma × 5 metrik = 20 test → Bonferroni eşiği
  0.05/20 = **0.0025**.

## Sonuçlar

### 1. `resource_capacity_per_agent` 75 → 150
Eski iddia: baskın kaldıraç (duyarlılık taraması + ISSUE-007).

| metrik | A (ort ± %95 GA) | B (ort ± %95 GA) | Welch p | Cohen d | Bonferroni sonrası |
|---|---|---|---|---|---|
| true_scarcity | 0.996 ± 0.007 | 0.021 ± 0.006 | 1.4e-80 | -54.98 | **anlamlı** |
| population | 75.369 ± 1.547 | 88.646 ± 1.976 | 3.2e-15 | +2.79 | **anlamlı** |
| avg_trust | -0.034 ± 0.002 | 0.031 ± 0.001 | 2.4e-54 | +15.93 | **anlamlı** |
| inequality_gini | 0.440 ± 0.010 | 0.368 ± 0.009 | 8.2e-16 | -2.86 | **anlamlı** |
| conflict_rate | 0.296 ± 0.004 | 0.159 ± 0.002 | 8.4e-42 | -15.72 | **anlamlı** |

### 2. `identity_feedback_strength` 0.0 → 0.5
Eski iddia: güveni aşındırır, doz-bağımlı (ISSUE-004, 5 seed).

| metrik | A (ort ± %95 GA) | B (ort ± %95 GA) | Welch p | Cohen d | Bonferroni sonrası |
|---|---|---|---|---|---|
| true_scarcity | 0.987 ± 0.016 | 0.999 ± 0.001 | 0.12 | +0.42 | anlamsız |
| population | 77.141 ± 1.847 | 72.798 ± 1.276 | 0.00023 | -1.02 | **anlamlı** |
| avg_trust | -0.021 ± 0.001 | -0.041 ± 0.002 | 4.2e-26 | -4.88 | **anlamlı** |
| inequality_gini | 0.370 ± 0.014 | 0.486 ± 0.008 | 7.1e-19 | +3.73 | **anlamlı** |
| conflict_rate | 0.271 ± 0.004 | 0.306 ± 0.004 | 6.8e-19 | +3.37 | **anlamlı** |

### 3. `reconciliation_bonus` 0.0 → 0.35
Eski iddia: `avg_trust`'ı iyileştirir (ISSUE-005, **tek seed**).

| metrik | A (ort ± %95 GA) | B (ort ± %95 GA) | Welch p | Cohen d | Bonferroni sonrası |
|---|---|---|---|---|---|
| true_scarcity | 0.993 ± 0.013 | 0.996 ± 0.007 | 0.64 | +0.12 | anlamsız |
| population | 74.624 ± 1.788 | 75.369 ± 1.547 | 0.52 | +0.17 | anlamsız |
| avg_trust | -0.051 ± 0.002 | -0.034 ± 0.002 | 3.9e-22 | +3.98 | **anlamlı** |
| inequality_gini | 0.435 ± 0.012 | 0.440 ± 0.010 | 0.54 | +0.16 | anlamsız |
| conflict_rate | 0.298 ± 0.004 | 0.296 ± 0.004 | 0.5 | -0.17 | anlamsız |

### 4. `misinformation_rate` 0.05 → 0.35
Eski sonuç: güvenilir etki yok, kapatıldı (ISSUE-001, 8 seed).

| metrik | A (ort ± %95 GA) | B (ort ± %95 GA) | Welch p | Cohen d | Bonferroni sonrası |
|---|---|---|---|---|---|
| true_scarcity | 0.996 ± 0.007 | 0.999 ± 0.002 | 0.49 | +0.18 | anlamsız |
| population | 75.369 ± 1.547 | 75.099 ± 1.385 | 0.79 | -0.07 | anlamsız |
| avg_trust | -0.034 ± 0.002 | -0.034 ± 0.002 | 0.87 | +0.04 | anlamsız |
| inequality_gini | 0.440 ± 0.010 | 0.443 ± 0.010 | 0.66 | +0.11 | anlamsız |
| conflict_rate | 0.296 ± 0.004 | 0.299 ± 0.006 | 0.36 | +0.24 | anlamsız |

### 4b. `misinformation_rate` 0.05 → 0.35, **bol-kaynak rejimi** (`resource_capacity_per_agent=150`)
Neden yapıldı: varsayılan rejimde `true_scarcity` ≈ 1.0'a yapışık (tavan etkisi);
"etki yok" sonucu bundan kaynaklanıyor olabilirdi. 6 test → eşik 0.0083.

| metrik | A (ort ± %95 GA) | B (ort ± %95 GA) | Welch p | Cohen d | Bonferroni sonrası |
|---|---|---|---|---|---|
| true_scarcity | 0.021 ± 0.006 | 0.020 ± 0.007 | 0.98 | -0.01 | anlamsız |
| population | 88.646 ± 1.976 | 88.203 ± 2.104 | 0.75 | -0.08 | anlamsız |
| avg_trust | 0.031 ± 0.001 | 0.031 ± 0.002 | 0.76 | +0.08 | anlamsız |
| inequality_gini | 0.368 ± 0.009 | 0.379 ± 0.007 | 0.048 | +0.52 | ham p<0.05, GEÇEMEDİ |
| conflict_rate | 0.159 ± 0.002 | 0.159 ± 0.003 | 0.9 | +0.03 | anlamsız |
| belief_polarization | 0.107 ± 0.001 | 0.106 ± 0.002 | 0.4 | -0.22 | anlamsız |

## Ne söyleyebiliyoruz

| Eski iddia | Durum | Not |
|---|---|---|
| Kaynak kapasitesi baskın kaldıraç | **Doğrulandı, çok güçlü** | 5 metriğin 5'inde anlamlı; etki büyüklükleri devasa (d = −55 … +16). |
| `identity_feedback_strength` güveni aşındırır | **Yönü doğrulandı** (uçlar 0.0 vs 0.5) | `avg_trust`, `conflict_rate`, `inequality_gini`, `population` anlamlı. **Ara dozlar (0.1/0.15/0.3) yeniden test edilmedi** → "monoton doz-bağımlılık" iddiası yeniden doğrulanmadı. Eski tablodaki mutlak `avg_trust` değerleri (0.011 → −0.023) yeni sonuçlarla (−0.021 → −0.041) KARŞILAŞTIRILAMAZ: config, n ve tick değişti. |
| Uzlaşma mekaniği `avg_trust`'ı iyileştirir | **Doğrulandı** (ama sınırlı) | Tek-seed iddiası n=30'da tutuyor (−0.051 → −0.034). **Fakat** `population`, `inequality_gini`, `conflict_rate` üzerinde hiçbir etkisi yok: ölçülen güveni düzeltiyor, davranışı/ekonomiyi değiştirmiyor. |
| `misinformation_rate` etkisiz | **Doğrulandı, iki rejimde** | Ne çöküş rejiminde ne bol-kaynak rejiminde anlamlı etki var. 4b'de `inequality_gini` ham p=0.048 çıktı ama Bonferroni'yi geçemedi. `belief_polarization` bile değişmiyor — beklenen kanal bu olduğu için ilginç; nedeni araştırılmadı. |

## Tekrarlanabilirlik doğrulaması
Üç ayrı karşılaştırmadaki aynı (varsayılan) config + aynı seed'ler, birbirinden
bağımsız süreçlerde koşuldu ve `avg_trust` ortalamaları **bit-bit aynı**
(−0.03396453997424015). PROJECT_CONSTITUTION kural 6 bu kez ölçülerek doğrulandı.

## Bu sonuçların YAPAMADIĞI şeyler (önemli)

1. **p-değerleri simülasyonda zayıf kanıttır.** Anlamlılık, kaç koşu yapmayı
   seçtiğime bağlı; yeterince çok seed ile her sistematik fark "anlamlı" olur.
   Bu yüzden asıl bilgi **etki büyüklüğü ve güven aralığı**dır, p değil. p<1e−50
   "gerçek dünyada önemli" demek değil, "bu model içinde seed gürültüsü değil"
   demektir.
2. **Cohen d = −55 gibi değerler gerçekçi etki büyüklükleri değildir.** Modelin
   seed'ler-arası varyansı, tavana yapışma yüzünden yapay olarak çok küçük;
   d dev çıkıyor. Sıralama/işaret bilgi verir, büyüklük yorumlanmamalı.
3. **Tümü modelin kendisi hakkında.** Hiçbiri gerçek toplumlar hakkında bir
   iddia değildir; `REFERENCES.md` mekanizmaların çoğunun ampirik kalibrasyon
   içermediğini açıkça yazıyor.
4. **Tek rejim.** 1-3 numaralı karşılaştırmalar yalnızca çöküş rejiminde
   (varsayılan config, `true_scarcity` ≈ 1.0) yapıldı. Yalnızca `misinformation_rate`
   bol-kaynak rejiminde de sınandı (4b). Bkz. `KNOWN_ISSUES.md` ISSUE-011.

## Yeniden doğrulanMAYAN bulgular (hâlâ küçük örneklemli)
- 19 parametrelik duyarlılık taraması: **4 seed**, güven aralığı yok (`run_sensitivity.py`).
- 2×2 etkileşim testi (`resource_capacity` × `food_regen_rate`): **4 seed**.
- ISSUE-007 nüfus-çöküşü oranları (%100 / %30 / %80): **10 seed**, 2000 tick.
- ISSUE-006 (nüfusun 1'e inmesi): **tek seed**.
- ISSUE-004 ara dozları: 5 seed, eski config.
- Ölçek testi: tek koşu/boyut.
Bunlar `KNOWN_ISSUES.md` ISSUE-012'de izleniyor.
