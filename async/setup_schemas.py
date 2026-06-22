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
        print("Metadata Success:", payload.get("type"), payload["args"].get("name", ""))
    except Exception as e:
        err = e.read().decode("utf-8") if hasattr(e, "read") else str(e)
        if "already exists" not in err:
            print("Metadata Error: " + err)

post_metadata({
    "type": "add_remote_schema",
    "args": {
        "name": "order_service",
        "definition": {
            "url": "http://order-service:8000/graphql",
            "timeout_seconds": 60,
            "customization": {
                "root_fields_namespace": "order_api",
                "type_names": {
                    "prefix": "OrderSvc_"
                }
            }
        }
    }
})

post_metadata({
    "type": "add_remote_schema",
    "args": {
        "name": "payment_service",
        "definition": {
            "url": "http://payment-service:8000/graphql",
            "timeout_seconds": 60,
            "customization": {
                "root_fields_namespace": "payment_api",
                "type_names": {
                    "prefix": "PaySvc_"
                }
            }
        }
    }
})
