CREATE TABLE sales_fact (
    id_x INTEGER,
    inv VARCHAR(50),
    date TIMESTAMP,
    catalog VARCHAR(50),
    pcode VARCHAR(50),
    qty FLOAT,
    custnum INTEGER,

    id_y INTEGER,
    type VARCHAR(100),
    descrip TEXT,
    price FLOAT,
    cost FLOAT,
    supplier TEXT
);
