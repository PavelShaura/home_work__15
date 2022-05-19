import sqlite3
from flask import Flask, jsonify


def main():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config['DEBUG'] = True

    def get_animal(query):
        con = sqlite3.connect("animal.db")
        cur = con.cursor()
        cur.execute(query)
        data = cur.fetchall()
        con.close()
        return data

    @app.route('/id/<uid>')
    def search_by_id(uid):
        query = f"""
                 SELECT 
                     animals_final.id,
                     animals_final.outcome_id
                 FROM animals_final
                 WHERE animals_final.id = {uid}
                 """
        response = get_animal(query)[0]
        response_json = {
            'animals_final.id': response[0],
            'animals_final.outcome_id': response[1],
        }
        return jsonify(response_json)

    app.run()


if __name__ == '__main__':
    main()
