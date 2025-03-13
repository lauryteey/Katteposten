import os, json
from flask import Flask, jsonify, render_template, request, session, request
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

# Oppretter en Flask-applikasjon
app = Flask(__name__, template_folder="./templates")
app.secret_key = 'Hei, secret key'  # En tilfeldig nøkkel som brukes for å kryptere sessions (brukerdata som lagres midlertidig).

#for artikkel i artikkler
ARTICLES_DIR = "articles"


# Kobler til en global MySQL-database
conn = mysql.connector.connect(
    host="10.0.0.19",         # Databasens adresse (lokal maskin (%))
    user="katteposten_admin",     # Brukernavnet til databasen.
    password="123",           # Passordet til databasen.
    database="katteposten"       # Navnet på databasen som brukes.
)

# Oppretter en global cursor for å kjøre SQL-spørringer
cursor = conn.cursor(dictionary=True)  # Konfigurerer til å returnere resultater som dictionaries keys (nøkkel-verdi-par).


# Rute for innlogging
@app.route('/login', methods=['POST'])
def login():
    try:
        # Henter data som sendes i forespørselen (JSON-format).
        data = request.get_json()

        # Sjekker om nødvendige felter finnes i forespørselen.
        if 'e_post' not in data or 'passord' not in data:
            return jsonify({"error": "E-post og passord er påkrevd"}), 400

        e_post = data['e_post']  # Leser e-post fra forespørselen.
        passord = data['passord']  # Leser passord fra forespørselen.

        # SQL-statement, den sjekker om e-posten finnes i databasen.
        query = "SELECT brukerID, passord FROM bruker WHERE e_post = %s" #%s placeholder for de ekte valuene
        cursor.execute(query, (e_post,)) #kjører query i datbasen bip bop
        user = cursor.fetchone()  # Henter resultatet fra databasen.

        if user:
            # Sjekker om passordet stemmer ved hjelp av hashing.
            if check_password_hash(user['passord'], passord):
                session['brukerID'] = user['brukerID']  # Lagre brukerID i session (midlertidig lagring).
                return jsonify({"message": "Klarte å logge inn YAY!", "redirect": "/calenderen"}), 200
            else:
                return jsonify({"error": "Feil passord."}), 401
        else:
            return jsonify({"error": "Bruker ble ikke funnet."}), 404
    except mysql.connector.Error as e:
        # Feil relatert til databasen er her.
        print(f"Feil i databasen under login: {e}")
        return jsonify({"error": "En feil i databasen oppsto"}), 500
    except Exception as e:
        # Andre uventede feil håndteres her.
        print(f"Uforventet feil under login: {e}")
        return jsonify({"error": "Det skjedde en uventet feil"}), 500

 
# Rute for å opprette en ny bruker
@app.route('/create_user', methods=['POST'])
def create_user():
    try:
        # Henter data som sendes i forespørselen (JSON-format)
        data = request.get_json()

        # Sjekker om alle nødvendige felt er med i forespørselen
        if not all(key in data for key in ('e_post', 'passord', 'fornavn', 'etternavn')):
            return jsonify({"error": "E-post, passord, fornavn og etternavn er påkrevd"}), 400

        e_post = data['e_post']  # Henter e-post fra forespørselen
        passord = data['passord']  # Henter passord fra forespørselen
        fornavn = data['fornavn']  # Henter fornavn fra forespørselen
        etternavn = data['etternavn']  # Henter etternavn fra forespørselen

        # Sjekker om e-posten allerede finnes i databasen
        query = "SELECT e_post FROM bruker WHERE e_post = %s"
        cursor.execute(query, (e_post,))
        if cursor.fetchone():
            return jsonify({"error": "E-posten er allerede registrert"}), 409

        # Genererer et hashed passord for sikker lagring
        hashed_passord = generate_password_hash(passord)

        # SQL-spørring for å legge til ny bruker
        query = """
            INSERT INTO bruker (e_post, passord, fornavn, etternavn)
            VALUES (%s, %s, %s, %s)
        """
        values = (e_post, hashed_passord, fornavn, etternavn)
        cursor.execute(query, values)
        conn.commit()  # Lagrer endringene i databasen

        return jsonify({"message": "Brukeren ble opprettet!"}), 201
    except mysql.connector.Error as e:
        # Håndterer databasefeil
        print(f"Databasefeil under oppretting av bruker: {e}")
        return jsonify({"error": "En feil oppsto med databasen"}), 500
    except Exception as e:
        # Håndterer andre uventede feil
        print(f"Uventet feil under oppretting av bruker: {e}")
        return jsonify({"error": "Det oppsto en uventet feil"}), 500



def list_articles(category):
    """Return a list of article previews for a given category."""
    category_dir = os.path.join(ARTICLES_DIR, category)
    articles = []
    if os.path.exists(category_dir):
        for filename in os.listdir(category_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(category_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    article = json.load(f)
                    preview = {
                        "id": article.get("id"),
                        "title": article.get("title"),
                        "date_published": article.get("date_published"),
                        "excerpt": article.get("content", "")[:150] + ("..." if len(article.get("content", "")) > 150 else "")
                    }
                    articles.append(preview)
    return articles



def fetch_article(category, article_id):
    """Retrieve a single article based on category and article id."""
    category_dir = os.path.join(ARTICLES_DIR, category)
    if os.path.exists(category_dir):
        for filename in os.listdir(category_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(category_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    article = json.load(f)
                    if article.get("id") == article_id:
                        return article
    return None



# Route to list articles as JSON data
@app.route("/get_articles/<category>", methods=["GET"])
def get_articles(category):
    articles = list_articles(category)
    return jsonify(articles)



@app.route('/')
def home():
    articles = list_articles("krim")
    return render_template('forside.html', articles=articles)


# Route for article detail using a clean URL.
@app.route('/article/<category>/<article_id>')
def article(category, article_id):
    article_data = fetch_article(category, article_id)
    if not article_data:
        return "Article not found", 404
    # If your template is in a subfolder 'nyheter', include that in the path.
    return render_template("nyheter/forsideNyhet.html", article=article_data)


# log in og sig in routes
@app.route('/log_in')
def log_in():
    return render_template('login.html')

@app.route('/sign_up')
def sign_up():
    return render_template('register.html')  



if __name__ == '__main__':
    app.run(debug=True)