# Kirjakatalogi

Sovelluksen avulla käyttäjät voivat pitää kirjaa lukemistaan kirjoista, arvostella niitä ja saada tilastoja luetuista kirjoista. Käyttäjät ovat peruskäyttäjiä tai ylläpitäjiä.

### Sovelluksen suunniteltuja ominaisuuksia
+ Käyttäjä voi
  + luoda uuden tunnuksen
  + kirjautua sisään (ja ulos)
  + hakea kirjoja esim. nimen ja kirjailijan perusteella
  + merkitä kirjoja luetuiksi
  + tarkastella tilastoja lukemistaan kirjoista (kirjojen määrä, yleisimmät genret tms.)
  + arvostella kirjoja
  + lukea muitten käyttäjien arvosteluja
  + tarkastella muitten käyttäjien tilastoja
+ Ylläpitäjä voi
  + Lisätä uusia kirjoja ja niiden tietoja (esim. sivumäärä, genre, kirjailijat)
  + Poistaa käyttäjien arvosteluja

### Tällä hetkellä toimii
+ Henkilö voi luoda uuden käyttäjän
  + Käyttäjänimi saa olla 1-30 merkkiä pitkä, salasana vähintään 1 merkkiä, eikä samannimisiä käyttäjiä voi luoda
+ Käyttäjä voi kirjautua sisään
  + Käyttäjänimen ja salasanan oltava oikein
+ Käyttäjä voi lisätä uuden kirjan (admin-roolia ei eritelty)
  + Kirjan tai kirjailijan nimi ei saa olla liian pitkä, vuoden ja sivumäärän oltava numeroarvoja
+ Käyttäjä näkee lisätyt kirjat listana ja voi klikata niiden sivulle
+ Käyttäjä voi merkitä kirjan luetuksi / poistaa sen luetuista
