# Ship of Fools — akademik ajan tabanlı simülasyon

Ship of Fools, gemi ortamında bireysel psikoloji, sosyal ilişkiler, kurumlar,
kültür ve kaynak dinamiklerini incelemek için geliştirilen bir ajan tabanlı
simülasyon araştırma projesidir. Model, davranışları kişilik, ihtiyaçlar,
stres, inançlar ve sosyal bağların etkileşiminden üretmeyi amaçlar.

Bu kod tabanı bir araştırma aracıdır; gerçek insanların davranışını veya
nörobiyolojiyi doğrulanmış biçimde yeniden ürettiği iddiasında değildir.
Mekanizmaların ve katsayıların önemli bir bölümü tasarım varsayımıdır. Kaynak
durumları ve model sınırlamaları için [REFERENCES.md](REFERENCES.md),
[KNOWN_ISSUES.md](KNOWN_ISSUES.md) ve [REVALIDATION.md](REVALIDATION.md)
okunmalıdır.

## Kurulum

Python 3.10 veya üstü gerekir. `requirements.txt`, PNG grafikleri için
`matplotlib`; istatistiksel yeniden sınama modülü için `scipy` kurar. Windows
PowerShell:

```powershell
cd ship_of_fools_project
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

macOS/Linux:

```bash
cd ship_of_fools_project
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Kullanım

Komutları proje klasöründen çalıştırın:

```bash
python run.py                         # tek koşu; output/metrics.csv ve PNG üretir
python run_experiments.py             # baseline ve misinformation karşılaştırması
python run_v5_lab.py                  # uzun çoklu-seed deney; birkaç dakika sürebilir
python run_sensitivity.py             # Morris-tipi parametre taraması
python run_interaction_test.py        # iki parametreli 2x2 faktöriyel deney
python run_revalidation.py            # istatistiksel yeniden sınama; yaklaşık birkaç dakika
python run_scale_test.py              # kısa çalışma zamanı ölçek ölçümü
python run_dashboard.py --agents 80 --ticks 500 --seed 42
python run_regime_calibration.py      # kaynak kıtlığı pilot taraması; birkaç dakika sürebilir
python run_resource_factorial.py     # final 2x2 deney; 120 dünya, birkaç dakika
python run_schedule_robustness.py    # sabit ve tick-başı karıştırılmış sıra karşılaştırması
python analyze_schedule_robustness.py # zamanlama sonuçları için faktöriyel kontrast analizi
python run_agent_rng_robustness.py   # ajan-başı RNG ile eş seedli 240 çizelge koşusu
python analyze_agent_rng_robustness.py # ajan-başı RNG sağlamlık analizini üretir
python run_identity_resource_factorial.py # kaynak rejimi × kimlik geri beslemesi; 240 dünya
python analyze_identity_resource_factorial.py # seed bloklu paired bootstrap analizi
python run_scarcity_link_ablation.py  # kaynak × kıtlık-inancı bağlantısı ablasyonu; 360 dünya
python analyze_scarcity_link_ablation.py # ablasyon kontrastları ve kalan pay
python run_identity_label_followup.py # kimlik deneyinin etiket/eylem payları; 240 dünya
python run_scarcity_link_ablation.py --arms intact,need_based --seed-start 70000 --out-dir output/need_based_decision --protocol EXPERIMENT_PROTOCOL_NEED_BASED_DECISION.md  # ihtiyaç temelli karar mimarisi; 240 dünya
python analyze_scarcity_link_ablation.py --dir output/need_based_decision
python run_scarcity_link_ablation.py --arms intact,provisions_only,scoring_only,need_based --seed-start 80000 --out-dir output/provision_scoring_factorial --protocol EXPERIMENT_PROTOCOL_PROVISION_SCORING_FACTORIAL.md  # erzak × skor ayrışımı; 480 dünya
python analyze_scarcity_link_ablation.py --dir output/provision_scoring_factorial --factorial provisions_only,scoring_only,need_based
python ship_of_fools/tests/test_basic.py
python ship_of_fools/tests/test_reproducibility.py
python ship_of_fools/tests/test_resource_factorial.py
python ship_of_fools/tests/test_schedule_robustness.py
python ship_of_fools/tests/test_scarcity_link_ablation.py
python ship_of_fools/tests/test_need_based_decision.py
```

Dashboard HTML dosyasını üretir; grafik kütüphanelerini CDN'den yüklediği için
dashboard'ı görüntülerken internet bağlantısı gerekir. Simülasyon motoru ve
rejim kalibrasyon pilotu Python standart kütüphanesini kullanır; PNG grafikleri
`matplotlib`, `run_revalidation.py` ise `scipy` gerektirir.

Her deneyde seed ve parametreleri kaydedin. Sonuçları mümkün olduğunda eşleşmiş
seed'lerle, birden fazla koşu üzerinden raporlayın; tek bir koşuyu kanıt olarak
yorumlamayın. Deney çıktıları `output/` altına yazılır. Tick düzeyindeki
`timeseries` CSV dosyaları (9–65 MB) git'te tutulmaz; ilgili `run_*.py` betiği
aynı seed'lerle yeniden üretir. Seed özetleri, deney metaverisi ve analiz
dosyaları depodadır.

## Model kapsamı

Mevcut modelde şunlar bulunur:

- Sürekli kişilik özellikleri, ihtiyaçlar, stres, enerji, ruh hâli ve sağlık.
- Gürültülü çevre algısı, inanç güncelleme, söylenti yayılımı ve basit
  metabilişsel özdeğerlendirme.
