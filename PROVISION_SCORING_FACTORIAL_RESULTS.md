# Yenebilir Erzak × İhtiyaç Temelli Skor × Kaynak Rejimi — Sonuçlar

## Durum ve yorum düzeyi

**Koşu tamamlandı: 2026-10-09.** Protokol
(`EXPERIMENT_PROTOCOL_PROVISION_SCORING_FACTORIAL.md`) koşudan önce yazıldı ve
commit edildi (`a29ff7f`). İlk deneme sistem belleği daraldığı için özet
dosyası yazmadan durduruldu; sonuçlarına bakılmadı ve deney aynı seed'lerle
baştan koşuldu. Model içi, kuramsal/keşifsel analizdir.

## Yöntem (özet)

- 2×2 kaynak (kapasite 90/120; yenilenme 0.016/0.019) × 4 karar kolu = 16
  hücre; 30 seed bloğu (80000–80029) her hücrede; 480 simülasyon.
- Kollar: `intact`; `provisions_only` (servet yenebilir, skorlar özgün);
  `scoring_only` (skorlar ihtiyaç temelli, servet yenemez); `need_based`
  (ikisi birden).
- 80 kurucu ajan, 500 tick, sabit sıra, `agent_rng_mode="shared"`. Son 100
  tick seed içinde ortalandı. Köşeli parantezler 10.000 çekilişli seed-blok
  bootstrap %95 aralığıdır.

## Birincil sonuçlar

Kapasite ve yenilenme ana etkileri (yüksek eksi düşük), kol içinde:

| Sonuç / kontrast | `intact` | `provisions_only` | `scoring_only` | `need_based` |
|---|---:|---:|---:|---:|
| Çatışma — kapasite | −0.097 [−0.104, −0.089] | −0.096 [−0.103, −0.088] | −0.016 [−0.018, −0.014] | −0.011 [−0.013, −0.010] |
| Çatışma — yenilenme | −0.045 [−0.051, −0.039] | −0.045 [−0.050, −0.040] | −0.007 [−0.009, −0.006] | −0.005 [−0.007, −0.003] |
| İşbirliği — kapasite | +0.090 [+0.084, +0.096] | +0.091 [+0.084, +0.097] | +0.019 [+0.017, +0.021] | +0.018 [+0.015, +0.020] |
| İşbirliği — yenilenme | +0.046 [+0.040, +0.051] | +0.045 [+0.039, +0.050] | +0.009 [+0.007, +0.011] | +0.009 [+0.006, +0.011] |

Bu kontrastların karar tarafındaki 2×2 ayrışımı:

| Sonuç / kontrast | Erzak ana etkisi | Skor ana etkisi | Erzak × skor |
|---|---:|---:|---:|
| Çatışma — kapasite | +0.003 [−0.002, +0.007] | +0.082 [+0.076, +0.089] | +0.004 [−0.004, +0.012] |
| Çatışma — yenilenme | +0.001 [−0.003, +0.005] | +0.039 [+0.035, +0.043] | +0.002 [−0.007, +0.010] |
| İşbirliği — kapasite | −0.000 [−0.004, +0.004] | −0.072 [−0.077, −0.067] | −0.001 [−0.009, +0.006] |
| İşbirliği — yenilenme | −0.001 [−0.005, +0.004] | −0.036 [−0.041, −0.032] | +0.001 [−0.007, +0.010] |

Önceden yazılan kurallara göre:

- **Skor faktörü** kaynak etkisini değiştiriyor: dört kontrastta da aralık
  sıfırı dışlıyor. `intact` ile `need_based` arasındaki farkın tamamına yakını
  skor biçimine ait.
- **Erzak faktörü** bu örneklemde ayırt edilemiyor: dört kontrastta da aralık
  sıfırı kapsıyor ve nokta tahminleri skor etkisinin yirmide birinden küçük.
- **Etkileşim** aralıkları sıfırı kapsıyor; iki parça ayrı ayrı yorumlanabilir.

Protokoldeki beklenti (farkın çoğu skora ait) doğrulandı. `provisions_only`
kolunun `intact`'e yakın kalacağı beklentisi de tuttu; öngörülen küçülme
görülmedi. Erzakın skor açıkken etkisi (işareti belirsiz denmişti) küçük ve
aralığı sıfıra dayanıyor.

Tekrarlar: `intact` dördüncü bağımsız seed bloğunda −0.097 (öncekiler −0.099,
−0.101, −0.098); `need_based` ikinci blokta −0.011 (önceki −0.012).

