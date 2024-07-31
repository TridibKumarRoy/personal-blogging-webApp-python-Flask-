# Flask Blog Application

A simple blog application built with Flask, SQLAlchemy, and Bootstrap. This application allows users to view posts, and administrators to manage content and user interactions.

## Features

- User authentication for admin access.
- CRUD operations for posts and contacts.
- Custom error handling for common HTTP errors.
- File upload and management for post images.
- Pagination for posts.

## Prerequisites

- Python 3.x
- Flask
- Flask-SQLAlchemy
- MySQL database

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/TridibKumarRoy/personal-blogging-webApp-python-Flask-.git


## Database Setup

This project uses a relational database to store data for contacts and posts. The database schema is managed using SQLAlchemy.

### `aql_queries.sql`

The `queries.sql` file contains SQL commands to set up and manage the database schema for the application. It includes commands to create, drop, and query tables for storing blog posts and contact information.

**Contents of `queries.sql`:**

```sql
-- Create the database
CREATE DATABASE blog1;

-- Use the created database
USE blog1;

-- Create the 'posts' table
CREATE TABLE posts (
    sno INT PRIMARY KEY AUTO_INCREMENT,
    title TEXT,
    content TEXT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    slug TEXT,
    img_path VARCHAR(100)
);

-- Drop the 'posts' table (for testing or reinitialization)
DROP TABLE posts;

-- Query to select all entries from 'posts'
SELECT * FROM posts;

-- Create the 'contacts' table
CREATE TABLE contacts (
    sno INT PRIMARY KEY AUTO_INCREMENT,
    name TEXT(50),
    email VARCHAR(50),
    phone_num VARCHAR(13),
    message TEXT(500),
    date DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Drop the 'contacts' table (for testing or reinitialization)
DROP TABLE contacts;

-- Query to select all entries from 'contacts'
SELECT * FROM contacts;


### Database Configuration

The database configuration is specified in the `config.json` file. Depending on the environment (local or production), different database URIs can be used.


**Example `config.json`:**

```json
{
  "params": {
    "local_server": {
      "val": true
    },
    "DBURI": "mysql://user:password@localhost/db_name", 
    "ProdDBURI": "mysql://user:password@localhost/db_name",
  }
}
