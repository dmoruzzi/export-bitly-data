import argparse
import json
import sqlite3
from pathlib import Path
from itertools import count


def main(args):
    if not (args.export_json or args.export_sqlite):
        args.export_json = True

    har_file = args.input or get_bitly_har()
    page_data = read_har_file(har_file)

    if args.export_json:
        output_json = args.output_json or generate_export_filename(
            filename="export", extension="json"
        )
        write_export_json(page_data, output_json)

    if args.export_sqlite:
        output_sqlite = args.output_sqlite or generate_export_filename(
            filename="export", extension="db"
        )
        write_export_sqlite(page_data, output_sqlite)


def generate_export_filename(extension, filename="export"):
    base_file = Path(filename).with_suffix(f".{extension}")

    if not base_file.exists():
        return base_file

    new_file = next(
        base_file.with_name(f"{filename}_{index}.{extension}")
        for index in count(1)
        if not base_file.with_name(f"{filename}_{index}.{extension}").exists()
    )

    return new_file


def get_bitly_har():
    files = list(Path().glob("app.bitly.com*.har"))
    if len(files) != 1:
        raise ValueError("Expected exactly one .har file")
    return files[0]


def read_har_file(file_path):
    with open(file_path, "r", encoding="utf-8") as har_file_fp:
        return json.load(har_file_fp)


def write_export_json(page_data, export_file):
    export_json = []

    for entry in page_data["log"]["entries"]:
        if "bitlinks" in entry["request"]["url"]:
            content = json.loads(entry["response"]["content"]["text"])
            for link in content.get("links", []):
                try:
                    title = link.get("title", "")
                    short_link = link["link"]
                    long_link = link["long_url"]
                    date = link["created_at"]
                    export_json.append(
                        {
                            "title": title,
                            "shortLink": short_link,
                            "longLink": long_link,
                            "date": date,
                        }
                    )
                except KeyError as e:
                    print(f"Error parsing link: {e}")

    with open(export_file, "w") as export_file_fp:
        json.dump(export_json, export_file_fp)


def write_export_sqlite(page_data, export_file, table="redirects"):
    conn = sqlite3.connect(export_file)
    c = conn.cursor()
    c.execute(
        f"""CREATE TABLE IF NOT EXISTS {table}
                 (title TEXT, shortLink TEXT, longLink TEXT, date TEXT)"""
    )

    for entry in page_data["log"]["entries"]:
        if "bitlinks" in entry["request"]["url"]:
            content = json.loads(entry["response"]["content"]["text"])
            for link in content.get("links", []):
                try:
                    title = link.get("title", "")
                    short_link = link["link"]
                    long_link = link["long_url"]
                    date = link["created_at"]
                    c.execute(
                        f"INSERT INTO {table} VALUES (?, ?, ?, ?)",
                        (title, short_link, long_link, date),
                    )
                except KeyError as e:
                    print(f"Error parsing link: {e}")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process HAR file from Bitly to export short link data."
    )
    parser.add_argument("-i", "--input", type=str, help="Input HAR file path.")
    parser.add_argument(
        "--export-json", action="store_true", help="Export to JSON format."
    )
    parser.add_argument(
        "--export-sqlite", action="store_true", help="Export to SQLite format."
    )
    parser.add_argument("--output-json", type=str, help="Output JSON file path.")
    parser.add_argument("--output-sqlite", type=str, help="Output SQLite file path.")
    args = parser.parse_args()

    main(args)
