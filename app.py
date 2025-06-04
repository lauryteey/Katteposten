# Importerer nødvendige moduler fra Flask og andre biblioteker
from flask import Flask, request, jsonify, session, render_template, redirect
import os               # For å jobbe med filer og mapper
import json             # For å lese og skrive JSON-data
import mysql.connector  # Kobling mot MySQL-database
import markdown         # For å konvertere Markdown til HTML
from werkzeug.security import generate_password_hash, check_password_hash  # For sikker hashing og sjekking av passord
from config import db_config  # Henter databaseinnstillinger fra en egen config-fil

# Oppretter Flask-applikasjonen og angir hvor malene (HTML) ligger
app = Flask(__name__, template_folder="./templates")
app.secret_key = 'Hei, secret key'  # Nødvendig for å kunne bruke sessions. OBS: Ikke bruk ekte nøkkel i produksjon!

# Mappen der artiklene og metadataene ligger
ARTICLES_DIR = "articles"

# Lager en kobling til MySQL-databasen
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor(dictionary=True)  # Gjør at resultatene returneres som ordbøker i stedet for tupler

# BRUKER-RELATERTE RUTER 

# Innlogging – sjekker legitimasjon og lagrer bruker-ID i sesjonen
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Henter JSON-data fra klienten (forventet e-post og passord)

    # Sjekker at både e-post og passord er oppgitt
    if 'e_post' not in data or 'passord' not in data:
        return jsonify({"error": "E-post og passord er påkrevd"}), 400

    e_post = data['e_post']
    passord = data['passord']

    # Søker etter brukeren i databasen basert på e-post
    query = "SELECT brukerID, passord FROM bruker WHERE e_post = %s"
    cursor.execute(query, (e_post,))
    user = cursor.fetchone()

    # Hvis brukeren finnes og passordet stemmer (sjekker hash)
    if user and check_password_hash(user['passord'], passord):
        session['brukerID'] = user['brukerID']  # Lagrer bruker-ID i sesjonen

        ip = hent_ip()  # Henter IP-adressen for loggføring

        # Registrerer innlogging i innloggingsloggen
        cursor.execute(
            "INSERT INTO innloggingslogg (brukerID, handling, ip_adresse) VALUES (%s, 'inn', %s)",
            (user['brukerID'], ip)
        )
        conn.commit()

        return jsonify({"message": "Klarte å logge inn YAY!", "redirect": "/"}), 200

    # Hvis passordet er feil, men brukeren finnes
    elif user:
        return jsonify({"error": "Feil passord."}), 401

    # Hvis brukeren ikke finnes
    else:
        return jsonify({"error": "Bruker ble ikke funnet."}), 404


# Oppretter en ny bruker og lagrer informasjonen i databasen
@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()

    # Sjekker at alle nødvendige felter er med
    if not all(key in data for key in ('e_post', 'passord', 'fornavn', 'etternavn')):
        return jsonify({"error": "E-post, passord, fornavn og etternavn er påkrevd"}), 400

    e_post = data['e_post']
    passord = data['passord']
    fornavn = data['fornavn']
    etternavn = data['etternavn']

    # Sjekker om e-posten allerede finnes i systemet
    query = "SELECT e_post FROM bruker WHERE e_post = %s"
    cursor.execute(query, (e_post,))
    if cursor.fetchone():
        return jsonify({"error": "E-posten er allerede registrert"}), 409

    # Hasher passordet før det lagres i databasen
    hashed_passord = generate_password_hash(passord)

    # Setter inn ny bruker i databasen
    query = """
        INSERT INTO bruker (e_post, passord, fornavn, etternavn)
        VALUES (%s, %s, %s, %s)
    """
    values = (e_post, hashed_passord, fornavn, etternavn)
    cursor.execute(query, values)
    conn.commit()

    return jsonify({"message": "Brukeren ble opprettet!"}), 201


