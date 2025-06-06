# Walmart Sales Analysis

![Walmart Logo](https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Walmart_logo.svg/1280px-Walmart_logo.svg.png)

A Python-based analysis of Walmart retail sales data (2001-2015) with data cleaning, MySQL integration, and visualization.

## Project Overview

This project analyzes Walmart retail sales data using Python, pandas, and MySQL. It includes data cleaning, database operations, advanced SQL queries with window functions, and visualizations to extract meaningful business insights from retail sales patterns.



## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
 - [Prerequisites](#prerequisites)
 - [Installation](#installation)
- [Usage](#usage)
 - [Data Cleaning](#data-cleaning)
 - [Database Operations](#database-operations)
 - [Data Analysis](#data-analysis)
- [Key Insights](#key-insights)
- [Deployment](#deployment)
- [Future Enhancements](#future-enhancements)
- [Author](#author)
- [License](#license)
- [Acknowledgements](#acknowledgements)


## Features

- **Data Cleaning**: Processes raw Excel data, handles special characters, and formats dates
- **MySQL Integration**: Connects to MySQL database for efficient data storage and retrieval
- **Sales Growth Analysis**: Calculates year-over-year sales growth rates by state
- **Profitability Analysis**: Identifies most profitable product categories by region
- **Data Visualization**: Creates insightful visualizations of sales trends and profitability

## Requirements

- Python 3.x
- pandas
- pymysql
- sqlalchemy
- matplotlib
- seaborn
- MySQL Server

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ramsharan47/walmart_analysis.git
   ```

2. Install required Python packages:
   ```bash
   pip install pandas pymysql sqlalchemy matplotlib seaborn
   ```

3. Set up MySQL database:
   ```bash
   sudo apt install mysql-server
   sudo mysql_secure_installation
   sudo systemctl status mysql
   ```

4. Create database and table:
   ```sql
   CREATE DATABASE walmart;
   USE walmart;
   
   CREATE TABLE sales (
     `Row ID` INT,
     `Order ID` INT,
     `Order Date` DATE,
     `Order Priority` TEXT,
     `Order Quantity` INT,
     `Sales` DOUBLE,
     `Discount` DOUBLE,
     `Ship Mode` TEXT,
     `Profit` DOUBLE,
     `Unit Price` DOUBLE,
     `Shipping Cost` DOUBLE,
     `Customer Name` TEXT,
     `Customer Age` TEXT,
     `City` TEXT,
     `Zip Code` INT,
     `State` TEXT,
     `Region` TEXT,
     `Customer Segment` TEXT,
     `Product Category` TEXT,
     `Product Sub-Category` TEXT,
     `Product Name` TEXT,
     `Product Container` TEXT,
     `Product Base Margin` TEXT,
     `Ship Date` TEXT
   );
   ```

5. Place the `WalmartRetailSales.xlsx` file in the project root directory.

## Usage

The script performs several operations in sequence:

1. **Data Cleaning**:
   - Reads Excel data
   - Removes special characters from product names
   - Converts date fields to proper format
   - Exports cleaned data as CSV

2. **Database Operations**:
   - Connects to MySQL
   - Updates data types
   - Performs state abbreviation normalization

3. **Analysis**:
   - Creates views for yearly state sales
   - Calculates sales growth rates using SQL window functions
   - Analyzes profitability by product sub-category and region

4. **Visualization**:
   - Creates clustered bar charts of profits by sub-category and region
   - Generates faceted plots for regional analysis
   - Highlights top-performing product sub-categories

## Key Visualizations

- Top 5 most profitable product sub-categories by region
- Regional profit analysis with separate bar plots
- Highest profit product sub-category in each region

## Configuration

Before running the script, update the database connection details:
```python
engine = create_engine('mysql+pymysql://username:password@localhost/walmart')
```

## Running the Analysis

```bash
python walmart_analysis.py
```

## Deployment

This project is designed for flexible deployment but still not deployed but can done by using GitHub CI/CD pipeline, flask/django framework, fastapi and aws server or heruko:

## Results

The analysis reveals:
- Year-over-year sales growth patterns by state
- Regional profitability differences
- Top-performing product subcategories across different regions
### Server Deployment

For server deployment:
1. Set up a server with Python and MySQL
2. Configure database connection parameters in the scripts
3. Schedule regular runs using cron or similar tools

### Dashboard Integration

The visualization components can be integrated with web frameworks:
1. Use Flask or Django to create a web interface
2. Embed visualizations in HTML templates
3. Deploy to a web server for team access


## Author

Ram Sharan Pokharel

## License

This project is open source and available under the [MIT License](LICENSE).
