from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

DB_PATH = "CarsDB.db"

def get_db(db, query, params=()):
    # Åbn forbindelsen. Row gør det muligt at bruge feltnavne i HTML-templaten.
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row

    # En cursor kører SQL-forespørgslen; fetchall() henter alle dens rækker.
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()

    # Luk cursor og forbindelse, og giv rækkerne tilbage til forsiden.
    cur.close()
    conn.close()
    return rows

@app.route("/", methods=["GET", "POST"])
def frontpage():
    cars = get_db(DB_PATH, "SELECT model, year FROM cars ORDER BY id")
    if request.method == "POST":
        search_term = request.form.get("search_term", "")
        app.logger.info(f"Search term received: {search_term}")
        return db_search(search_term)

    # Send rækkerne til HTML-templaten under navnet Cars.
    return render_template("index.html", cars=cars)

@app.route("/search", methods=["GET", "POST"])
def search_page():
    # POST request: do search
    if request.method == "POST":
        search_term = request.form.get("search_term", "")
        return db_search(search_term)
    # GET request: show search form
    return render_template("index.html", title="Search Page", members=[])

def db_search(search_term):
    # Perform a search in the database with the LIKE operator
    data = get_db(
        DB_PATH,
        "SELECT * FROM Cars WHERE model LIKE ?",
        ('%' + search_term + '%',),
    )
    cars = {"cars": [dict(u) for u in data]}
    app.logger.info(f"Search results for '{search_term}': {cars}")
    return render_template("index.html", title="Search Results", cars=cars['cars'])
# Start Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
