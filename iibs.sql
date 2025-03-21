CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL, 
    description TEXT, 
    status VARCHAR(20) DEFAULT 'Active' 
);

CREATE TABLE services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    category_id INTEGER NOT NULL,
    image VARCHAR(255), 
    description TEXT, 
    status VARCHAR(20) DEFAULT 'Active',
    supporting_files VARCHAR(255),
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

CREATE TABLE service_attributes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_id INTEGER NOT NULL,
    attribute_name VARCHAR(100) NOT NULL, 
    attribute_value TEXT NOT NULL, 
    attribute_type VARCHAR(50),
    FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
);

CREATE TABLE announcements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    image VARCHAR(255),
    description TEXT,
    publish_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Draft',
    is_urgent BOOLEAN DEFAULT FALSE,
);

CREATE TABLE business_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL, 
    logo VARCHAR(255), 
    description TEXT 
);

CREATE TABLE business_info_attributes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_info_id INTEGER NOT NULL,
    attribute_name VARCHAR(100) NOT NULL, 
    attribute_value TEXT NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (business_info_id) REFERENCES business_info(id) ON DELETE CASCADE
);

CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    operating_hours VARCHAR(100),
    contact_info TEXT
);

CREATE TABLE downloads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    file VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50)
);