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
@click.option(
    "verbose",
    "--verbose",
    "-v",
    is_flag=True,
    help="Verbose output",
)
def main(file: click.File("r"), verbose: bool) -> None:
    with open("export.csv", "w") as csv_file:
        data = json.load(file)
        writer = csv.writer(csv_file)
        writer.writerow(
            [
                "folder",
                "favorite",
                "type",
                "name",
                "notes",
                "fields",
                "reprompt",
                "login_uri",
                "login_username",
                "login_password",
                "login_totp",
            ]
        )

        for account in data["accounts"]:
            print(f"Processing account: {account['attrs']['name']}")

            for vault in account["vaults"]:
                folder = vault["attrs"]["name"]
                print(f"Processing folder: {folder}")

                for item in vault["items"]:
                    # 1Password sometimes nests an item inside an item
                    if hasattr(item, "item"):
                        item = item["item"]

                    # Root level items
                    favorite = item["favIndex"] if hasattr(item, "favIndex") else 0

                    # Overview Subsection
                    overview = item["overview"]
                    name = overview["title"]
                    login_uri = overview["url"]

                    if verbose:
                        print(f"Processing item: {name}")

                    # Details Subsection
                    details = item["details"]
                    notes = details["notesPlain"] if "notesPlain" in details else None

                    login_username, login_password = None, None
                    for field in details["loginFields"]:
                        if "designation" not in field:
                            continue
                        if field["designation"] == "username":
                            login_username = field["value"]
                        if field["designation"] == "password":
                            login_password = field["value"]

                    login_totp = None
                    for section in details["sections"]:
                        fields = section["fields"]
                        if len(fields) == 0:
                            continue
                        for field in fields:
                            value = field["value"]
                            login_totp = value["totp"] if "totp" in value else None

                    writer.writerow(
                        [
                            folder,
                            favorite,
                            "login",
                            name,
                            notes,
                            None,
                            0,
                            login_uri,
                            login_username,
                            login_password,
                            login_totp,
                        ]
                    )