# Henter ip for innloggingslogg
def hent_ip():
    if request.headers.get('X-Forwarded-For'):# X-Forwarded-For used when the user is behind a proxy, so it gets the original IP
        return request.headers.get('X-Forwarded-For').split(',')[0] # Tar første elementen i listen
    return request.remote_addr     # If there's no proxy header, just return the direct IP address from the request
    # request.remote_addr used when there is no proxy, so gets the direct IP.



# Sletter brukerens konto hvis riktig passord er oppgitt
@app.route('/slettkonto', methods=['POST'])
def slett_konto():
    if 'brukerID' not in session:
        return redirect('/log_in')  # Brukeren må være logget inn

    bruker_id = session['brukerID']
    passord = request.form['passord']

    # Henter det lagrede (hasha) passordet til brukeren
    cursor.execute("SELECT passord FROM bruker WHERE brukerID = %s", (bruker_id,))
    user = cursor.fetchone()

    # Sjekker at oppgitt passord stemmer
    if user and check_password_hash(user['passord'], passord):
        # Sletter først tilknyttede loggdata og deretter brukeren
        cursor.execute("DELETE FROM innloggingslogg WHERE brukerID = %s", (bruker_id,))
        cursor.execute("DELETE FROM bruker WHERE brukerID = %s", (bruker_id,))
        conn.commit()

        session.clear()  # Tømmer sesjonen (logger ut brukeren)
        return render_template('sletteKonto.html')  # Viser bekreftelsesside

    else:
        # Hvis passordet er feil, vis feilmelding
        return render_template('minside.html', fornavn=get_fornavn(), feilmelding="Feil passord. Kontoen ble ikke slettet."), 401


# Henter fornavnet til brukeren fra databasen (brukes flere steder)
def get_fornavn():
    if 'brukerID' in session:
        cursor.execute("SELECT fornavn FROM bruker WHERE brukerID = %s", (session['brukerID'],))
        user = cursor.fetchone()
        if user:
            return user['fornavn']
    return None


# Article Helper Functions

# Hjelpefunksjon som henter metadata (tittel, publiseringsdato osv.) for én spesifikk artikkel
def fetch_article_metadata(category, article_id):
    metadata_file = os.path.join(ARTICLES_DIR, "metadata", "metadata.json")  # Full sti til metadata-filen
    if not os.path.exists(metadata_file):  # Hvis metadata-filen ikke finnes
        return None

    with open(metadata_file, "r", encoding="utf-8") as f:  # Åpner metadata-filen
        data = json.load(f)  # Leser innholdet som JSON

    for article in data.get("articles", []):  # Går gjennom alle artiklene
        try:
            current_id = int(article.get("id"))  # Sørger for at id kan sammenlignes som tall
        except ValueError:
            continue  # Hopper over hvis id ikke er et gyldig tall

        # Sjekker om både kategori og id matcher det som ble etterspurt
        if current_id == int(article_id) and article.get("category") == category:
            return article  # Returnerer metadata for den riktige artikkelen

    return None  # Fant ingen match


