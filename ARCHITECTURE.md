# Mimari

Bu belge mevcut kodu tarif eder. Araştırma varsayımları ve modelin bilimsel
sınırları [REFERENCES.md](REFERENCES.md) ile [KNOWN_ISSUES.md](KNOWN_ISSUES.md)
dosyalarında tutulur. Yeni mekanizma eklenince bu belge ve
[TASK_GRAPH.md](TASK_GRAPH.md) güncellenmelidir.

## Katmanlar

```text
configuration/config.py
        │
environment/ship.py ── fiziksel kaynak havuzu ve çevresel olaylar
        │
economy/resources.py ── ortak kaynaklar, forage ve servet
        │
agents/agent.py ── personality, ihtiyaçlar, memory, identity, metacognition
        ├── cognition/beliefs.py, decision.py, mental_models.py
        ├── sociology/social_network.py ── güven grafiği ve small-world komşuluk
        ├── information/rumors.py ── söylenti ve inanç aktarımı
        ├── institutions/ ── leadership, kolluk, eğitim, sağlık, medya
        ├── culture/norms.py ── yardım ve otorite normları
        └── population/lifecycle.py ── yaşlanma, ölüm ve doğum
        │
simulation/engine.py ── katmanları bağlayan ana simülasyon döngüsü
        ├── metrics/ ── popülasyon, ekonomi ve ağ ölçümleri
        ├── experiments/ ── çoklu seed, istatistik, karşı-olgusal ve duyarlılık
        └── visualization/ ── PNG grafikleri ve HTML dashboard verisi
```

`Config` simülasyon parametrelerinin tek kaynağıdır. `share`/`steal`
skorlarındaki kıtlık inancı terimleri de buradadır (`steal_scarcity_weight`,
`share_scarcity_weight`, `action_scarcity_reference`; ISSUE-013); karar
formülündeki diğer katsayılar hâlâ `cognition/decision.py` içinde sabittir.

`decision_architecture` iki karar mimarisi arasında seçer. Varsayılan
`"heuristic"` özgün skorlardır. `"need_based"` (ISSUE-014) iki şeyi değiştirir:
servet yenebilir erzak olur (`_update_internal_state` içinde, ihtiyaç
`provision_eat_threshold` altındayken) ve `forage`/`steal`/`share` skorları
doğrudan kıtlık inancı katsayısı yerine ajanın ihtiyaç aciliyeti × eylemin
ihtiyaca getirisiyle hesaplanır. Tick sırası ve RNG çekilişleri değişmez. Varsayılan `shared` RNG
modunda rastgele model işlemleri `Simulation.rng` üzerinden yürütülür. Deneysel
`per_agent` modunda ajan eylemleri ve ajan başına lifecycle çekilişleri sabit
ajan-ID seed'li akışlardan alınır; ortam, medya ve ağ kurulumundaki rastgele
işlemler hâlâ simülasyon akışını kullanır. Tick çizelgelemesi de `fixed` veya
`shuffled` seçilebilir. Dashboard dışa aktarımı ayrı RNG kullanır.

## Tick akışı

`Simulation.step()` her tick'te kabaca şu sırayı izler:

1. Çevre ve kaynak havuzu güncellenir; sosyal bağların güveni azalır.
2. Liderlik ve önceki tick'ten gelen gözlemlerle normlar güncellenir.
3. Her yaşayan ajan çevreyi gürültülü algılar, inançlarını ve özdeğerlendirmesini
   günceller, sonra utility/softmax karar mekanizmasıyla eylem seçer.
4. Eylemler kaynakları, güven ilişkilerini, söylentileri ve kurum etkileşimlerini
   değiştirir; ajanın iç durumu ve kimliği güncellenir.
5. Yaşlanma, ölüm, eğitim ve doğum süreçleri işletilir; varsa kamu rezervi
   dağıtılır.
6. Metrikler kaydedilir.

Uygulamadaki kesin sıra değişebilir; mekanik değişikliklerinde bu bölüm
`simulation/engine.py` ile birlikte güncellenmelidir.

## Uygulanan mekanizmalar

- **Biliş:** gürültülü kıtlık ve meşruiyet algısı, inanç güncelleme, hafıza,
  özdeğerlendirme ve kısmi ikinci-derece zihin modeli.
- **Sosyal yapı:** small-world yerel komşuluk, uzun menzilli etkileşimler,
  güven/ilişki güncellemeleri ve söylenti aktarımı.
- **Ekonomi ve kurumlar:** kaynak toplama ve paylaşma, hırsızlık, liderlik,
  vergi/yeniden dağıtım, kolluk, eğitim, sağlık iyileşmesi ve kısmi medya yayını.
- **Kültür ve nüfus:** yardım ve otorite normları; tekrarlanan davranıştan kimlik;
  yaşlanma, ölüm, doğum ve aileden kişilik/inanç aktarımı.
- **Araştırma araçları:** metrik izleyici, çoklu-seed ve eşleşmiş karşı-olgusal
  koşular, Morris-tipi tarama, sınırlı 2x2 etkileşim analizi, istatistiksel
  özetler ve görselleştirme.

Bu mekanizmaların varlığı, ampirik geçerliliklerinin kanıtlandığı anlamına
gelmez. Parametrelerin ve mekanizma varsayımlarının dayanak seviyesi için
`REFERENCES.md`'ye bakın.

## Bilinçli kapsam sınırları

- **Eksik kurumlar:** din ve bilim kurumları modellenmemiştir. Kolluk, eğitim,
  sağlık ve medya basit yaklaşımlardır; kurumların toplumsal etkileri ampirik
  olarak kalibre edilmemiştir.
- **Ekonomi:** fiyatlar, emek piyasası, işsizlik ve çoklu meslek sistemi yoktur;
  forage uzmanlaşması basit bir öğrenme etkisidir.
- **Kültür:** norm sistemi iki basit eksenden oluşur; dil/jargon evrimi ve geniş
  kültürel uzay modellenmez.
- **Biliş:** tam iç içe geçmiş theory-of-mind ve predictive processing/active
  inference uygulanmamıştır (TASK-602b).
- **Deney tasarımı:** Morris-tipi tarama parametre etkileşimlerini ölçmez;
  yalnızca belirli iki parametre için 2x2 deney vardır. Varsayılan rejimde
  kıtlık tavan etkisi ve bazı küçük örneklemli bulgular açık araştırma
  sınırlamalarıdır (ISSUE-011/012).
- **Ölçek:** `run_scale_test.py` kısa koşularda çalışma zamanını ölçer; uzun
  dönem sonuçların nüfus boyutuna göre eşdeğerliğini doğrulamaz.
- **Dashboard:** örnek ajanlar ve son-tick ağı gösteren ilk sürümdür. CDN
  bağımlılıkları nedeniyle çevrimdışı çalışmaz; gerçek tarayıcıda görsel
  doğrulaması açık ISSUE-010'dur.

## Kaynak kapasitesi tasarımı

`environment/ship.py` kaynak kapasitesini kurucu nüfus (`config.n_agents`)
üzerinden hesaplar. Nüfus doğumlarla artarsa kapasite otomatik büyümez; bu,
taşıma kapasitesi baskısını incelemek için seçilmiş bir varsayımdır. Bu seçim
araştırma sorusuna bağlıdır ve sonuçların yorumunda belirtilmelidir.
