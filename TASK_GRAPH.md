# TASK GRAPH — V0 → V6 (doc 3'teki sıralamaya göre)

AI orkestrasyon akışı her görev için: **Research → Architecture → Implementation
→ Test → Review** (bkz. `PROJECT_CONSTITUTION.md`). Bağımlılıklar aşağıda
sıralı; bir V aşamasına geçmeden önceki tamamlanmalı.

## ✅ V0 — Artificial Individual + minimal society (TAMAMLANDI)
- [x] TASK-001 Agent mimarisi (personality, needs, stress, memory)
- [x] TASK-002 Beliefs (gerçeklikten sapabilen algı)
- [x] TASK-003 Cognition (utility-tabanlı karar verme)
- [x] TASK-004 SocialNetwork (güven grafiği)
- [x] TASK-005 Information/rumors (inanç yayılımı + çarpıtma)
- [x] TASK-006 Economy (paylaşılan kaynak havuzu)
- [x] TASK-007 Environment (Ship + rastgele şoklar)
- [x] TASK-008 Simulation engine (tick döngüsü)
- [x] TASK-009 Metrics + Gini
- [x] TASK-010 Experiment runner (çoklu-seed karşılaştırma)
- [x] TASK-011 Visualization (zaman serisi grafikleri)
- [x] TASK-012 Sanity testleri

## V1 — Social Individual (derinleştirme)
- [x] TASK-101 Komşuluk/topluluk yapısı: small-world graf (`build_neighbor_structure`),
      etkileşimlerin %85'i sabit yerel bağlardan, %15'i uzun-menzilli rastgele temas
      (dedikodu/haber yayılım kanalı). `relationship_decay` de 0.01→0.004 indirildi.
      *requires: TASK-004* — **done**
- [x] TASK-102 Zihin modelleri (`cognition/mental_models.py`): her agent, diğerleri
      hakkında (gerçek kişilikten sapabilen, gözlemcinin empatisine göre çarpıtılan)
      bir `PerceivedOther` tutuyor. `social_perception_gap` metriğiyle ölçülüyor.
      *requires: TASK-101* — **done**
