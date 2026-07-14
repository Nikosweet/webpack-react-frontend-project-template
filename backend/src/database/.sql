CREATE DATABASE pisdata;

CREATE TABLE person(
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    hashpassword VARCHAR(72),
    email VARCHAR(50),
    phone VARCHAR(15)
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    slug VARCHAR(50) NOT NULL UNIQUE,
    parent_id INTEGER NULL,
    
    CONSTRAINT fk_category_parent 
        FOREIGN KEY (parent_id) 
        REFERENCES categories(id) 
        ON DELETE SET NULL
);

CREATE INDEX idx_categories_parent_id ON categories(parent_id);
CREATE INDEX idx_categories_slug ON categories(slug);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    slug VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    sku VARCHAR(50) NOT NULL UNIQUE,
    brand VARCHAR(50),
    rating FLOAT DEFAULT 0.0 CHECK (rating >= 0 AND rating <= 5),
    review_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    specifications JSONB DEFAULT '{}'::jsonb,
);

CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_rating ON products(rating DESC);
CREATE INDEX idx_products_brand ON products(brand);
CREATE INDEX idx_products_active ON products(is_active);
CREATE INDEX idx_products_sku ON products(sku);


CREATE TABLE product_categories (
    product_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    
    PRIMARY KEY (product_id, category_id),

    CONSTRAINT fk_product_categories_product 
        FOREIGN KEY (product_id) 
        REFERENCES products(id) 
        ON DELETE CASCADE,
    
    CONSTRAINT fk_product_categories_category 
        FOREIGN KEY (category_id) 
        REFERENCES categories(id) 
        ON DELETE CASCADE
);

CREATE INDEX idx_product_categories_product ON product_categories(product_id);
CREATE INDEX idx_product_categories_category ON product_categories(category_id);

CREATE TABLE product_images (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    url VARCHAR(500) NOT NULL UNIQUE,
    is_main BOOLEAN DEFAULT FALSE,
    sort_order INTEGER DEFAULT 0,
    alt_text VARCHAR(40),
    
    CONSTRAINT fk_product_images_product 
        FOREIGN KEY (product_id) 
        REFERENCES products(id) 
        ON DELETE CASCADE
);

CREATE INDEX idx_product_images_product ON product_images(product_id);
CREATE INDEX idx_product_images_main ON product_images(is_main);
CREATE INDEX idx_product_images_order ON product_images(product_id, sort_order);