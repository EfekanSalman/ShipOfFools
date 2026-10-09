# Akademik Araştırma ve Simülasyon Planı

Bu belge, Ship of Fools'u araştırma amaçlı ajan tabanlı simülasyon olarak
geliştirmek için kullanılacak yöntemleri, öncelikleri ve önerilen ilk çalışmayı
toplar. Bu plan, modelin gerçek insan davranışını şimdiden doğruladığı anlamına
gelmez. Mevcut model öncelikle kuramsal mekanizmaları ve yapay dünyadaki
sonuçlarını inceleyen bir araştırma aracıdır.

## 1. Akademik çerçeve

### Modelin iddia düzeyi

Çalışmanın her aşamasında şu ayrım korunacak:

- **Kod doğrulaması (verification):** Kod, amaçlanan kuralları uyguluyor mu?
- **Kavramsal doğrulama:** Seçilen mekanizmalar araştırma sorusu ve dayandığı
  teorilerle tutarlı mı?
- **Davranışsal değerlendirme:** Modelin ürettiği örüntüler beklenen veya
  gözlenen örüntülerle uyuşuyor mu?
- **Ampirik kalibrasyon/doğrulama:** Parametreler gerçek veriye göre seçildi
  mi; sonuçlar kullanılmayan veri ya da bağımsız bir örüntüyle sınandı mı?

Bir aşamadaki başarı diğer aşamaların kanıtı sayılmaz. Model gerçek veriye
bağlanmadıkça sonuçlar “gerçek toplumda böyle olur” biçiminde sunulmayacak;
“bu varsayımlar altındaki modelde gözlendi” diye raporlanacak.

### Model dokümantasyonu: ODD ve ODD+D

Mevcut kod, ODD (Overview, Design concepts, Details) yapısında başkalarının
yeniden kurabileceği açıklıkta belgelenmeli. ODD; amaç, ajan/durum değişkenleri
ve ölçekler, süreç sırası, tasarım kavramları, başlangıç, girdiler ve alt
modelleri kapsar. İnsan kararları içerdiğimiz için ODD+D'nin karar vericiler,
seçenekler, karar süreci, öğrenme ve bilgi varsayımlarına ilişkin soruları da
uygulanmalı.

Belgelenecek somut konular:

- Bir ajan hangi bilgiyi gerçekten görür, neyi yalnızca hatalı inanç olarak
  taşır?
- Her kararın seçenekleri, skorları/olasılıkları ve parametreleri nelerdir?
- Hangi süreç hangi sırada, hangi ajan kümesi üzerinde işler?
- Ajanlar öğreniyor veya uyum sağlıyorsa tam olarak hangi değişken güncellenir?
- Başlangıç nüfusu, yaşları, kaynak düzeyleri ve ağ nasıl kurulur?
- Her mekanizma hangi teoriye dayanır; hangi kısımları tasarım varsayımıdır?

### Örüntü odaklı değerlendirme

Tek bir genel skorla “model geçerli” demek yerine, araştırma sorusuyla ilgili
birkaç gözlenebilir örüntü önceden seçilmeli. Mümkünse farklı düzeylerde
örüntüler birlikte ele alınmalı (ajan davranışı, ağ/kurum, nüfus veya zaman
serisi). Alternatif mekanizmalar da aynı örüntüyü üretiyor mu diye
karşılaştırılmalı. Hedef örüntü ve veri yoksa, sonuç kuramsal/keşifsel olarak
sınıflandırılmalı; ampirik doğrulama iddiası yapılmamalı.

## 2. Mevcut koşudan başlangıç gözlemi

Varsayılan konfigürasyonda (80 ajan, 500 tick, seed 42) çalıştırılan tek koşuda:

- `true_scarcity` 300. tick'te 1.0'a ulaştı ve koşunun sonuna kadar tavanda
  kaldı.