- Small-world komşuluk ağı, güven ilişkileri, zihin modelleri ve kısmi
  ikinci-derece zihin kuramı.
- Paylaşılan kaynak havuzu, forage/share/steal eylemleri ve servet ölçümleri.
- Organik liderlik, vergi ve yeniden dağıtım, kolluk, eğitim, sağlık ve kısmi
  medya mekanikleri.
- Norm oluşumu, iki norm ekseni, davranıştan türeyen kimlikler ve nesiller
  arası basit aktarım; doğum, yaşlanma ve ölüm.
- Zaman serisi metrikleri, sosyal ağ ölçümleri, çoklu-seed deneyleri,
  karşı-olgusal karşılaştırmalar, duyarlılık ve etkileşim analizleri.

Ayrıntılı modül ve tick akışı [ARCHITECTURE.md](ARCHITECTURE.md), kod temelli
ODD+D taslağı [ODD_D.md](ODD_D.md), akademik yöntem ve deney planı
[ACADEMIC_RESEARCH_PLAN.md](ACADEMIC_RESEARCH_PLAN.md), kaynak deneyi protokolü
[EXPERIMENT_PROTOCOL_RESOURCE_STRESS.md](EXPERIMENT_PROTOCOL_RESOURCE_STRESS.md),
deney sonuç raporu [RESOURCE_STRESS_RESULTS.md](RESOURCE_STRESS_RESULTS.md),
güncelleme sırası sağlamlık raporu [SCHEDULE_ROBUSTNESS_RESULTS.md](SCHEDULE_ROBUSTNESS_RESULTS.md),
ajan-başı RNG sağlamlık raporu [AGENT_RNG_ROBUSTNESS_RESULTS.md](AGENT_RNG_ROBUSTNESS_RESULTS.md),
kimlik × kaynak faktöriyel protokolü [EXPERIMENT_PROTOCOL_IDENTITY_BY_RESOURCE.md](EXPERIMENT_PROTOCOL_IDENTITY_BY_RESOURCE.md)
ve sonuçları [IDENTITY_RESOURCE_RESULTS.md](IDENTITY_RESOURCE_RESULTS.md),
kıtlık-inancı bağlantısı ablasyon protokolü
[EXPERIMENT_PROTOCOL_SCARCITY_LINK_ABLATION.md](EXPERIMENT_PROTOCOL_SCARCITY_LINK_ABLATION.md)
ve sonuçları [SCARCITY_LINK_ABLATION_RESULTS.md](SCARCITY_LINK_ABLATION_RESULTS.md),
ihtiyaç temelli karar mimarisi protokolü
[EXPERIMENT_PROTOCOL_NEED_BASED_DECISION.md](EXPERIMENT_PROTOCOL_NEED_BASED_DECISION.md)
ve sonuçları [NEED_BASED_DECISION_RESULTS.md](NEED_BASED_DECISION_RESULTS.md),
erzak × skor ayrışımı protokolü
[EXPERIMENT_PROTOCOL_PROVISION_SCORING_FACTORIAL.md](EXPERIMENT_PROTOCOL_PROVISION_SCORING_FACTORIAL.md)
içindedir.
Aşamalı geliştirme planı [TASK_GRAPH.md](TASK_GRAPH.md) içindedir.

## Bilimsel yorum ve bilinen sınırlar

- Model katsayılarının çoğu ampirik olarak kalibre edilmemiştir. Bilimsel
  literatürden esinlenme, tek başına mekanizmanın doğrulandığı anlamına gelmez.
- Varsayılan parametre rejiminde kıtlık tavan etkisine yaklaşır; bazı sonuçlar
  başka rejimlerde değişebilir. Duyarlılık taraması parametre etkileşimlerini
  tam olarak kapsamaz.
- Bazı eski bulgular küçük örneklemli veya güven aralıksızdır; yeniden
  sınanma durumu `REVALIDATION.md` ve `KNOWN_ISSUES.md`'de belirtilir.
- Dashboard ilk dilimdir: sınırlı sayıda ajanı ve son-tick ağını gösterir;
  gerçek tarayıcıda uçtan uca görsel doğrulaması henüz tamamlanmamıştır.
- Ekonomi fiyat/emek piyasası içermez. Kültür iki basit normla sınırlıdır;
  tam iç içe geçmiş zihin kuramı ve predictive processing henüz yoktur.

Bu sınırlar, bilimsel sonuçları değerlendirirken modelin kapsamı içinde
kalınmasını sağlar; açık işler [KNOWN_ISSUES.md](KNOWN_ISSUES.md) içinde
izlenir.

## Proje yapısı

```text
ship_of_fools/
  agents/ cognition/ sociology/ information/ economy/ environment/
  institutions/ culture/ population/ simulation/ metrics/ experiments/
  visualization/ tests/
run*.py                 simülasyon ve deney giriş noktaları
ARCHITECTURE.md         gerçek modül yapısı ve tick akışı
PROJECT_CONSTITUTION.md modelleme ve geliştirme ilkeleri
TASK_GRAPH.md           yol haritası ve kalan görevler
KNOWN_ISSUES.md         açık sorunlar ve karar geçmişi
REFERENCES.md           mekanizma-kaynak eşlemesi ve kanıt notları
REVALIDATION.md         istatistiksel yeniden sınama sonuçları
requirements.txt        çalışma zamanı bağımlılıkları
```
