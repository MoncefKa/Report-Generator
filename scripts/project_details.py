import requests as rq
import os
import json as js
from dotenv import load_dotenv
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

load_dotenv()

# Configuration
PATH_QUERY = "../GraphQL/projects.graphql"  # Ensure this file exists
URL = "https://api.github.com/graphql"
TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    raise ValueError("GITHUB_TOKEN not found in environment variables.")

HEADER = {
    "user-agent": "MoncefKa",
    "authorization": f"Bearer {TOKEN}",
    "accept": "application/vnd.github.v3+json"
}
VARIABLES = {
    "org": 'Liebert-Industries-LLC',
    "number": 3
}

def get_organization_project(query_path):
    try:
        with open(query_path, 'r') as query_file:
            query_ = query_file.read()

        fetch_url = RequestsHTTPTransport(url=URL, headers=HEADER)
        client = Client(transport=fetch_url, fetch_schema_from_transport=True)
        return client.execute(gql(query_), variable_values=VARIABLES)

    except Exception as e:
        raise RuntimeError(f"Error executing GraphQL query: {e}")

def to_json(data, file_path):
    try:
        json_dump = js.dumps(data, skipkeys=False)
        with open(file_path, 'w') as file_handle:
            file_handle.write(json_dump)
    except Exception as e:
        raise IOError(f"Error writing JSON to file: {e}")


try:
    retrieve_data = get_organization_project(PATH_QUERY)

    if not os.path.exists("../data/"):
        os.mkdir("../data/")

    file_path = "../data/github_data.json"
    to_json(retrieve_data, file_path)

    print(f"Data successfully written to {file_path}")

except Exception as e:
    print(f"An error occurred: {e}")
