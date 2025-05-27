# Katteposten 🐾

**Katteposten** er en digital nyhetsplattform laget for katteelskere. Her kan brukere logge inn, lese spennende artikler om katteliv, kattekrim, kattehelse og mye mer. 

## ✨ Hva prosjektet gjør

- Brukere kan registrere seg og logge inn med sikker passordhåndtering
- Artikler vises i ulike kategorier som "kattekrim", "livsstil", og "nyheter"
- Artiklene er lagret som Markdown-filer og hentes dynamisk via Flask og JSON

## 🎯 Målgruppe

Dette prosjektet er laget for både unge og voksne som er glad i katter og ønsker et sted for katteinspirert lesing. Samtidig fungerer det som et skoleprosjekt som viser hvordan man bygger en full-stack applikasjon.

## 🛠️ Teknologier brukt

- **Frontend:** HTML, CSS (med egen stil), JavaScript
- **Backend:** Python (Flask), Jinja2
- **Database:** MySQL (MariaDB)
- **Annet:** Markdown for artikler, Git for versjonskontroll

## 🚀 Hvordan bruke prosjektet

For å bruke applikasjonen må du ha følgende på plass:

- Tilgang til en MariaDB-database med riktig oppsett. Hvis du er usikker på hvordan dette gjøres, kan du følge disse veiledningene for å sette opp MariaDB på Ubuntu 20.04 eller 22.04.
  
📍  [How To Install MariaDB on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-install-mariadb-on-ubuntu-20-04)
📍 [How To Install MariaDB on Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/how-to-install-mariadb-on-ubuntu-22-04)

  

### **Installasjon**
1. **Last ned applikasjonen:**
   - Applikasjonen ligger på GitHub, klon den til datamaskinen din med:

     ```bash
     git clone https://github.com/lauryteey/katteposten.git
     ```
   - Eller last ned ZIP-filen og pakk den ut.

### **Installer og sett opp virtuelt miljø**

2. **Opprett et virtuelt miljø:**
   Gå til prosjektmappen og kjør kommandoen:

     ```bash
     python -m venv myenv
     ```

3. **Aktiver det virtuelle miljøet:**
   - På Windows:

     ```bash
     .\myenv\Scripts\activate
     ```

   - På macOS/Linux:
     ```bash
     source myenv/bin/activate
     ```

---

### **Installer nødvendige biblioteker**

- Sørg for at du har en fil kalt `requirements.txt` i prosjektmappen.
- Installer biblioteker med kommandoen:

   ```bash
   pip install -r requirements.txt
   ````
- Hvis filen requirements.txt mangler, kan du installere de viktigste bibliotekene manuelt:

````bash
pip install flask mysql-connector
pip install Flask
````
   - Deretter gå til mappen der filene ligger.
   - Start applikasjonen ved å kjøre denne kommandoen i terminalen i mappen der filene ligger:

     ```bash
     python app.py
     ```
     
   - Åpne nettleseren og gå til ip adressen du får fra flask med ````CTRL + click````

 Nå kan du registrere en bruker, logge inn, og lese artikler om katter 😸


 
---

# FAQ – Ofte stilte spørsmål 🐱❓

### Hvordan registrerer jeg meg?
Klikk på “Registrer deg"-ikonet på forsiden og fyll ut skjemaet med e-post, passord og navn.

---

### Jeg får feilmelding ved innlogging. Hva gjør jeg?
Sjekk først at du har skrevet riktig e-post og passord. Hvis det fortsatt ikke virker, kan det hende brukeren ikke finnes – prøv å registrere deg først.

---

### Hvor lagres artiklene?
Artiklene lagres som Markdown-filer og hentes inn av Flask via metadata i en `metadata.json`-fil.

---

### Hva skjer med informasjonen min?
Programmet lagrer kun det som trengs (e-post og navn), og passordene er alltid sikret med hashing. Programmet deler ikke data med noen.

---

### Kan jeg bruke dette på mobil?
Nei, I denne versjonen av prosjektet er nettsiden ikke responsiv. 

---

### Hvordan kan jeg bidra?
Hvis du ønsker å foreslå nye funksjoner eller artikler, send gjerne en e-post til [laura@katteposten.online](mailto:laura@katteposten.online) eller opprett et “issue” på GitHub-repoet! 🌸

ps kristian lien var veldig sigma og lagde kattespråk translator 😸
https://www.github.com/kristianlien 😼


