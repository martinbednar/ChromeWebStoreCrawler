#!/usr/bin/env python3

# Author: Martin Bednar (2024)

liborContacts = {}

for line in open("LiborContacts.csv", "r", encoding="utf-8"):
    email, _, extnames = line.split(";")
    email = email.strip().lower()
    extnames = extnames.strip()
    if email in liborContacts:
        liborContacts[email] += extnames.split(",")
    else:
        liborContacts[email] = extnames.split(",")


martinContactsOrigin = {}
martinContacts = {}
header_line = False

intersectionContacts = {}

for line in open("PrivacyAndSecurityExtensionsEmails.csv", "r", encoding="utf-8"):
    if not header_line:
        header_line = line.rstrip().split(';')
        continue
    line_arr = line.strip().split(";")
    extname, emails = line_arr[0], line_arr[1:]
    extname = extname.strip()
    martinContactsOrigin[extname] = emails

    for email in emails:
        email = email.lower()
        if email in liborContacts:
            if email in intersectionContacts:
                intersectionContacts[email] += [extname]
            else:
                intersectionContacts[email] = liborContacts[email] + [extname]
            liborContacts.pop(email, None)
        else:
            if email not in intersectionContacts:
                if email in martinContacts:
                    martinContacts[email] += [extname]
                else:
                    martinContacts[email] = [extname]


with open("liborOnlyContacts.csv", "w", encoding="utf-8") as f:
    for email in liborContacts:
        extnames = ','.join(set(liborContacts[email]))
        f.write(email + ";" + extnames + "\n")

with open("martinOnlyContacts.csv", "w", encoding="utf-8") as f:
    for email in martinContacts:
        extnames = ','.join(set(martinContacts[email]))
        f.write(email + ";" + extnames + "\n")

with open("intersectionContacts.csv", "w", encoding="utf-8") as f:
    for email in intersectionContacts:
        extnames = ','.join(set(intersectionContacts[email]))
        f.write(email + ";" + extnames + "\n")
