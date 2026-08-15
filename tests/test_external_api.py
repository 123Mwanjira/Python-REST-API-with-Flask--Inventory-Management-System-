"""Tests for the OpenFoodFacts API integration."""

import requests

from external_api import (
    get_product_by_barcode,
    search_product_by_name
)


def test_get_product_by_barcode(mocker):
    mock_response = mocker.Mock()

    mock_response.raise_for_status.return_value = None

    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "code": "5449000000996",
            "product_name": "Coca-Cola Original",
            "brands": "Coca-Cola"
        }
    }

    mocker.patch(
        "external_api.requests.get",
        return_value=mock_response
    )

    product = get_product_by_barcode("5449000000996")

    assert product is not None
    assert product["code"] == "5449000000996"
    assert product["product_name"] == "Coca-Cola Original"
    assert product["brands"] == "Coca-Cola"


def test_get_product_by_barcode_not_found(mocker):
    mock_response = mocker.Mock()

    mock_response.raise_for_status.return_value = None

    mock_response.json.return_value = {
        "status": 0
    }

    mocker.patch(
        "external_api.requests.get",
        return_value=mock_response
    )

    product = get_product_by_barcode("0000000000000")

    assert product is None


def test_get_product_by_barcode_request_error(mocker):
    mocker.patch(
        "external_api.requests.get",
        side_effect=Exception("Connection error")
    )

    product = get_product_by_barcode("5449000000996")

    assert product is None


def test_search_product_by_name(mocker):
    mock_response = mocker.Mock()

    mock_response.raise_for_status.return_value = None

    mock_response.json.return_value = {
        "products": [
            {
                "code": "5449000000996",
                "product_name": "Coca-Cola Original",
                "brands": "Coca-Cola",
                "categories": "Soft Drinks",
                "ingredients_text": "Carbonated water, sugar",
                "quantity": "330 ml"
            }
        ]
    }

    mocker.patch(
        "external_api.requests.get",
        return_value=mock_response
    )

    product = search_product_by_name("Coca-Cola")

    assert product is not None
    assert product["code"] == "5449000000996"
    assert product["product_name"] == "Coca-Cola Original"


def test_get_product_by_barcode_request_error(mocker):
    mocker.patch(
        "external_api.requests.get",
        side_effect=requests.RequestException("Connection error")
    )

    product = get_product_by_barcode("5449000000996")

    assert product is None