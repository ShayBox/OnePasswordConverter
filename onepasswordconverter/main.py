import csv
import json

import click


# Append index to duplicated keys
# https://stackoverflow.com/a/29323197
def fix_dup_keys(ordered_pairs):
    index = 0
    dictionary = {}
    for key, value in ordered_pairs:
        if key in dictionary:
            dictionary[key + str(index)] = value
            index += 1
        else:
            dictionary[key] = value
    return dictionary


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
    help="Verbose output (WARNING! Prints passwords to stdout)",
)
def main(file: click.File("r"), verbose: bool) -> None:
    with open("export.csv", "w") as csv_file:
        data = json.load(file, object_pairs_hook=fix_dup_keys)
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

                # 1Password sometimes nests an item inside an item
                iterable = vault["items"]
                if "item" in iterable[0]:
                    iterable = iterable[0].values()

                for item in iterable:
                    if verbose:
                        print(item)
                        print("\033[93mWARNING! This is a verbose output!\033[0m")
                        print("\033[93mThere may be private information in this output!\033[0m")
                        print("\033[93mRemove any sensitive information before sharing!\033[0m")

                    # Root level items
                    favorite = item["favIndex"] if "favIndex" in item else 0

                    # Overview Subsection
                    overview = item["overview"]
                    name = overview["title"]
                    login_uri = overview["url"]

                    # Details Subsection
                    details = item["details"] if "details" in item else {}
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