## Manipülasyon kontrolü

Gerçek kıtlık kapasite kontrastı dört kolda −0.51 ile −0.55 arasında,
yenilenme kontrastı −0.25 ile −0.28 arasında; hepsinin aralığı sıfırı dışlıyor.
Ayrışımda erzak ve skor faktörlerinin kıtlık kontrastına etkisi sıfırı
kapsıyor. Birincil kontrastlar yorumlanabilir.

## Hücre ortalamaları

| Ölçü | Kol | 90/0.016 | 90/0.019 | 120/0.016 | 120/0.019 |
|---|---|---:|---:|---:|---:|
| `steal` payı | `intact` | 0.321 | 0.291 | 0.239 | 0.179 |
| | `provisions_only` | 0.322 | 0.291 | 0.240 | 0.181 |
| | `scoring_only` | 0.195 | 0.184 | 0.176 | 0.172 |
| | `need_based` | 0.190 | 0.182 | 0.176 | 0.173 |
| `share` payı | `intact` | 0.082 | 0.105 | 0.138 | 0.186 |
| | `provisions_only` | 0.081 | 0.103 | 0.138 | 0.187 |
| | `scoring_only` | 0.166 | 0.177 | 0.185 | 0.189 |
| | `need_based` | 0.164 | 0.176 | 0.184 | 0.189 |
| Gerçek kıtlık | `intact` | 0.997 | 0.849 | 0.553 | 0.192 |
| | `provisions_only` | 0.992 | 0.858 | 0.561 | 0.197 |
| | `scoring_only` | 0.923 | 0.692 | 0.455 | 0.133 |
| | `need_based` | 0.949 | 0.696 | 0.420 | 0.143 |
| Stres | `intact` | 0.849 | 0.777 | 0.668 | 0.525 |
| | `provisions_only` | 0.832 | 0.775 | 0.661 | 0.524 |
| | `scoring_only` | 0.625 | 0.561 | 0.534 | 0.517 |
| | `need_based` | 0.576 | 0.553 | 0.526 | 0.522 |
| Ortalama servet | `intact` | 62.0 | 57.3 | 51.6 | 49.0 |
| | `provisions_only` | 58.9 | 55.8 | 51.7 | 48.8 |
| | `scoring_only` | 41.6 | 45.9 | 46.8 | 48.8 |
| | `need_based` | 37.1 | 44.0 | 46.3 | 48.4 |
| Gini | `intact` | 0.420 | 0.407 | 0.412 | 0.435 |
| | `provisions_only` | 0.435 | 0.413 | 0.418 | 0.431 |
| | `scoring_only` | 0.447 | 0.441 | 0.437 | 0.421 |
| | `need_based` | 0.457 | 0.441 | 0.434 | 0.429 |
| Nüfus | `intact` | 93.0 | 106.4 | 113.2 | 118.9 |
| | `provisions_only` | 95.2 | 107.6 | 114.4 | 119.1 |
| | `scoring_only` | 111.7 | 116.5 | 119.7 | 117.1 |
| | `need_based` | 114.9 | 116.5 | 117.8 | 118.2 |

## İkincil keşifsel sonuçlar

Kapasite kontrastının ayrışımı:

| Ölçü | Erzak ana etkisi | Skor ana etkisi |
|---|---:|---:|
| Ortalama servet | +2.5 [+1.6, +3.4] | +13.6 [+12.5, +14.8] |
| Gini | −0.006 [−0.015, +0.002] | −0.021 [−0.030, −0.014] |
| Stres | +0.017 [+0.004, +0.029] | +0.159 [+0.144, +0.175] |
| Nüfus | −1.5 [−3.6, +0.6] | −12.5 [−15.3, −9.6] |
| Ortalama güven | −0.001 [−0.002, +0.000] | −0.030 [−0.031, −0.028] |
| `forage` payı | −0.001 [−0.002, +0.001] | +0.023 [+0.021, +0.025] |

**Önceki raporun düzeltilmesi.** `NEED_BASED_DECISION_RESULTS.md`'de servetin
ve Gini'nin kaynak rejimine tepkisinin işaret değiştirmesini "servet yendiği
için" diye yorumlamış ve bunu ISSUE-014'ün veride görünen hâli saymıştım. Bu
deney o yorumu desteklemiyor: işaret değişimi servetin yenemediği
`scoring_only` kolunda da var (servet kapasite etkisi +4.0), servetin yendiği
ama skorların özgün kaldığı `provisions_only` kolunda yok (−7.1). Değişim
ağırlıkla skor biçimine ait; erzakın payı servet için küçük (+2.5), Gini için
ayırt edilemiyor. Nüfusun kıtlığa dayanıklılığı da skora ait. O rapora
düzeltme notu eklendi.

