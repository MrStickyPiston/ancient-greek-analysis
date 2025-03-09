import requests
import sys
import os


HEADERS = {
    "User-Agent": "AncientGreekAnalysisBot/0.1 (https://github.com/MrStickyPiston/ancient-greek-analysis; https://mrstickypiston.is-a.dev/contact)"
}


def list_pages(category):
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": category,
        "cmtype": "page",
        "cmlimit": "500",
        "format": "json",
    }

    session = requests.Session()
    pages = []
    continue_params = {}

    while True:
        query_params = params.copy()
        query_params.update(continue_params)

        response = session.get('https://en.wiktionary.org/w/api.php', params=query_params, headers=HEADERS)
        data = response.json()

        category_members = data.get("query", {}).get("categorymembers", [])

        # Save each pageid as a string
        for member in category_members:
            if member["title"].startswith("Unsupported titles"):
                continue
            pages.append(member["title"].replace(" ", "_"))

        print(f"\rLoading {category}: {len(pages)} pages found", end="")

        # Check if there is a continuation token for more results
        if "continue" in data:
            continue_params = data["continue"]
        else:
            break  # No further data

    print()

    return pages

def main(category, folder):
    pages = list_pages(category)

    os.makedirs(folder, exist_ok=True)

    with open(folder + "index.txt", 'w') as f:
        f.writelines("\n".join(pages))

    s = requests.Session()

    for i, page in enumerate(pages):
        print(f"\rProgress for {category}: {i+1}/{len(pages)}", end="")

        if os.path.exists(f"{folder}{page}.html") and os.path.getsize(f"{folder}{page}.html") > 0:
            continue

        with open(f"{folder}{page}.html", 'w') as f:
            r = s.get(f'https://en.wiktionary.org/w/api.php?action=parse&page={page}&format=json', headers=HEADERS)
            r.raise_for_status()
            f.write(r.json()['parse']['text']['*'])
    print()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])