- Stres yükseldi; güven hafif pozitif başlangıç değerinden negatife indi.
- İşbirliği başlangıca göre düştü; çatışma ve Gini yükseldi.
- Nüfus 102'ye kadar çıkıp 76'ya indi.

Bu yalnızca **bir konfigürasyon ve seed için betimleyici bir gözlem**; genellenen
bulgu değildir. Varsayılan kıtlık tavanı, daha fazla araştırma öncesi ele
alınması gereken rejim/duyarlılık sorunudur (ayrıca `KNOWN_ISSUES.md`
ISSUE-011/012).

### İlk kıtlık rejimi pilotu (2026-10-04)

`run_regime_calibration.py` ile 80 ajan, 400 tick, son 100 tick analizi ve 16
parametre birleşimi (kapasite 75/90/105/120 × regen 0.010/0.013/0.016/0.019)
koşturuldu. Her hücre 4 ayrı seed aldı; adaylar için seed aralıkları
birbirinden ayrıdır (10000–10063). Önceden belirlenen ölçüt: ortalama kıtlık
0.30–0.60 ve analiz penceresindeki tick'lerin en fazla %10'unda kıtlık ≥0.98.

| Kapasite/ajan | Food+water regen | Son pencere kıtlık ort. ± seedler arası SD | Tavanda tick payı | Ölçüt |
|---:|---:|---:|---:|---|
| 90 | 0.019 | 0.515 ± 0.088 | 0.0% | uygun |
| 120 | 0.016 | 0.337 ± 0.151 | 0.0% | uygun |
| 105 | 0.016 | 0.579 ± 0.228 | 0.0% | uygun |

Kıtlık ölçütüne göre ilk aday **kapasite 90, regen 0.019** oldu. İşbirliği ve
çatışma oranları çıktı dosyasında keşifsel olarak raporlandı; sıralamayı
etkilemedi. Dört seed yalnızca ön tarama için yeterlidir, bu aday kalibre
edilmiş nihai ayar değildir. Tam sonuç:
`output/regime_calibration_pilot.json`.

**Sonraki adım:** bu ilk aday ve en az bir uygun alternatif, daha geniş ve
birbirinden bağımsız yeni pilot seed bloklarında tekrar incelendi. 2026-10-04'te
2×2 takip taraması (80 ajan, 500 tick, son 100 tick, her hücrede 20 seed;
seed blokları 20000–20079) yapıldı:

| Kapasite/ajan | Regen | Kıtlık ort. ± seedler arası SD | Seed ortalaması hedef bantta | Tavanda tick payı | Ölçüt |
|---:|---:|---:|---:|---:|---|
| 120 | 0.016 | 0.582 ± 0.189 | 11/20 (55%) | 4.1% | ortalama/tavan ölçütü geçti |
| 120 | 0.019 | 0.232 ± 0.179 | 8/20 (40%) | 0.0% | ortalama hedefin altında |
| 90 | 0.019 | 0.853 ± 0.136 | 1/20 (5%) | 35.9% | kıtlık yüksek/tavan fazla |
| 90 | 0.016 | 0.989 ± 0.032 | 0/20 (0%) | 89.2% | kıtlık tavana yapışık |

Önemli sonuç: ilk pilotta öne çıkan `90 / 0.019` ayarı yeni seed bloğunda
orta kıtlığı **tekrarlamadı**. `120 / 0.016` ayarı 20-seed ortalamasında hedef
bandın içinde ve tavan payı düşük olsa da seedlerin yalnızca 11/20'sinde
son-pencere ortalaması hedef bandına girdi; seedler arası değişkenlik yüksek.
Dolayısıyla henüz güvenilir/kararlı bir orta rejim bulmuş değiliz. Bu, aday
seçimini tek ortalamaya dayandırmamak ve run-to-run değişkenliği araştırma
sonucunun parçası olarak ele almak gerektiğini gösteriyor.

