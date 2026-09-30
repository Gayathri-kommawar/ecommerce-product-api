from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Application configuration from environment variables
APP_ENV = os.getenv("APP_ENV", "development")
DB_HOST = os.getenv("DB_HOST", "localhost")
APP_PORT = int(os.getenv("APP_PORT", "5000"))

# Temporary in-memory product data
products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 50000,
        "quantity": 10
    }
]


# Health API
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "UP",
        "environment": APP_ENV
    })


# Get all products
@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)


# Get one product
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    for product in products:
        if product["id"] == product_id:
            return jsonify(product)

    return jsonify({"error": "Product not found"}), 404


# Add a product
@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()

    new_product = {
        "id": len(products) + 1,
        "name": data["name"],
        "price": data["price"],
        "quantity": data["quantity"]
    }

    products.append(new_product)

    return jsonify(new_product), 201


# Update a product
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    for product in products:
        if product["id"] == product_id:
            data = request.get_json()

            product["name"] = data.get("name", product["name"])
            product["price"] = data.get("price", product["price"])
            product["quantity"] = data.get("quantity", product["quantity"])

            return jsonify(product)

    return jsonify({"error": "Product not found"}), 404


# Delete a product
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return jsonify({"message": "Product deleted successfully"})

    return jsonify({"error": "Product not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=APP_PORT)