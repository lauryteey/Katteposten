# 📰 Katteposten – Digital Avis med Flask, Python, JavaScript og JSON

## 👩‍💻 Om Katteposten

Katteposten er et nyhetsnettsted der brukere kan logge inn og lese artikler som lagres i Markdown-filer. Metadata om artiklene (tittel, utdrag, dato, osv.) lagres i en ````JSON````-fil. Jeg bruker ````Flask```` (````Python````) til backend, ````JavaScript```` til frontend, og ````MariaDB```` til brukerinformasjon.

Katteposten har egne ruter for innlogging og registrering. Brukere lagres i databasen i tabellen `bruker`.

---
## 🙋‍♀️ Brukerstøtte

**Dette skal jeg vise og forklare:**

- Hvordan brukeren registrerer seg og logger inn.

- Hvordan systemet gir tydelige tilbakemeldinger ved feil (f.eks. feil passord, tomme felt).

- At passord lagres trygt (med generate_password_hash).

- Tilgjengelighet: gode kontraster, alt-tekst på bilder, og ryddig struktur.

  **Eksempler jeg kan nevne:**

    1. ````logIn.js```` viser meldinger med ````showMessage()````.

  	2. ````register.js```` validerer input før det sendes til serveren.

    3. ````slett_konto()````-funksjonen lar brukeren slette seg selv etter å ha bekreftet passord.

## ⚙️ Drift

**Dette skal jeg vise og forklare:**

Jeg bruker ````config.py```` til å lagre database-innstillinger.

````Flask```` kobler seg til ````MariaDB```` med ````mysql.connector````.

Artiklene lagres lokalt som ````Markdown-filer````, og metadata hentes fra ````articles/metadata/metadata.json.````

## SQL-kommandoer jeg kan skrive på eksamen:

````sql
-- Se alle brukere:
SELECT * FROM bruker;
````

````sql
-- Legg til en testbruker:
INSERT INTO bruker (e_post, passord, fornavn, etternavn) 
VALUES ('test@test.no', '1234', 'Test', 'Person');
````
````sql
-- Oppdater en adresse:
UPDATE bruker SET adresse = 'Gate 12' WHERE e_post = 'test@test.no';
````
````sql
-- Slett logger for en bruker:
DELETE FROM innloggingslogg WHERE brukerID = 3;
````
**Viktig:** Jeg bruker ikke brukerinndata direkte i SQL, men sender dem som parametre:

## Eksempel på usikker kode (SQL injection):

**Ikke gjør dette:**
````python
query = f"SELECT * FROM bruker WHERE e_post = '{e_post}'"
cursor.execute(query)
````

Hvis en bruker skriver inn dette som **e-post**: ````test@test.no```` ELLER ````1'='1````, vil hele tabellen bli returnert fordi betingelsen alltid blir sann.

**Sikker måte:**
````python
cursor.execute("SELECT * FROM bruker WHERE e_post = %s", (e_post,))
````

Dette forklarer hvordan SQL-spørringer skrives sikkert med parametere for å unngå SQL-injection. Da blir verdiene sendt trygt til databasen og ikke blandet inn som kode.

## 🧑‍💻 Utvikling

**Dette skal jeg forklare og vise fra koden:**

Jeg bruker ````@app.route('/login')```` og ````@app.route('/create_user')```` for innlogging og registrering.

````session```` ved bruk av ````flask```` lagrer hvem som er logget inn så lenge brukeren inntil brukeren logger ut eller 

````IP-adresse```` Når noen logger inn eller ut, lagres IP-adressen deres i en egen tabell i databasen, sammen med tidspunkt og handlingen (inn/ut).

Artikler vises med ````Flask```` ````(render_template)```` eller hentes med ````fetch (JS)````. Noen ganger vises artiklene direkte i ````HTML-sider```` jeg lager med ````Flask````, da bruker jeg ````render_template````. Andre ganger henter jeg artiklene med ````JavaScript```` og viser dem dynamisk på siden uten å laste hele siden på nytt.

---


## Kode jeg kan skrive foran sensor (for å vise kunnskap):

`````` python 
# Validering av e-post:

def er_gyldig_epost(epost):
    return "@" in epost and "." in epost
``````

2. Telle artikler i en kategori:

import os

def tell_artikler():
    path = "articles/nyheter"
    return len([f for f in os.listdir(path) if f.endswith(".md")])

3. Filtrere artikler fra metadata:

def hent_artikler_fra_kategori(metadata, kategori):
    return [art for art in metadata.get("articles", []) if art.get("category") == kategori]

