import json

files = [
    {"path": "async/EAI_Microservices_Collection.json", "host": "http://localhost:8085"},
    {"path": "async/EAI_Microservices_Collection_Teammates.json", "host": "http://192.168.1.246:8085"}
]

supergraph_item = {
    "name": "🌟 SUPERGRAPH (Hasura API Gateway)",
    "item": [
        {
            "name": "Query: Get Data From All Services",
            "request": {
                "method": "POST",
                "header": [
                    {
                        "key": "x-hasura-admin-secret",
                        "value": "my-super-secret-key",
                        "type": "text"
                    }
                ],
                "body": {
                    "mode": "graphql",
                    "graphql": {
                        "query": "query SupergraphQuery {\n  user_api {\n    users {\n      id\n      name\n      email\n    }\n  }\n  product_api {\n    products {\n      id\n      name\n      price\n    }\n  }\n  order_api {\n    orders {\n      id\n      total_price\n      status\n    }\n  }\n  menus {\n    id\n    name\n    price\n    stock\n  }\n}",
                        "variables": ""
                    }
                },
                "url": {
                    "raw": "{host}/v1/graphql",
                    "host": [
                        "{host_only}"
                    ],
                    "port": "8085",
                    "path": [
                        "v1",
                        "graphql"
                    ]
                }
            }
        }
    ]
}

for f in files:
    try:
        with open(f["path"], "r") as file:
            data = json.load(file)
        
        # Check if SUPERGRAPH already exists to avoid duplicates
        exists = any(item.get("name", "").startswith("🌟 SUPERGRAPH") for item in data.get("item", []))
        if not exists:
            # Customize URL
            item_copy = json.loads(json.dumps(supergraph_item))
            host_only = f["host"].replace("http://", "").split(":")[0]
            item_copy["item"][0]["request"]["url"]["raw"] = f["host"] + "/v1/graphql"
            item_copy["item"][0]["request"]["url"]["host"] = [host_only]
            
            # Insert at the top
            data["item"].insert(0, item_copy)
            
            with open(f["path"], "w") as file:
                json.dump(data, file, indent=2)
            print("Updated", f["path"])
    except Exception as e:
        print("Error on", f["path"], e)
