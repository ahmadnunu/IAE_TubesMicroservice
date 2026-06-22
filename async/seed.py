import json
import urllib.request

HASURA_URL = "http://localhost:8085"
HASURA_ADMIN_SECRET = "my-super-secret-key"

headers = {
    "Content-Type": "application/json",
    "X-Hasura-Admin-Secret": HASURA_ADMIN_SECRET
}

def post_query(payload):
    req = urllib.request.Request(f"{HASURA_URL}/v2/query", data=json.dumps(payload).encode("utf-8"), headers=headers)
    try:
        response = urllib.request.urlopen(req)
        print("Query Success:", payload.get("type"))
    except Exception as e:
        err = e.read().decode("utf-8") if hasattr(e, "read") else str(e)
        print("Query Error: " + err)

post_query({
    "type": "run_sql",
    "args": {
        "source": "default",
        "sql": "TRUNCATE TABLE menus; ALTER TABLE menus ADD COLUMN IF NOT EXISTS stock INTEGER NOT NULL DEFAULT 0; ALTER TABLE menus DROP CONSTRAINT IF EXISTS menus_name_key; ALTER TABLE menus ADD CONSTRAINT menus_name_key UNIQUE (name);"
    }
})

post_query({
    "type": "run_sql",
    "args": {
        "source": "default",
        "sql": "INSERT INTO menus (name, price, stock) VALUES ('Nasi Goreng Spesial', 25000, 50), ('Mie Goreng Seafood', 30000, 30), ('Sate Ayam Madura', 20000, 100) ON CONFLICT DO NOTHING;"
    }
})
