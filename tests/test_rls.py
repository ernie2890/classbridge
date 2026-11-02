from getpass import getpass
from classbridge.db import get_anon_client

# Assumes the same password for all three fake users
PASSWORD = getpass("Fake users' password: ")


def login(email):
    client = get_anon_client()
    client.auth.sign_in_with_password({"email": email, "password": PASSWORD})
    return client


def titles(client):
    rows = client.table("assignments").select("title").execute().data
    return sorted(r["title"] for r in rows)


def names(client):
    rows = client.table("students").select("first_name").execute().data
    return sorted(r["first_name"] for r in rows)


def check(label, actual, expected):
    status = "PASS" if actual == expected else "FAIL"
    print(f"{status}  {label}: {actual}")


parent1 = login("parent1@example.com")
check("Parent 1 assignments", titles(parent1), ["Fractions Practice"])
check("Parent 1 students", names(parent1), ["Mateo"])

parent2 = login("parent2@example.com")
check("Parent 2 assignments", titles(parent2), ["Fractions Practice"])
check("Parent 2 students", names(parent2), ["Taylor"])

teacher = login("teacher@example.com")
check("Teacher assignments", titles(teacher),
      ["Fractions Practice", "Teacher-only draft"])
check("Teacher students", names(teacher), ["Mateo", "Taylor"])

anon = get_anon_client()
check("Logged-out assignments", titles(anon), [])
check("Logged-out students", names(anon), [])