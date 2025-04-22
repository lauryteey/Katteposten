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

