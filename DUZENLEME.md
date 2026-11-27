# Siteyi düzenleme

Sitedeki yazılar, listeler ve fotoğraflar `content/` klasöründeki dosyalarda durur. Bunları kod görmeden **Pages CMS** panelinden değiştirebilirsiniz.

## İlk kurulum (bir kez)

1. https://app.pagescms.org adresine gidin ve **Sign in with GitHub** ile GitHub hesabınızla girin.
2. Pages CMS, GitHub uygulamasını kurmanızı ister. **Only select repositories** seçin, `plant-biogeography` deposunu işaretleyin ve onaylayın.
3. Panelde `canalkan00/plant-biogeography` deposunu ve `main` dalını açın.

## Düzenleme

- Soldaki menüden bölümü seçin: Ana sayfa, Hakkımızda, Barış Özüdoğru profili, Araştırma konuları, Projeler, Yayınlar, Tezler, Ekip, İletişim, Fotoğraflar.
- Her yazının **İngilizce** ve **Türkçe** kutusu ayrıdır.
- Listelere **Add an entry** ile yeni öğe eklenir. Öğeler sürüklenerek sıralanır, çöp kutusu simgesiyle silinir.
- **Save** düğmesine bastığınızda değişiklik GitHub'a kaydedilir. Site 1–2 dakika içinde güncellenir.

## Yazım kuralları

- İtalik için kelimeyi yıldız içine alın: `*Noccaea aucheri*`
- Kalın için çift yıldız kullanın: `**kalın**`
- Bağlantı için: `[görünen yazı](https://adres)`
- Uzun metinlerde (Hakkımızda, biyografi) paragraflar arasında boş satır bırakın.
- Yazar listelerinde "Özüdoğru B." kendiliğinden kalın yazılır.
- Yayınlar ve tezler yıla göre kendiliğinden sıralanır. Sayılar, filtre etiketleri ve yıl çubukları da kendiliğinden hesaplanır.

## Fotoğraflar

Telefondan çekilmiş büyük fotoğrafları doğrudan yükleyebilirsiniz. Site, sayfalar için küçültülmüş kopyaları kendisi hazırlar (`img/sized/`). Ekip üyelerinde fotoğraf yoksa harita deseni ve baş harfler gösterilir.

## Bir şey ters giderse

Her kayıttan sonra site otomatik olarak kontrol edilir. Kontrolden geçemeyen bir değişiklik yayınlanmaz ve GitHub size e-posta gönderir. O durumda eski site yayında kalır. Hatalı değişikliği panelden düzeltip yeniden kaydetmeniz yeterli. Bütün değişiklikler GitHub'da kayıtlıdır ve geri alınabilir.

## Panelden değiştirilemeyenler

Renkler, yerleşim, menü, bölüm başlıkları, logo ve rölyef animasyonu `templates/site.html` dosyasındadır. Bunlar için kod değişikliği gerekir.
