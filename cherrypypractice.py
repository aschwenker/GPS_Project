import psycopg2
import json
import cherrypy


class brooklynadoptedtreetypes(object):
    def brooklynadoptedtreetypes(self,route='K082'):
        pgcnxn = psycopg2.connect(host="localhost", database="AKSchwenker", user="postgres", password="postgres")
        cursor = pgcnxn.cursor()

        query = "SELECT St_asgeojson(geom) FROM nov16_joined WHERE route LIKE '%"+route+"'"
        cursor.execute(query)
        rows = cursor.fetchall()

        results = { "type": "FeatureCollection",
                "features": [] }

        for row in rows:
            s = row[0]
            obj = json.loads(s)
            results["features"].append({ "type": "Feature", "geometry": obj, "properties": { "tree_species": int(row[2])} })
        print (json.dumps(results))

    brooklynadoptedtreetypes.exposed= True

cherrypy.quickstart(brooklynadoptedtreetypes())