Tam sonuç: `output/regime_calibration_confirmation.json`. Coop/conflict
kolonları keşifseldir ve rejim sıralamasına katılmamıştır. Karar: daha geniş
kalibrasyonla tek bir istikrarlı orta kıtlık ayarı aramayı zorlamıyoruz. Bunun
yerine kapasite×yenilenme faktöriyel koşullarını sabitleyip kaynak rejimlerinin
sonuç dağılımına etkisini sınayacağız. Ayrıntılı protokol
`EXPERIMENT_PROTOCOL_RESOURCE_STRESS.md` içindedir.

## 3. Çalışma ilkeleri

1. **Önce soru, sonra özellik:** Yeni alt sistem eklemeden önce hangi araştırma
   sorusuna ve ölçülebilir hipoteze hizmet ettiğini yaz.
2. **İddia ve kanıtı ayır:** Simülasyon içi örüntü, ampirik veriyle uyum ve
   nedensellik ayrı iddialardır.
3. **Mekanizmaları gerekçelendir:** Kaynak, teori, basitleştirme ve sınırı her
   mekanizma için kaydet; kaynak bulunamadığında bunu açıkça “tasarım varsayımı”
   diye işaretle.
4. **Model katmanlarını ayrı değerlendir:** Kod doğruluğu, mekanizma davranışı,
   tüm-model örüntüleri ve ampirik karşılaştırma ayrı aşamalardır.
5. **Birden çok örüntü ve koşu kullan:** Seed dağılımını raporla. Seed sayısını
   sabit bir sihirli eşik olarak seçme; belirsizlik aralığı veya önceden
   belirlenen hassasiyet hedefi yeterli olana kadar gerekçelendir.
6. **Kalibrasyon ve değerlendirme koşularını ayır:** Parametre/rejim seçerken
   kullanılan seed'leri nihai hipotez sınamasında tekrar kullanma.
7. **Alternatif yapıları sınama:** Sonuç yalnızca katsayıları değiştirmeye değil,
   makul alternatif karar kurallarına/ağ yapılarına da dayanıyor mu incele.
8. **Tekrar üretim bilgisini sakla:** Kod sürümü, parametreler, seed'ler,
   Python/bağımlılık sürümleri, deney tanımı, ham sonuç ve analiz özeti birlikte
   saklansın.
9. **Sonuç yönüne göre katsayı ayarlama:** İstenilen hipotezi desteklemek için
   mekanizma katsayılarını sonradan zorlama; ayarlama araştırma sorusuna göre
   gerekçelendirilmeli ve ayrı veride sınanmalı.

## 4. Kritik teknik konu: seed eşleştirme

Simülasyon tek bir `Simulation.rng` akışını birçok süreçte kullanıyor. İki
koşul aynı seed ile başlasa bile, koşullar farklı davranışlar üretince rastgele
çekiliş sayıları ve sıraları ayrışabilir. Bu nedenle `run_paired_counterfactual`
aynı seed kullanıyor olsa da, seed eşleşmesinin tick boyunca ortak rastgele
şokları garanti ettiği varsayılmamalı.

Eşleşmiş tasarım kullanmadan önce şu seçeneklerden biri değerlendirilip
belgelenmeli:

- Her koşulda bağımsız seed'ler kullanıp koşul farkını seed dağılımlarıyla
  karşılaştırmak.
- Ortak rastgele sayılar gerekiyorsa süreç/ajan/tick bazlı bağımsız RNG
  akışları veya anahtarlı deterministik rastgele çekiliş tasarlamak; bunun
  mevcut tekrar üretilebilirlik kayıtlarıyla uyumunu sınamak.

Hangi tasarım seçilirse seçilsin, RNG düzeni ve sürümü deney çıktısına yazılmalı.

## 5. Önerilen araştırma soruları

### A. Kaynak baskısı, işbirliği ve çatışma — önerilen ilk çalışma

