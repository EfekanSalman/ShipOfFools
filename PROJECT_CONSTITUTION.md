# PROJECT CONSTITUTION — Ship of Fools

Bu proje AI orkestrasyonuyla geliştiriliyor: araştırma, mimari, kodlama ve
review farklı "rollerde" ilerliyor (bkz. doc 4). Bu dosya o rollerin hepsinin
uyması gereken sabit kuralları tanımlıyor. Yeni bir özellik eklenirken önce
bu kurallara karşı kontrol edilmeli.

1. **Emergence > scripting.** Davranış kişilik + ihtiyaç + stres + inançların
   etkileşiminden ortaya çıkmalı; "eğer X ise Y yap" tipi sabit kurallarla
   zorlanmamalı.
2. **Sabit etiket yok.** Hiçbir agent koda "aptal", "akıllı", "iyi", "kötü"
   olarak yazılmaz. `Agent.foolishness` gibi türetilmiş metrikler zamana
   bağlı durumlardır, kimlik değildir.
3. **Gerçeklik ≠ agent'ın inancı.** Her agent kendi (yanlış olabilen)
   dünya modeline sahip olmalı; hiçbir agent global state'e doğrudan erişmez,
   yalnızca `_perceive_and_update_beliefs` üzerinden gürültülü/yanlı gözlem alır.
4. **Bilimsel iddialar belgelenmeli.** Nörobilim/psikolojiden esinlenen her
   mekanizma şunu içermeli: (a) hangi fenomeni temsil ediyor, (b) neden dahil
   edildi, (c) hangi basitleştirme yapıldı, (d) basitleştirmenin sınırları.
   Bu proje beynin biyolojik olarak doğru bir modeli olduğunu iddia etmez.
5. **ML her yere zorlanmaz.** Basit utility/softmax gibi yöntemler yeterliyse
   derin öğrenme eklenmez (V0 `cognition/decision.py` buna örnek).
6. **Reprodüksiyon zorunlu.** Aynı kod, konfigürasyon ve seed aynı model
   yörüngesini üretmeli. Rastgele akış tasarımı açıkça belgelenmeli: varsayılan
   ortak `Simulation.rng` veya deneysel ajan-başı akışlar. Metrik örneklemesi
   gibi model dışı rastgele yardımcı işler ayrı, belgeli seed/akış kullanmalı
   ve simülasyonun RNG dizisini tüketmemeli.
7. **Tek koşuya güvenme.** Deneysel sonuçlar (`experiments/runner.py`)
   birden çok seed üzerinden dağılım (mean/std) olarak raporlanmalı, tek bir
   koşunun sonucu "kanıt" sayılmaz. Aynı seed ile iki farklı konfigürasyonu
   başlatmak tek başına ortak rastgelelik / eşleşmiş deney sağlamaz: koşulların
   farklı dalları RNG çekilişlerini farklı hizaya sokabilir. Eşleşmiş çıkarım
   öncesinde kullanılan RNG tasarımı açıklanmalı ve doğrulanmalıdır
   (`ODD_D.md`, `ACADEMIC_RESEARCH_PLAN.md`).
8. **"İyi toplum" hedefi yok.** Sistem hiçbir konfigürasyonu "en iyi" olarak
   işaretlemez; yalnızca stability, cooperation, inequality, trust gibi
   ölçülebilir metrikleri raporlar. Değer yargısı kullanıcıya bırakılır.
9. **Her alt sistem test edilir.** Yeni bir mekanizma eklenirken
   `tests/` altına en az bir sanity testi eklenmeli.
10. **Mimari kararlar belgelenir.** Yeni bir katman/mekanizma eklerken
    `ARCHITECTURE.md` ve `TASK_GRAPH.md` güncellenmeli.
