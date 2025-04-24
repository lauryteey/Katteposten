# Lovverk og etikk 🧾

I dette prosjektet har jeg vært bevisst på to viktige områder: **personvern** og **universell utforming**.

## 📌 Personvern

- Passord blir aldri lagret som klartekst i databasen. Jeg bruker `werkzeug.security` til å hashe passordene.
- Brukerinformasjon (e-post og navn) håndteres trygt og deles ikke videre.
- Jeg bruker `session` i Flask for å holde brukeren innlogget, men uten sensitive data som vises i nettleseren.
- Ingen informasjon lastes inn før brukeren har logget inn.

## 📌 Universell utforming

- Fargekontraster er brukt bevisst for å gjøre tekst og knapper tydelige.
- Jeg har brukt `aria-label` på viktige knapper (som "hamburgermeny" og "logg inn") for skjermlesere.
- Alt‑tekst er lagt til på logoen og viktige bilder.


