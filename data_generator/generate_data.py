"""
Generate sample data for the testbed project.

Creates:
- Stores with SCD2 history
- Customers with SCD2 history
- Sales transactions over the last year
"""

import duckdb
from datetime import datetime, timedelta
import random
from pathlib import Path

random.seed(42)

end_date = datetime.now()
start_date = end_date - timedelta(days=365)


def generate_stores():
    """Generate store dimension with SCD2 history."""
    stores = []
    store_id = 1

    store_data = [
        ("Downtown Flagship", "New York, NY", "flagship"),
        ("Mall Location Alpha", "Los Angeles, CA", "mall"),
        ("Strip Mall Beta", "Chicago, IL", "strip"),
        ("Outlet Store Gamma", "Houston, TX", "outlet"),
        ("City Center Delta", "Phoenix, AZ", "city_center"),
        ("Suburban Epsilon", "Philadelphia, PA", "suburban"),
        ("Airport Store Zeta", "San Antonio, TX", "airport"),
    ]

    for name, location, store_type in store_data:
        valid_from = start_date - timedelta(days=random.randint(400, 800))

        # Some stores have history (store type changes, relocations)
        if store_id <= 3:
            old_valid_from = valid_from - timedelta(days=random.randint(200, 400))
            old_valid_to = valid_from
            old_store_type = "pop_up" if store_id == 1 else store_type
            old_location = location if store_id != 2 else "Miami, FL"

            stores.append({
                "store_id": store_id,
                "store_name": name,
                "location": old_location,
                "store_type": old_store_type,
                "opened_date": old_valid_from.date(),
                "valid_from": old_valid_from.date(),
                "valid_to": old_valid_to.date(),
                "is_current": False
            })

        # Current record
        stores.append({
            "store_id": store_id,
            "store_name": name,
            "location": location,
            "store_type": store_type,
            "opened_date": valid_from.date(),
            "valid_from": valid_from.date(),
            "valid_to": None,
            "is_current": True
        })

        store_id += 1

    return stores


def generate_customers():
    """Generate customer dimension with SCD2 history."""
    customers = []
    customer_id = 1

    first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry",
                   "Iris", "Jack", "Karen", "Leo", "Mary", "Nathan", "Olivia", "Paul",
                   "Quinn", "Rachel", "Steve", "Tina", "Uma", "Victor", "Wendy", "Xavier",
                   "Yara", "Zack"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
                  "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
                  "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]

    for first, last in zip(first_names, last_names[:len(first_names)]):
        name = f"{first} {last}"
        email = f"{first.lower()}.{last.lower()}@example.com"
        signup_date = start_date - timedelta(days=random.randint(100, 600))

        # Customer tier (can change over time for SCD2)
        current_tier = random.choice(["bronze", "silver", "gold", "platinum"])

        # Some customers have tier changes (SCD2 history)
        if customer_id <= 8:
            # Add historical record with different tier
            tier_change_date = signup_date + timedelta(days=random.randint(60, 200))
            old_tier = "bronze" if current_tier != "bronze" else "silver"

            customers.append({
                "customer_id": customer_id,
                "customer_name": name,
                "email": email,
                "signup_date": signup_date.date(),
                "tier": old_tier,
                "valid_from": signup_date.date(),
                "valid_to": tier_change_date.date(),
                "is_current": False
            })

            # Current record
            customers.append({
                "customer_id": customer_id,
                "customer_name": name,
                "email": email,
                "signup_date": signup_date.date(),
                "tier": current_tier,
                "valid_from": tier_change_date.date(),
                "valid_to": None,
                "is_current": True
            })
        else:
            # No history, just current record
            customers.append({
                "customer_id": customer_id,
                "customer_name": name,
                "email": email,
                "signup_date": signup_date.date(),
                "tier": current_tier,
                "valid_from": signup_date.date(),
                "valid_to": None,
                "is_current": True
            })

        customer_id += 1

    return customers


def generate_products():
    """Generate product dimension."""
    products = []
    product_id = 1

    product_data = [
        # Electronics
        ("Laptop Pro 15", "Electronics", 1299.99),
        ("Wireless Mouse", "Electronics", 29.99),
        ("4K Monitor", "Electronics", 499.99),
        ("Bluetooth Headphones", "Electronics", 149.99),
        ("USB-C Cable", "Electronics", 19.99),
        # Clothing
        ("Cotton T-Shirt", "Clothing", 24.99),
        ("Denim Jeans", "Clothing", 79.99),
        ("Winter Jacket", "Clothing", 149.99),
        ("Running Shoes", "Clothing", 89.99),
        ("Baseball Cap", "Clothing", 19.99),
        # Home & Garden
        ("Coffee Maker", "Home & Garden", 79.99),
        ("Plant Pot Set", "Home & Garden", 34.99),
        ("LED Desk Lamp", "Home & Garden", 44.99),
        ("Throw Pillow", "Home & Garden", 24.99),
        # Sports
        ("Yoga Mat", "Sports", 39.99),
        ("Dumbbells 10lb", "Sports", 49.99),
        ("Tennis Racket", "Sports", 129.99),
        ("Water Bottle", "Sports", 14.99),
        # Books
        ("Python Programming", "Books", 49.99),
        ("Mystery Novel", "Books", 14.99),
        ("Cookbook", "Books", 29.99),
        # Toys
        ("Board Game", "Toys", 34.99),
        ("LEGO Set", "Toys", 79.99),
        ("Action Figure", "Toys", 19.99),
        # Beauty
        ("Face Cream", "Beauty", 39.99),
        ("Shampoo", "Beauty", 12.99),
        ("Lipstick", "Beauty", 24.99),
        # Food
        ("Organic Coffee Beans", "Food", 16.99),
        ("Dark Chocolate", "Food", 5.99),
        ("Protein Bar Box", "Food", 29.99),
    ]

    for name, category, price in product_data:
        products.append({
            "product_id": product_id,
            "product_name": name,
            "category": category,
            "base_price": price
        })
        product_id += 1

    return products


