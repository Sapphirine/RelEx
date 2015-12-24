from bottle import request, route, run, static_file
from py2neo import authenticate, Graph

authenticate("localhost:7474", "neo4j", "neo4j")
graph = Graph("http://localhost:7474/db/data/")

# user interface
@route('/')
def homepage():
    return static_file("index.html", root=".")

# main logic of the web app
@route('/path')
def path():
    try:
        a_name = request.query["obj1"].strip()
        b_name = request.query["obj2"].strip()
    except KeyError:
        return []
    else:
        # no empty input
        if len(a_name) == 0 or len(b_name) == 0:
            return []

        # query database
        results = graph.cypher.execute(
            "MATCH path = (a:Thing)-[*1..4]-(b:Thing)"
            "WHERE a.name = {object1} AND b.name = {object2}"
            "RETURN path",
            {"object1": a_name, "object2": b_name}
        )

        # result json
        nodes = []
        edges = []

        # add two endpoints
        nodes.append({"name": a_name, "x": 100, "y": 300, "fixed": "true"})
        nodes.append({"name": b_name, "x": 900, "y": 300, "fixed": "true"})
        node_map = dict()
        node_map[a_name] = 0
        node_map[b_name] = 1

        # vertical padding
        padding_y = 600/(len(results) + 1)
        current_y = 0

        # construct result
        for record in results:
            current_y += padding_y

            # horizontal padding
            padding_x = 800/len(record.path.relationships)
            current_x = 100

            for rel in record.path.relationships:
                current_x += padding_x
                s = rel.start_node;
                e = rel.end_node;
                if s.properties["name"] not in node_map:
                    node_map[s.properties["name"]] = len(nodes)
                    nodes.append({"name": s.properties["name"], "x": current_x, "y": current_y, "fixed": "true"})
                if e.properties["name"] not in node_map:
                    node_map[e.properties["name"]] = len(nodes)
                    nodes.append({"name": e.properties["name"], "x": current_x, "y": current_y, "fixed": "true"})
                edges.append({"source": node_map[s.properties["name"]],
                              "target": node_map[e.properties["name"]],
                              "name": rel.type})

        return {"nodes": nodes, "edges": edges}

if __name__ == "__main__":
    run(host='localhost', port=8080)
