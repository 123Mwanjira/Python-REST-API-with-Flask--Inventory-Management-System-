from flask import Flask, jsonify, request
from inventory import inventory

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "Inventory Management API"
    })


# GET all inventory items
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)


# GET one inventory item
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item)

    return jsonify({
        "error": "Inventory item not found"
    }), 404


# POST a new inventory item
@app.route("/inventory", methods=["POST"])
def create_inventory_item():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body must contain JSON data"
        }), 400

    required_fields = [
        "barcode",
        "product_name",
        "brand",
        "category",
        "price",
        "stock",
        "ingredients_text",
        "quantity"
    ]

    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields
        }), 400

    new_id = max(item["id"] for item in inventory) + 1 if inventory else 1

    new_item = {
        "id": new_id,
        "barcode": data["barcode"],
        "product_name": data["product_name"],
        "brand": data["brand"],
        "category": data["category"],
        "price": data["price"],
        "stock": data["stock"],
        "ingredients_text": data["ingredients_text"],
        "quantity": data["quantity"]
    }

    inventory.append(new_item)

    return jsonify(new_item), 201


# PATCH an existing inventory item
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body must contain JSON data"
        }), 400

    for item in inventory:
        if item["id"] == item_id:

            allowed_fields = [
                "barcode",
                "product_name",
                "brand",
                "category",
                "price",
                "stock",
                "ingredients_text",
                "quantity"
            ]

            for field in allowed_fields:
                if field in data:
                    item[field] = data[field]

            return jsonify(item), 200

    return jsonify({
        "error": "Inventory item not found"
    }), 404


# DELETE an inventory item
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)

            return jsonify({
                "message": "Inventory item deleted successfully",
                "item": item
            }), 200

    return jsonify({
        "error": "Inventory item not found"
    }), 404


if __name__ == "__main__":
    app.run(debug=True)