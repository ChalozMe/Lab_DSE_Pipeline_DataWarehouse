DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_supplier;
DROP TABLE IF EXISTS dim_tiempo;

CREATE TABLE dim_product (

    id SERIAL PRIMARY KEY,

    pcode VARCHAR(50) UNIQUE,

    tipo VARCHAR(100),

    descripcion VARCHAR(255),

    precio NUMERIC(10,2),

    costo NUMERIC(10,2)
);

CREATE TABLE dim_supplier (

    id SERIAL PRIMARY KEY,

    nombre VARCHAR(255) UNIQUE
);

CREATE TABLE dim_tiempo (

    id SERIAL PRIMARY KEY,

    fecha DATE UNIQUE,

    anio INTEGER,

    mes INTEGER,

    dia INTEGER
);

CREATE TABLE fact_sales (

    id SERIAL PRIMARY KEY,

    product_id INTEGER REFERENCES dim_product(id),

    supplier_id INTEGER REFERENCES dim_supplier(id),

    date_id INTEGER REFERENCES dim_tiempo(id),

    cantidad INTEGER,

    costo NUMERIC(10,2),

    ganancia NUMERIC(10,2)
);
