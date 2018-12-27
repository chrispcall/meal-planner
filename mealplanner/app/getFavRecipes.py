from app import db
from sqlalchemy import text

def get_favs():
    sql = text("""SELECT url, COUNT(url) AS value_occurrence
    FROM post
    GROUP BY url
    ORDER BY value_occurrence DESC
    LIMIT 6;""")

    result = db.engine.execute(sql)
 
    output = []
    for i in result:
        output.append(i[0])

    return output
