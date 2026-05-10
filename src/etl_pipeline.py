from extract import extract
from transform import transform
from load import load


def main():

    # Extract
    catalog, web, products = extract()

    # Transform
    final_df = transform(catalog, web, products)

    print(final_df.head())

    # Load
    load(final_df)


if __name__ == "__main__":
    main()
