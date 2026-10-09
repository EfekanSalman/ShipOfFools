# REFERENCES — bilimsel dayanak envanteri

PROJECT_CONSTITUTION kural 4 ve doc 1 §14 gereği: her mekanizma için "neyi temsil
ediyor / neden var / hangi araştırmadan esinlendi / nasıl yaklaşıklandı / sınırı ne".
Bu dosya o envanterin **dürüst** halidir.

## Önce en önemli uyarı

Bu modeldeki mekanizmaların **çoğu bir literatürden türetilmedi**. Ben (Claude)
onları makul-görünen sezgisel formüller olarak yazdım; sonradan bazılarını
literatürdeki genel bir fenomenle **ilişkilendirdim**. "Şu makaleden esinlendi"
demek ile "şu makalenin modeli uygulandı" demek farklı şeylerdir; aşağıdaki
tabloda yalnızca birincisi vardır ve bazı satırlarda o bile zayıftır.
Sayısal katsayıların (0.3, 0.4, 0.6 …) **hiçbiri ampirik kalibrasyondan gelmiyor**.

## Doğrulama durumu (atıfları nasıl kontrol ettim)

- **DOĞRULANDI** = bu oturumda web aramasıyla künye (yazar, yıl, dergi, cilt/sayfa)
  arama sonuçlarında eşleşti.
- **KISMEN** = başlık/yıl/dergi eşleşti ama cilt/sayfa aramada teyit edilmedi.
- **DOĞRULANMADI** = hafızamdan yazıldı, kontrol edilmedi. Bunlara güvenme;
  kullanmadan önce kendin doğrula.

