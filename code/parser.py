import fileinput
from py2neo import authenticate, Graph

authenticate("localhost:7474", "neo4j", "neo4j")
graph = Graph("http://localhost:7474/db/data/")

def parse():
    # create index on name property of type Thing
    graph.cypher.execute("CREATE INDEX ON :Thing(name)")

    # parse tsv from stdin
    for line in fileinput.input():
        if fileinput.isfirstline():
            continue        # skip header
        record = line.split()
        a_name = record[1].strip("<>").replace("_", " ")        # node 1
        r_name = record[2].strip("<>")                          # relationship
        b_name = record[3].strip("<>").replace("_", " ")        # node 2

        # echo process
        print(a_name, r_name, b_name)

        # inject into database
        graph.cypher.execute("MERGE (a:Thing {name: {name}})", {"name": a_name})
        graph.cypher.execute("MERGE (b:Thing {name: {name}})", {"name": b_name})
        graph.cypher.execute(
            "MATCH (a:Thing {name: {a_name}}), (b:Thing {name: {b_name}}) "
            "MERGE (a)-[:" + r_name + "]->(b)",
            {"a_name": a_name, "b_name": b_name}
        )

if __name__ == "__main__":
    parse()
