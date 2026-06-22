import json
import urllib.request

HASURA_URL = "http://localhost:8085"
HASURA_ADMIN_SECRET = "my-super-secret-key"

headers = {
    "Content-Type": "application/json",
    "X-Hasura-Admin-Secret": HASURA_ADMIN_SECRET
}

def post_metadata(payload):
    req = urllib.request.Request(f"{HASURA_URL}/v1/metadata", data=json.dumps(payload).encode("utf-8"), headers=headers)
    try:
        response = urllib.request.urlopen(req)
        print("Success:", payload["args"].get("name", ""))
    except Exception as e:
        err = e.read().decode("utf-8") if hasattr(e, "read") else str(e)
        if "not found" not in err:
            print("Error:", payload["args"].get("name", ""), err)

# Remove all first
for name in ["user_service", "product_service", "order_service", "payment_service"]:
    post_metadata({
        "type": "remove_remote_schema",
        "args": {
            "name": name
        }
    })

# Add them back with prefixes
services = [
    {"name": "user_service", "url": "http://user-service:8000/graphql", "namespace": "user_api", "prefix": "UserSvc_"},
    {"name": "product_service", "url": "http://product-service:8000/graphql", "namespace": "product_api", "prefix": "ProdSvc_"},
    {"name": "order_service", "url": "http://order-service:8000/graphql", "namespace": "order_api", "prefix": "OrderSvc_"},
    {"name": "payment_service", "url": "http://payment-service:8000/graphql", "namespace": "payment_api", "prefix": "PaySvc_"}
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
                    "root_fields_namespace": svc["namespace"],
                    "type_names": {
                        "prefix": svc["prefix"]
                    }
                }
            }
        }
    })
