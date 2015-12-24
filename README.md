# RelEx: Relationship Explainer Using Knowledge Base

Given a pair of objects, people are often interested to know if they are related and how they are related. For the purpose of better solving such problems, in this project we build a prototype system for explaining relationships between two objects from general domains. The system is powered by a large knowledge base (YAGO), has a clean user interface, and demonstrates useful relationships in an organized and intuitive manner.

The software does not include the Neo4j database, which has to be download separately. In addition, the system requires a Python interpreter for execution. Python 3 is preferred. All other components are included. By default, the system uses YAGO core data, but more data can be downloaded from http://www.mpi-inf.mpg.de/departments/databases-and-information-systems/research/yago-naga/yago/downloads.

## Setup
To setup and use the system, follow the steps below:

1. Download and setup Neo4j graph database. Start the database service by "bin/neo4j start".
2. Configure database credentials in the code directory.
3. Extract and import knowledge base data by "python3 code/parser.py < data/yagoFacts.tsv".
4. Start the app by "python3 code/relex.py".

## Usage

Now the web application is served at http://localhost:8080 (The url and port can also be configured). A clean interface will be shown in the browser. Users can simply type two objects of interest into the form and then click "Explain". Then the system will generate relationship results and display them in an organized manner. The user can also drag the nodes themselves to further adjust the layouts.
