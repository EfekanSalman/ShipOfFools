# KNOWN ISSUES / OPEN THREADS

Bu dosya, "review agent" rolündeki her AI'ın yeni bir V-aşamasına geçmeden
önce kontrol etmesi gereken teknik borç listesi (doc 4'teki `DECISIONS/`
klasörünün sadeleştirilmiş hali). Bir madde kapatıldığında buradan silinmez —
"closed" olarak işaretlenir ve nasıl kapatıldığı not edilir, böylece karar
geçmişi kaybolmaz.

## Açık

### ISSUE-010 — Dashboard gerçek bir tarayıcıda uçtan uca doğrulanmadı + bilinen kapsam sınırları
- **Nerede**: `ship_of_fools/visualization/dashboard_export.py`, `dashboard_template.html`, `run_dashboard.py`
- **Ne doğrulandı**: (a) gömülü JS'in sözdizimi `node --check` ile temiz;
  (b) veri paketinin (`meta`, `timeseries`, `agents`, `network`) JS'in okuduğu
  TÜM alanları içerdiği Python'la programatik olarak kontrol edildi; (c)
  `test_dashboard_export_bundle_shape` testi geçiyor.
- **Ne doğrulanMADI**: sandbox'ın ağ kısıtı yüzünden Chart.js/D3 CDN scriptleri
  yüklenemedi, yani sayfa gerçek bir tarayıcıda render edilip gözle kontrol
  edilmedi. Çalışma-zamanı hatası (örn. gizli sekmede oluşturulan grafiklerin
  boyutu — buna karşı `resize()` çağrısı eklendi ama görülmedi) olabilir.
- **Bilinen kapsam sınırları** (hata değil, bilinçli ilk-dilim kararları):
  1. Agent inceleme paneli yalnızca **18 örneklenmiş kurucu agent** için
     (tüm agent'lar değil; sonradan doğanlar dahil değil) — tam per-agent
     export boyutu çok büyütürdü.
  2. Sosyal ağ yalnızca **son tick'in** grafiği (zaman kaydırıcısı/animasyon
     yok), en bağlantılı ~90 agent ile sınırlı.
  3. Yakınlaştırma sürükle-bırak değil, iki aralık kaydırıcısıyla.
  4. Tek koşu — iki dünyanın (counterfactual) yan yana karşılaştırması yok.
  5. İki CDN bağımlılığı (Chart.js 4.4.4, D3 7.9.0) — çevrimdışı açılmaz.
- **Önerilen kapanış**: sayfayı gerçek bir tarayıcıda açıp üç sekmeyi gözle
  kontrol etmek; bulunan hataları buraya not edip düzeltmek.
- **İlgili task**: TASK-701 (`TASK_GRAPH.md`)
- **Durum**: **açık**.

### ISSUE-011 — Deneylerin çoğu "çöküş rejiminde" (tavan etkisi) koşuluyor
- **Nerede**: varsayılan config; `run_sensitivity.py`, `run_revalidation.py`
- **Belirti**: n=60/300 tick varsayılan rejimde `true_scarcity` = 0.996 ± 0.007
  (tavana yapışık); `identity_formed_rate` de 1.0'a yapışıyor (ISSUE-004).
  Tavandaki bir metrik, ona etki eden bir parametreyi göstermez.
- **Sonuç**: (a) duyarlılık taramasının tamamı bu rejimde yapıldı, yani sıralama
  başka bir rejimde farklı olabilir; (b) `identity_feedback_strength` ve
  `reconciliation_bonus` bulguları yalnızca bu rejimde sınandı.
- **Kısmi hafifletme**: `misinformation_rate` bol-kaynak rejiminde de yeniden
  sınandı (`REVALIDATION.md` 4b) — orada da etki yok, yani o sonuç rejime bağlı değil.
