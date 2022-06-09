#!/usr/bin/env python3

import os
import sys

import click
from simple_rest_client.api import API

YOUTRACK_API_URL = os.getenv("YOUTRACK_API_URL")
assert YOUTRACK_API_URL, "YOUTRACK_API_URL not set"
YOUTRACK_API_TOKEN = os.getenv("YOUTRACK_API_TOKEN", None)
assert (
    YOUTRACK_API_TOKEN
), "Make sure to set a youtrack token to the YOUTRACK_API_TOKEN environment variable"


def get_project_id(api):
    api.add_resource(api_root_url=(YOUTRACK_API_URL + "admin/"), resource_name="projects")
    r = api.projects.list(params={"fields": "id,name,shortName"})
    project = next(filter(lambda x: x["name"] == "Memfault", r.body))
    return project["id"], project["shortName"]


def main():
    assert len(sys.argv) == 3, 'Usage: youtrack.py "<Project name>" "<Issue title>"'
    project_name = sys.argv[1]
    title = sys.argv[2]

    # create api instance
    api = API(
        api_root_url=YOUTRACK_API_URL,
        headers={"Authorization": f"Bearer {YOUTRACK_API_TOKEN}"},
        json_encode_body=True,
    )

    # get project id
    project_id, project_shortname = get_project_id(api)
    print(f"Found project id: {project_id}")
    print(f"Found project shortname: {project_shortname}")

    # create a new issue with the title from the command line
    api.add_resource(resource_name="issues")
    r = api.issues.retrieve(f"{project_shortname}-4493")
    print(r)


if __name__ == "__main__":
    main()