**Araştırma sorusu:** Kaynak kıtlığı, modelin tanımlı koşullarında işbirliği ve
çatışma örüntülerini nasıl değiştiriyor? Bu ilişki doğrusal mı; başlangıçtaki
güven/ağ yapısına veya kurumsal koşullara bağlı mı?

**Neden ilk sırada:** Kaynak havuzu, stres, eylem seçimi ve nüfus dinamikleri
mevcut motorda birbirine bağlı. Pilotlar seed'ler arasında rejim farkı
gösterdiğinden araştırma yalnızca sabit bir “orta kıtlık” seviyesi aramayacak;
kapasite/yenilenme koşullarının sonuç dağılımlarını ve etkileşimini ölçecek.

**İlk aşamada ölçülecekler:** `true_scarcity`, stres, cooperation/conflict
rate, güven, eşitsizlik, nüfus ve ölümler. Son tick değeriyle yetinilmeyip
önceden tanımlı bir son dönem penceresi ve tam zaman serisi raporlansın.

**Önemli tasarım kuralı:** Kaynak parametreleri araştırma koşulları olarak
belirlenir; koşul sonuçları görülünce hedef işbirliği/çatışma değerleri elde
etmek için yeniden ayarlanmaz. Pilot seed'leri final analizine katılmaz.

### B. Gerçek ve algılanan kurumsal meşruiyet

Kurumun gerçek meşruiyeti ile ajanların inancı arasındaki fark davranışları ve
kurumun devamlılığını nasıl etkiliyor? Önce kurumsal değişkenlerin ölçüm ve
mekanizma zinciri netleştirilmeli; liderliğin nadiren oluşması tasarımda hesaba
katılmalı.

### C. Kimlik pekişmesi, ağ yapısı ve güven

Davranıştan oluşan kimliklerin güven ilişkileri ve ağ kümelenmesiyle bağı nedir?
Mevcut kimlik geri beslemesi ve ağ metrikleri başlangıç sağlayabilir; alternatif
kimlik oluşum kuralları ve yeterli örneklem gerekir.

### D. Kurumlar, kıtlık ve dağıtım

Vergi/yeniden dağıtım veya kolluk hangi kaynak rejimlerinde sonuçları
değiştiriyor? Bunu sınamadan önce liderlik/meşruiyet oluşumunu ve müdahalenin
hangi ajanlara ne zaman uygulandığını açık biçimde tanımlamak gerekir.

## 6. Önerilen aşamalı yol haritası

**İlerlemenin durumu:** ODD+D ilk kod-temelli taslağı eklendi; aynı-seed
tekrar-üretilebilirlik kontrolü geçti; 16-hücre ilk taraması ve 20-seed 2×2
takip taraması yapıldı. Tekrarlanabilir “orta rejim” bulunmadığı için, seed
dağılımını sonuç olarak ele alan 2×2 final deney protokolü uygulandı ve final
koşu tamamlandı. Sonuçlar `RESOURCE_STRESS_RESULTS.md`'de.

### Aşama 1 — Araştırma kapsamı ve model tarifi

- İlk soru (kaynak baskısı → işbirliği/çatışma) ve kuramsal/keşifsel başlangıç
  çerçevesi seçildi.
- `ODD_D.md` oluşturuldu: mevcut kodu ve insan karar mekanizmalarını ODD+D
  başlıklarında, gerçek uygulamayı esas alarak belgeleyelim.
- Mevcut `REFERENCES.md` kaynaklarını ve “tasarım tercihi” olan noktaları
  mekanizma bazında ODD+D'ye bağlayalım.

### Aşama 2 — Kod doğrulaması ve tekrar üretim

- Aynı konfigürasyon/seed ile tam metrik yörüngesinin aynı olduğu test edildi.
- Faktöriyel analiz fonksiyonu, bilinen 2×2 kontrastlar ve küçük CLI koşusu
  smoke-test edildi.