| # | Kaynak | Durum |
|---|--------|-------|
| 1 | Watts, D. J. & Strogatz, S. H. (1998). Collective dynamics of 'small-world' networks. *Nature* 393, 440–442. | DOĞRULANDI |
| 2 | Nickerson, R. S. (1998). Confirmation bias: A ubiquitous phenomenon in many guises. *Review of General Psychology* 2(2), 175–220. | DOĞRULANDI |
| 3 | Baumeister, R. F., Bratslavsky, E., Finkenauer, C. & Vohs, K. D. (2001). Bad is stronger than good. *Review of General Psychology* 5(4), 323–370. | DOĞRULANDI |
| 4 | Mezulis, A. H., Abramson, L. Y., Hyde, J. S. & Hankin, B. L. (2004). Is there a universal positivity bias in attributions? A meta-analytic review of individual, developmental, and cultural differences in the self-serving attributional bias. *Psychological Bulletin* 130(5), 711–747. | DOĞRULANDI |
| 5 | Esteban, J.-M. & Ray, D. (1994). On the measurement of polarization. *Econometrica* 62(4), 819–851. | DOĞRULANDI |
| 6 | Freeman, L. C. (1978/79). Centrality in social networks: Conceptual clarification. *Social Networks* 1(3), 215–239. | DOĞRULANMADI (hafızadan) |
| 7 | Gini, C. (1912) / standart Gini katsayısı tanımı | DOĞRULANMADI; standart, düşük risk |
| 8 | Morris, M. D. (1991). Factorial sampling plans for preliminary computational experiments. *Technometrics* 33(2), 161–174. (`sensitivity.py`'nin "Morris-tipi" adı bunu anıyor) | DOĞRULANMADI (hafızadan) |
| 9 | Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience* 11, 127–138. (yalnızca TASK-602b planı için; henüz kodda kullanılmıyor) | DOĞRULANMADI (hafızadan) |

## Mekanizma → dayanak tablosu (dürüst sınıflandırma)

Sınıflar: **[E]** ampirik olarak iyi belgelenmiş bir fenomenle *ilişkili*;
**[T]** kuramsal/yapısal varsayım; **[S]** tamamen sezgisel/tasarım tercihi.
Hiçbiri "ampirik olarak kalibre edildi" (**[K]**) değildir.

| Mekanizma (dosya) | Sınıf | İlişkilendirilen kaynak / not |
|---|---|---|
| Sosyal ağ topolojisi: halka örgü + yeniden bağlama (`sociology/social_network.py`) | [T], kaynak net | #1. Watts–Strogatz üretim algoritmasının **basitleştirilmiş** bir uyarlaması; k, rewire_prob değerleri model ihtiyacından seçildi, gerçek bir ağa kalibre değil. |
| İnanç güncellemesi: önsel ağırlıklı harmanlama (`cognition/beliefs.py`, `confirmation_bias`) | [E] zayıf ilişki | #2. Doğrulama yanlılığı literatürüyle *kavramsal* ilişki; gerçek bir Bayes güncellemesi DEĞİL, sabit-ağırlıklı üstel ortalama. 0.6 katsayısı sezgisel. |
| Olumsuz olayların olumluya baskın olması (`steal` → hedef −0.8 vs `share` → +0.6; `update_from_interaction`'daki `harshness`) | [E] zayıf ilişki | #3. "Bad is stronger than good" ile yönce tutarlı; büyüklük oranları (−0.8/+0.6, 0.35/0.25) literatürden değil, sezgisel. |
| Kendini kayırma yanlılığı (`cognition/metacognition.py`) | [E] zayıf ilişki | #4. Meta-analiz böyle bir yanlılığın varlığını ve kültürel/gelişimsel farklarını destekliyor; modeldeki formül (`(1-openness) * stres çarpanı`) o meta-analizden türetilmedi, yapı sezgisel. |
| Stres → algı yanlılığı (`+0.15 * agent.stress`, `engine.py`) | [S] | Kaynak yok. |
| Kişilik özellikleri (openness, conscientiousness, empathy…) (`agents/personality.py`) | [S] | Beş-faktör literatürünün *adlarını* ödünç alıyor ama BFI/NEO ölçümüne, dağılımlara ya da korelasyonlara bağlı DEĞİL; hepsi bağımsız kırpılmış Gauss(0.5, 0.18). Bu gerçek bir kişilik modeli değil. |
| İhtiyaç/stres/sağlık dinamiği (`engine._update_internal_state`) | [S] | Kaynak yok. Sabitler (0.03, 0.08, 0.02…) sistemin makul davranması için seçildi. |
| Utility/softmax karar verme (`cognition/decision.py`) | [S] | Softmax seçim kuralı standart bir hesaplama tekniği; skor katsayıları tasarım tercihi. |
| Norm oluşumu: gözlenen davranışa üstel yakınsama (`culture/norms.py`) | [T] | Sosyal norm/ uyum literatürüyle kavramsal ilişki; spesifik bir modele dayanmıyor. |
| Kimlik oluşumu ve pekişmesi (`agents/identity.py`) | [S] | Kimlik teorisine gevşek ilişki; 5-tekrar eşiği ve 1.3× yapışkanlık sabiti icat. |
| Liderlik oluşumu: güven-ağırlıklı etki skoru (`institutions/leadership.py`) | [S] | Kaynak yok. |
| Yakalanma/caydırıcılık, eğitim, sağlık, medya kurumları | [S] | Kaynak yok; yalnızca "kurumlar legitimacy ile ölçeklenir" yapısal varsayımı. |
| Yaşlanma/üreme/ölüm (`population/lifecycle.py`) | [S] | Gerçek yaşam tablosu/doğurganlık verisine bağlı DEĞİL. `elderly_age=60`, `ticks_per_year=15` vb. keyfi. |
| Kaynak havuzu ve yenilenme (`economy/resources.py`) | [S] | Kaynak yok; basit bir stok-akış soyutlaması. |
| İhtiyaç temelli karar mimarisi ve yenebilir erzak (`decision_architecture="need_based"`; `cognition/decision.py`, `engine._update_internal_state`) | [T] | #19–20: eylemin çekiciliği ihtiyaca getirisinden hesaplanır. Yalnızca yapı ödünç alındı; `provision_*` değerleri ve skor biçimi bu kod tabanının seçimi, kalibre değil. Varsayılan değildir. |
| Polarizasyon metriği (`metrics/social_metrics.py`) | [E] metrik tanımı için kaynak net | #5. Ölçüm tanımı kaynaktan; **alpha=1.6 ve 10 kutu seçimi** bu kod tabanının seçimi olarak alındı — makale α'yı aralık [1, 1.6] içinde tartışır; bu, "α=1.6'nın doğru değer olduğu" anlamına gelmez, üst sınırdır. Kutu sayısı sonuçları etkiler; duyarlılığı test edilmedi. |
| Ağ merkezileşmesi (`social_metrics.py`) | [T] tanım için kaynak | #6, doğrulanmadı. Uygulama star-graph maksimumuna normalize edilmiş giriş-derecesi merkezileşmesi; `test_social_metrics_known_cases` bilinen grafiklerde (yıldız→>0.9, halka→~0) doğruladı. |
| Kümelenme katsayısı (`social_metrics.py`) | [T] | #1. Örnekleme ile tahmin (>300 düğümde). |
| Sosyal hareketlilik: iki an arası servet sıra korelasyonu | [S] | Yaygın bir sıra-kalıcılığı fikri; belirli bir kaynağa bağlı değil. **Nesiller-arası hareketlilik DEĞİL** (yeni doğanların önceki sırası yok). |
| "Foolishness" endeksi (`Agent.foolishness`) | [S] | Tamamen bu projeye özgü, keyfi ağırlıklı bir bileşik; herhangi bir psikometrik ölçüme karşılık gelmez. |

## Ölçülmeyen ve neden

- **İnovasyon / bilgi birikimi:** Modelde teknoloji veya fikir üretme mekanizması
  yok; herhangi bir "inovasyon" sayısı uydurma olurdu. Yerine yalnızca
  `human_capital_total` (toplam `forage_skill`) raporlanır ve bu bir
  beceri-birikimi yaklaşığıdır, inovasyon değildir.
- **GDP-benzeri üretim:** Fiyat/pazar yok, bu yüzden değerli bir toplam üretim
  tanımlanamaz. `human_capital_total` ve toplam servet dışında bir şey
  eklenmedi.

## İlgili literatür ve tasarım kaynakları (2026-10-07 incelemesi)

Bu bölüm modele henüz **uygulanmamış** kaynakları listeler: ISSUE-013/014'ün
çözümünde ve bulguların konumlandırılmasında kullanılabilecek adaylar. Künyeler
bu oturumda web aramasıyla eşleştirildi (yazar, yıl, yayın yeri); makalelerin
tam metni okunmadı, "ne işe yarar" sütunu benim (Claude) yorumumdur.

| # | Kaynak | Durum | Bu proje için anlamı |
|---|--------|-------|----------------------|
| 10 | Epstein, J. M. (2002). Modeling civil violence: An agent-based computational approach. *PNAS* 99 (Suppl. 3). | DOĞRULANDI | Karar kuralı: hoşnutsuzluk = zorluk × (1 − meşruiyet); risk = riskten kaçınma × tutuklanma olasılığı. `steal` skoru aynı bileşenleri (kıtlık, `institution_trust`, `risk_tolerance`, yakalanma) toplamsal ve sezgisel katsayılarla kullanıyor. Alternatif karar kuralı ve "docking" hedefi adayı. |
| 11 | Axtell, R., Axelrod, R., Epstein, J. M. & Cohen, M. D. (1996). Aligning simulation models: A case study and results. *Computational and Mathematical Organization Theory* 1, 123–141. | DOĞRULANDI | "Docking": iki modelin aynı sonucu üretip üretmediğini sınama yöntemi. Ampirik veri yokken yapılabilecek doğrulama adımı. |
| 12 | Brander, J. A. & Taylor, M. S. (1998). The simple economics of Easter Island: A Ricardo-Malthus model of renewable resource use. *American Economic Review* 88(1). | DOĞRULANDI (cilt/sayı hafızadan) | Yenilenebilir kaynak + nüfus = Lotka-Volterra türü "bolluk ve kıtlık" döngüsü. ISSUE-006/007'deki aşım-çöküş örüntüsü için karşılaştırma modeli. |
| 13 | Prediger, S., Vollan, B. & Herrmann, B. (2014). Resource scarcity and antisocial behavior. *Journal of Public Economics* 119, 1–9. | DOĞRULANDI | Saha deneyi: kıt bölgede antisosyal davranış iki kat. `steal_scarcity_weight` işaretini destekleyen ampirik kaynak (büyüklüğünü değil). |
| 14 | von Dawans, B., Fischbacher, U., Kirschbaum, C., Fehr, E. & Heinrichs, M. (2012). The social dimension of stress reactivity: Acute stress increases prosocial behavior in humans. *Psychological Science* 23(6), 651–660. | DOĞRULANDI | Akut stres güveni ve paylaşımı **artırıyor**. Modeldeki "kıtlık/stres → daha az paylaşım" işareti tek olası yön değil; işaret bir deney faktörü olmalı. |
| 15 | Drăgulescu, A. & Yakovenko, V. M. (2000). Statistical mechanics of money. *European Physical Journal B* 17, 723. | DOĞRULANDI | Korunan bir miktarın rastgele ikili aktarımı tek başına üstel dağılım (Gini 0.5) üretir. `steal`/`share` aktarımları için null model; Gini bulguları buna karşı okunmalı. |
| 16 | Bem, D. J. (1972). Self-perception theory. *Advances in Experimental Social Psychology* 6, 1–62. | DOĞRULANDI | Kişi tutumunu kendi davranışından çıkarır. `agents/identity.py` ve `metacognition.py` mekanizmalarının en yakın kuramsal dayanağı ([S] → zayıf [E]). |
| 17 | Edmonds, B. & Moss, S. (2005). From KISS to KIDS — an 'anti-simplistic' modelling approach. *Multi-Agent and Multi-Agent-Based Simulation*, Springer. | DOĞRULANDI | Çok mekanizmalı modeli savunan konum: önce betimleyici kur, sadeleştirmeyi kanıt gerektirdiğinde yap. Ablasyon bu sadeleştirmenin aracıdır. |
| 18 | Starr, P. (1994). Seductions of Sim: Policy as a simulation game. *The American Prospect* 17, 19–29. | DOĞRULANDI | SimCity eleştirisi: varsayımlar erişilemeyen bir kara kutuda; oyuncu modelin kuralını dünyanın yasası sanıyor. ISSUE-013'ün 1994'teki hâli. |
| 19 | Forbus, K. D. & Wright, W. (2001?). Some notes on programming objects in The Sims. Northwestern University ders notu. | DOĞRULANDI (yıl hafızadan) | Nesneler güdü tatminini "ilan eder"; Sim ilanı o anki ihtiyacına göre ağırlıklandırır. ISSUE-014 için tasarım örüntüsü. |
| 20 | Zubek, R. (2010). Needs-based AI. *Game Programming Gems 8*. | KISMEN (kitap ve yazar eşleşti; bölüm içeriği hafızadan) | Aynı mimarinin açık anlatımı; ihtiyaç düzeyine göre doğrusal olmayan zayıflatma eğrileri. |
| 21 | Willmott, A. (2012). Inside GlassBox. GDC 2012 konuşması. | DOĞRULANDI | SimCity (2013) motoru: Resources, Units, Maps, Globals; şehir düzeyi davranış ajanlardan çıkar. |
| 22 | Gingold, C. (2024). *Building SimCity: How to Put the World in a Machine.* MIT Press. | DOĞRULANDI | SimCity'nin Forrester sistem dinamiği ve hücresel otomat kökenleri; Maxis tarihi. |
| 23 | Park, J. S. et al. (2023). Generative Agents: Interactive Simulacra of Human Behavior. *UIST '23*. | DOĞRULANDI | The Sims'ten esinlenen ortamda dil modeli tabanlı ajanlar. Anayasa kural 5 gereği çekirdek için önerilmez; karşılaştırma literatürü. |

Hafızadan, bu oturumda kontrol edilmeyenler (kullanmadan önce doğrula): Epstein &
Axtell (1996) *Growing Artificial Societies* (Sugarscape); Forrester (1969)
*Urban Dynamics*; Meadows vd. (1972) *The Limits to Growth*; Watson & Lovelock
(1983) Daisyworld; McKelvey & Palfrey (1995) quantal response equilibrium
(softmax seçim kuralının oyun kuramındaki karşılığı); Ostrom (1990) *Governing
the Commons*.

## Bu dosyanın sınırı

Bu, literatür taraması DEĞİLDİR. Aramalar yalnızca "bu künye gerçek mi" sorusunu
yanıtlar; "bu mekanizma o kaynakla ne kadar örtüşüyor" sorusunu yanıtlamaz —
o yargı hâlâ benim ve zayıf. Gerçek bir dayanak çalışması, her [S] satırı için
alan literatüründen kalibre edilmiş bir değer bulmayı veya o satırı açıkça
"tasarım tercihi" olarak bırakmayı gerektirir.
