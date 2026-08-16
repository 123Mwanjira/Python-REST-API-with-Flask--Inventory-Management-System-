"""Functions for interacting with the OpenFoodFacts API."""

import requests


BASE_URL = "https://world.openfoodfacts.org"

HEADERS = {
    "User-Agent": "InventoryManagementSystem/1.0 (Python requests)"
}


def get_product_by_barcode(barcode):
    """Fetch a product from OpenFoodFacts using its barcode."""

    url = f"{BASE_URL}/api/v2/product/{barcode}.json"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if data.get("status") != 1:
            return None

        return data.get("product")

    except requests.RequestException:
        return None


def search_product_by_name(product_name):
    """Search OpenFoodFacts for a product by name."""

    url = f"{BASE_URL}/api/v2/search"

    params = {
        "search_terms": product_name,
        "page_size": 1,
        "fields": (
            "code,"
            "product_name,"
            "brands,"
            "categories,"
            "ingredients_text,"
            "quantity"
        )
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        products = data.get("products", [])

        if not products:
            return None

        return products[0]

    except requests.RequestException:
        return None