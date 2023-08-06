import requests


weblate_host = ""  # https://weblate_host.com/
token = ""  # api token


headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
}


def enable_suggestions_on_all_components():
    response = requests.get(f"{weblate_host}/api/components/", headers=headers)
    component_list = []
    while True:
        components = response.json()
        next_page = components["next"]
        for component in components["results"]:
            name = component["name"]
            component_list.append(name)
        if next_page:
            response = requests.get(next_page.replace("http", "https"), headers=headers)
            print(next_page)
        else:
            break

    for component in component_list:
        data = '{"enable_suggestions": "on"}'
        component = component.replace(".", "").lower()
        response = requests.patch(f"{weblate_host}/api/components/dqx/{component}/", data=data, headers=headers)
        if response.status_code == 404:
            print(response.text)
        print(component)


def get_number_of_suggestions():
    response = requests.get(f"{weblate_host}/api/projects/dqx/statistics/", headers=headers)
    return response.json()["suggestions"]

enable_suggestions_on_all_components()
