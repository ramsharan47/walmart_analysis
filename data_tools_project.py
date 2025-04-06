
import pandas as pd
import csv
import pymysql
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt
import seaborn as sns
# Set visualization style
sns.set(style="whitegrid")
plt.figure(figsize=(12, 8))

"""## Data File Clean Up Prior to Import into MySQL"""

#Get dataset to clean and covert to CSV.
sales = pd.read_excel("WalmartRetailSales.xlsx")

# Remove ASCII special characters
sales["Product Name"] = sales["Product Name"].str.encode('ascii', errors='ignore').str.decode('ascii')

# Clean Up Orderdate
sales['Order Date'] = pd.to_datetime(sales['Order Date'])

# Export clean dataset as csv file.
sales.to_csv("WalmartRetailSales_Cleaned.csv", sep="|", quoting=csv.QUOTE_ALL, doublequote=False, escapechar="\\", index=False)

"""## Question Analysis Starts Here

"""

#Connect to MySQL Server Database

#****UPDATE THIS ONE WITH YOUR DATABASE USER INFO***

engine = create_engine('mysql+pymysql://root:database123@localhost/walmart')

#Create connection variable.
com = engine.connect()

#review dataframe
pd.read_sql_query("SELECT * FROM walmart.sales", com)

#Update Order Date to a DATE type column
com.execute(text("ALTER TABLE sales MODIFY `Order Date` DATE;"))

#review column types to check upate to Order Date column
query = "SHOW COLUMNS FROM sales;"
df_columns = pd.read_sql(query, con=engine)
print(df_columns)

pd.read_sql_query("SELECT YEAR(`Order Date`) AS Year,COUNT(*) AS Order_Line_Items FROM sales GROUP BY Year ORDER BY Year;", com)

# Update state abbreviations to full names
update_query = """
UPDATE sales
SET State = CASE
    WHEN State = 'MA' THEN 'Massachusetts'
    WHEN State = 'MO' THEN 'Missouri'
    ELSE State
END;
"""
com.execute(text(update_query))
com.commit()

# Step 2: Create Yearly Sales per State (2012-2015)
# create a SQL view for easier reference
view_query = """
CREATE OR REPLACE VIEW yearly_state_sales AS
SELECT
    State,
    YEAR(`Order Date`) AS Order_Year,
    SUM(Sales) AS Total_Sales
FROM sales
WHERE YEAR(`Order Date`) BETWEEN 2012 AND 2015
GROUP BY State, Order_Year
ORDER BY State, Order_Year;
"""
com.execute(text(view_query))

#Step 3: Calculate Sales Growth Rate
# Query with LAG function to calculate growth rate
growth_query = """
WITH yearly_data AS (
    SELECT * FROM yearly_state_sales
)
SELECT
    State,
    Order_Year,
    Total_Sales,
    LAG(Total_Sales) OVER (PARTITION BY State ORDER BY Order_Year) AS Previous_Year_Sales,
    ROUND(
        (Total_Sales - LAG(Total_Sales) OVER (PARTITION BY State ORDER BY Order_Year)) /
        LAG(Total_Sales) OVER (PARTITION BY State ORDER BY Order_Year) * 100,
    2) AS Growth_Rate_Pct
FROM yearly_data
ORDER BY State, Order_Year;
"""

# Save to DataFrame for visualization
sales_growth_df = pd.read_sql_query(growth_query, com)
sales_growth_df

# Save to DataFrame for visualization
sales_growth_df = pd.read_sql_query(growth_query, com)
sales_growth_df

## Getting profit per Product Sub-Category per Region (2012-2015)
profit_query = """
SELECT
    Region,
    `Product Sub-Category` AS Sub_Category,
    SUM(Profit) AS Total_Profit,
    COUNT(*) AS Order_Count
FROM sales
WHERE YEAR(`Order Date`) BETWEEN 2012 AND 2015
GROUP BY Region, `Product Sub-Category`
ORDER BY Region, Total_Profit DESC;
"""

profit_df = pd.read_sql_query(profit_query, com)
print("Profit by Sub-Category and Region:")
display(profit_df.head())

#STEP 2: Finding top Product Sub-Category in each Region
top_products_query = """
WITH ranked_products AS (
    SELECT
        Region,
        `Product Sub-Category` AS Sub_Category,
        SUM(Profit) AS Total_Profit,
        RANK() OVER (PARTITION BY Region ORDER BY SUM(Profit) DESC) AS rank_num
    FROM sales
    WHERE YEAR(`Order Date`) BETWEEN 2012 AND 2015
    GROUP BY Region, `Product Sub-Category`
)
SELECT Region, Sub_Category, Total_Profit
FROM ranked_products
WHERE rank_num = 1
ORDER BY Total_Profit DESC;
"""

top_products_df = pd.read_sql_query(top_products_query, com)

print("\nTop Products by Region:")
display(top_products_df)

## STEP 3: Create Visualizations

# Visualization 1: Clustered Bar Chart of Profits by Sub-Category and Region
plt.figure(figsize=(14, 8))
top_n = 5  # Show top 5 sub-categories per region

# Get top sub-categories for each region
top_subcats = profit_df.groupby('Region').apply(
    lambda x: x.nlargest(top_n, 'Total_Profit')
).reset_index(drop=True)

# Create clustered bar plot
sns.barplot(
    x='Total_Profit',
    y='Sub_Category',
    hue='Region',
    data=top_subcats,
    palette='viridis'
)

plt.title(f'Top {top_n} Most Profitable Product Sub-Categories by Region (2012-2015)')
plt.xlabel('Total Profit ($)')
plt.ylabel('Product Sub-Category')
plt.tight_layout()
plt.show()

# Visualization 2: Separate Bar Plots for Each Region
g = sns.FacetGrid(
    top_subcats,
    col='Region',
    col_wrap=2,
    height=5,
    aspect=1.5,
    sharey=False
)
g.map(sns.barplot, 'Total_Profit', 'Sub_Category', palette='rocket')
g.set_axis_labels('Total Profit ($)', 'Product Sub-Category')
g.fig.suptitle('Most Profitable Product Sub-Categories by Region (2012-2015)', y=1.02)
plt.tight_layout()
plt.show()

# Visualization 3: Top Product per Region (Highlighted)
plt.figure(figsize=(10, 6))
sns.barplot(
    x='Total_Profit',
    y='Region',
    hue='Sub_Category',
    data=top_products_df,
    palette='coolwarm',
    dodge=False
)
plt.title('Highest Profit Product Sub-Category in Each Region (2012-2015)')
plt.xlabel('Total Profit ($)')
plt.ylabel('Region')
plt.legend(title='Product Sub-Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