- Tam `test_basic.py` koşusu ilk ortamda SciPy bulunmadığı için tamamlanamamıştı.
  2026-10-07'de SciPy kurulu ortamda tüm test paketi geçti (Python 3.14).
- Sınır değerleri, nüfus/kaynak/olasılık değişmezlerini ve önemli süreç
  sırasını kapsayan testleri belirle.
- Seed eşleştirme tasarımını karara bağla; deney çıktısı şemasını sabitle.

### Aşama 3 — Kıtlık rejimi kalibrasyonu

- İlk tarama ve 20 seed/hücrelik 2×2 takip yapıldı; orta kıtlık adaylarının
  seedler arasında kararlı olmadığı görüldü.
- Kararı: tek bir “orta” konfigürasyonu zorla seçmiyoruz; 90/120 kapasite ve
  0.016/0.019 yenilenme düzeylerini final deney koşulları olarak sabitliyoruz.
- Pilot ve final seed'leri ayrıldı; parametre, seed, özet ve zaman serisi
  makinece okunabilir dosyalara yazılır.

### Aşama 4 — Önceden tanımlı deney

- `EXPERIMENT_PROTOCOL_RESOURCE_STRESS.md` protokolü yazıldı; 2×2 koşullar,
  hipotezler, birim (seed), metrik penceresi ve bootstrap kontrastları
  tanımlandı.
- Final deney tamamlandı: 30 seed/hücre; bootstrap %95 GA. 30 seed
  evrensel bir yeterlilik garantisi değildir; seed düzeyindeki belirsizlik
  sonuç raporunda gösterilmiştir.
- Sonuç tabloları, seed dağılımı ve yorum sınırları
  `RESOURCE_STRESS_RESULTS.md` içinde; ham JSON ve CSV dosyaları
  `output/resource_factorial/` içinde.

### Aşama 5 — Yapısal sağlamlık ve paylaşım

- Temel sonucu makul alternatif parametre rejimi ve mekanizma seçimiyle
  sınamayı planla.
- Kurulum, komut satırı arayüzü, veri sözlüğü ve ODD+D dokümanını tekrar
  üretilebilir şekilde tamamla.
- Daha sonra uygun görülürse CoMSES Net gibi hesaplamalı model arşivlerinin
  dokümantasyon ve paylaşım standartlarına göre yayın hazırlığı yap.

## 7. Karar kaydı ve sonraki sorular

Başlangıç kararları verildi ve ilk kodlama dilimi tamamlandı:

- İlk araştırma odağı: **kaynak kapasitesi/yenilenmesi → işbirliği ve çatışma**.
- İlk iddia düzeyi: **kuramsal/keşifsel model içi analiz**.
- Karar: seed'ler arası orta kıtlık istikrarsız olduğu için final deney, bir
  tek orta rejime değil 2×2 kaynak koşullarındaki sonuç dağılımlarına bakacak.
- İlk uygulama: ODD+D belgesi, seed tekrarlanabilirlik kontrolü, rejim pilot
  kalibratörü, protokol ve faktöriyel deney çalıştırıcısı hazırlandı.

