import sqlite3


def sql_connect(query):
    con = sqlite3.connect("animal.db")
    cur = con.cursor()
    cur.execute(query)
    data = cur.fetchall()
    con.close()
    return data


def main():
    query = (
        """
             CREATE TABLE IF NOT EXISTS colors (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             color VARCHAR(50)
             )
             """
    )
    print(sql_connect(query))
    query_1 = (
        """
             CREATE TABLE IF NOT EXISTS animals_colors (
             animals_id INTEGER,
             colors_id INTEGER,
             FOREIGN KEY (animals_id) REFERENCES animals("index"),
             FOREIGN KEY (colors_id) REFERENCES colors("id")
             )
             """
    )
    print(sql_connect(query_1))
    query_2 = (
             """
             INSERT INTO colors (color)
             SELECT DISTINCT * FROM (
                 SELECT DISTINCT
                     color1 AS color
                 FROM animals
                 UNION ALL 
                 SELECT DISTINCT
                     color2 AS color
                 FROM animals)
             """
    )
    print(sql_connect(query_2))
    query_3 = (
             """
             INSERT INTO animals_colors (animals_id, colors_id)
             SELECT DISTINCT
                 animals."index", colors.id
             FROM animals
             JOIN colors
                 ON colors.color = animals.color1
             UNION ALL
             SELECT DISTINCT
                 animals."index", colors.id
             FROM animals
             JOIN colors
                 ON colors.color = animals.color2
             """
    )
    print(sql_connect(query_3))
    query_3_1 = (
             """
             INSERT INTO animals_colors (animals_id, colors_id)
             SELECT DISTINCT
                 animals_final.id, colors.id
             FROM animals
             JOIN colors
             ON colors.color = animals.color1
             JOIN animals_final
             ON animals_final.animal_id = animals.animal_id
             UNION ALL
             SELECT DISTINCT
                 animals_final.id, colors.id
             FROM animals
             jOIN colors
                 ON colors.color = animals.color2
             JOIN animals_final
                 ON animals_final.animal_id = animals.animal_id
             """
    )
    print(sql_connect(query_3_1))
    query_4 = (
        """
             CREATE TABLE IF NOT EXISTS outcome (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             subtype VARCHAR(50),
             "type" VARCHAR(50),
             "month" INTEGER,
             "year" INTEGER
             )
             """
    )
    print(sql_connect(query_4))
    query_5 = (
        """
        INSERT INTO outcome (subtype, "type", "month", "year")
        SELECT DISTINCT
            animals.outcome_subtype, 
            animals.outcome_type,
            animals.outcome_month,
            animals.outcome_year
        FROM animals
        """
    )
    print(sql_connect(query_5))
    query_6 = (
        """
        CREATE TABLE IF NOT EXISTS animals_final (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age_upon_outcome VARCHAR(50),
        animal_id VARCHAR(50),
        animal_type VARCHAR(50),
        name VARCHAR(50),
        breed VARCHAR(50),
        date_of_birth VARCHAR(50),
        outcome_id INTEGER,
        FOREIGN KEY (outcome_id) REFERENCES outcome("id")
        )
        """
    )
    print(sql_connect(query_6))
    query_7 = (
        """
        INSERT INTO animals_final (age_upon_outcome, animal_id, animal_type, name, breed, date_of_birth, outcome_id)
        SELECT
            animals.age_upon_outcome, animals.animal_id, animals.animal_type, animals.name, animals.breed, 
            animals.date_of_birth, outcome_id
        FROM animals
        JOIN outcome
            ON outcome.subtype = animals.outcome_subtype 
            AND outcome."type" = animals.outcome_type
            AND outcome."month" = animals.outcome_month
            AND outcome."year" = animals.outcome_year
        """
    )
    print(sql_connect(query_7))


if __name__ == '__main__':
    main()
