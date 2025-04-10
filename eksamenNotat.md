# 📰 Katteposten – Digital Avis med Flask, Python, JavaScript og JSON

## 👩‍💻 Om Katteposten

Katteposten er en nettside for å publisere artikler, med brukerpålogging og kategoribasert lagring. Artiklene lagres som **Markdown-filer**, og metadata til hver artikkel lagres i en felles `metadata.json`-fil med informasjon som tittel, utdrag, publiseringsdato og filsti til selve Markdown-filen.

Katteposten har egne ruter for innlogging og registrering. Brukere lagres i databasen i tabellen `bruker`.

---

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
