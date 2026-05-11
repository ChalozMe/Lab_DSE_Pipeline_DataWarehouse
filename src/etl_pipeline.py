from extract import extract
from load import create_tables, load_data
from transform import transform


def main():

    # Extract
    catalog, web, products = extract()

    # Transform
    final_df = transform(catalog, web, products)
    
    create_tables()
    # Load
    load_data(final_df)


if __name__ == "__main__":
    main()