## Erzak neden etkisiz? (keşifsel tanı)

Protokol dışı küçük bir tanı koşusu (iki uç kaynak hücresi × 3 kol × 5 seed,
seed 90000–90004, son 100 tick; yeni `avg_min_need` ve `need_deficit_rate`
metrikleriyle):

| Hücre | Kol | Gerçek kıtlık | Ortalama en düşük ihtiyaç | İhtiyacı 0.4 altında olan pay |
|---|---|---:|---:|---:|
| 90/0.016 | `intact` | 0.998 | 0.798 | 0.039 |
| 90/0.016 | `provisions_only` | 0.967 | 0.806 | 0.019 |
| 90/0.016 | `scoring_only` | 0.862 | 0.769 | 0.075 |
| 120/0.019 | `intact` | 0.157 | 0.861 | 0.002 |
| 120/0.019 | `provisions_only` | 0.205 | 0.859 | 0.001 |
| 120/0.019 | `scoring_only` | 0.066 | 0.855 | 0.004 |

Gerçek kıtlığın tavanda (≈1.0) olduğu hücrede ajanların ortalama en düşük
ihtiyacı 0.80 ve yalnızca %4'ü 0.4 eşiğinin altında. Ajanlar "azami kıtlıkta"
bile toktur; erzak yenmiyor çünkü yemeyi tetikleyen açlık nadiren oluşuyor.

Bunun nedeni ölçünün tanımıdır: `true_scarcity = 1 − stok/kapasite`
(`economy/resources.py`), yani depo doluluğunu ölçer, yoksunluğu değil.
Varsayılan değerlerle kaba hesap: kapasite 90 × 80 = 7200 ve yenilenme 0.016
ile her tick ~115 birim yiyecek gelir; ihtiyaç bozunumu 0.03/tick ve toplama
verimi 10 birim = 1.0 ihtiyaç olduğundan 100 ajanı doyurmak için ~30 birim
yeter. Akış ihtiyacın birkaç katıdır. Depo yine de boşalır, çünkü bir toplama
5–12 birim alır ve ihtiyaç 1.0'da kırpılır; fazlası kaybolur. Bu,
ISSUE-006'daki "kimse açlıktan ölmüyor" gözlemiyle uyumludur. Ayrıntı ve
sonuçları ISSUE-015'te.

Bu tanı 5 seed'lik keşifsel bir bakıştır; hesap ise koddan türetilmiştir.

## Sonuç

1. `need_based` mimarisinin kaynak → çatışma ilişkisini küçültmesi skor
   biçiminden geliyor; servetin yenebilir olması bu modelde davranışı
   değiştirmiyor.
2. Servetin hiçbir ihtiyacı karşılamaması (ISSUE-014) yapısal olarak doğru,
   ama pratik önemi sanıldığından düşük: ajanlar zaten aç kalmıyor.
3. Asıl mesele bir üst katmanda: modeldeki "kıtlık" bir depo göstergesidir
   ve ajanların davranışını etkilediği tek yol bu göstergeye dair inançtır.
   Kaynak deneylerinin tamamı "ajanlar depoyu boş sandığında ne yapar"
   sorusunu yanıtlıyor, "ajanlar aç kaldığında ne yapar" sorusunu değil.

## Yorum sınırları

- Önceki protokoldeki sınırlar geçerli: kollar aynı kıtlık düzeyinde çalışmaz;
  toplamada kütle korunumu tam değil; dış veriyle kalibrasyon yok.
- Erzakın etkisizliği `provision_eat_threshold=0.4` değerine özgü olabilir;
  daha yüksek bir eşik sınanmadı.
- Seed bootstrap seed belirsizliğini özetler; model belirsizliğini kapsamaz.

## Tekrar üretim dosyaları

- Protokol ve komutlar: `EXPERIMENT_PROTOCOL_PROVISION_SCORING_FACTORIAL.md`.
- `output/provision_scoring_factorial/experiment.json`, `analysis.json`
  (`arm_factorial` anahtarı ayrışımı içerir), `seed_summaries.csv` (480 satır);
  `timeseries.csv` git dışında.