- [x] TASK-103 Theory of mind (basitleştirilmiş, tek seviye): `reflected_self` —
      "insanlar beni nasıl görüyor sanıyorum" — gerçek toplumsal itibardan (`avg_trust`)
      bağımsız sürüklenebiliyor (bkz. metrics.png). Tam iç içe geçmiş ("A, B'nin C
      hakkında ne düşündüğünü sanıyor" gibi) ToM henüz yok — bu V6'ya bırakıldı.
      *requires: TASK-102* — **done (simplified)**
- [x] TASK-104 Parametre kalibrasyonu — **kısmen tamamlandı**:
      - Kaynak kapasitesi/tüketimi artık `n_agents`'a göre ölçekleniyor
        (`*_per_agent` config alanları + `Ship.__init__`), böylece popülasyon
        değiştiğinde denge bozulmuyor (önceden n=80'de dengeliyken n=60'ta
        `true_scarcity`→0 çöküyordu — düzeltildi).
      - Kapasite ve yenilenme oranları ölçeklenmiştir; ancak varsayılan
        konfigürasyonda uzun koşularda kıtlık tavana yaklaşabilir. ISSUE-011,
        orta kıtlık rejiminin ayrıca kalibre edilmesini ve analizlerin orada
        yinelenmesini ister.
      - `misinformation_rate`'in davranışsal etkisi güncel modelde güvenilir
        bulunmamıştır (ISSUE-001, REVALIDATION.md). Etkiyi istenen sonuca göre
        zorlamak yerine bu sonuç belgelenmiştir.
      *requires: TASK-006*

## V2 — Society
- [x] TASK-201 Institutions modülü (`institutions/leadership.py`): liderlik agent
      etkileşimlerinden organik olarak ortaya çıkıyor — güven-ağırlıklı
      "etki skoru" popülasyona göre ölçeklenen bir eşiği geçen agent lider
      oluyor; kimse geçemezse (varsayılan V0/V1 durumunda olduğu gibi)
      **kurum hiç oluşmuyor**. `has_leader`/`institution_legitimacy` metrikleriyle
      izleniyor. *requires: V1* — **done (liderlik; ek kurumların durumu
      TASK-205–208'de)**
- [x] TASK-202 Basit ekonomi genişletmesi: bir lider varken forage gelirinden
      legitimacy-ölçekli bir "vergi" kesiliyor, ortak rezervde birikiyor,
      periyodik olarak nüfusa eşit dağıtılıyor (`redistribution_interval`).
      Uzmanlaşma/fiyat mekanizması henüz yok. *requires: TASK-006* —
      **done (yalnızca vergi+eşit dağıtım)**
- [x] TASK-203 Institutional trust ↔ Beliefs.institution_trust geri besleme:
      her agent kurumun gerçek `legitimacy`'sini değil, kendi gürültülü/yanlı
      algısını görüyor (`Beliefs.update_institution_trust`). Gözlenen davranış:
      `avg_institution_trust` başlangıç önyargısından (0.6) gerçek legitimacy
      seviyesine (~0.02-0.03) 500 tick içinde tam yakınsamıyor — confirmation_bias
      kurumsal güvenin neden yavaş değiştiğine dair makul bir açıklama, ama
      kasıtlı mı tesadüfi mi net değil; TASK-204 olarak izlenmeli.

### V2'de henüz olmayanlar (ileride ayrı alt-task'lar)
- [x] TASK-204 `avg_institution_trust`'ın yakınsama hızını incele/kalibre et — **kapalı, bkz. KNOWN_ISSUES.md ISSUE-003**
- [x] TASK-205 Courts/police (`institutions/law_enforcement.py`): yalnızca bir
      lider VARSA teçhizata sahip — yakalanma olasılığı kurumun GERÇEK
      legitimacy'siyle ölçekleniyor; caydırıcılık ise agent'ın KENDİ
      `institution_trust` İNANCIYLA (`cognition/decision.py`'deki `steal`
      skoruna `deterrence_strength` terimi) — yani gerçeklik/inanç ayrımı
      burada da var. 5 seed'den 3'ünde lider oluşuyor ve oluştuğunda hırsızlar
      gerçekten yakalanıyor (4-12 kez/koşu), ama legitimacy hep düşük kaldığı
      için (~0.01-0.03) caydırıcılık zayıf — bu, projenin genel "kırılgan
      kurumlar" örüntüsüyle tutarlı, ayrı bir hata değil.
- [x] TASK-206 Education (`institutions/education.py`): çocuklar her tick küçük
      bir temel ("köy tarafından büyütülme") + kurumun GERÇEK legitimacy'siyle
      ölçeklenen ekstra bir gelişim oranı alıyor (conscientiousness/openness).
      Lider yoksa yalnızca temel oran işliyor.
- [x] Ekonomi: basit uzmanlaşma (learning-by-doing) — `Agent.forage_skill`,
      her forage eyleminde artıyor ve yem verimini yükseltiyor. Tam fiyat/emek
      piyasası hâlâ yok, ama "aynı işi çok yapan daha iyi olur" ilkesi artık var.
- [x] TASK-207 Healthcare (`institutions/healthcare.py`): sağlık iyileşme oranı
      temel + legitimacy-ölçekli ekstra bonustan oluşuyor (education/leadership
      ile aynı desen). *requires: TASK-201* — **done**
- [x] TASK-208 Media (`institutions/media.py`) — **yalnızca media, religion/science
      hâlâ yok**: lider varken, `media_broadcast_interval` her tick'te
      legitimacy-ölçekli bir "yayın" — lider inancı, organik dedikodudan
      (komşuluk + %15 uzun-menzil) çok daha geniş bir kitleye, aynı
      `transmit_belief` çarpıtma mekanikleriyle ulaşıyor.
- [x] Çok boyutlu kültür (kısmi): `culture/norms.py`'ye ikinci bir eksen —
      `authority_norm` (0=özerklik, 1=hiyerarşi/itaat) — bir önceki tick'in
      `avg_institution_trust`'ından oluşuyor, conformity'si yüksek
      agent'ların `steal`/`spread_belief` skorlarına geri besleniyor.
      doc 1'in önerdiği 7 eksenden yalnızca 2'si (helping_norm, authority_norm)
      var; individualism/collectivism, tradition/change, economic preferences
      vb. hâlâ yok.
- [ ] Din/bilim kurumları hâlâ modellenmedi (TASK-208'in geri kalanı).
- [ ] Gerçek fiyat/emek piyasası hâlâ yok — yalnızca basit forage-uzmanlaşması var.

## V3 — Culture
- [x] TASK-301 Norm oluşumu (`culture/norms.py`): `helping_norm` — popülasyonun
      "burada yardımlaşmak normal mi?" algısı — sıfırdan (0.5, nötr) başlayıp
      bir önceki tick'in `cooperation_rate`'ini izleyerek kendiliğinden
      oluşuyor, sonra conformity'si yüksek agent'ların `share`/`steal`
      skorlarına geri besleniyor (norm ne kadar "bencil"e kaymışsa, uyumcu
      agent da o kadar çalmaya yatkınlaşıyor). *requires: V2* —
      **done (yalnızca tek bir norm boyutu — identity/dil henüz yok)**
- [x] TASK-302 Identity ("Ben bir X'im"): `agents/identity.py` — identity
      sıfırdan (`label=None`) başlıyor, en az 5 tekrar eden davranış
      (liderlik/yardım/hırsızlık/mağduriyet) biriktikten sonra oluşuyor,
      oluştuktan sonra o davranışı `identity_feedback_strength` katsayısıyla
      pekiştiriyor (sunk-cost). **Parametre taramasıyla doğrulandı**
      (`KNOWN_ISSUES.md` ISSUE-004): katsayı 0.0→0.5 arttıkça `avg_trust` ve
      `positive_relationship_rate` 5 seviyenin tamamında monoton düşüyor —
      gerçek, doz-bağımlı bir etki. (Bu 5 seed'lik taramadır; n=30'da yalnızca
      0.0/0.5 uçları yeniden sınandı, ara dozlar sınanmadı — `REVALIDATION.md`.)
      *requires: V3* — **done**
- [x] TASK-303 Basit "jargon" — aynı objektif eylemin farklı kimlik/gruplarda
      farklı öznel anlam kazanması: `identity.label == "opportunist"` olan bir
      agent, kendisine yapılan `share` (yardım) eylemini güven artışı değil
      küçümseme olarak okuyor (trust nudge işareti tersine dönüyor). Kelime
      bazlı gerçek bir dil modeli değil — doc 3, point 5'in davranışsal bir
      yaklaşıklaması. *requires: TASK-302* — **done (basitleştirilmiş)**

### Gözlemlenen açık soru (V3 sonrası)
`identity_feedback_strength` etkisi ve uzlaşma mekaniği daha sonra çoklu-seed
yeniden sınandı; sonuçlar ve yorum sınırları `REVALIDATION.md`'dedir.

## V4 — Evolution (nesiller)
- [x] TASK-401 Doğum/yaşlanma/ölüm döngüsü (`population/lifecycle.py`):
      kurucular 18-50 yaş arası çeşitli yaşlarda başlıyor (tek kohort değil);
      yaşlılık ölüm riski `elderly_age`(60)'tan sonra yaşla birlikte artıyor;
      doğum, anne uygun yaşta/ihtiyaçları karşılanmış/az stresli olduğunda VE
      yerel sosyal çevresinde uygun yaşta bir "baba" bulunduğunda gerçekleşiyor
      (rastgele bir eş değil). `max_population_multiplier` taşıma kapasitesi
      güvenlik valfı. *requires: V3* — **done**
- [x] TASK-402 Kültür aktarımı (kısmi — "aile" düzeyinde): çocuk kişiliği
      ebeveynlerin harmanlanmış+mutasyonlu ("nature") kişiliğini, inançları
      (`scarcity_belief`, `institution_trust`) ebeveynlerin GÜNCEL dünya
      görüşünü ("nurture") devralıyor. **Identity ASLA devralınmıyor** —
      TASK-302'nin "kimlik yaşanmışlıktan doğar" kuralı çocuklar için de
      geçerli. Toplum-geneli kültür emilimi (okul/geniş sosyalleşme) yok,
      yalnızca ebeveyn aktarımı var. *requires: TASK-301, TASK-302* —
      **done (yalnızca aile düzeyi)**

### Gözlemlenen emergent bulgu (V4 sonrası, varsayılan config)
80 kurucu (çeşitli yaşlarda, hepsi doğurgan yaşta) → ilk ~150 tick'te nüfus
110'a fırlıyor ("baby boom", çünkü kurucuların tamamı başlangıçta uygun yaşta)
→ `resource_capacity` yalnızca KURUCU nüfusa (80) göre sabitlendiği için (bkz.
`ARCHITECTURE.md`) kaynak talebi arzı aşıyor → `true_scarcity` ~tick 250'de
1.0'a kilitleniyor ve 500'e kadar orada kalıyor → nüfus tekrar ~88'e düşse
bile (hâlâ kurucu kapasitenin üstünde) toparlanma görülmüyor → stres, çatışma,
güvensizlik hepsi sürekli yükseliyor. Bu, doc 1'in beklediği türden bir
"nüfus patlaması → taşıma kapasitesini aşma → çöküş" senaryosu.
2000 tick ve 10 seed ile yapılan takip koşusunda nüfusun çöküşü 10/10 seed'de
görüldü. Kapasitenin iki katına çıkarıldığı koşulda çöküş büyük ölçüde önlendi.
Sonuç ve sınırları ISSUE-007'de kayıtlıdır.

## V5 — Experimental Laboratory
- [x] TASK-501 Counterfactual world (`experiments/counterfactual.py`):
      `run_seeds()` — aynı config'i N farklı seed'le koşturup dağılım verir;
      `run_paired_counterfactual()` — aynı seed'le, tek bir parametre farkıyla
      iki dünyayı koşturup **ilk ayrışma tick'ini** raporlar (doc 3, "World A
      vs World B"). *requires: TASK-010* — **done**
- [x] TASK-502 Causal narrative çıkarımı (`experiments/causal_narrative.py`):
      bir koşunun metrik geçmişini gezip önceden tanımlı uyarı işaretlerinin
      (kaynak tükenmesi, stres, güven, çatışma, liderlik kaybı, nüfus düşüşü)
      İLK tetiklendiği tick'i buluyor, kronolojik sırayla raporluyor.
      **Bu bir nedensellik kanıtı değil** — yalnızca gözlemlenen sıralama
      (PROJECT_CONSTITUTION kural 4). Liderlik sinyali hiç lider oluşmaması
      ile liderin sonradan kaybolmasını ayırır (ISSUE-008).

### ISSUE-007'yi kapatan bulgu (bkz. `run_v5_lab.py`, `KNOWN_ISSUES.md`)
10 seed × 2000 tick, 3 koşul: (A) varsayılan config → **%100'ü kurucu
nüfusun altına düşüyor**, %30'u neredeyse soyu tükeniyor; (B) `birth_rate_base`
düşürülünce (0.008→0.003) **daha da kötüleşiyor** (%100'ü ≤5 nüfusa iniyor —
saf sezgi yanlış çıktı); (C) `resource_capacity_per_agent` ikiye katlanınca
(75→150) **çöküş neredeyse tamamen ortadan kalkıyor** (%0'ı ≤20 nüfusa
iniyor, çoğu taşıma kapasitesinde (144) istikrar buluyor). Gerçek darboğaz
doğum oranı değil, kaynak kapasitesiymiş — V5'in tam da yapması gereken
türden bir bulgu.

## V6 — NeuroAI
- [x] TASK-601 Metacognition (`cognition/metacognition.py`): her agent her
      tick kendi hafızasından ("gave_help" vs "stole" olayları) son ~40
      tick'teki kendi davranışını yeniden okuyor — ve bu okuma, açıklık
      (openness) düşük/stresi yüksek agent'larda kendini kayırma yanlılığıyla
      (self-serving bias) çarpıtılıyor. Sonuç, `conscientiousness`'ı yüksek
      agent'larda `share`/`steal` skorlarına geri besleniyor (özdüzeltme);
      düşük conscientiousness'lı agent'lar bu sinyali büyük ölçüde yok
      sayıyor (doc 2, point 2: özdeğerlendirme davranışı HER ZAMAN
      değiştirmez). *requires: V3* — **done**
- [~] TASK-602 İkinci-derece theory-of-mind + predictive processing —
      **yalnızca ilk yarısı yapıldı**: `MentalModel`'e her (agent, diğer-agent)
      çifti için ayrı bir `they_probably_think_of_me` alanı eklendi ("bu
      SPESİFİK kişi bana nasıl bakıyor sanıyorum" — V1'deki popülasyon-geneli
      `reflected_self`'ten farklı, ilişkiye özel bir tahmin). Tam iç içe geçmiş
      ToM ("A, B'nin C hakkında ne düşündüğünü sanıyor" gibi 3'lü zincirler)
      ve predictive processing/active inference'ın `cognition/decision.py`'nin
      yerine geçmesi **yapılmadı** — bu, mevcut utility/softmax mimarisinin
      tamamen değiştirilmesini gerektiren, kapsamı çok daha büyük ayrı bir
      görev; TASK-602b olarak bölünüp ileride ele alınmalı.

## PLANLANDI (TASK-602b henüz başlanmadı; TASK-701'in ilk dilimi yapıldı)

### TASK-602b — Predictive processing / active inference (NeuroAI çekirdeği)
**Durum: planlandı, hiç kod yazılmadı.** Bu, projenin "Neuro" tarafının şu ana
kadar en zayıf kalan parçası — mevcut `cognition/decision.py` saf utility/
softmax skorlama kullanıyor, nörobilimden ilham alan hiçbir hesaplama
mekanizması yok.

Kabaca plan:
1. `cognition/predictive_processing.py` — decision.py'ye ALTERNATİF (onu
   silmeden) bir karar modülü: agent'ın her an bir "üretici model"i olsun
   (dünyanın nasıl olmasını beklediği — `needs`, `beliefs`, `social` durumu
   üzerinden), gerçek gözlemle bu beklenti arasındaki fark ("prediction
   error") hesaplansın.
2. Aksiyon seçimi, şu anki gibi elle yazılmış utility skorları yerine,
   "hangi aksiyon beklenen prediction error'ı en çok azaltır" (active
   inference'ın basitleştirilmiş bir versiyonu) ilkesine göre yapılsın.
3. `Simulation`'a bir `cognitive_architecture: str` config alanı eklenip
   ("utility" | "predictive_processing") ikisi arasında seçim yapılabilsin —
   TASK_GRAPH'ın kendi kuralı gereği (PROJECT_CONSTITUTION kural 7: tek
   koşuya güvenme) ikisi aynı senaryoda KARŞILAŞTIRMALI olarak koşturulup
   emergent sonuçlar (stres, işbirliği, çöküş dinamikleri) karşılaştırılmalı.
4. Her mekanizma için PROJECT_CONSTITUTION kural 4 gereği belgeleme: hangi
   nörobilimsel fenomeni temsil ediyor, hangi basitleştirme yapıldı.
- **Bağımlılık**: yok, bağımsız başlanabilir; mevcut `Agent`/`Beliefs`
  yapısını bozmadan üstüne eklenebilir (mimari zaten buna izin verecek
  şekilde modüler tasarlandı — bkz. `ARCHITECTURE.md`).
- **Tahmini kapsam**: bu projedeki tek bir V-aşamasından (örn. V3) daha büyük
  — kendi başına ayrı bir çalışma turu gerektirir.

### TASK-701 — İnteraktif görselleştirme / dashboard
**Durum: İLK DİLİM YAPILDI (bkz. altta "Yapılanlar"); açık kalanlar
`KNOWN_ISSUES.md` ISSUE-010'da.**

#### Yapılanlar
- `visualization/dashboard_export.py`: çekirdek motora DOKUNMADAN ayrı bir
  enstrümante döngü (`Simulation.step()`'i doğrudan çağırıp her 10 tick'te
  örneklenmiş kurucu agent'ların anlık görüntüsünü alıyor) + son-tick güven
  ağı export'u. Çıktı: tek bir JSON paketi (~850 KB, 80 agent/500 tick).
- `visualization/dashboard_template.html` + `run_dashboard.py`: tek dosyalık
  HTML dashboard üreticisi (`python3 run_dashboard.py --agents 120 --ticks 800`).
  Üç sekme: **Popülasyon** (metrik seçici, tick aralığı kaydırıcıları, hover
  tooltip), **Agent İnceleme** (18 örneklenmiş agent; kişilik radar grafiği
  başlangıç-vs-güncel; seçilen alanın zaman serisi), **Sosyal Ağ** (D3
  force-directed graf; düğüm rengi=identity etiketi, kenar rengi=güven
  işareti, kalınlık=|güven|).
- Claude artifact olarak yayınlandı (private, sahibi paylaşana kadar).

#### Yapılmayanlar (orijinal plandan)
- Tüm agent'lar için tam per-agent export (yalnızca 18 örnek).
- Sosyal ağın zaman içinde animasyonu/kaydırıcısı (yalnızca son tick).
- İki koşunun/counterfactual dünyanın yan yana karşılaştırması.
- Gerçek tarayıcıda uçtan uca görsel doğrulama (bkz. ISSUE-010).

#### Kalan dashboard işleri
İlk dilim uygulanmıştır; kapsam ve doğrulama sınırları ISSUE-010'da tutulur.
Eski plan aşağıdaki maddelerde tarihsel referans olarak korunmuştur.

Kabaca plan:
1. HTML/JS tabanlı tek-dosya bir dashboard (Claude'un artifact/publish
   akışıyla uyumlu) — `metrics.csv`'yi okuyup zaman serisi grafiklerini
   interaktif çizsin (zoom, tick üzerine gelince değer gösterme).
2. Tekil agent inceleme paneli: bir agent id'si seçilince o agent'ın
   personality/needs/beliefs/identity/mental_model durumunu ve zaman
   içindeki değişimini gösterebilsin (`Agent` zaten bu veriyi tutuyor,
   yalnızca dışa aktarım eksik).
3. Sosyal ağ görselleştirmesi: `SocialNetwork.trust`'ı bir graf olarak
   (node=agent, edge=güven, renk=pozitif/negatif) çizsin — özellikle
   identity kümelenmesi ve leadership oluşumu görsel olarak çok daha
   çarpıcı olur.
4. `Simulation`'ın her tick'te tam agent-seviyesi state'i dışa aktarmasını
   sağlayacak bir "agent snapshot" exporter gerekecek (şu an yalnızca
   popülasyon-ortalaması metrikler kaydediliyor, `metrics/tracker.py`) —
   bu, depolama boyutunu ciddi büyütür (n_agents × n_ticks × alan sayısı),
   o yüzden muhtemelen yalnızca son N tick veya seyrek örnekleme (her 10
   tick'te bir) mantıklı olur.
- **Bağımlılık**: yok, bağımsız başlanabilir.
- **Tahmini kapsam**: orta — TASK-602b'den küçük ama yine de kendi başına
  bir çalışma turu gerektirir (özellikle agent-snapshot exporter'ı).

### V6 sonrası dürüst durum
`TASK_GRAPH.md`'deki V0→V6 planının tamamı en azından ilk-dilim (first-slice)
düzeyinde uygulandı. Kurumlar artık 4/7 (leadership, courts/police, education,
healthcare, media — religion/science hâlâ yok), kültür 2 boyutlu (7'den),
ekonomi basit uzmanlaşmaya sahip (tam piyasa değil). Duyarlılık analizi hem
tekil (Morris) hem sınırlı-etkileşim (2x2 faktöriyel) düzeyinde yapıldı;
ölçek testi tamamlandı ve gerçek bir performans hatası düzeltildi. Kalan en
büyük iki iş yukarıda TASK-602b ve TASK-701 olarak planlandı.

## Sistematik duyarlılık analizi ve ölçek testi (V6 sonrası)

### Sistematik duyarlılık analizi: etkileşim testi eklendi
`experiments/sensitivity.py::factorial_interaction` — en etkili iki parametre
(`resource_capacity_per_agent`, `food_regen_rate`) için 2x2 faktöriyel tasarım
(`run_interaction_test.py`). **Bulgu**: `true_scarcity` üzerindeki etkileşim
(-0.391), `food_regen_rate`'in tek başına ana etkisinden (-0.195) neredeyse
İKİ KAT güçlü — yani kapasite zaten yüksekken regen oranının etkisi çok daha
güçlü oluyor (düşük kapasitede regen'i artırmanın faydası sınırlı, sert bir
tavan var). `population` üzerinde de azalan getiri türü bir etkileşim var
(-9.925). Bu, salt tek-tek (Morris) taramanın KAÇIRACAĞI, yalnızca faktöriyel
tasarımın yakalayabileceği türden bir bulgu — tam Sobol'un neden değerli
olacağının somut kanıtı, ama hâlâ yalnızca 1 çift için yapıldı (19 parametrenin
C(18,2)=153 çifti için tam bir tarama yapılmadı — çok pahalı olurdu).
- **Duyarlılık analizi** (`experiments/sensitivity.py`, `run_sensitivity.py`):
  tam Sobol yerine Morris-tipi "elementary effects" tarama — 19 parametre,
  her biri tek başına perturbe edilip 4 seed'le ölçüldü. **`resource_capacity_per_agent`
  ve `food_regen_rate` açık ara en etkili iki parametre çıktı** — bu, ISSUE-007'nin
  ad-hoc bulgusunu tamamen bağımsız bir yöntemle doğruladı. Yöntemin bilinen
  sınırı: parametreler arası ETKİLEŞİMİ yakalamıyor (yalnızca tekil etkiler).
- **Ölçek testi** (`run_scale_test.py`): 100→10.000 agent aralığında ölçüldü.
  İlk turda (100-1600 agent) doğrusala yakın çıktı (üstel≈1.05), ama 1600-10.000
  aralığında gerçek bir süper-doğrusal davranış ortaya çıktı (üstel≈1.26).
  Kök neden izole edildi: `SocialNetwork.random_acquaintance`'ın her çağrıda
  tüm popülasyonu filtrelemesi (`[x for x in agent_ids if x != a]`) — bu
  **gerçek bir performans hatasıydı, düzeltildi** (reddet-ve-tekrar-dene,
  O(1) beklenen). Düzeltme sonrası üstel 1.26→1.09'a indi. n=10.000'de artık
  tick başına ~0.35s (500 tick ≈ 3 dakika) — doc 1'in "10.000 agent" hedefi
  artık pratik olarak ulaşılabilir.


## KALAN İŞ ENVANTERİ (V6 sonrası tarihsel not; güncel durum yukarıdaki bölümlerde)

Bu liste hafızadan değil, kod taranarak çıkarıldı (grep sonuçları oturumda
gösterildi). Öncelik sırası bizim önerimizdir, kesin değil.

**A. AI orkestrasyonu hiç kurulmadı (projenin orijinal iddiası).** Klasör bu
envanter yazıldığında git repo değildi (2026-10-07'de `git init` yapıldı). Ayrı araştırma/mimari/kodlama/review
rolleri, branch disiplini, bağımsız çapraz-kontrol yok; tüm iş tek bir sürekli
akışta yapıldı, "review" da aynı akışın kendi hatalarını sonradan bulmasıydı.

**B. TASK-602b — predictive processing / active inference.** Hiç kod yok.
Ayrıca doc 1 §2A'daki nöral katman (attention, working memory, uyku, alışkanlık
oluşumu) ve §8'deki öğrenme yöntemleri (RL, Bayes güncellemesi, imitation,
evrimsel adaptasyon) büyük ölçüde yok — yalnızca inanç harmanlama ve
`forage_skill` var. Bilişsel önyargılardan yalnızca confirmation/negativity/
self-serving benzeri olanlar var; anchoring, availability, loss aversion vb. yok.

**C. Bilimsel dayanak eksik.** `REFERENCES.md` mekanizma-kaynak eşlemesini ve
kanıt düzeyini kaydeder; doğrulanmamış atıflar işaretlidir ve mekanizmaların
çoğu sezgisel tasarım tercihidir. Literatür taraması, geçerli kaynak bulma ve
ampirik kalibrasyon hâlâ açık iştir.

**D. Ölçüm ve istatistik.** Polarizasyon, ağ merkezileşmesi, sosyal kohezyonun
birkaç ölçüsü ve servet-sıra hareketliliği eklendi; `human_capital_total`
inovasyon değildir. İstatistiksel araçlar ve n=30 yeniden sınaması
`REVALIDATION.md`'de belgeli. Tüm parametre çiftleri taranmadı; kalan örneklem
ve rejim sınırlamaları ISSUE-011/012'de izleniyor.

**E. Grup/fraksiyon yapısı yok.** İttifak, grup kurma/terk etme, fraksiyon kodu
yok. Bu yüzden doc 1'in emergent fenomenleri (siyasi fraksiyonlar, isyan,
devrim, kült benzeri gruplar, göç) şu an tespit edilemez, yalnızca
dolaylı olarak izlenebilir.

**F. Ekonomi/teknoloji.** Ticaret, fiyat, emek piyasası, işsizlik yok
(`engine.py`'de "no market yet" notu). Teknoloji evrimi (doc 3 §6) hiç
yapılmadı. Din ve bilim kurumları yok. Kültürde 7 eksenden yalnızca 2'si var
(`helping_norm`, `authority_norm`). Aldatma/manipülasyon/ihanet eylemleri
`steal` ve dedikodu çarpıtmasının ötesinde yok. Tam iç içe geçmiş ToM yok.

**G. Ölçek.** Yalnızca tick başına süre ölçüldü (20/15 tick, doğumlar kapalı).
10.000 agent'ta 500 tick'lik DİNAMİKLERİN makul kalıp kalmadığı ve bellek
kullanımı test edilmedi.

**H. ISSUE-010** — dashboard gerçek tarayıcıda doğrulanmadı (bkz. KNOWN_ISSUES.md).

**I. Test kapsamı.** Tek bir sanity test modülü var; emergent davranış için
regresyon testi, CI ve kapsam ölçümü henüz yok. Test sayısı zaman içinde
değişebileceğinden burada sabit sayı tutulmuyor.


### Tarihsel envanter güncellemesi
- **C — kısmen yapıldı.** `REFERENCES.md`: 5 künye web aramasıyla doğrulandı, 4'ü
  doğrulanMADI diye işaretli; her mekanizma [E]/[T]/[S] olarak dürüstçe sınıflandırıldı.
  Sonuç: mekanizmaların **çoğu [S]** (sezgisel), hiçbiri ampirik kalibre değil. Bu eksik
  KAPANMADI, yalnızca görünür hâle geldi; kalibrasyon işi hâlâ açık.
- **D — kısmen yapıldı.** Eklendi: polarizasyon (inanç+servet), ağ merkezileşmesi,
  karşılıklılık/kümelenme/dev-bileşen, servet-sıra hareketliliği, `human_capital_total`;
  `experiments/statistics.py` (GA, Welch, Cohen d, Bonferroni); 4 eski bulgu n=30 ile
  yeniden sınandı (`REVALIDATION.md`). **Yapılmayanlar:** inovasyon/GDP (modelde
  mekanizma yok, uydurulmadı), nesiller-arası hareketlilik, sosyal kohezyonun
  bütünsel bir tanımı, kalan bulguların yeniden sınanması (ISSUE-012), orta rejim (ISSUE-011).

## Akademik araştırma planı uygulama başlangıcı (2026-10-04)

- `ACADEMIC_RESEARCH_PLAN.md`: ODD/ODD+D, kod doğrulaması, pattern-oriented
  değerlendirme, seed ve deney ilkeleri.
- `ODD_D.md`: mevcut ajan kararlarını, schedule ve operasyonel metrik
  tanımlarını kaynak koda göre belgeleyen ilk ODD+D taslağı.
- `run_regime_calibration.py`: kapasite/yenilenme pilotu. İlk 16 hücre × 4 seed
  ve takip 2×2 × 20 seed yapıldı. Orta kıtlık seedler arasında istikrarlı
  tekrarlanmadığından ISSUE-011 açık; sonuçlar `ACADEMIC_RESEARCH_PLAN.md` ve
  `output/regime_calibration_*.json` içinde.
- `EXPERIMENT_PROTOCOL_RESOURCE_STRESS.md` ve
  `run_resource_factorial.py`: önceden tanımlı 2×2 faktöriyel protokol ve
  çalıştırıcı (30 seed/hücre, bağımsız seed blokları, seed düzeyi bootstrap
  belirsizlik aralıkları). Final koşu tamamlandı; rapor
  `RESOURCE_STRESS_RESULTS.md`, ham dosyalar `output/resource_factorial/`.
- Doğrulama: aynı-seed tekrar üretilebilirlik testi, factorial smoke testi ve
  küçük CLI smoke koşusu geçti. Tam `test_basic.py` bu ortamda SciPy
  (`requirements.txt`'e eklendi) olmadığı için tamamlanmadı.
- Güncelleme sırası sağlamlık analizi tamamlandı: `agent_update_order` sabit
  veya tick başına karıştırılmış seçilebilir. Aynı 120 seed-koşul çiftiyle
  faktöriyel kontrast farkları hesaplandı; dokuz farkın bootstrap aralığı
  sıfırı kapsadı. Yönler iki çizelgede aynı. Rapor `SCHEDULE_ROBUSTNESS_RESULTS.md`,
  ham dosyalar `output/schedule_robustness/` içinde.
- RNG aktarımını azaltan takip tamamlandı: `agent_rng_mode="per_agent"` ile aynı
  seedleri sabit/karıştırılmış sırada koşan 240 simülasyon. Dokuz faktöriyel etki
  farkı sıfırı kapsadı; yönler korundu. `shared` varsayılan kaldı. Rapor
  `AGENT_RNG_ROBUSTNESS_RESULTS.md`, ham veriler `output/agent_rng_robustness/`.
- Eski identity-feedback bulgusu kaynak rejimleri içinde yeniden sınandı:
  2×2×2, 30 eş seed bloğu/hücre, toplam 240 koşu. Güven azaldı ve çatışma
  arttı; çatışma artışı düşük kapasitede daha büyüktü. Rapor
  `IDENTITY_RESOURCE_RESULTS.md`, protokol `EXPERIMENT_PROTOCOL_IDENTITY_BY_RESOURCE.md`.
  Ara dozlar ve Gini/nüfus mekanizmasının açıklaması açık takip işleridir.

## Bulguların formüle bağımlılığı incelemesi (2026-10-07)

Belgeler ve `cognition/decision.py` birlikte okununca iki ana deneyin birincil
sonuçlarının karar formülüne doğrudan yazılı olduğu görüldü (ISSUE-013).

- [x] `steal`/`share` skorlarındaki kıtlık inancı katsayıları `Config`'e taşındı;
      `action_scarcity_reference` ile bağlantı kesilebiliyor. Varsayılan davranış
      bit-bit aynı.
- [x] Eylem payı metrikleri (`action_*_rate`) eklendi.
- [x] Sanity testleri: `tests/test_scarcity_link_ablation.py`.
- [x] Ablasyon protokolü koşudan önce yazıldı:
      `EXPERIMENT_PROTOCOL_SCARCITY_LINK_ABLATION.md` (2×2×3, 30 seed bloğu, 360 koşu).
- [x] Ablasyon koşusu ve raporu: `SCARCITY_LINK_ABLATION_RESULTS.md`.
- [x] Kimlik deneyi etiket/eylem dağılımı (post hoc): `run_identity_label_followup.py`.
- [ ] Kimlik geri beslemesi için ayrı ablasyon (etiket → skor terimi) — protokol yok.
- [ ] ISSUE-007 doğum oranı bulgusunu n≥30 ile yeniden sınama (ISSUE-012).
- [ ] `120/0.016` hücresindeki seed'ler arası rejim ayrışmasını ayrı soru olarak inceleme.
- [ ] `shared` / `per_agent` RNG varsayılanı kararı.

## İhtiyaç temelli karar mimarisi (2026-10-07)

ISSUE-014: servet hiçbir ihtiyacı karşılamıyordu, bu yüzden çalmanın kıtlıkla
bağı ancak elle yazılmış bir katsayıyla kurulabiliyordu.

- [x] `decision_architecture` anahtarı; `"need_based"` kolunda yenebilir erzak ve
      aciliyet × getiri skorları. Varsayılan değişmedi.
- [x] Sanity testleri: `tests/test_need_based_decision.py`.
- [x] Protokol koşudan önce: `EXPERIMENT_PROTOCOL_NEED_BASED_DECISION.md`
      (2×2 kaynak × 2 mimari, 30 seed bloğu, 240 koşu).
- [ ] Koşu ve rapor: `NEED_BASED_DECISION_RESULTS.md`.
- [ ] `provision_*` parametrelerine duyarlılık (özellikle `provision_max_per_tick`).
- [ ] Toplamada kütle korunumu: yenen ve saklanan payın açık ayrımı.
- [ ] Gini için null model (yalnızca rastgele aktarım) — `REFERENCES.md` #15.
- [ ] Epstein (2002) karar kuralıyla karşılaştırma ("docking") — `REFERENCES.md` #10–11.