- **Rejim pilotu ve final faktöriyel (2026-10-04)**: `run_regime_calibration.py`
  ile önce 16 hücre × 4 seed tarandı; `90 / 0.019` hücresi ilk sıradaydı. Ancak
  yeni seed bloğundaki 2×2 takipte (`n=20`/hücre, son 100 tick) bu ayar ortalama
  kıtlık 0.853'e çıktı ve uygun olmadı. `120 / 0.016` ayarı ortalama 0.582,
  seedler arası SD 0.189 ve tavanda geçirilen tick payı %4.1 verdi; buna rağmen
  20 seed'in yalnızca 11'inde son-pencere seed ortalaması 0.30–0.60 bandındaydı.
  Ardından sabitlenen 2×2 final deney (30 seed/hücre, son 100 tick), `90/0.016`
  için kıtlık 0.978 [0.963,0.992], `120/0.016` için 0.493 [0.431,0.555]
  verdi. `120/0.016` seedlerinin 17/30'unda kıtlık seed-ortalaması 0.30–0.60
  aralığındaydı; seedler arası SD 0.178. Bu, tavan rejiminden ari bir
  faktöriyel inceleme verdi ama istikrarlı “orta kıtlık” rejiminin her seed'de
  oluştuğunu göstermedi. İşbirliği/çatışma ve kontrastlar:
  `RESOURCE_STRESS_RESULTS.md`; ham sonuçlar `output/resource_factorial/`.
- **Yeni rejimde eski bulgu (2026-10-05)**: `identity_feedback_strength` 0→0.5
  kaynak 2×2'siyle çaprazlandı (30 aynı seed bloğu/hücre). Güven düşüşü ve
  çatışma artışı dört rejimde de aynı yönde; çatışma etkisi düşük kapasitede
  daha büyük. Ayrıntı `IDENTITY_RESOURCE_RESULTS.md`. Bu sonuç tüm eski
  parametre bulgularını yeni rejimde doğrulamaz; seçili identity kontrastına
  aittir.
- **Önerilen kapanış**: kapsamı bu final faktöriyel ile sınırlandırıp, daha
  önce tavan rejiminde yapılan hangi bulguların yeniden sınanması gerektiğini
  araştırma sorusuna göre belirlemek; genel parametre taramasını otomatik
  olarak tekrarlama.
- **Durum**: **açık — ilk rejim karşılaştırması tamamlandı; eski bulguların yeni
  rejimlerde sağlamlığı ayrı değerlendirilmelidir**.

### ISSUE-012 — Bulguların bir kısmı hâlâ küçük örneklemli / güven aralıksız
- **Ne**: duyarlılık taraması (4 seed × 19 parametre), 2×2 etkileşim testi (4 seed),
  ISSUE-007 oranları (10 seed), ISSUE-006 (1 seed), ISSUE-004 ara dozları, ölçek testi.
- **Yeniden doğrulananlar** (n=30, Welch, Bonferroni): ISSUE-001, 004 (yalnızca uçlar),
  005 ve kaynak-kapasitesi bulgusu — bkz. `REVALIDATION.md`.
- **Önerilen kapanış**: kalanları da n≥30 ve güven aralığıyla yeniden koşmak;
  ISSUE-007 için 2000 tick × 30 seed ≈ 15 dk.
- **Durum**: **açık**.

