import click
import csv
import json


@click.command()
@click.option(
    "file",
    "--file",
    "-f",
    default="export.data",
    help="JSON file to convert",
    prompt="Which file?",
    type=click.File("r"),
)
def main(file):
    data = json.load(file)
    for account in data["accounts"]:
        print(f"Processing account: {account['attrs']['name']}")
        for vault in account["vaults"]:
            vault_name = vault["attrs"]["name"]
            print(f"Processing vault: {vault_name}")
            with open(f"{vault_name}.csv", "w") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Title", "URL", "Username", "Password"])
                for item in vault["items"]:
                    item = item["item"]
                    overview = item["overview"]
                    title = overview["title"]
                    url = overview["url"]
                    print(f"Processing item: {title}")
                    username, password = None, None
                    for field in item["details"]["loginFields"]:
                        if "designation" not in field:
                            continue
                        if field["designation"] == "username":
                            username = field["value"]
                        if field["designation"] == "password":
                            password = field["value"]
                    writer.writerow([title, url, username, password])
