"""Command-line interface for the inventory management system."""

import requests

API_BASE_URL = "http://127.0.0.1:5000"
OPENFOODFACTS_BASE_URL = "https://world.openfoodfacts.org"

HEADERS = {
    "User-Agent": "InventoryManagementSystem/1.0 (Python requests)"
}


def get_inventory():
    """Get all inventory items from the Flask API."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/inventory",
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        print(f"Error fetching inventory: {error}")
        return None

    except Exception as error:
        print(f"Error fetching inventory: {error}")
        return None


def get_inventory_item(item_id):
    """Get one inventory item by ID."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/inventory/{item_id}",
            timeout=10
        )

        if response.status_code == 404:
            print("Inventory item not found.")
            return None

        response.raise_for_status()
        return response.json()

    except Exception as error:
        print(f"Error fetching inventory item: {error}")
        return None


def add_inventory_item(item):
    """Add a new inventory item through the Flask API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/inventory",
            json=item,
            timeout=10
        )

        if response.status_code == 400:
            print(f"Error: {response.json()}")
            return None

        response.raise_for_status()

        print("Inventory item added successfully.")
        return response.json()

    except Exception as error:
        print(f"Error adding inventory item: {error}")
        return None


def update_inventory_item(item_id, updates):
    """Update an inventory item through the Flask API."""
    try:
        response = requests.patch(
            f"{API_BASE_URL}/inventory/{item_id}",
            json=updates,
            timeout=10
        )

        if response.status_code == 404:
            print("Inventory item not found.")
            return None

        response.raise_for_status()

        print("Inventory item updated successfully.")
        return response.json()

    except Exception as error:
        print(f"Error updating inventory item: {error}")
        return None


def delete_inventory_item(item_id):
    """Delete an inventory item through the Flask API."""
    try:
        response = requests.delete(
            f"{API_BASE_URL}/inventory/{item_id}",
            timeout=10
        )

        if response.status_code == 404:
            print("Inventory item not found.")
            return None

        response.raise_for_status()

        print("Inventory item deleted successfully.")
        return response.json()

    except Exception as error:
        print(f"Error deleting inventory item: {error}")
        return None


def find_product_by_barcode(barcode):
    """Find a product on OpenFoodFacts by barcode."""
    try:
        url = (
            f"{OPENFOODFACTS_BASE_URL}"
            f"/api/v2/product/{barcode}.json"
        )

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if data.get("status") != 1:
            print("Product not found on OpenFoodFacts.")
            return None

        return data.get("product")

    except Exception as error:
        print(f"OpenFoodFacts API error: {error}")
        return None


def find_product_by_name(product_name):
    """Find a product on OpenFoodFacts by name."""
    try:
        url = f"{OPENFOODFACTS_BASE_URL}/api/v2/search"

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
            print("Product not found on OpenFoodFacts.")
            return None

        return products[0]

    except Exception as error:
        print(f"OpenFoodFacts API error: {error}")
        return None


def display_inventory(items):
    """Display inventory items in a readable format."""
    if not items:
        print("No inventory items found.")
        return

    for item in items:
        print("-" * 40)
        print(f"ID: {item.get('id')}")
        print(f"Product: {item.get('product_name')}")
        print(f"Brand: {item.get('brand')}")
        print(f"Category: {item.get('category')}")
        print(f"Price: {item.get('price')}")
        print(f"Stock: {item.get('stock')}")
        print(f"Quantity: {item.get('quantity')}")
        print(f"Barcode: {item.get('barcode')}")
        print(f"Ingredients: {item.get('ingredients_text')}")


def print_menu():
    """Display the CLI menu."""
    print("\n" + "=" * 50)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 50)
    print("1. View all inventory")
    print("2. View inventory item")
    print("3. Add inventory item")
    print("4. Update inventory item")
    print("5. Delete inventory item")
    print("6. Find product by barcode")
    print("7. Find product by name")
    print("8. Exit")
    print("=" * 50)


def run_cli():
    """Run the interactive command-line interface."""

    while True:
        print_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            items = get_inventory()
            display_inventory(items)

        elif choice == "2":
            try:
                item_id = int(input("Enter inventory ID: "))
                item = get_inventory_item(item_id)

                if item:
                    display_inventory([item])

            except ValueError:
                print("Invalid ID. Please enter a number.")

        elif choice == "3":
            print("\nEnter the new inventory item details:")

            item = {
                "barcode": input("Barcode: ").strip(),
                "product_name": input("Product name: ").strip(),
                "brand": input("Brand: ").strip(),
                "category": input("Category: ").strip(),
                "price": float(input("Price: ")),
                "stock": int(input("Stock: ")),
                "ingredients_text": input("Ingredients: ").strip(),
                "quantity": input("Quantity: ").strip()
            }

            add_inventory_item(item)

        elif choice == "4":
            try:
                item_id = int(input("Enter inventory ID: "))

                print("Enter the fields you want to update.")
                price = input("New price (press Enter to skip): ").strip()
                stock = input("New stock (press Enter to skip): ").strip()

                updates = {}

                if price:
                    updates["price"] = float(price)

                if stock:
                    updates["stock"] = int(stock)

                if not updates:
                    print("No changes entered.")
                else:
                    update_inventory_item(item_id, updates)

            except ValueError:
                print("Invalid input. Price and stock must be numbers.")

        elif choice == "5":
            try:
                item_id = int(input("Enter inventory ID: "))
                delete_inventory_item(item_id)

            except ValueError:
                print("Invalid ID. Please enter a number.")

        elif choice == "6":
            barcode = input("Enter product barcode: ").strip()
            product = find_product_by_barcode(barcode)

            if product:
                print("\nProduct found:")
                print(f"Name: {product.get('product_name')}")
                print(f"Brand: {product.get('brands')}")
                print(f"Category: {product.get('categories')}")
                print(f"Quantity: {product.get('quantity')}")
                print(f"Ingredients: {product.get('ingredients_text')}")

        elif choice == "7":
            product_name = input("Enter product name: ").strip()
            product = find_product_by_name(product_name)

            if product:
                print("\nProduct found:")
                print(f"Name: {product.get('product_name')}")
                print(f"Brand: {product.get('brands')}")
                print(f"Category: {product.get('categories')}")
                print(f"Barcode: {product.get('code')}")
                print(f"Quantity: {product.get('quantity')}")
                print(f"Ingredients: {product.get('ingredients_text')}")

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1-8.")


if __name__ == "__main__":
    run_cli()
