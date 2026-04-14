from __future__ import annotations

import csv
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RAW_FILE = BASE_DIR / "phonebook_raw.csv"
RESULT_FILE = BASE_DIR / "phonebook.csv"

PHONE_PATTERN = re.compile(
    r"(?:\+7|8)\s*"
    r"\(?([0-9]{3})\)?[\s-]*"
    r"([0-9]{3})[\s-]*"
    r"([0-9]{2})[\s-]*"
    r"([0-9]{2})"
    r"(?:\s*(?:\(?доб\.?\s*|доб\.?\s*\(?)([0-9]+)\)?)?"
)


def normalize_fio(contact: list[str]) -> list[str]:
    fio_parts = " ".join(contact[:3]).split()
    contact[:3] = (fio_parts + ["", "", ""])[:3]
    return contact


def normalize_phone(phone: str) -> str:
    if not phone:
        return ""

    def repl(match: re.Match[str]) -> str:
        area, first, second, third, ext = match.groups()
        formatted = f"+7({area}){first}-{second}-{third}"
        if ext:
            formatted += f" доб.{ext}"
        return formatted

    return PHONE_PATTERN.sub(repl, phone)


def merge_contacts(contacts: list[list[str]]) -> list[list[str]]:
    merged: dict[tuple[str, str], list[str]] = {}

    for contact in contacts:
        key = (contact[0], contact[1])
        if key not in merged:
            merged[key] = contact
            continue

        saved_contact = merged[key]
        for index, value in enumerate(contact):
            if not saved_contact[index] and value:
                saved_contact[index] = value

    return list(merged.values())


def main() -> None:
    with RAW_FILE.open(encoding="utf-8") as file:
        rows = csv.reader(file)
        contacts_list = list(rows)

    header, contacts = contacts_list[0], contacts_list[1:]

    prepared_contacts = []
    for contact in contacts:
        contact = normalize_fio(contact)
        contact[5] = normalize_phone(contact[5])
        prepared_contacts.append(contact)

    result = [header] + merge_contacts(prepared_contacts)

    with RESULT_FILE.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(result)


if __name__ == "__main__":
    main()
