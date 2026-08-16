"""Tests for the inventory management CLI."""

import cli


def test_get_inventory(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = [
        {
            "id": 1,
            "product_name": "Coca-Cola Original",
            "price": 2.50,
            "stock": 25
        }
    ]
    mock_response.raise_for_status.return_value = None

    mocker.patch(
        "cli.requests.get",
        return_value=mock_response
    )

    result = cli.get_inventory()

    assert result[0]["id"] == 1
    assert result[0]["product_name"] == "Coca-Cola Original"


def test_get_inventory_item(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "product_name": "Coca-Cola Original"
    }
    mock_response.raise_for_status.return_value = None

    mocker.patch(
        "cli.requests.get",
        return_value=mock_response
    )

    result = cli.get_inventory_item(1)

    assert result["id"] == 1
    assert result["product_name"] == "Coca-Cola Original"


def test_add_inventory_item(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "id": 4,
        "product_name": "Organic Almond Milk"
    }
    mock_response.raise_for_status.return_value = None

    mock_post = mocker.patch(
        "cli.requests.post",
        return_value=mock_response
    )

    item = {
        "barcode": "1234567890123",
        "product_name": "Organic Almond Milk",
        "brand": "Silk",
        "category": "Plant-Based Milk",
        "price": 5.50,
        "stock": 20,
        "ingredients_text": "Filtered water, almonds",
        "quantity": "1 L"
    }

    result = cli.add_inventory_item(item)

    assert result["id"] == 4
    mock_post.assert_called_once()


def test_update_inventory_item(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "product_name": "Coca-Cola Original",
        "price": 3.00,
        "stock": 50
    }
    mock_response.raise_for_status.return_value = None

    mock_patch = mocker.patch(
        "cli.requests.patch",
        return_value=mock_response
    )

    result = cli.update_inventory_item(
        1,
        {
            "price": 3.00,
            "stock": 50
        }
    )

    assert result["price"] == 3.00
    assert result["stock"] == 50
    mock_patch.assert_called_once()


def test_delete_inventory_item(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": "Inventory item deleted successfully",
        "item": {
            "id": 3,
            "product_name": "Oreo Original"
        }
    }
    mock_response.raise_for_status.return_value = None

    mock_delete = mocker.patch(
        "cli.requests.delete",
        return_value=mock_response
    )

    result = cli.delete_inventory_item(3)

    assert result["item"]["id"] == 3
    mock_delete.assert_called_once()


def test_find_product_by_barcode(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Coca-Cola Original",
            "brands": "Coca-Cola",
            "code": "5449000000996"
        }
    }
    mock_response.raise_for_status.return_value = None

    mocker.patch(
        "cli.requests.get",
        return_value=mock_response
    )

    result = cli.find_product_by_barcode("5449000000996")

    assert result["product_name"] == "Coca-Cola Original"
    assert result["brands"] == "Coca-Cola"


def test_find_product_by_name(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "products": [
            {
                "product_name": "Nutella",
                "brands": "Ferrero",
                "code": "3017620422003"
            }
        ]
    }
    mock_response.raise_for_status.return_value = None

    mocker.patch(
        "cli.requests.get",
        return_value=mock_response
    )

    result = cli.find_product_by_name("Nutella")

    assert result["product_name"] == "Nutella"
    assert result["brands"] == "Ferrero"


def test_get_inventory_request_error(mocker, capsys):
    mocker.patch(
        "cli.requests.get",
        side_effect=Exception("Connection error")
    )

    result = cli.get_inventory()

    assert result is None


def test_find_product_by_barcode_not_found(mocker, capsys):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": 0
    }
    mock_response.raise_for_status.return_value = None

    mocker.patch(
        "cli.requests.get",
        return_value=mock_response
    )

    result = cli.find_product_by_barcode("0000000000000")

    assert result is None
