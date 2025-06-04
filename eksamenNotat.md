# 📰 Katteposten – Digital Avis med Flask, Python, JavaScript og JSON

## 👩‍💻 Om Katteposten

Katteposten er et nyhetsnettsted der brukere kan logge inn og lese artikler som lagres i Markdown-filer. Metadata om artiklene (tittel, utdrag, dato, osv.) lagres i en ````JSON````-fil. Jeg bruker ````Flask```` (````Python````) til backend, ````JavaScript```` til frontend, og ````MariaDB```` til brukerinformasjon.

Katteposten har egne ruter for innlogging og registrering. Brukere lagres i databasen i tabellen `bruker`.`

## 🎯 Målgruppe

Dette prosjektet er laget for både unge og voksne som er glad i katter og ønsker et sted for katteinspirert lesing. Samtidig fungerer det som et skoleprosjekt som viser hvordan man bygger en full-stack applikasjon.


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

    4. **Ofte stilte spørsmål** delen på **README**-filen

    5.  Bruk av ````crontab```` for å automatisere Git pull-requestene

## Lovverk og etikk 🧾

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

## Bruk av Crontab for automatisk Git pull- request

Ved å bruke et skript og cron-jobb for å kjøre git pull automatisk, kan prosjektet på Raspberry Pi holdes oppdatert uten manuell innsats. Dette gir fordeler innen både drift og brukerstøtte.

**📂 Kommandoer med forklaring**
1. Vis skriptet og loggfilen

```` bash
# Dette viser at skriptet og loggen finnes, og hvem som eier dem.
ls -l /home/laura/auto_git_pull.sh /home/laura/git_pull.log
````
2. Se innholdet i skriptet

```` bash
# Viser hva skriptet gjør – viktig for feilsøking og dokumentasjon.
sudo nano /home/laura/auto_git_pull.sh
````

3. Se innholdet i loggfilen

```` bash
# Viser hva som skjer når skriptet kjører. Viktig for å se om oppdateringer går som de skal.
cat /home/laura/git_pull.log
````
4. Se cron-jobbene som kjører
```` bash
# Viser automatiske oppgaver som er satt opp for brukeren – her ser man at prosjektet oppdateres hvert 5. minutt.
crontab -l
````

## EXTRAS : 

1. commandoen for å kjøre Scripten **(ikke skrive på eksamen)**

````bash 
sudo chmod +x /home/laura/auto_git_pull.sh
````

2. Kommandoen for å gå til **crontab** (den kan kjøre task som brukeren bror)

````bash 
crontab -e
````

## 💡 Hvorfor er dette nyttig?

✅ Brukerstøtte (User Support):
- Man slipper å be brukeren gjøre manuelle oppdateringer.

- Kan hjelpe sluttbrukere med feil som skyldes gammel kode ved å vite at oppdateringer skjer regelmessig.

- Forenkler vedlikehold og gjør det lettere å reprodusere feil.

✅ Drift: 
- Systemet holder seg automatisk oppdatert uten at man trenger logge inn manuelt.

- Mindre risiko for at eldre versjoner kjører i produksjon.

- Logging gjør det enkelt å feilsøke hvis noe går galt.

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
UPDATE bruker SET etternavn = 'NyEtternavn' WHERE e_post = 'test@test.no';

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

Dette forklarer hvordan SQL-spørringer skrives sikkert med parametere for å unngå SQL-injection. Da blir verdiene sendt trygt til databasen og ikke blandet inn som kode. I tillegg til at hvis man skriver SQL direkte med brukerinput, kan noen prøve å hacke seg inn med "SQL injection".

## 🧑‍💻 Utvikling

**Dette skal jeg forklare og vise fra koden:**

Jeg bruker ````@app.route('/login')```` og ````@app.route('/create_user')```` for innlogging og registrering.

````session```` ved bruk av ````flask```` lagrer hvem som er logget inn så lenge brukeren inntil brukeren logger ut eller 

````IP-adresse```` Når noen logger inn eller ut, lagres IP-adressen deres i en egen tabell i databasen, sammen med tidspunkt og handlingen (inn/ut).

Artikler vises med ````Flask```` ````(render_template)```` eller hentes med ````fetch (JS)````. Noen ganger vises artiklene direkte i ````HTML-sider```` jeg lager med ````Flask````, da bruker jeg ````render_template````. Andre ganger henter jeg artiklene med ````JavaScript```` og viser dem dynamisk på siden uten å laste hele siden på nytt.

## 🔐 Om pålogging

- Flask-session brukes for å holde brukeren innlogget.
- Passord hashet med `werkzeug.security`.
- Input valideres (f.eks. e-postformat og passordlengde).
- Feilmeldinger vises ved ugyldig registrering eller pålogging.

---
## 📄 Lagring av artikler - Struktur

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
---
## Admin-funksjon (idé jeg kan snakke om):

- Lag en admin-funksjon som viser liste over alle brukere.

- Admin kan slette eller "banne" brukere basert på e-post.

- Når en bruker er bannet, kan de ikke logge inn (sjekkes i login-ruten).

--- 

# 👮 Admin-funksjon (idé jeg kan snakke om):

- Lag en admin-funksjon som viser liste over alle brukere.

- Admin kan slette eller banne brukere basert på e-post.

- Når en bruker er bannet, kan de ikke logge inn (det sjekkes i login-ruten).

**Eksempel på bannet-sjekk i login-rute:**

````python 
# I login-funksjonen
query = "SELECT brukerID, passord, er_bannet FROM bruker WHERE e_post = %s"
cursor.execute(query, (e_post,))
user = cursor.fetchone()

if user and user.get("er_bannet"):
    return jsonify({"error": "Denne brukeren er utestengt."}), 403
````
**VIKITG!** Forklar at "er_bannet" er en ekstra kolonne i databasen ````(f.eks. TINYINT(1)````, altså en boolsk verdi 0 eller 1).

Hvis jeg ville utvide denne funksjonen under eksamen, kan jeg:

- Vise hvordan du henter alle brukere (kun hvis session inneholder en admin-ID).

- Legge til en knapp for å slette eller banne brukere.

- Forklare at du må ha ekstra kolonne i tabellen bruker:

````sql
ALTER TABLE bruker ADD er_bannet TINYINT(1) DEFAULT 0;
````
---

# Funksjon jeg skal lage live: Favoritt-artikkel

**Steg-for-steg guide jeg følger under eksamen:**

1. Lag tabellen i databasen:

````sql
CREATE TABLE favoritter (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brukerID INT,
    article_id INT,
    category VARCHAR(50),
    title VARCHAR(255),
    FOREIGN KEY (brukerID) REFERENCES bruker(brukerID)
);
````

2. Lag knapp i HTML-siden:

- Legg til denne knappen i filen ````forsideNyhet.html```` (hvor én artikkel vises) og evt. i ````artikkel-forhåndsvisningen```` hvis jeg tror jeg kan:

````HTML
<button onclick="leggTilFavoritt('{{ article.id }}', '{{ article.category }}', '{{ article.title }}')">Legg til favoritt</button>
````
3. Lag JavaScript-funksjon:

I ````viseNyheter.js```` (eller et nytt skript som lastes inn på artikkelsiden):

````javaScript
function leggTilFavoritt(id, kategori, tittel) {
    fetch('/leggtil_favoritt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ article_id: id, category: kategori, title: tittel })
    })
        .then(res => res.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
            } else if (data.error) {
                alert(data.error);
            } else {
                alert("Ukjent svar fra serveren.");
            }
        })
        .catch(err => alert("Noe gikk galt!"));
}

````

4. Lag route i Flask i ````app.py````:

```` python
# Flask-rute for å legge til favoritt
@app.route('/leggtil_favoritt', methods=['POST'])
def leggtil_favoritt():
    if 'brukerID' not in session:
        return jsonify({'error': 'Ikke logget inn'}), 401

    data = request.get_json()
    cursor.execute(
        "INSERT INTO favoritter (brukerID, article_id, category, title) VALUES (%s, %s, %s, %s)",
        (session['brukerID'], data['article_id'], data['category'], data['title'])
    )
    conn.commit()
    return jsonify({'message': 'Artikkel lagt til favoritter'})

````

5. Vis favoritter på ````minSide.html````:

Endre Flask-ruten for ````@app.route('/minside')```` slik at den sender med favoritter:

```` python
#Route til min side, slette kontoen eller logg av
@app.route('/minside', methods=['GET', 'POST'])
def minside():
    if 'brukerID' not in session:
        return redirect('/log_in')

    cursor.execute("SELECT fornavn FROM bruker WHERE brukerID = %s", (session['brukerID'],))
    user = cursor.fetchone()
    fornavn = user['fornavn'] if user else None

    cursor.execute("SELECT * FROM favoritter WHERE brukerID = %s", (session['brukerID'],))
    favoritter = cursor.fetchall()

    return render_template('minSide.html', fornavn=fornavn, favoritter=favoritter)
````

6. Vis dem i ````minSide.html````:

````HTML
<ul>
  {% for f in favoritter %}
    <li>
      <a href="/article/{{ f.category }}/{{ f.article_id }}">{{ f.title }}</a>
    </li>
  {% endfor %}
</ul>
````

7. Oppdatere slett def, for å slette alle info i kontoen

````python

@app.route('/slettkonto', methods=['POST'])
def slett_konto():
    if 'brukerID' not in session:
        return redirect('/log_in')

    bruker_id = session['brukerID']
    passord = request.form['passord']

    cursor.execute("SELECT passord FROM bruker WHERE brukerID = %s", (bruker_id,))
    user = cursor.fetchone()

    if user and check_password_hash(user['passord'], passord):
        # Slett alle relaterte rader først
        cursor.execute("DELETE FROM favoritter WHERE brukerID = %s", (bruker_id,))
        cursor.execute("DELETE FROM innloggingslogg WHERE brukerID = %s", (bruker_id,))
        cursor.execute("DELETE FROM bruker WHERE brukerID = %s", (bruker_id,))
        conn.commit()
        session.clear()
        return render_template('sletteKonto.html')  # bekreftelse side

    else:
        return render_template(
            'minside.html',
            fornavn=get_fornavn(),
            feilmelding="Feil passord. Kontoen ble ikke slettet."
        ), 401

````

🎯 Denne funksjonen viser at jeg kan:

Bruke session (brukerstøtte)

Bruke database og SQL (drift)

Lage dynamisk funksjon med Flask og JS (utvikling)

---
## Extra kode jeg kan skrive foran sensor (for å vise kunnskap):

`````` python 
# Validering av e-post:

def er_gyldig_epost(epost):
    return "@" in epost and "." in epost
``````
````python 
# Telle artikler i en kategori:

import os

def tell_artikler():
    path = "articles/nyheter"
    return len([f for f in os.listdir(path) if f.endswith(".md")])

````
````python
# Filtrere artikler fra metadata:

def hent_artikler_fra_kategori(metadata, kategori):
    return [art for art in metadata.get("articles", []) if art.get("category") == kategori]

````

````python
# Legge til metadata i JSON:

import json

def legg_til_metadata(ny_metadata):
    with open("articles/metadata/metadata.json", "r+", encoding="utf-8") as fil:
        data = json.load(fil)
        data["articles"].append(ny_metadata)
        fil.seek(0)
        json.dump(data, fil, indent=4)

````

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

🗄️ Databasestruktur

````sql
-- Tabell bruker

CREATE TABLE bruker (
    brukerID INT AUTO_INCREMENT PRIMARY KEY,
    e_post VARCHAR(255) NOT NULL UNIQUE,
    passord VARCHAR(255) NOT NULL,
    fornavn VARCHAR(100) NOT NULL,
    etternavn VARCHAR(100) NOT NULL
);

``````

````sql
-- Tabell innloggingslogg

CREATE TABLE innloggingslogg (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brukerID INT,
    tidspunkt DATETIME DEFAULT CURRENT_TIMESTAMP,
    handling VARCHAR(10),
    ip_adresse VARCHAR(45),
    FOREIGN KEY (brukerID) REFERENCES bruker(brukerID)
);

````
````sql
-- Tabell favoritter (demo under eksamen)

CREATE TABLE favoritter (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brukerID INT,
    article_id INT,
    category VARCHAR(50),
    title VARCHAR(255),
    FOREIGN KEY (brukerID) REFERENCES bruker(brukerID)
);
````


---

## Eksempel på rute i Flask:

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

# Denne funksjonen:
- Henter riktig artikkel basert på kategori og ID

- Leser innholdet fra .md-filen

- Viser det på nettsiden med tittel, innhold og dato

---

# Hva bør jeg huske til eksamen: 

- Hvordan JSON-filer håndteres i Python 

- Hvordan man kobler Flask til MariaDB

- Hvordan man bruker os og glob for å finne artikler

- HTML/CSS struktur og JavaScript-funksjoner for dynamisk innhold

- Hvordan man sikrer input og håndterer brukersesjoner
