from flask import Flask, jsonify, request
from inventory import inventory
from external_api import get_product_by_barcode, search_product_by_name

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
        field
        for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields
        }), 400

    new_id = (
        max(item["id"] for item in inventory) + 1
        if inventory
        else 1
    )

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


# GET product from OpenFoodFacts by barcode
@app.route("/inventory/search/barcode/<barcode>", methods=["GET"])
def find_product_by_barcode(barcode):
    product = get_product_by_barcode(barcode)

    if product is None:
        return jsonify({
            "error": "Product not found or external API unavailable"
        }), 404

    return jsonify({
        "source": "OpenFoodFacts",
        "product": product
    }), 200


# GET product from OpenFoodFacts by name
@app.route("/inventory/search/name/<path:product_name>", methods=["GET"])
def find_product_by_name(product_name):
    product = search_product_by_name(product_name)

    if product is None:
        return jsonify({
            "error": "Product not found or external API unavailable"
        }), 404

    return jsonify({
        "source": "OpenFoodFacts",
        "product": product
    }), 200


# POST product from OpenFoodFacts into inventory
@app.route("/inventory/import/barcode/<barcode>", methods=["POST"])
def import_product_by_barcode(barcode):
    product = get_product_by_barcode(barcode)

    if product is None:
        return jsonify({
            "error": "Product not found or external API unavailable"
        }), 404

    new_id = (
        max(item["id"] for item in inventory) + 1
        if inventory
        else 1
    )

    new_item = {
        "id": new_id,
        "barcode": product.get("code", barcode),
        "product_name": product.get(
            "product_name",
            "Unknown Product"
        ),
        "brand": product.get(
            "brands",
            "Unknown Brand"
        ),
        "category": product.get(
            "categories",
            "Unknown Category"
        ),
        "price": 0,
        "stock": 0,
        "ingredients_text": product.get(
            "ingredients_text",
            ""
        ),
        "quantity": product.get(
            "quantity",
            ""
        )
    }

    inventory.append(new_item)

    return jsonify({
        "message": "Product imported successfully",
        "source": "OpenFoodFacts",
        "item": new_item
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
