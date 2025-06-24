GET http://localhost:8000/items/3?q=test
HTTP 200
[Asserts]
jsonpath "$.item_id" == 3
jsonpath "$.q" == "test"