reservations_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["reserved_by", "table", "reservation_time"],
        "properties": {
            "reserved_by": {"bsonType": "string"},
            "table": {
                "bsonType": "object",
                "required": ["table_name", "table_number", "table_seats"],
                "properties": {
                    "table_name": {"bsonType": "string"},
                    "table_number": {"bsonType": "int", "minimum": 1, "maximum": 12},
                    "table_seats": {"bsonType": "int", "minimum": 1, "maximum": 6}
                }
            },
            "reservation_time": {"bsonType": "string"}
        }
    }
}

tables_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["table_name", "table_number", "table_seats"],
        "properties": {
            "table_name": {"bsonType": "string"},
            "table_number": {"bsonType": "int", "minimum": 1, "maximum": 12},
            "table_seats": {"bsonType": "int", "minimum": 1, "maximum": 6}
        }
    }
}
