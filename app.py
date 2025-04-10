from flask import Flask, request, jsonify, session, render_template
import os
import json
import mysql.connector
import markdown
from werkzeug.security import generate_password_hash, check_password_hash
from config import db_config

app = Flask(__name__, template_folder="./templates")
app.secret_key = 'Hei, secret key'  # Used for session encryption

# Base directory for articles
ARTICLES_DIR = "articles"

# Create database connection using settings from config.py
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor(dictionary=True)

# User Routes

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if 'e_post' not in data or 'passord' not in data:
        return jsonify({"error": "E-post og passord er påkrevd"}), 400

    e_post = data['e_post']
    passord = data['passord']
    query = "SELECT brukerID, passord FROM bruker WHERE e_post = %s"
    cursor.execute(query, (e_post,))
    user = cursor.fetchone()

    if user and check_password_hash(user['passord'], passord):
        session['brukerID'] = user['brukerID']
        return jsonify({"message": "Klarte å logge inn YAY!", "redirect": "/forside"}), 200
    elif user:
        return jsonify({"error": "Feil passord."}), 401
    else:
        return jsonify({"error": "Bruker ble ikke funnet."}), 404

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    if not all(key in data for key in ('e_post', 'passord', 'fornavn', 'etternavn')):
        return jsonify({"error": "E-post, passord, fornavn og etternavn er påkrevd"}), 400

    e_post = data['e_post']
    passord = data['passord']
    fornavn = data['fornavn']
    etternavn = data['etternavn']

    query = "SELECT e_post FROM bruker WHERE e_post = %s"
    cursor.execute(query, (e_post,))
    if cursor.fetchone():
        return jsonify({"error": "E-posten er allerede registrert"}), 409

    hashed_passord = generate_password_hash(passord)
    query = """
        INSERT INTO bruker (e_post, passord, fornavn, etternavn)
        VALUES (%s, %s, %s, %s)
    """
    values = (e_post, hashed_passord, fornavn, etternavn)
    cursor.execute(query, values)
    conn.commit()
    return jsonify({"message": "Brukeren ble opprettet!"}), 201


# Article Helper Functions

def fetch_article_metadata(category, article_id):
    metadata_file = os.path.join(ARTICLES_DIR, "metadata", "metadata.json")
    if not os.path.exists(metadata_file):
        return None

    with open(metadata_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for article in data.get("articles", []):
        try:
            current_id = int(article.get("id"))
        except ValueError:
            # Skip this entry if the id is not a number
            continue
        if current_id == int(article_id) and article.get("category") == category:
            return article
    return None


def list_articles(category):
    # Return a list of articles filtered by category from the metadata file.
    metadata_file = os.path.join(ARTICLES_DIR, "metadata", "metadata.json")
    if not os.path.exists(metadata_file):
        return []
    with open(metadata_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Return only articles that match the given category
    return [article for article in data.get("articles", []) if article.get("category") == category]


# Article API and Page Routes

@app.route('/api/article/<category>/<article_id>', methods=['GET'])
def get_article_content(category, article_id):
    article = fetch_article_metadata(category, article_id)
    if not article:
        return jsonify({"error": "Article not found"}), 404

    try:
        # Open the Markdown file instead of a plain text file
        with open(article["content_file"], "r", encoding="utf-8") as f:
            md_content = f.read()
    except FileNotFoundError:
        return jsonify({"error": "Content file not found"}), 404

    # Convert Markdown to HTML
    html_content = markdown.markdown(md_content)
    
    return jsonify({
        "id": article["id"],
        "title": article["title"],
        "content": html_content,
        "date_published": article["date_published"],
        "category": article.get("category", category)
    })


@app.route('/article/<category>/<article_id>')
def show_article(category, article_id):
    article = fetch_article_metadata(category, article_id)
    if not article:
        return "Artikkel ikke funnet", 404

    # Construct the full file path
    content_path = os.path.join(ARTICLES_DIR, article["content_file"])
    print("Loading content from:", content_path)  # Debug print

    try:
        with open(content_path, "r", encoding="utf-8") as f:
            md_content = f.read()
    except FileNotFoundError as fnf_error:
        print("Content file not found:", fnf_error)
        return "Innhold ikke funnet", 404
    except Exception as e:
        print("Error loading content:", e)
        return "Noe gikk galt med å laste artikkelen", 500

    # Convert the Markdown content to HTML
    article["content"] = markdown.markdown(md_content)

    try:
        return render_template("nyheter/forsideNyhet.html", article=article)
    except Exception as e:
        print("Error rendering template:", e)
        return "Feil med å vise artikkelen", 500



@app.route('/get_articles/<category>', methods=['GET'])
def get_articles(category):
    articles = list_articles(category)
    return jsonify(articles)

@app.route('/')
def home():
    # Render the home page with articles from a default category (e.g., "krim")
    articles = list_articles("krim")
    return render_template('main.html', articles=articles)

@app.route('/log_in', methods=['GET'] )
def log_in():
    return render_template('login.html')

@app.route('/sign_up')
def sign_up():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