# Henter alle artikler innenfor en spesifikk kategori
def list_articles(category):
    metadata_file = os.path.join(ARTICLES_DIR, "metadata", "metadata.json")
    if not os.path.exists(metadata_file):
        return []

    with open(metadata_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Filtrerer og returnerer kun artiklene som tilhører gitt kategori
    return [article for article in data.get("articles", []) if article.get("category") == category]



# Article API and Page Routes

# API-endepunkt: Returnerer innholdet i en artikkel som HTML via JSON
@app.route('/api/article/<category>/<article_id>', methods=['GET'])
def get_article_content(category, article_id):
    article = fetch_article_metadata(category, article_id)
    if not article:
        return jsonify({"error": "Article not found"}), 404

    try:
        # Åpner selve Markdown-filen basert på filstien lagret i metadata
        with open(article["content_file"], "r", encoding="utf-8") as f:
            md_content = f.read()
    except FileNotFoundError:
        return jsonify({"error": "Content file not found"}), 404

    # Konverterer Markdown-innholdet til HTML
    html_content = markdown.markdown(md_content)

    # Returnerer en JSON-respons med HTML og metadata
    return jsonify({
        "id": article["id"],
        "title": article["title"],
        "content": html_content,
        "date_published": article["date_published"],
        "category": article.get("category", category)
    })

    
# Henter ALLE artikler fra metadata.json, sortert etter publiseringsdato
@app.route('/get_articles/all')
def get_all_articles():
    metadata_file = os.path.join(ARTICLES_DIR, "metadata", "metadata.json")
    if not os.path.exists(metadata_file):
        return jsonify({"error": "metadata.json not found"}), 500

    with open(metadata_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_articles = data.get("articles", [])

    # Sorterer artiklene etter publiseringsdato (siste først)
    sorted_articles = sorted(
        all_articles,
        key=lambda a: a.get('date_published', ''),
        reverse=True
    )

    return jsonify({'articles': sorted_articles})


# Viser én artikkel som HTML-side (ikke API, men vanlig side med template)
@app.route('/article/<category>/<article_id>')
def show_article(category, article_id):
    article = fetch_article_metadata(category, article_id)
    if not article:
        return "Artikkel ikke funnet", 404

    # Leser innholdet fra Markdown-filen
    content_path = os.path.join(ARTICLES_DIR, article["content_file"])
    try:
        with open(content_path, "r", encoding="utf-8") as f:
            md_content = f.read()
    except Exception:
        return "Innhold ikke funnet", 404

    # Konverterer til HTML
    article["content"] = markdown.markdown(md_content)

    # Henter fornavn dersom bruker er logget inn
    fornavn = None
    if 'brukerID' in session:
        cursor.execute("SELECT fornavn FROM bruker WHERE brukerID = %s", (session['brukerID'],))
        user = cursor.fetchone()
        if user:
            fornavn = user['fornavn']

    # Sender både artikkel og fornavn til HTML-templaten
    return render_template("nyheter/forsideNyhet.html", article=article, fornavn=fornavn)



# Henter alle artikler innenfor en gitt kategori og returnerer dem som JSON
@app.route('/get_articles/<category>', methods=['GET'])
def get_articles(category):
    articles = list_articles(category)

    # Debug-utskrifter (kan fjernes senere)
    print("category: ", category)
    print("articles: ", articles)

    return jsonify(articles)

# Hjemmeside – viser fornavn hvis bruker er logget inn
@app.route('/')
def home():
    fornavn = None
    if 'brukerID' in session:
        query = "SELECT fornavn FROM bruker WHERE brukerID = %s"
        cursor.execute(query, (session['brukerID'],))
        user = cursor.fetchone()
        if user:
            fornavn = user['fornavn']

    return render_template('main.html', fornavn=fornavn)



# Viser innloggingssiden
@app.route('/log_in', methods=['GET'])
def log_in():
    return render_template('login.html')

# Viser registreringssiden
@app.route('/sign_up')
def sign_up():
    return render_template('register.html')


# Logger brukeren ut og lagrer en loggoppføring
@app.route('/logout')
def logout():
    if 'brukerID' in session:
        bruker_id = session['brukerID']
        ip = hent_ip()

        # Registrerer utlogging i loggen
        cursor.execute(
            "INSERT INTO innloggingslogg (brukerID, handling, ip_adresse) VALUES (%s, 'ut', %s)",
            (bruker_id, ip)
        )
        conn.commit()

    session.clear()  # Tømmer sesjonen (brukeren logges ut)
    return redirect('/')


#Route til min side, slette kontoen eller logg av
# "Min side" – brukes til å slette konto eller logge ut
@app.route('/minside', methods=['GET', 'POST'])
def minside():
    if 'brukerID' not in session:
        return redirect('/log_in')  # Brukeren må være logget inn

    fornavn = None
    cursor.execute("SELECT fornavn FROM bruker WHERE brukerID = %s", (session['brukerID'],))
    user = cursor.fetchone()
    if user:
        fornavn = user['fornavn']

    return render_template('minSide.html', fornavn=fornavn)


if __name__ == '__main__':
    app.run(debug=True)  # Starter Flask-serveren i utviklingsmodus (debug gir mer feilsøking)
