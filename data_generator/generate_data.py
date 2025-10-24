"""
Generate sample data for the testbed project.

Creates:
- Stores with SCD2 history
- Customers with SCD2 history
- Sales transactions over the last year
"""

import polars as pl
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

    return pl.DataFrame(stores)


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

    return pl.DataFrame(customers)


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

    return pl.DataFrame(products)


def generate_sales(stores_df, customers_df, products_df):
    """Generate sales transactions over the last year."""
    sales = []
    transaction_id = 1000

    # Get current stores and customers for transaction generation
    current_stores = stores_df.filter(pl.col("is_current") == True)["store_id"].to_list()
    current_customers = customers_df.filter(pl.col("is_current") == True)["customer_id"].to_list()
    all_products = products_df["product_id"].to_list()

    # Generate ~100 sales transactions
    for _ in range(100):
        sale_date = start_date + timedelta(days=random.randint(0, 365))
        customer_id = random.choice(current_customers)
        store_id = random.choice(current_stores)
        product_id = random.choice(all_products)

        # Get product base price and apply slight variation
        base_price = products_df.filter(pl.col("product_id") == product_id)["base_price"].item()
        # Apply 0-10% discount randomly
        discount_factor = random.uniform(0.9, 1.0)
        unit_price = round(base_price * discount_factor, 2)

        # Quantity varies by product
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

    return pl.DataFrame(sales)


def main():
    """Generate all data and save as parquet files."""
    print("Generating stores data...")
    stores_df = generate_stores()
    print(f"  Created {len(stores_df)} store records ({stores_df['is_current'].sum()} current)")

    print("Generating customers data...")
    customers_df = generate_customers()
    print(f"  Created {len(customers_df)} customer records ({customers_df['is_current'].sum()} current)")

    print("Generating products data...")
    products_df = generate_products()
    print(f"  Created {len(products_df)} product records")

    print("Generating sales data...")
    sales_df = generate_sales(stores_df, customers_df, products_df)
    print(f"  Created {len(sales_df)} sales transactions")

    # Save to parquet
    output_dir = Path(__file__).parent.parent / "src_db" / "src_data"
    output_dir.mkdir(exist_ok=True)
    print(f"\nSaving data to {output_dir}...")

    stores_df.write_parquet(output_dir / "raw_stores.parquet")
    print(f"  ✓ Saved raw_stores.parquet")

    customers_df.write_parquet(output_dir / "raw_customers.parquet")
    print(f"  ✓ Saved raw_customers.parquet")

    products_df.write_parquet(output_dir / "raw_products.parquet")
    print(f"  ✓ Saved raw_products.parquet")

    sales_df.write_parquet(output_dir / "raw_sales.parquet")
    print(f"  ✓ Saved raw_sales.parquet")


if __name__ == "__main__":
    main()
