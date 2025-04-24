# Feilsøking og problemløsning 🔧

Underveis i prosjektet støtte jeg på flere utfordringer som jeg lærte mye av:

## ❌ SVG-logoen vises ikke

**Problem:** Kun logoens navn (alt‑tekst) ble vist.  
**Løsning:** Jeg brukte feil path og hadde glemt `.svg` på slutten. Jeg byttet ut:
```html
<img src="../static/svg icons/katteposten_white">
```
med:
```html
<img src="{{ url_for('static', filename='svg/icons/katteposten_white.svg') }}">
```

---

## ❌ Login fungerte, men jeg ble sendt til en feil adresse

**Problem:** Etter innlogging ble brukeren sendt til `/forside`, som ikke fantes.  
**Løsning:** Jeg endret Flask-route `redirect` til `"/"` i `app.py` etter login.

---

## ❌ Inputfeltene var ikke riktig sentrert

**Problem:** Det så ut som det var mer padding på venstre side enn høyre.  
**Løsning:** Jeg la til:
```css
*, *::before, *::after {
  box-sizing: border-box;
}
```
for å sikre at `padding` og `border` inkluderes i total bredde.

---

## ❌ Feilmeldinger ble ikke vist riktig

**Problem:** Feil passord eller manglende input ga ingen respons.  
**Løsning:** Jeg brukte `textContent` + `style.color` for å vise meldinger via JS-funksjonen `showMessage()`.


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