### ISSUE-013 — Birincil deney sonuçları karar formülüne doğrudan yazılı
- **Nerede**: `cognition/decision.py` (`score_actions`), `metrics/tracker.py`
- **Ne**: `steal` skoru `+0.9 × scarcity_belief`, `share` skoru
  `−0.5 × scarcity_belief` içerir; `conflict_rate` ise son eylemi `steal`
  olanların payıdır. Kaynak deneyinin H2 sonucu ("elverişli kaynak → daha az
  `steal`, daha çok `share`/`socialize`") bu yüzden en azından kısmen formülün
  geri okunmasıdır; emergent bir bulgu olarak sunulamaz. Aynı durum kimlik
  deneyinde de var: `opportunist` etiketi `steal` skoruna doğrudan
  `identity_feedback_strength` ekler, net etkinin yönü hangi etiketin baskın
  olduğuna bağlıdır ve etiket dağılımı ilk koşuda kaydedilmemişti.
- **Yapılanlar (2026-10-07)**:
  1. İki katsayı `Config`'e taşındı (`steal_scarcity_weight`,
     `share_scarcity_weight`) ve bağlantıyı kesen `action_scarcity_reference`
     eklendi. Varsayılanlar eski davranışı bit-bit korur (üç konfigürasyonda
     yörünge özeti değişiklik öncesi/sonrası aynı).
  2. Altı eylemin ayrı payları (`action_*_rate`) metriklere eklendi.
  3. Ablasyon deneyi: `EXPERIMENT_PROTOCOL_SCARCITY_LINK_ABLATION.md`,
     sonuçlar `SCARCITY_LINK_ABLATION_RESULTS.md`.
  4. Kimlik deneyinin etiket/eylem dağılımı için post hoc takip:
     `run_identity_label_followup.py`, sonuçlar `IDENTITY_RESOURCE_RESULTS.md`
     içinde ek bölüm.
- **Ablasyon sonucu (2026-10-07, 360 koşu)**: doğrudan terim kesilince kapasite
  etkisi çatışma ölçüsünde işaret değiştiriyor (`intact` −0.101; `zero` +0.012;
  `fixed` +0.014; aralıklar sıfırı dışlıyor). İşbirliği ölçüsünde etkinin
  %14–25'i kalıyor. Kaynak rejiminin güven, stres, yardım normu ve etiket
  bileşimi üzerindeki etkileri de ablasyonda kayboluyor veya onda bire iniyor.
  H2 emergent bulgu değil, karar kuralının doğrulamasıdır.
- **Kimlik takibi (post hoc)**: `steal` artışının en büyük olduğu hücrede
  `opportunist` payı artmıyor; artış sabit bonusla uyumlu. Gini artışı
  (+0.10–0.11) dört rejimde aynı ve çalma oranıyla açıklanamıyor.
- **Elle yazılmamış, öne çıkarılmaya aday bulgular**: `120/0.016` hücresinde
  seed'lerin 0.085–0.819 kıtlık aralığına dağılması; doğum oranını düşürmenin
  çöküşü kötüleştirmesi (ISSUE-007, hâlâ 10 seed — ISSUE-012); kaynak
  bolluğunun Gini'yi düşürmemesi ve kimlik geri beslemesinin Gini'yi artırması;
  RNG eşleştirme/güncelleme sırası yöntem çalışması.
- **Önerilen kapanış**: ablasyon sonucuna göre H2'nin raporlanma biçimini
  ("doğrudan terim" ve "dolaylı kanal" payları ayrı) sabitlemek; kimlik etkisi
  için benzer bir ablasyonu ayrı protokolle değerlendirmek.
- **Durum**: **açık**.

### ISSUE-014 — Servet hiçbir ihtiyacı karşılamıyor; `steal` kıtlığı gideremez
- **Nerede**: `simulation/engine.py` (`_apply_action`), `cognition/decision.py`
- **Ne**: `wealth` yalnızca şuralarda okunur/yazılır: `forage` geliri, `share` ve
  `steal` aktarımları, vergi/yeniden dağıtım, ceza, doğum maliyeti ve `share`
  skorundaki `wealth > 15` eşiği. Servet yiyeceğe veya suya **çevrilemez**
  (piyasa yok). Yiyecek/su ihtiyacını yalnızca `forage` (ve çocuklar için
  kendilerine yapılan `share`) karşılar.