def generate_sales(con):
    """Generate sales transactions over the last year."""
    sales = []
    transaction_id = 1000

    current_stores = [r[0] for r in con.execute(
        "SELECT store_id FROM stores WHERE is_current = true"
    ).fetchall()]
    current_customers = [r[0] for r in con.execute(
        "SELECT customer_id FROM customers WHERE is_current = true"
    ).fetchall()]
    all_products = [r[0] for r in con.execute(
        "SELECT product_id FROM products"
    ).fetchall()]
    product_prices = {r[0]: r[1] for r in con.execute(
        "SELECT product_id, base_price FROM products"
    ).fetchall()}

    for _ in range(100):
        sale_date = start_date + timedelta(days=random.randint(0, 365))
        customer_id = random.choice(current_customers)
        store_id = random.choice(current_stores)
        product_id = random.choice(all_products)

        base_price = product_prices[product_id]
        discount_factor = random.uniform(0.9, 1.0)
        unit_price = round(base_price * discount_factor, 2)

        quantity = random.randint(1, 5)
        amount = round(unit_price * quantity, 2)

        sales.append({
            "transaction_id": transaction_id,
            "customer_id": customer_id,
            "store_id": store_id,
            "product_id": product_id,
            "sale_date": sale_date.date(),
            "quantity": quantity,
            "unit_price": unit_price,
            "amount": amount
        })

        transaction_id += 1

    return sales


def load_table(con, name, ddl, rows):
    """Create a table and bulk insert rows."""
    keys = rows[0].keys()
    placeholders = ", ".join(f"${i+1}" for i in range(len(keys)))
    con.execute(ddl)
    con.executemany(f"INSERT INTO {name} VALUES ({placeholders})",
                    [tuple(r[k] for k in keys) for r in rows])


def main():
    """Generate all data and save as parquet files."""
    con = duckdb.connect()

    print("Generating stores data...")
    stores = generate_stores()
    load_table(con, "stores", """
        CREATE TABLE stores (
            store_id BIGINT, store_name VARCHAR, location VARCHAR, store_type VARCHAR,
            opened_date DATE, valid_from DATE, valid_to DATE, is_current BOOLEAN
        )""", stores)
    current_stores = con.execute("SELECT count(*) FROM stores WHERE is_current = true").fetchone()[0]
    print(f"  Created {len(stores)} store records ({current_stores} current)")

    print("Generating customers data...")
    customers = generate_customers()
    load_table(con, "customers", """
        CREATE TABLE customers (
            customer_id BIGINT, customer_name VARCHAR, email VARCHAR, signup_date DATE,
            tier VARCHAR, valid_from DATE, valid_to DATE, is_current BOOLEAN
        )""", customers)
    current_customers = con.execute("SELECT count(*) FROM customers WHERE is_current = true").fetchone()[0]
    print(f"  Created {len(customers)} customer records ({current_customers} current)")

    print("Generating products data...")
    products = generate_products()
    load_table(con, "products", """
        CREATE TABLE products (
            product_id BIGINT, product_name VARCHAR, category VARCHAR, base_price DOUBLE
        )""", products)
    print(f"  Created {len(products)} product records")

    print("Generating sales data...")
    sales = generate_sales(con)
    load_table(con, "sales", """
        CREATE TABLE sales (
            transaction_id BIGINT, customer_id BIGINT, store_id BIGINT, product_id BIGINT,
            sale_date DATE, quantity BIGINT, unit_price DOUBLE, amount DOUBLE
        )""", sales)
    print(f"  Created {len(sales)} sales transactions")

    # Save to parquet
    output_dir = Path(__file__).parent.parent / "data" / "generated_data"
    output_dir.mkdir(exist_ok=True)
    print(f"\nSaving data to {output_dir}...")

    for table in ["stores", "customers", "products", "sales"]:
        con.execute(f"COPY {table} TO '{output_dir}/raw_{table}.parquet' (FORMAT PARQUET)")
        print(f"  ✓ Saved raw_{table}.parquet")

    con.close()


if __name__ == "__main__":
    main()
