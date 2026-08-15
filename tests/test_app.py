import pytest

from app import app
from inventory import inventory


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_inventory():
    inventory.clear()

    inventory.extend([
        {
            "id": 1,
            "barcode": "5449000000996",
            "product_name": "Coca-Cola Original",
            "brand": "Coca-Cola",
            "category": "Soft Drinks",
            "price": 2.5,
            "stock": 25,
            "ingredients_text": "Carbonated water, sugar, caramel colour",
            "quantity": "330 ml"
        },
        {
            "id": 2,
            "barcode": "3017620422003",
            "product_name": "Nutella",
            "brand": "Ferrero",
            "category": "Spreads",
            "price": 6.5,
            "stock": 15,
            "ingredients_text": "Sugar, palm oil, hazelnuts, cocoa",
            "quantity": "400 g"
        },
        {
            "id": 3,
            "barcode": "7622210449283",
            "product_name": "Oreo Original",
            "brand": "Oreo",
            "category": "Biscuits",
            "price": 3.75,
            "stock": 30,
            "ingredients_text": "Wheat flour, sugar, cocoa powder",
            "quantity": "154 g"
        }
    ])


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Inventory Management API"


def test_get_all_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 3
    assert data[0]["product_name"] == "Coca-Cola Original"


def test_get_single_inventory_item(client):
    response = client.get("/inventory/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == 1
    assert data["product_name"] == "Coca-Cola Original"


def test_get_nonexistent_inventory_item(client):
    response = client.get("/inventory/99")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Inventory item not found"


def test_create_inventory_item(client):
    new_item = {
        "barcode": "1234567890123",
        "product_name": "Organic Almond Milk",
        "brand": "Silk",
        "category": "Plant-Based Milk",
        "price": 5.50,
        "stock": 20,
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "quantity": "1 L"
    }

    response = client.post(
        "/inventory",
        json=new_item
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["id"] == 4
    assert data["product_name"] == "Organic Almond Milk"
    assert data["brand"] == "Silk"


def test_create_inventory_missing_fields(client):
    incomplete_item = {
        "product_name": "Incomplete Product",
        "price": 5.00
    }

    response = client.post(
        "/inventory",
        json=incomplete_item
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Missing required fields"
    assert "barcode" in data["fields"]


def test_update_inventory_item(client):
    response = client.patch(
        "/inventory/1",
        json={
            "price": 3.00,
            "stock": 50
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["price"] == 3.00
    assert data["stock"] == 50
    assert data["product_name"] == "Coca-Cola Original"


def test_update_nonexistent_inventory_item(client):
    response = client.patch(
        "/inventory/99",
        json={
            "price": 10.00
        }
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Inventory item not found"


def test_delete_inventory_item(client):
    response = client.delete("/inventory/3")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Inventory item deleted successfully"
    assert data["item"]["id"] == 3

    # Confirm item was actually removed from the inventory list
    assert not any(item["id"] == 3 for item in inventory)


def test_delete_nonexistent_inventory_item(client):
    response = client.delete("/inventory/99")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Inventory item not found"