- **Sonuç**: (a) Bir ajan çalarak açlığını gideremez; kıtlığın çalmayı
  "rasyonel" kılacağı bir yol modelde yoktur. `steal` skorundaki doğrudan
  `scarcity_belief` terimi (ISSUE-013) bu eksik bağın yerine elle yazılmıştır.
  (b) Gini, hayatta kalmaya etkisi olmayan bir sayının dağılımını ölçer;
  korunan bir miktarın ikili aktarımı tek başına yüksek eşitsizlik üretir
  (`REFERENCES.md` #15), dolayısıyla Gini bulguları bir null modele karşı
  okunmalıdır.
- **Önerilen kapanış**: alternatif (varsayılanı değiştirmeyen) bir karar
  mimarisi: eylemler ihtiyaç tatminini "ilan eder" (The Sims örüntüsü,
  `REFERENCES.md` #19–20), `steal` yiyecek/su aktarır veya servet ihtiyaca
  çevrilebilir. O zaman kıtlık → çalma ilişkisi katsayıdan değil ihtiyaçtan
  doğar ve yönü önceden yazılı olmaz. Ayrı protokol ve `Config` anahtarı gerekir.
- **Yapılanlar (2026-10-07)**: `decision_architecture="need_based"` eklendi
  (varsayılan `"heuristic"`; eski yörüngeler bit-bit aynı). Servet eşik altındaki
  ihtiyaç için yenebiliyor; `forage`/`steal`/`share` skorları aciliyet × getiri
  ile hesaplanıyor. Testler `tests/test_need_based_decision.py`. Protokol
  `EXPERIMENT_PROTOCOL_NEED_BASED_DECISION.md`, sonuçlar
  `NEED_BASED_DECISION_RESULTS.md`. `avg_wealth` metriği eklendi.
- **Sonuç (2026-10-09, 240 koşu)**: `need_based` kolda kapasite etkisi çatışma
  ölçüsünde −0.012 [−0.013, −0.010] (`intact` −0.098), işbirliğinde +0.016
  (`intact` +0.092): aynı yön, yaklaşık sekizde bir–altıda bir büyüklük.
  Servet ve Gini'nin kaynak rejimine tepkisi iki mimaride ters işaretli:
  `intact` kolda en kıt hücre en zengin hücredir (servet yenemediği için
  birikir). Ablasyonla birlikte okununca kaynak → çatışma etkisinin büyüklüğü
  karar kuralına göre yaklaşık sekiz kat değişiyor.
- **Kalan**: erzak ile karar kuralının ayrı etkisi; `provision_*` duyarlılığı;
  toplamada kütle korunumu. Varsayılan mimari kararı verilmedi.
- **Durum**: **açık**.

## Kapalı

### ISSUE-001 — misinformation_rate'in davranışsal etkisi zayıf [KAPATILDI — güncel modelde yeniden test edildi]
- **Nerede**: `configuration/config.py` (`misinformation_rate`), `cognition/decision.py`
- **Geçmiş**: V2 döneminde 6/8 seed'de tutarlı bir "misinformation ↑ →
  true_scarcity ↓" etkisi bulunmuş ve "kısmen kapatıldı" olarak işaretlenmişti.
- **Yeniden test (V6, tüm katmanlar aktifken)**: aynı karşılaştırma (n=60,
  300 tick, 8 seed) güncel modelde **4/8 seed'de** aynı yönde çıktı — yazı
  tura, artık güvenilir bir etki değil. Diğer metrikler (conflict_rate,
  cooperation_rate, inequality_gini, population) zaten anlamlı bir fark
  göstermiyordu.
- **Yorum**: identity (V3), culture/norms (V3) ve population/lifecycle (V4)
  eklendikten sonra sistemde çok daha güçlü, baskın geri besleme döngüleri
  (nüfus patlaması/çöküşü, identity pekişmesi) oluştu; bunlar
  `misinformation_rate`'in dolaylı etkisini gürültü seviyesine indirdi.
  Doğrudan mekanik etki hâlâ duruyor (misinformation_rate arttıkça
  `scarcity_belief`'in popülasyon-geneli std'si hafifçe artıyor: tek-seed
  testte 0.074→0.078) ama bu, aşağı akış davranışına anlamlı şekilde
  yansımıyor artık.
- **Karar**: daha güçlü bir etki elde etmek için katsayıları zorlamak
  istenen bir sonuca göre kalibrasyon olurdu (PROJECT_CONSTITUTION kural 8'e
  aykırı). Mevcut durum olduğu gibi belgelenip kapatıldı.
- **İlgili task**: TASK-104
- **Durum**: **kapalı**.

### ISSUE-002 — avg_trust mutlak değer olarak hâlâ düşük [DÜZELTİLDİ — kök neden yanlış tespit edilmişti]
- **Nerede**: `sociology/social_network.py`
- **Belirti**: TASK-101 (komşuluk yapısı) sonrası `avg_trust` toplanabilir hale
  geldi ama yine de ~0.03-0.05 civarında.
- ~~**Önceki (YANLIŞ) hipotez**: `average_trust()`'ın hiç etkileşmemiş çiftleri de
  0 olarak sayıp ortalamayı seyrelttiği düşünülmüştü.~~ **Ölçüldü, doğru değil**:
  `self.trust[a]` sözlüğü yalnızca `nudge()` çağrıldığında (yani gerçekten
  etkileşim olduğunda) bir anahtar kazanıyor; `average_trust()` zaten sadece
  etkileşmiş çiftler üzerinden ortalama alıyor. n=80'de 300 tick sonra 6320
  olası yönlü çiftin %34'ü (2153) etkileşmiş, ve bu 2153 çiftin **kendi
  ortalaması** ~0.037 — düşüklük seyrelmeden değil, gerçek dinamikten geliyor.
- **Gerçek kök neden**: pozitif (`socialize`/`share`, hedef ~0.3-0.7) ve negatif
  (`steal`, hedef -0.8) etkileşimler nüfus genelinde birbirini büyük ölçüde
  götürüyor (%44'ü |trust|<0.05), üstüne `relationship_decay` tazelenmeyen
  kenarları sürekli sıfıra çekiyor. Bu bir "seyrelme hatası" değil, karma
  işbirliği+ihanet ortamının makul bir sonucu olabilir.
- **Karar**: Sayıyı yapay olarak yükseltmek yerine (PROJECT_CONSTITUTION kural 8:
  "iyi toplum" hedefi yok), altta yatan dağılımı gösteren iki yeni metrik
  eklendi: `positive_relationship_rate`, `negative_relationship_rate`.
- **İlgili task**: TASK-104
- **Durum**: **kapalı** — kök neden düzeltildi, "hata" değil ölçülebilir bir
  metrik eksikliğiymiş; yeni metriklerle giderildi.

### ISSUE-003 — avg_institution_trust, institution_legitimacy'ye yavaş yakınsıyor [KAPATILDI — kök neden bulundu ve düzeltildi]
- **Nerede**: `simulation/engine.py` (`_perceive_and_update_beliefs`), `cognition/beliefs.py`
- **Kök neden bulundu**: gürültülü gözlem (`observed_legitimacy`), blend'e
  girmeden ÖNCE her tick [0,1]'e kırpılıyordu. Gerçek `legitimacy` neredeyse
  her zaman 0'a çok yakın olduğu için, bu kırpma yalnızca gürültünün pozitif
  yarısını hayatta bırakıyor (yarı-normal dağılım) — bu da sistematik bir
  YUKARI yanlılık yaratıyor (matematiksel olarak E[max(0,X)] ≈ 0.4×std,
  gözlemlenen ~0.08 sapmayla neredeyse birebir örtüşüyor).
- **Düzeltme**: gürültülü gözlem artık blend'e girmeden ÖNCE kırpılmıyor;
  yalnızca NİHAİ `institution_trust` [0,1]'e kırpılıyor (zaten
  `update_institution_trust` içinde yapılıyordu). Aynı desen `scarcity_belief`
  gözleminde de vardı, tutarlılık için o da düzeltildi.
- **Doğrulama** (3000 tick, seed=42): düzeltme sonrası `avg_institution_trust`
  ~0.08-0.15 bandından ~0.045-0.07 bandına indi — gerçek `legitimacy`'ye
  (~0.01) çok daha yakın. Kalan küçük fark, inancın [0,1] ile sınırlı olması
  ve gerçek legitimacy'nin sıfıra çok yakın olmasından kaynaklanan doğal bir
  "yansıyan sınır" etkisi — beklenen ve makul.
- **İlgili task**: TASK-203
- **Durum**: **kapalı**.

### ISSUE-004 — helping_norm sürekli ~0.30'a doğru düşüyor [KAPATILDI — parametre taraması yapıldı]
- **Nerede**: `culture/norms.py`, `cognition/decision.py`
- **Yöntem**: `identity_feedback_strength`'i 0.0 (tamamen kapalı) → 0.1 → 0.15 →
  0.3 (varsayılan) → 0.5 aralığında, n_agents=80/500 tick/5 seed ile tarayıp
  `summarize_window(window=50)` ile ölçtük.

  | identity_feedback_strength | avg_trust | helping_norm | identity_formed_rate | positive_relationship_rate |
  |---|---|---|---|---|
  | 0.00 (kapalı) | 0.011±0.002 | 0.303±0.004 | 1.000±0.000 | 0.212±0.012 |
  | 0.10 | 0.005±0.003 | 0.298±0.004 | 1.000±0.000 | 0.194±0.009 |
  | 0.15 | 0.004±0.002 | 0.295±0.005 | 1.000±0.000 | 0.197±0.009 |
  | 0.30 (varsayılan) | -0.007±0.003 | 0.268±0.009 | 1.000±0.000 | 0.166±0.008 |
  | 0.50 | -0.023±0.009 | 0.224±0.024 | 1.000±0.000 | 0.127±0.020 |

- **Sonuç 1 (ISSUE-004'ü kapatıyor)**: `identity_feedback_strength=0.0`'da (yani
  identity'nin davranışa hiç geri beslemesi YOKKEN) bile `helping_norm` aynı
  ~0.30 seviyesine yakınsıyor. Demek ki bu bir "kendini besleyen çöküş"
  değilmiş — `helping_norm` yalnızca zaten V1'den beri var olan
  `cooperation_rate` denge seviyesini (~0.25-0.35) doğru şekilde takip ediyor.
  Tasarlandığı gibi çalışıyor; düzeltme gerekmedi.
- **Sonuç 2 (doğrulanmış bulgu)**: `identity_feedback_strength` arttıkça
  `avg_trust` VE `positive_relationship_rate` 5 seviyenin tamamında **monoton**
  düşüyor, dar hata payıyla. Bu, TASK-302'nin "identity sunk-cost'u toplumsal
  güveni aşındırır" iddiasının gerçek, doz-bağımlı bir etki olduğunu
  doğruluyor — hata değil, doğrulanmış bir mekanizma.
- **İlgili task**: TASK-301, TASK-302
- **Durum**: **kapalı**.

### ISSUE-005 — güveni onaran/pekiştiren simetrik bir mekanizma yok [KAPATILDI — uzlaşma (reconciliation) mekaniği eklendi]
- **Nerede**: `simulation/engine.py` (`socialize` dalı), `configuration/config.py` (`reconciliation_bonus`)
- **Çözüm**: `socialize` eyleminde, mevcut güven ZATEN negatifse (`social.get(...) < 0`
  — yani ilişki daha önce zedelenmişse), güven-nudge hedefi `reconciliation_bonus`
  (varsayılan 0.35) kadar güçlendiriliyor. Yani zedelenmiş bir ilişkiyi aktif
  olarak onarmaya çalışmak (tekrar tekrar `socialize` etmek), sıfırdan bir
  tanışıklık kurmaktan daha hızlı sonuç veriyor — pasif decay'in sağlayamadığı
  aktif bir onarım yolu.
- **Doğrulama**: `test_reconciliation_repairs_damaged_trust_faster` — n=2
  agent, elle -0.5 güvene ayarlanmış bir ilişkide tek bir `socialize`
  çağrısının, uzlaşma bonusu olmadan beklenenden daha büyük bir iyileşme
  ürettiği doğrulandı. Varsayılan koşuda (500 tick) `avg_trust` -0.047'den
  -0.035'e iyileşti — mütevazı ama gerçek bir etki (aşındırma güçleri hâlâ
  baskın; bu KASITLI, bkz. ISSUE-004'ün doğrulanmış bulgusu).
- **İlgili task**: TASK-301/TASK-302 ile ilişkili, yeni bir alt-görev olarak
  numaralandırılmadı.
- **Durum**: **kapalı**.

### ISSUE-006 — 500 tick sonrası true_scarcity gerçekten toparlanıyor mu [KAPATILDI — soyu tükenmeye kadar koşuldu]
- **Nerede**: `environment/ship.py`, `population/lifecycle.py`
- **Yöntem**: aynı varsayılan config, n_ticks=500 yerine **2000** ile koşuldu (n=80, seed=42).
- **Bulgu — beklenen "toparlanma" değil, soyu tükenme**:

  | tick | popülasyon | true_scarcity | avg_stress | cumulative_births | cumulative_deaths_old_age |
  |---|---|---|---|---|---|
  | 1 | 80 | 0.328 | 0.220 | — | — |
  | 201 | 109 | 0.913 | 0.796 | (baby boom) | — |
  | 601 | 79 | 0.667 | 0.739 | — | — |
  | 801 | 54 | 0.012 | 0.380 | — | — |
  | 1201 | 15 | 0.007 | 0.356 | — | — |
  | 2000 | **1** | 0.000 | 0.126 | 33 (toplam) | **112** |

  `true_scarcity` gerçekten ~tick 800'de düşüyor — ama nüfus çöktüğü İÇİN
  düşüyor, sağlıklı bir dengeye dönüldüğü için değil. Nüfus 80'den 1'e
  iniyor. `cumulative_deaths_starvation=0` (final): kimse doğrudan açlıktan
  ölmüyor; doğum durduktan sonra nüfus yaşlılıktan teker teker tükeniyor.
- **Yorum**: kurucuların TAMAMI başlangıçta doğurgan yaşta olduğu için tek
  seferlik bir "baby boom" taşıma kapasitesini aşıyor, sistemde bunu tersine
  çevirecek bir mekanizma yok. Bilinçli bir "hata" değil — tek-seed bulgusu
  ISSUE-007'de çok-seed olarak doğrulandı.
- **İlgili task**: TASK-401
- **Durum**: **kapalı**.

### ISSUE-007 — nüfus çöküşünün çok-seed sağlamlığı [KAPATILDI — evrensel olduğu doğrulandı]
- **Nerede**: `population/lifecycle.py`, `environment/ship.py`, `experiments/counterfactual.py`
- **Yöntem**: `run_v5_lab.py` — n=80, 2000 tick, 3 koşul × 10 seed:

  | Koşul | ≤5 pop | ≤20 pop | kurucu (80) altında |
  |---|---|---|---|
  | A) varsayılan config | %30 | %80 | **%100** |
  | B) `birth_rate_base` 0.008→0.003 (daha az doğum) | **%100** | %100 | %100 |
  | C) `resource_capacity_per_agent` 75→150 (2x kaynak) | **%0** | **%0** | %10 |

- **Sonuç**: (A) çöküş evrensel (10/10 seed kurucu nüfusun altına düşüyor).
  (B) sezgisel "daha az doğum yardımcı olur" hipotezi **yanlış çıktı** — daha
  da kötüleştiriyor. (C) gerçek darboğazın doğum oranı değil, **kaynak
  kapasitesi** olduğu doğrulandı.
- **Karar**: varsayılan config BİLİNÇLİ OLARAK değiştirilmedi (PROJECT_CONSTITUTION
  kural 8) — isteyen `resource_capacity_per_agent=150` gibi bir override ile
  istikrarlı bir senaryo koşturabilir (bkz. `run_v5_lab.py` koşul C).
- **İlgili task**: TASK-501
- **Durum**: **kapalı**.

### ISSUE-008 — causal_narrative'de has_leader==0 tick 1'de anlamsızca tetikleniyor [KAPATILDI]
- **Nerede**: `experiments/causal_narrative.py`
- **Belirti**: "liderlik kurumu yok/kayboldu" işareti, lider HİÇ oluşmamışsa
  tick 1'de tetikleniyordu — "kayboldu" ile "henüz hiç oluşmadı" arasındaki
  farkı ayırt etmiyordu.
- **Düzeltme**: liderlik artık genel eşik listesinden çıkarılıp ayrı bir geçiş
  mantığıyla izleniyor: yalnızca gerçek bir 1→0 geçişi "kayboldu" olarak
  raporlanıyor; hiç oluşmadıysa ayrı, nötr bir bilgilendirme notu
  ("liderlik hiç oluşmadı") olarak veriliyor, uyarı işareti olarak değil.
- **Doğrulama**: seed 0, n=80/500 tick üzerinde çalıştırıldı — artık tick 1'de
  anlamsız bir "kayboldu" satırı yok, yalnızca gerçek uyarılar ve sondaki
  bilgilendirme notu görünüyor.
- **İlgili task**: TASK-502
- **Durum**: **kapalı**.

### ISSUE-000 — true_scarcity popülasyon değişince dengesi bozuluyordu [KAPATILDI]
- **Belirti**: n_agents=80 için kalibre edilen regen/tüketim dengesi n_agents=60'ta
  `true_scarcity`→0'a çöküyordu.
- **Çözüm**: kaynak kapasitesi/başlangıç stoku `*_per_agent` config alanlarına
  çevrildi, `Ship.__init__` bunları `n_agents` ile çarpıyor.
- **Durum**: **kapalı**.

### ISSUE-009 — random_acquaintance O(n) filtreleme yapıyordu, ölçekte süper-doğrusal davranışa yol açıyordu [KAPATILDI]
- **Nerede**: `sociology/social_network.py`
- **Bulgu yöntemi**: `run_scale_test.py` — 100'den 10.000 agent'a kadar
  wall-clock ölçüldü. 100-1600 aralığında üstel≈1.05 (doğrusal, sorun yok),
  ama 1600-10.000 aralığında üstel≈1.26'ya çıktı — gerçek bir süper-doğrusal
  davranış.
- **Kök neden izolasyonu**: `long_range_interaction_prob=0.0` yapılınca üstel
  1.26'dan 1.04'e düştü — sorumlu kesin olarak `random_acquaintance`'ın uzun-
  menzilli etkileşim fallback'inde her çağrıda `[x for x in agent_ids if x != a]`
  ile TÜM popülasyonu filtrelemesiymiş (O(n) çağrı × n_agents çağrı/tick = O(n²)).
- **Düzeltme**: reddet-ve-tekrar-dene stratejisine geçildi (`rng.choice` + eşitse
  tekrar dene, en fazla 5 deneme, patolojik durumlarda eski filtrelemeye düşer)
  — beklenen O(1).
- **Doğrulama**: düzeltme sonrası 1600-10.000 aralığında üstel 1.26→1.09'a indi.
  n=10.000'de artık tick başına ~0.35s (500 tick ≈ 3 dakika).
- **İlgili task**: ölçek testi (V6 sonrası genişletme)
- **Durum**: **kapalı**.


## Revalidasyon notları (n=30, formal test — ayrıntı: REVALIDATION.md)
- **ISSUE-001** (misinformation etkisiz): yeniden sınandı, **iki rejimde de** anlamlı etki yok;
  kapanış artık istatistiksel olarak desteklenen bir sıfır sonucu.
- **ISSUE-004** (identity aşındırır): yalnızca uç noktalar (0.0 vs 0.5) yeniden sınandı, yön
  doğrulandı; ara dozlar/“monoton” iddiası yeniden sınanmadı.
- **ISSUE-005** (uzlaşma): tek-seed iddiası n=30'da tuttu (−0.051 → −0.034), ama etki
  yalnızca `avg_trust`'ta; çatışma/eşitsizlik/nüfus değişmiyor.
