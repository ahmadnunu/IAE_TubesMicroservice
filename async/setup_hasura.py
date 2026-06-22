import json
import urllib.request

HASURA_URL = "http://localhost:8085"
HASURA_ADMIN_SECRET = "my-super-secret-key"

headers = {
    "Content-Type": "application/json",
    "X-Hasura-Admin-Secret": HASURA_ADMIN_SECRET
}

def post_metadata(payload):
    req = urllib.request.Request(f"{HASURA_URL}/v1/metadata", data=json.dumps(payload).encode('utf-8'), headers=headers)
    try:
        response = urllib.request.urlopen(req)
        print("Metadata Success:", payload.get("type"))
    except Exception as e:
        err = e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
        if "already exists" not in err and "already tracked" not in err:
            print(f"Metadata Error on {payload.get('type')}: {err}")

def post_query(payload):
    req = urllib.request.Request(f"{HASURA_URL}/v2/query", data=json.dumps(payload).encode('utf-8'), headers=headers)
    try:
        response = urllib.request.urlopen(req)
        print("Query Success:", payload.get("type"))
    except Exception as e:
        err = e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
        print(f"Query Error on {payload.get('type')}: {err}")

print("=== 1. CREATING TABLE & TRACKING ===")
post_query({
    "type": "run_sql",
    "args": {
        "source": "default",
        "sql": "CREATE TABLE IF NOT EXISTS menus (id SERIAL PRIMARY KEY, name TEXT UNIQUE NOT NULL, price INTEGER NOT NULL, stock INTEGER NOT NULL DEFAULT 0);"
    }
})

post_metadata({
    "type": "pg_track_table",
    "args": {
        "source": "default",
        "schema": "public",
        "table": "menus"
    }
})

print("=== 2. SEEDING DATA ===")
post_query({
    "type": "run_sql",
    "args": {
        "source": "default",
        "sql": "INSERT INTO menus (name, price, stock) VALUES ('Nasi Goreng Spesial', 25000, 50), ('Mie Goreng Seafood', 30000, 30), ('Sate Ayam Madura', 20000, 100) ON CONFLICT DO NOTHING;"
    }
})

print("=== 3. REGISTERING REMOTE SCHEMAS ===")
services = [
    {"name": "user_service", "url": "http://user-service:8000/graphql", "namespace": "user_api"},
    {"name": "product_service", "url": "http://product-service:8000/graphql", "namespace": "product_api"},
    {"name": "order_service", "url": "http://order-service:8000/graphql", "namespace": "order_api"},
    {"name": "payment_service", "url": "http://payment-service:8000/graphql", "namespace": "payment_api"}
]

for svc in services:
    post_metadata({
        "type": "add_remote_schema",
        "args": {
            "name": svc["name"],
            "definition": {
                "url": svc["url"],
                "timeout_seconds": 60,
                "customization": {
                    "root_fields_namespace": svc["namespace"]
                }
            }
        }
    })

print("=== SETUP COMPLETE ===")
