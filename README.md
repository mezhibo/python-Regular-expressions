 ""Домашнее задание «Регулярные выражения»"""

 ```
 from pprint import pprint
import csv
import re

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

pprint(contacts_list)

# шаблон для телефона
phone_pattern = re.compile(
    r"(\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(?:\s*\(?доб\.?\s*(\d+)\)?)?"
)

def normalize_phone(phone):
    return phone_pattern.sub(r"+7(\2)\3-\4-\5 доб.\6", phone).replace(" доб.None", "")

# отделяем заголовок
header = contacts_list[0]
contacts = contacts_list[1:]

# 1. Приводим ФИО и телефоны к нужному виду
for contact in contacts:
    fio = " ".join(contact[:3]).split()
    contact[:3] = (fio + ["", "", ""])[:3]
    contact[5] = normalize_phone(contact[5])

# 2. Объединяем дубли по Фамилии и Имени
unique_contacts = {}

for contact in contacts:
    key = (contact[0], contact[1])  # lastname, firstname

    if key not in unique_contacts:
        unique_contacts[key] = contact
    else:
        saved_contact = unique_contacts[key]
        for i in range(len(contact)):
            if saved_contact[i] == "" and contact[i] != "":
                saved_contact[i] = contact[i]

# итоговый список
contacts_list = [header] + list(unique_contacts.values())

pprint(contacts_list)

# сохраняем в CSV
with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)
 ```