4. Legge til metadata i JSON:

import json

def legg_til_metadata(ny_metadata):
    with open("articles/metadata/metadata.json", "r+", encoding="utf-8") as fil:
        data = json.load(fil)
        data["articles"].append(ny_metadata)
        fil.seek(0)
        json.dump(data, fil, indent=4)

Dette forklarer jeg også under utvikling:


## 🛠️ Dette har jeg laget:

- En struktur der **metadata til hver artikkel** lagres i en felles JSON-fil (`metadata.json`), og **innholdet** til hver artikkel lagres i en separat `.md`-fil.
- Artiklene er organisert i **mapper etter kategori**.
- Flask bruker `os` og `json` for å lese artikler og metadata fra filsystemet og sende dem til HTML-templates.
- Artiklene vises i nettleseren ved hjelp av `render_template`, som sender inn riktig data til HTML-malene.
- Jeg har laget egne Flask-ruter, for eksempel:
  - `/article/<category>/<article_id>` for å vise én artikkel
- Bruk av **JavaScript (`fetch`)** kan brukes for å hente og vise artikler dynamisk på én enkelt HTML-side.

---

## 🧱 Struktur av applikasjonen

- **Backend:** Flask (Python)
- **Database:** MariaDB (brukerinformasjon lagres i `bruker`-tabellen)
- **Frontend:** HTML, CSS, JavaScript
- **Lagring av artikler:** Markdown-filer i kategorimapper, metadata samlet i `metadata.json`

---

## 🗄️ Databasestruktur

**Tabell: `bruker`**
- `brukerID` – Primærnøkkel
- `epost`  
- `passord`  
- `fornavn`  
- `etternavn`

---

## 🔐 Pålogging

- Flask-session brukes for å holde brukeren innlogget.
- Passord hashet med `werkzeug.security`.
- Input valideres (f.eks. e-postformat og passordlengde).
- Feilmeldinger vises ved ugyldig registrering eller pålogging.

---

## 📄 Lagring av artikler

Hver artikkel lagres som en **Markdown-fil** i en mappe basert på kategori. Metadata for alle artikler lagres i én felles JSON-fil (`metadata.json`). Eksempel:

```json
{
  "articles": [
    {
      "id": 1,
      "category": "krim",
      "title": "Ranet midt på dagen",
      "Redaktør": "Jonnathan Cats",
      "excerpt": "Ble ranet av naboen i sollys",
      "content_file": "artikler/krim/ranet-midt-på-dagen.md",
      "date_published": "2025-03-26"
    }
  ]
}
```

### Funksjoner 
- Bruker kan registrere og logge inn

- Bruker kan skrive og publisere artikler

- Artikler vises per kategori

- Artikler lastes inn dynamisk via JavaScript ```fetch```


### Eksempel på rute i Flask:

```python
@app.route('/article/<category>/<article_id>')
def article_detail(category, article_id):
    article = fetch_article(category, article_id)
    if not article:
        abort(404)
    with open(article["content_file"], "r", encoding="utf-8") as f:
        article["content"] = f.read()
    return render_template("article.html", article=article)

```

Denne funksjonen:
- Henter riktig artikkel basert på kategori og ID

- Leser innholdet fra .md-filen

- Viser det på nettsiden med tittel, innhold og dato

## Drift

Jeg kjører Flask på en lokal server (for utvikling) og kan enkelt tilpasse det for produksjon.

Artiklene er lagret som filer på maskinen, så det er lett å legge til nye artikler ved å redigere JSON-filer og legge til en HTML-fil.

Jeg holder strukturen enkel og oversiktlig med mapper for artikkelene og metadata:

``` md
articles/
├── metadata/
│   └── krim.json
└── tekster/
    └── forsideNyhet.md
````

## 🙋‍♀️ Brukerstøtte

- rukeren får en enkel og oversiktlig opplevelse:

- Artikler vises med tittel, utdrag og publiseringsdato

Jeg har laget:

    - En innloggingsside (/log_in)

    - En registreringsside (/sign_up)

- Flask validerer e-post og passord og gir tydelige feilmeldinger ved feil

- Session brukes for å håndtere innlogging på en trygg måte


### Hva bør jeg huske til eksamen: 

- Hvordan JSON-filer håndteres i Python 

- Hvordan man kobler Flask til MariaDB

- Hvordan man bruker os og glob for å finne artikler

- HTML/CSS struktur og JavaScript-funksjoner for dynamisk innhold

- Hvordan man sikrer input og håndterer brukersesjoner