Güncelleme sırası sağlamlık analizi tamamlandı: aynı 120 seed-koşul çifti
karıştırılmış ajan sırasıyla çalıştırıldı. Dokuz birincil faktöriyel etki
farkının bootstrap aralıkları sıfırı kapsadı ve kapasite/yenilenme etkilerinin
yönleri aynı kaldı. Bu eşdeğerlik kanıtı değildir; seed eşleştirmesi tam ortak
rastgele sayı tasarımı değildir. Ardından 240 koşuluk takipte eylem RNG
akışları ajan başına ayrıldı ve aynı karşılaştırma yinelendi; birincil
kontrastlar yine yönünü korudu. Ayrıntılar `SCHEDULE_ROBUSTNESS_RESULTS.md` ve
`AGENT_RNG_ROBUSTNESS_RESULTS.md` içinde. `shared` mevcut varsayılan olarak
kalır; araştırma için hangi modun tercih edileceği ayrı yöntem kararıdır.
Sonraki takipte eski `identity_feedback_strength` bulgusu 2×2 kaynak
koşullarıyla çaprazlandı (0.0/0.5; 30 eş seed bloğu/hücre). Güven ve çatışma
etkileri tüm rejimlerde aynı yönde çıktı; çatışma artışı ve işbirliği düşüşü
düşük kapasitede daha büyüktü. Yöntem `EXPERIMENT_PROTOCOL_IDENTITY_BY_RESOURCE.md`,
sonuçlar `IDENTITY_RESOURCE_RESULTS.md` içinde. Bu analiz de model içidir;
ara doz ve mekanizma ayrıştırması açık iştir.
Tam test paketi 2026-10-07'de SciPy kurulu ortamda yeniden çalıştırıldı ve geçti.

2026-10-07 incelemesi: kaynak ve kimlik deneylerinin birincil sonuçları karar
formülündeki doğrudan terimlere bağlıdır (`steal`/`share` skorlarında
`scarcity_belief`; `opportunist` etiketinde `steal` bonusu) — ISSUE-013. İlke 7
ve Aşama 5 kapsamında doğrudan bağlantıyı kesen 2×2×3 ablasyon deneyi
protokolle (`EXPERIMENT_PROTOCOL_SCARCITY_LINK_ABLATION.md`) koşuldu; sonuçlar
`SCARCITY_LINK_ABLATION_RESULTS.md` içinde. Kimlik deneyinin etiket/eylem
dağılımı post hoc olarak çıkarıldı (`IDENTITY_RESOURCE_RESULTS.md` eki).

2026-10-09: alternatif, ihtiyaç temelli karar mimarisi (ISSUE-014) 2×2×2
protokolle sınandı (`NEED_BASED_DECISION_RESULTS.md`). Kaynak → çatışma
ilişkisi aynı yönde ama yaklaşık sekizde bir büyüklükte çıktı. Üç deney
birlikte, bu ilişkinin büyüklüğünün karar kuralı varsayımına bağlı olduğunu
gösteriyor; raporlanacak ana sonuç bu yapısal belirsizliktir.

2026-10-09 (devam): erzak × skor ayrışımı farkın skor biçimine ait olduğunu
gösterdi (`PROVISION_SCORING_FACTORIAL_RESULTS.md`). `true_scarcity`'nin depo
doluluğunu ölçtüğü, ajanların tavanda bile tok olduğu (ISSUE-015) ve sabit
ajan sırasının kıtlıkta kimliğe göre öncelik ürettiği (ISSUE-016) bulundu.
Karıştırılmış sırayla kurulan gerçek yoksunluk deneyinde
(`DEPRIVATION_RESULTS.md`) yoksunluğun çatışma ölçüsüne etkisinin yönü karar
kuralına göre ters çıktı. Ana sonuç genişledi: kıtlık → çatışma ilişkisi hem
kıtlığın inanç mı yoksunluk mu olduğuna hem karar kuralına bağlıdır.

## Kaynaklar

- Grimm et al. (2020), “The ODD Protocol for Describing Agent-Based and Other
  Simulation Models”: <https://doi.org/10.18564/jasss.4259>
- Müller et al. (2013), “Describing human decisions in agent-based models —
  ODD+D”: <https://doi.org/10.1016/j.envsoft.2013.06.003>
- Grimm et al. (2005), “Pattern-Oriented Modeling of Agent-Based Complex
  Systems”: <https://doi.org/10.1126/science.1116681>
- Windrum, Fagiolo & Moneta (2007), “Empirical Validation of Agent-Based
  Models: Alternatives and Prospects”: <https://jasss.soc.surrey.ac.uk/10/2/8.html>
- CoMSES Net, model and documentation standards:
  <https://www.comses.net/resources/standards/>
