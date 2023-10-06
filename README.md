# Kirjakatalogi

Sovelluksen avulla käyttäjät voivat pitää kirjaa lukemistaan kirjoista, arvostella niitä ja saada tilastoja luetuista kirjoista. Käyttäjät ovat peruskäyttäjiä tai ylläpitäjiä.

### Sovelluksen suunniteltuja ominaisuuksia
_Tällä hetkellä toimivat raksitettu_
+ Käyttäjä voi
  + [X] luoda uuden tunnuksen
  + [X] kirjautua sisään (ja ulos)
  + [X] hakea kirjoja esim. nimen ja kirjailijan perusteella
  + [X] merkitä kirjoja luetuiksi
  + [X] tarkastella tilastoja lukemistaan kirjoista (kirjojen määrä, yleisimmät genret tms.)
  + [X] arvostella kirjoja
  + [X] lukea muitten käyttäjien arvosteluja
  + [X] tarkastella muitten käyttäjien tilastoja
+ Ylläpitäjä voi
  + [X] Lisätä uusia kirjoja ja niiden tietoja (esim. sivumäärä, genre, kirjailijat)
  + [X] Poistaa käyttäjien arvosteluja

### Käynnistysohjeet
1. Kloonaa repositorio ja siirry juurikansioon
2. Luo .env -tiedosto ja määritä sen sisältö näin:  
   ```
   DATABASE_URL=<tietokannan-paikallinen-osoite>  
   SECRET_KEY=<salainen-avain>
   ```
4. Aktivoi virtuaaliympäristö:  
   ```
   python3 -m venv venv
   ```
   ```
   source venv/bin/activate
   ``` 
6. Asenna riippuvuudet:
   ```
   pip install -r ./requirements.txt
   ```
8. Määritä tietokannan skeema:
   ```
   psql < schema.sql
   ```
10. Käynnistä:  
   ```
   flask run
   ```

### Admin-käyttäjän luominen
Luo käyttäjätili käyttäjätunnuksella *admin*. Kirjautuessasi tälle tilille, saat käyttöösi admin-oikeudet.
