# 🧪 Feilsøking og problemløsning 🔧
Underveis i prosjektet støtte jeg på flere utfordringer som jeg lærte mye av. Her er en oversikt over hva som gikk galt, hvorfor det skjedde, og hvordan jeg løste det.

## ❌ feilsøking ved 404
Jeg fikk en 404-feil da jeg prøvde å hente en artikkel. Jeg fant ut at Flask bygger filstien med ARTICLES_DIR + content_file, så det var viktig at content_file i metadata.json pekte til riktig undermappe – i mitt tilfelle tekster/.
Eksempel:
````json
"content_file": "tekster/forsideNyhet.md"
````

## ❌ SVG-logoen vises ikke
Problem: Kun logoens alt‑tekst ble vist i stedet for selve bildet.
Årsak: Jeg brukte feil path og hadde glemt .svg på slutten.
Løsning: Jeg endret pathen slik at Flask fant filen riktig med url_for():

````
<img src="{{ url_for('static', filename='svg/icons/katteposten_white.svg') }}">
`````
## ❌ Login fungerte, men jeg ble sendt til feil adresse
Problem: Etter innlogging ble brukeren sendt til /forside, som ikke fantes.
Årsak: redirect-verdien etter innlogging var feil i app.py.
Løsning: Jeg endret redirect til å peke på / i stedet:

````
return jsonify({"message": "Klarte å logge inn YAY!", "redirect": "/"})
````
## ❌ Inputfeltene var ikke riktig sentrert

Problem: Det så ut som inputfeltene var skjevt plassert med for mye padding på én side.

Årsak: Standard CSS-modell inkluderte ikke padding og border i total bredde.
Løsning: Jeg la til box-sizing: border-box i CSS:

````
*, *::before, *::after {
  box-sizing: border-box;
}
````
## ❌ Feilmeldinger ble ikke vist riktig ved login og registrering

Problem: Ved feil input eller feil passord fikk brukeren ingen tilbakemelding.

Årsak: Ingen synlig respons ble lagt inn i JavaScript.

Løsning: Jeg laget en showMessage()-funksjon som brukte textContent og style.color for å vise feilmeldinger i grensesnittet.

## ❌ Artikler vises ikke når man klikker på kategorier fra artikkelsiden
Problem: Når man var inne på en artikkel (f.eks. ``forsideNyhet.html``) og klikket på en kategori i menyen, ble man sendt til ````/````, men så ikke riktig artikler.

Årsak: Artikler ble tidligere lastet med JavaScript basert på valgt kategori, men vi hentet ikke ````?category=...```` fra URL.

Løsning: Jeg gjorde menyvalgene om til ````<a href="/?category=...">```` -lenker og la til logikk i forside.js som henter kategori fra URL og kaller ````loadArticles(...)````.

## ❌ JavaScript fungerte ikke riktig på artikkelsiden
Problem: Jeg prøvde å bruke samme ````forside.js```` på ````forsideNyhet.html```` men det førte til feil fordi den siden har annen struktur.

Årsak: ````forside.js```` forventet elementer som ikke fantes på artikkelsiden.

Løsning: Jeg holdt ````forsideNyhet.html```` som en rendret enkeltside og lot menylenkene føre brukeren tilbake til ````/```` med kategori i URL.

## ❌ TypeError: articles.forEach is not a function

Problem: Jeg fikk en JavaScript-feil når jeg prøvde å vise alle artikler.

Årsak: ````fetch()```` returnerte et JSON-objekt, men jeg prøvde å bruke ````forEach```` på hele objektet i stedet for ````data.articles````.

Løsning: Jeg endret ````fetchArticles()```` slik at den returnerer kun data.articles:

`````js 
const data = await response.json();
return data.articles || [];
``````
## ❌ 500 Internal Server Error ved lasting av alle artikler

Problem: Flask ga en intern serverfeil når jeg prøvde å laste alle artikler via ````/get_articles/all.````

Årsak: ````metadata.json```` ble forsøkt åpnet med feil path.

Løsning: Jeg brukte ````os.path.join()```` med riktig base:

````python
metadata_file = os.path.join(ARTICLES_DIR, "metadata", "metadata.json")
````

## ❌ Hosting av egen nettside med AWS og Gunicorn

I dette prosjektet prøvde jeg å sette opp min egen server for å hoste en webapplikasjonen. Målet var å lære hvordan sette opp mitt eget domene altså å gjøre det “helt selv” med en virtuell server fra **Amazon Web Services (AWS)**.

## Hva jeg prøvde å gjøre

- Jeg lagde en Flask-applikasjon.

- Jeg opprettet en **EC2-instans** (en virtuell maskin) på AWS med **Ubuntu** som operativsystem.

- Jeg installerte nødvendige programmer og pakker, som Python, pip, og opprettet et **virtuelt miljø**.

- Jeg installerte og brukte **Gunicorn** for å kjøre Flask-appen, siden det er en mer produksjonsklar server enn Flask sin innebygde utviklingsserver.

- Jeg planla også å bruke **Nginx** for å koble trafikk fra nettleseren til Gunicorn og Flask-appen.

## Problem
Hver gang jeg prøvde å starte Gunicorn, fikk jeg en **feil 9: "bad file descriptor"**.

## Løsning 
- Jeg prøvde å bytte porter, sjekke filrettigheter og bruke forskjellige kommandoer for å starte Gunicorn, men feilen kom fortsatt.

- Jeg prøvde også å legge databasen (som appen brukte) direkte på EC2-serveren, men det fungerte heller ikke – mest sannsynlig på grunn av samme eller lignende tilkoblingsproblemer.

- På grunn av disse feilene klarte jeg **ikke å få applikasjonen opp og kjøre på serveren**, verken med backend eller database.


## Filendringer som ble berørt

templates/forsideNyhet.html – menyen bruker nå ````<a>-lenker````

templates/main.html – viser kun tomt oppsett, ikke ferdig renderte artikler

static/js/forside.js – leser kategori fra URL og laster innhold dynamisk

app.py – endret /-ruten til å ikke returnere artikler direkte


# Lovverk og etikk 🧾

I dette prosjektet har jeg vært bevisst på to viktige områder: **personvern** og **universell utforming**.

## 📌 Personvern

- Passord blir aldri lagret som klartekst i databasen. Jeg bruker `werkzeug.security` til å hashe passordene.
- Brukerinformasjon (e-post og navn) håndteres trygt og deles ikke videre.
- Jeg bruker `session` i Flask for å holde brukeren innlogget, men uten sensitive data som vises i nettleseren.
- Ingen informasjon lastes inn før brukeren har logget inn.

## 📌 Universell utforming

- Fargekontraster er brukt bevisst for å gjøre tekst og knapper tydelige.
- Sidene fungerer også på mobil og mindre skjermer.
- Jeg har brukt `aria-label` på viktige knapper (som "hamburgermeny" og "logg inn") for skjermlesere.
- Alt‑tekst er lagt til på logoen og viktige bilder.

Dette viser at prosjektet prøver å følge både GDPR og krav til tilgjengelighet.


