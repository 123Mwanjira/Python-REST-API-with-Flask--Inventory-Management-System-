 Python REST API with Flask - Inventory Management System

## Summative Lab Project

A Flask-based REST API and command-line inventory management system for a small retail company.

The application allows employees to:

- View all inventory items
- View an individual inventory item
- Add new inventory items
- Update inventory items
- Delete inventory items
- Search for product information using the OpenFoodFacts API
- Interact with the inventory system through a CLI
- Run automated tests for the Flask API, CLI, and external API integration

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Running the Flask API](#running-the-flask-api)
- [REST API Endpoints](#rest-api-endpoints)
- [External API Integration](#external-api-integration)
- [CLI Application](#cli-application)
- [Testing](#testing)
- [Example API Requests](#example-api-requests)
- [Git Workflow](#git-workflow)
- [Error Handling](#error-handling)
- [Project Data](#project-data)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Project Overview

This project implements an inventory management system using Python and Flask.

The application uses a simulated in-memory Python list as the inventory database. Each inventory item contains an ID and product information such as:

- Barcode
- Product name
- Brand
- Category
- Price
- Stock
- Ingredients
- Quantity

The REST API follows standard RESTful conventions and provides CRUD operations for managing inventory.

The project also integrates with the OpenFoodFacts API to retrieve real-world product information using a barcode or product name.

---

## Features

### Flask REST API

The API provides complete CRUD functionality:

- `GET /inventory`
- `GET /inventory/<id>`
- `POST /inventory`
- `PATCH /inventory/<id>`
- `DELETE /inventory/<id>`

### External API Integration

The project integrates with OpenFoodFacts to:

- Find products by barcode
- Search for products by name
- Retrieve product details such as:
  - Product name
  - Brand
  - Category
  - Ingredients
  - Quantity
  - Barcode

### CLI Interface

The command-line interface allows users to:

1. View all inventory
2. View an individual inventory item
3. Add an inventory item
4. Update an inventory item
5. Delete an inventory item
6. Find a product by barcode
7. Find a product by name
8. Exit the application

### Automated Testing

The project uses `pytest` and `pytest-mock` to test:

- Flask routes
- CRUD operations
- Validation
- Error handling
- External API interactions
- CLI functions

External API calls are mocked during testing so that tests do not depend on the availability of the external service.

---

## Technologies Used

- Python 3.8.13
- Flask
- Requests
- pytest
- pytest-mock
- OpenFoodFacts API
- Git
- GitHub
- Bash / WSL Ubuntu

---

## Project Structure

```text
Python-REST-API-with-Flask--Inventory-Management-System/
│
├── app.py
├── cli.py
├── external_api.py
├── inventory.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── tests/
    ├── test_app.py
    ├── test_cli.py
    └── test_external_api.py

    File Descriptions
app.py

Contains the Flask application and REST API routes.

It implements:

Home route
GET inventory
GET individual inventory item
POST inventory item
PATCH inventory item
DELETE inventory item
inventory.py

Contains the simulated inventory database.

The inventory is represented by a Python list of dictionaries.

external_api.py

Contains functions for communicating with OpenFoodFacts.

Functions include:

get_product_by_barcode(barcode)

and:

search_product_by_name(product_name)
cli.py

Contains the command-line interface.

The CLI communicates with the Flask API and provides product search functionality.

tests/test_app.py

Contains tests for the Flask REST API and CRUD functionality.

tests/test_external_api.py

Contains tests for OpenFoodFacts API integration.

tests/test_cli.py

Contains tests for the CLI functions.

Installation and Setup
1. Clone the repository
git clone https://github.com/123Mwanjira/Python-REST-API-with-Flask--Inventory-Management-System-.git

Move into the project directory:

cd Python-REST-API-with-Flask--Inventory-Management-System-
2. Create a virtual environment

The project uses Python's built-in venv environment.

python3 -m venv venv
3. Activate the virtual environment

On Linux, WSL, or macOS:

source venv/bin/activate

On Windows Command Prompt:

venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt

The project requires Flask, Requests, pytest, and pytest-mock.

If necessary, the dependencies can also be installed manually:

pip install Flask requests pytest pytest-mock
Running the Flask API

Start the Flask development server with:

python app.py

The API will be available at:

http://127.0.0.1:5000

The application runs in Flask debug mode when app.py is executed directly.

REST API Endpoints
1. Home
Request
GET /
Example
curl http://127.0.0.1:5000/
Response
{
  "message": "Inventory Management API"
}
2. Get All Inventory
Request
GET /inventory
Example
curl http://127.0.0.1:5000/inventory
Example Response
[
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
  }
]
3. Get One Inventory Item
Request
GET /inventory/<id>
Example
curl http://127.0.0.1:5000/inventory/1
Successful Response
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
}
Non-existent Item
curl -i http://127.0.0.1:5000/inventory/99

Response:

{
  "error": "Inventory item not found"
}

HTTP status:

404 NOT FOUND
4. Create an Inventory Item
Request
POST /inventory
Example
curl -X POST http://127.0.0.1:5000/inventory \
-H "Content-Type: application/json" \
-d '{
  "barcode": "1234567890123",
  "product_name": "Organic Almond Milk",
  "brand": "Silk",
  "category": "Plant-Based Milk",
  "price": 5.50,
  "stock": 20,
  "ingredients_text": "Filtered water, almonds, cane sugar",
  "quantity": "1 L"
}'
Successful Response

The API returns HTTP:

201 CREATED

and returns the newly created inventory item.

5. Update an Inventory Item

The API uses PATCH so that individual fields can be updated without replacing the entire item.

Request
PATCH /inventory/<id>
Example
curl -X PATCH http://127.0.0.1:5000/inventory/1 \
-H "Content-Type: application/json" \
-d '{
  "price": 3.00,
  "stock": 50
}'
Response
{
  "id": 1,
  "barcode": "5449000000996",
  "product_name": "Coca-Cola Original",
  "brand": "Coca-Cola",
  "category": "Soft Drinks",
  "price": 3.0,
  "stock": 50,
  "ingredients_text": "Carbonated water, sugar, caramel colour",
  "quantity": "330 ml"
}
6. Delete an Inventory Item
Request
DELETE /inventory/<id>
Example
curl -i -X DELETE http://127.0.0.1:5000/inventory/3
Successful Response
{
  "item": {
    "id": 3,
    "barcode": "7622210449283",
    "brand": "Oreo",
    "category": "Biscuits",
    "ingredients_text": "Wheat flour, sugar, cocoa powder",
    "price": 3.75,
    "product_name": "Oreo Original",
    "quantity": "154 g",
    "stock": 30
  },
  "message": "Inventory item deleted successfully"
}

The API returns:

200 OK

Attempting to delete an item that does not exist returns:

404 NOT FOUND
External API Integration

The project uses the OpenFoodFacts API to retrieve product information.

The integration is implemented in:

external_api.py

The application provides two main functions:

get_product_by_barcode(barcode)

and:

search_product_by_name(product_name)

The functions use Python's requests library.

A custom User-Agent is supplied when making external API requests.

The application also uses exception handling so that external API failures do not crash the application.

If the external API cannot be reached or a product cannot be found, the functions return:

None
CLI Application

The CLI provides an interactive interface for the inventory management system.

Start the Flask API first:

python app.py

Then, in another terminal with the virtual environment activated, run:

python cli.py

The CLI displays:

==================================================
INVENTORY MANAGEMENT SYSTEM
==================================================
1. View all inventory
2. View inventory item
3. Add inventory item
4. Update inventory item
5. Delete inventory item
6. Find product by barcode
7. Find product by name
8. Exit
==================================================
CLI Examples
View inventory

Select:

1

The CLI requests:

GET /inventory

from the Flask API.

View an individual item

Select:

2

Then provide an inventory ID:

Enter inventory ID: 1
Add an item

Select:

3

The CLI asks for:

Barcode
Product name
Brand
Category
Price
Stock
Ingredients
Quantity

The information is sent to:

POST /inventory
Update an item

Select:

4

Provide the inventory ID and the new price or stock level.

The CLI sends a:

PATCH /inventory/<id>

request.

Delete an item

Select:

5

Provide the inventory ID.

The CLI sends:

DELETE /inventory/<id>
Find a product by barcode

Select:

6

Enter a barcode:

5449000000996

The CLI queries OpenFoodFacts.

Find a product by name

Select:

7

Enter a product name:

Nutella

The CLI searches OpenFoodFacts and displays the first matching product.

Testing

The project uses pytest for automated testing.

Tests are divided according to the application's features.

Flask API Tests

Run:

pytest -v tests/test_app.py

The Flask API test suite covers:

Home route
GET all inventory
GET individual item
GET non-existent item
POST inventory item
POST validation
PATCH inventory item
PATCH non-existent item
DELETE inventory item
DELETE non-existent item
External API Tests

Run:

pytest -v tests/test_external_api.py

The tests use mocked HTTP responses rather than relying on the live OpenFoodFacts service.

The tests cover:

Successful barcode lookup
Product not found
Request failure handling
Successful product-name search
CLI Tests

Run:

pytest -v tests/test_cli.py

The CLI tests use pytest-mock to mock HTTP requests.

The tests cover:

Getting inventory
Getting an individual item
Adding an item
Updating an item
Deleting an item
Searching by barcode
Searching by product name
Request error handling
Product-not-found handling
Run All Tests

To run the complete test suite:

pytest -v

The project is designed so that the Flask API, external API integration, and CLI can be tested independently and together.

Error Handling

The application provides error handling for common problems.

Missing request data

A POST or PATCH request without JSON data returns:

400 BAD REQUEST
Missing required fields

Creating an inventory item without all required fields returns:

{
  "error": "Missing required fields",
  "fields": [
    "barcode"
  ]
}
Inventory item not found

Requests for an ID that does not exist return:

404 NOT FOUND

with:

{
  "error": "Inventory item not found"
}
External API failure

External API request failures are caught and handled without crashing the application.

Project Data

The application uses a simulated in-memory database rather than a permanent database.

The data is stored in:

inventory.py

Example:

inventory = [
    {
        "id": 1,
        "barcode": "5449000000996",
        "product_name": "Coca-Cola Original",
        "brand": "Coca-Cola",
        "category": "Soft Drinks",
        "price": 2.50,
        "stock": 25,
        "ingredients_text": "Carbonated water, sugar, caramel colour",
        "quantity": "330 ml"
    }
]

This satisfies the lab requirement to use an array/list as simulated data storage.

Changes made through POST, PATCH, and DELETE modify the list while the application is running.

Because this is an in-memory data store, changes are reset when the application restarts.

Git Workflow

Git was used to manage the project using feature branches.

Examples of feature branches used during development include:

feature/setup
feature/flask-crud
feature/external-api

The workflow used was:

main
  |
  +-- feature/flask-crud
  |
  +-- feature/external-api

Features were developed on separate branches and merged into main through GitHub Pull Requests.

Completed feature branches were deleted after merging to keep the repository clean.

Development Workflow

The development process followed these general steps:

Create the Python project.
Create and activate a virtual environment.
Install Flask and supporting packages.
Create the simulated inventory data.
Implement Flask RESTful routes.
Write Flask API tests.
Integrate OpenFoodFacts.
Write external API tests using mocks.
Develop the CLI.
Write CLI tests.
Run the complete test suite.
Commit changes using Git.
Push feature branches to GitHub.
Create Pull Requests.
Merge completed features into main.
Delete completed feature branches.
Prepare final documentation and evidence.
API Testing with curl

The API can be tested directly from the terminal.

Get all products
curl http://127.0.0.1:5000/inventory
Get product 1
curl http://127.0.0.1:5000/inventory/1
Create product
curl -X POST http://127.0.0.1:5000/inventory \
-H "Content-Type: application/json" \
-d '{
  "barcode": "1234567890123",
  "product_name": "Organic Almond Milk",
  "brand": "Silk",
  "category": "Plant-Based Milk",
  "price": 5.50,
  "stock": 20,
  "ingredients_text": "Filtered water, almonds, cane sugar",
  "quantity": "1 L"
}'
Update product
curl -X PATCH http://127.0.0.1:5000/inventory/1 \
-H "Content-Type: application/json" \
-d '{
  "price": 3.00,
  "stock": 50
}'
Delete product
curl -i -X DELETE http://127.0.0.1:5000/inventory/3
Verify deletion
curl -i http://127.0.0.1:5000/inventory/3

Expected:

404 NOT FOUND
Future Improvements

Possible improvements for a production version include:

Replace the in-memory list with SQLite, PostgreSQL, or MongoDB.
Add user authentication and authorization.
Add database persistence.
Add pagination for large inventories.
Add more extensive input validation.
Add inventory filtering and search.
Add automated API documentation.
Add a web-based administrator dashboard.
Add Docker support.
Add continuous integration with GitHub Actions.
Add more comprehensive CLI validation.
Add product import functionality from OpenFoodFacts directly into inventory.
Learning Outcomes

This project demonstrates practical understanding of:

Python programming
Flask
RESTful API design
HTTP methods
CRUD operations
JSON
Request/response handling
HTTP status codes
External API integration
Error handling
Automated testing
Mocking external services
CLI application development
Git branching
GitHub Pull Requests
Project documentation
Author

Maurine Gichuhi

