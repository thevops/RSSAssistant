import sys
from todoist_api_python.api import TodoistAPI


def get_todoist_ids(token):
    api = TodoistAPI(token)

    projects = api.get_projects()
    for project in projects:
        print(f"Project name: {project.name} | ID: {project.id}")
        sections = api.get_sections(project_id=project.id)
        for section in sections:
            print(f"\tSection name: {section.name} | ID: {section.id}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        token = sys.argv[1]
    else:
        token = input("Enter Todoist token: ")

    get_todoist_ids(token)
