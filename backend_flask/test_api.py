import requests, random, string, sys, json

BASE = "http://127.0.0.1:5000"

def rand_email():
    suf = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"test_{suf}@example.com"

def pprint_resp(title, r):
    print(f"\n=== {title} ({r.status_code}) ===")
    try:
        print(json.dumps(r.json(), ensure_ascii=False, indent=2))
    except Exception:
        print(r.text[:500])

def main():
    # registro
    email = rand_email()
    pwd = "12345678"
    r = requests.post(f"{BASE}/auth/register", json={"email": email, "password": pwd})
    pprint_resp("register", r)
    if r.status_code not in (201, 409):
        sys.exit(1)

    # login
    r = requests.post(f"{BASE}/auth/login", json={"email": email, "password": pwd})
    pprint_resp("login", r)
    token = r.json().get("access_token")
    if not token:
        sys.exit("No token")
    headers = {"Authorization": f"Bearer {token}"}

    # crear juego
    body = {
        "nombre": "Los Simpsons " + "".join(random.choices(string.ascii_lowercase+string.digits,k=5)),
        "descripcion": "Simpsons game",
        "popularidad": 6,
        "categoria": "Accion",
        "link": "https://en.bandainamcoent.eu/elden-ring/elden-ring"
    }
    r = requests.post(f"{BASE}/games", json=body, headers=headers)
    pprint_resp("create_game", r)

    # solo intentamos leer el id si es 201 y hay JSON
    game_id = None
    try:
        if r.status_code == 201:
            game_id = r.json()["id"]
        elif r.status_code == 409:
            print("Duplicado controlado, paro aquí.")
            return
        else:
            sys.exit("Fallo al crear juego")
    except Exception:
        sys.exit("Respuesta no-JSON al crear juego")

    # listar
    r = requests.get(f"{BASE}/games")
    pprint_resp("list_games", r)

    # actualizar
    r = requests.patch(f"{BASE}/games/{game_id}", json={"popularidad": 10}, headers=headers)
    pprint_resp("update_game", r)

    # borrar
    r = requests.delete(f"{BASE}/games/{game_id}", headers=headers)
    print("\n=== delete_game ===", r.status_code)

if __name__ == "__main__":
    main()
