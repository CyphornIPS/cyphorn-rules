#!/usr/bin/env python3

import argparse
import hashlib
import json
import mimetypes
from datetime import datetime, timezone
from pathlib import Path


CHUNK_SIZE = 1024 * 1024  # 1 MiB

SCHEMA_VERSION = 1
SOURCE = "generate_intel_py"


def calculate_hashes(file_path):
    """Calculate MD5, SHA-1, SHA-256 and SHA3-384 hashes."""

    hashes = {
        "md5": hashlib.md5(),
        "sha1": hashlib.sha1(),
        "sha256": hashlib.sha256(),
        "sha3_384": hashlib.sha3_384(),
    }

    with file_path.open("rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            for hash_object in hashes.values():
                hash_object.update(chunk)

    return {
        "sha256_hash": hashes["sha256"].hexdigest(),
        "sha3_384_hash": hashes["sha3_384"].hexdigest(),
        "sha1_hash": hashes["sha1"].hexdigest(),
        "md5_hash": hashes["md5"].hexdigest(),
    }


def detect_mime(file_path):
    """Detect MIME type based on the file extension."""

    mime_type, _ = mimetypes.guess_type(file_path.name)

    if mime_type is None:
        mime_type = "application/octet-stream"

    return mime_type


def generate_record(file_path, tags):
    """Generate a CyphornIPS File Intelligence record."""

    hashes = calculate_hashes(file_path)

    return {
        **hashes,
        "file_name": file_path.name,
        "file_type_mime": detect_mime(file_path),
        "tags": tags,
    }


def create_database():
    """Create a new CyphornIPS File Intelligence database."""

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": SOURCE,
        "records": []
    }


def load_database(output_path):
    """
    Load existing CyphornIPS File Intelligence database.

    Expected format:

    {
        "schema_version": 1,
        "generated_at": "...",
        "source": "...",
        "records": [
            {
                "sha256_hash": "...",
                ...
            }
        ]
    }
    """

    if not output_path.exists():
        print("Database does not exist. Creating a new database.")
        return create_database()

    try:
        with output_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"Error: Invalid JSON file: {output_path}\n{exc}"
        )

    if not isinstance(data, dict):
        raise SystemExit(
            "Error: File Intelligence database must be a JSON object."
        )

    # ---------------------------------------------------------
    # Ensure schema_version exists
    # ---------------------------------------------------------

    if "schema_version" not in data:
        data["schema_version"] = SCHEMA_VERSION

    # ---------------------------------------------------------
    # Ensure generated_at exists
    # ---------------------------------------------------------

    if "generated_at" not in data:
        data["generated_at"] = datetime.now(
            timezone.utc
        ).isoformat()

    # ---------------------------------------------------------
    # Ensure source exists
    # ---------------------------------------------------------

    if "source" not in data:
        data["source"] = SOURCE

    # ---------------------------------------------------------
    # Ensure records exists
    # ---------------------------------------------------------

    if "records" not in data:
        data["records"] = []

    # ---------------------------------------------------------
    # Validate header fields
    # ---------------------------------------------------------

    if not isinstance(data["schema_version"], int):
        raise SystemExit(
            "Error: 'schema_version' must be an integer."
        )

    if not isinstance(data["generated_at"], str):
        raise SystemExit(
            "Error: 'generated_at' must be a string."
        )

    if not isinstance(data["source"], str):
        raise SystemExit(
            "Error: 'source' must be a string."
        )

    if not isinstance(data["records"], list):
        raise SystemExit(
            "Error: 'records' must be a list."
        )

    return data


def add_indicator(database, record):
    """
    Add a new indicator.

    Duplicate detection is based on SHA-256.
    """

    new_sha256 = record["sha256_hash"].lower()

    for existing_record in database["records"]:

        existing_sha256 = existing_record.get(
            "sha256_hash"
        )

        if existing_sha256:
            if existing_sha256.lower() == new_sha256:
                return False

    database["records"].append(record)

    return True


def save_database(output_path, database):
    """Save the CyphornIPS File Intelligence database."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(
            database,
            f,
            indent=2,
            ensure_ascii=False
        )
        f.write("\n")


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Generate and maintain "
            "CyphornIPS File Intelligence JSON"
        )
    )

    parser.add_argument(
        "file",
        help="Path to the file"
    )

    parser.add_argument(
        "--tag",
        action="append",
        dest="tags",
        default=[],
        help=(
            "Add a tag. "
            "Can be used multiple times."
        )
    )

    parser.add_argument(
        "-o",
        "--output",
        default="output/file-intelligence.json",
        help=(
            "Output database "
            "(default: output/file-intelligence.json)"
        )
    )

    args = parser.parse_args()

    file_path = Path(args.file)
    output_path = Path(args.output)

    # ---------------------------------------------------------
    # Validate input file
    # ---------------------------------------------------------

    if not file_path.is_file():
        parser.error(
            f"File not found: {file_path}"
        )

    # ---------------------------------------------------------
    # Generate record
    # ---------------------------------------------------------

    record = generate_record(
        file_path,
        args.tags
    )

    # ---------------------------------------------------------
    # Load or create database
    # ---------------------------------------------------------

    database = load_database(
        output_path
    )

    # ---------------------------------------------------------
    # Add indicator
    # ---------------------------------------------------------

    added = add_indicator(
        database,
        record
    )

    if not added:

        print()
        print("=" * 60)
        print("CyphornIPS File Intelligence")
        print("=" * 60)
        print("Indicator already exists.")
        print()
        print(f"File:   {file_path.name}")
        print(
            f"SHA256: {record['sha256_hash']}"
        )
        print()
        print(
            f"Total records: "
            f"{len(database['records'])}"
        )
        print("=" * 60)
        print()

        return

    # ---------------------------------------------------------
    # Update generated_at
    # ---------------------------------------------------------

    database["generated_at"] = (
        datetime.now(timezone.utc).isoformat()
    )

    # ---------------------------------------------------------
    # Save database
    # ---------------------------------------------------------

    save_database(
        output_path,
        database
    )

    # ---------------------------------------------------------
    # Display results
    # ---------------------------------------------------------

    print()
    print("=" * 60)
    print("CyphornIPS File Intelligence")
    print("=" * 60)

    print(f"Database: {output_path}")
    print(f"Schema:   {database['schema_version']}")
    print(f"Source:   {database['source']}")
    print(f"File:     {file_path.name}")
    print(
        f"Size:     "
        f"{file_path.stat().st_size} bytes"
    )
    print(
        f"MIME:     "
        f"{record['file_type_mime']}"
    )

    print()

    print(
        f"SHA256:   "
        f"{record['sha256_hash']}"
    )

    print(
        f"SHA3-384: "
        f"{record['sha3_384_hash']}"
    )

    print(
        f"SHA1:     "
        f"{record['sha1_hash']}"
    )

    print(
        f"MD5:      "
        f"{record['md5_hash']}"
    )

    print()

    print(
        f"Tags:     "
        f"{', '.join(args.tags) if args.tags else '(none)'}"
    )

    print()

    print(
        f"Total records: "
        f"{len(database['records'])}"
    )

    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
