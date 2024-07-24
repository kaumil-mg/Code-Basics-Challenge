import pandas as pd
from sqlalchemy import create_engine
from dash import Dash, dcc, html
import plotly.express as px

# Replace the following placeholders with your actual database credentials
db_username = 'root'
db_password = '@Work00'
db_host = '127.0.0.1'
db_port = '8080'
db_name = 'gdb023'

# Create a database connection
engine = create_engine(f'mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')

def execute_query(query):
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

# Execute all queries
query1 = """
SELECT DISTINCT market 
FROM dim_customer 
WHERE customer = 'Atliq Exclusive' 
AND region = 'APAC';
"""
result1 = execute_query(query1)

query2 = """
WITH product_counts AS (
    SELECT COUNT(DISTINCT product_code) AS unique_products_2020 
    FROM fact_sales_monthly 
    WHERE fiscal_year = 2020 
    UNION ALL 
    SELECT COUNT(DISTINCT product_code) AS unique_products_2021 
    FROM fact_sales_monthly 
    WHERE fiscal_year = 2021
)
SELECT 
    (SELECT unique_products_2020 FROM product_counts WHERE unique_products_2020 IS NOT NULL) AS unique_products_2020,
    (SELECT unique_products_2021 FROM product_counts WHERE unique_products_2021 IS NOT NULL) AS unique_products_2021,
    ((SELECT unique_products_2021 FROM product_counts WHERE unique_products_2021 IS NOT NULL) - 
    (SELECT unique_products_2020 FROM product_counts WHERE unique_products_2020 IS NOT NULL)) * 100.0 / 
    (SELECT unique_products_2020 FROM product_counts WHERE unique_products_2020 IS NOT NULL) AS percentage_chg;
"""
result2 = execute_query(query2)

query3 = """
SELECT 
    segment, 
    COUNT(DISTINCT product_code) AS product_count 
FROM dim_product 
GROUP BY segment 
ORDER BY product_count DESC;
"""
result3 = execute_query(query3)

query4 = """
WITH product_counts AS (
    SELECT 
        segment,
        COUNT(DISTINCT CASE WHEN fiscal_year = 2020 THEN product_code END) AS product_count_2020,
        COUNT(DISTINCT CASE WHEN fiscal_year = 2021 THEN product_code END) AS product_count_2021
    FROM fact_sales_monthly 
    JOIN dim_product USING (product_code)
    GROUP BY segment
)
SELECT 
    segment,
    product_count_2020,
    product_count_2021,
    (product_count_2021 - product_count_2020) AS difference
FROM product_counts
ORDER BY difference DESC
LIMIT 1;
"""
result4 = execute_query(query4)

query5 = """
(SELECT 
    product_code, 
    product, 
    manufacturing_cost 
FROM fact_manufacturing_cost 
JOIN dim_product USING (product_code)
ORDER BY manufacturing_cost DESC 
LIMIT 1)
UNION ALL
(SELECT 
    product_code, 
    product, 
    manufacturing_cost 
FROM fact_manufacturing_cost 
JOIN dim_product USING (product_code)
ORDER BY manufacturing_cost ASC 
LIMIT 1);
"""
result5 = execute_query(query5)

query6 = """
SELECT 
    dc.customer_code, 
    dc.customer, 
    AVG(fpd.pre_invoice_discount_pct) AS average_discount_percentage
FROM fact_pre_invoice_deductions fpd
JOIN dim_customer dc ON fpd.customer_code = dc.customer_code
WHERE fpd.fiscal_year = 2021 AND dc.market = 'India'
GROUP BY dc.customer_code, dc.customer
ORDER BY average_discount_percentage DESC
LIMIT 5;
"""
result6 = execute_query(query6)

query7 = """
SELECT 
    DATE_FORMAT(date, '%Y-%m') AS Month,
    YEAR(date) AS Year,
    SUM(sold_quantity * gross_price) AS Gross_sales_Amount
FROM fact_sales_monthly fsm
JOIN dim_customer dc ON fsm.customer_code = dc.customer_code
JOIN fact_gross_price fgp ON fsm.product_code = fgp.product_code AND fsm.fiscal_year = fgp.fiscal_year
WHERE dc.customer = 'Atliq Exclusive'
GROUP BY Year, Month
ORDER BY Year, Month;
"""
result7 = execute_query(query7)

query8 = """
WITH quarterly_sales AS (
    SELECT 
        QUARTER(date) AS Quarter,
        SUM(sold_quantity) AS total_sold_quantity
    FROM fact_sales_monthly
    WHERE fiscal_year = 2020
    GROUP BY QUARTER(date)
)
SELECT 
    CONCAT('Q', Quarter) AS Quarter,
    total_sold_quantity
FROM quarterly_sales
ORDER BY total_sold_quantity DESC
LIMIT 1;
"""
result8 = execute_query(query8)

query9 = """
WITH total_sales AS (
    SELECT 
        SUM(sold_quantity * gross_price) AS total_gross_sales
    FROM fact_sales_monthly fsm
    JOIN fact_gross_price fgp ON fsm.product_code = fgp.product_code AND fsm.fiscal_year = fgp.fiscal_year
    WHERE fsm.fiscal_year = 2021
)
SELECT 
    channel,
    SUM(fsm.sold_quantity * fgp.gross_price) / 1000000 AS gross_sales_mln,
    (SUM(fsm.sold_quantity * fgp.gross_price) / ts.total_gross_sales) * 100 AS percentage
FROM fact_sales_monthly fsm
JOIN dim_customer dc ON fsm.customer_code = dc.customer_code
JOIN fact_gross_price fgp ON fsm.product_code = fgp.product_code AND fsm.fiscal_year = fgp.fiscal_year
JOIN total_sales ts
WHERE fsm.fiscal_year = 2021
GROUP BY channel
ORDER BY gross_sales_mln DESC;
"""
result9 = execute_query(query9)

query10 = """
WITH ranked_products AS (
    SELECT 
        dp.division,
        fsm.product_code,
        dp.product,
        SUM(fsm.sold_quantity) AS total_sold_quantity,
        RANK() OVER (PARTITION BY dp.division ORDER BY SUM(fsm.sold_quantity) DESC) AS rank_order
    FROM fact_sales_monthly fsm
    JOIN dim_product dp ON fsm.product_code = dp.product_code
    WHERE fsm.fiscal_year = 2021
    GROUP BY dp.division, fsm.product_code, dp.product
)
SELECT 
    division,
    product_code,
    product,
    total_sold_quantity,
    rank_order
FROM ranked_products
WHERE rank_order <= 3
ORDER BY division, rank_order;
"""
result10 = execute_query(query10)

# Close the database connection
engine.dispose()

# Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1('SQL Queries and Results'),

    html.H2('Query 1: Markets in which customer "Atliq Exclusive" operates in the APAC region'),
    dcc.Graph(figure=px.bar(result1, x='market', title='Markets for Atliq Exclusive in APAC')),

    html.H2('Query 2: Percentage of unique product increase in 2021 vs. 2020'),
    html.Table([
        html.Tr([html.Th(col) for col in result2.columns])] + 
        [html.Tr([html.Td(result2.iloc[0][col]) for col in result2.columns])]
    ),

    html.H2('Query 3: Unique product counts for each segment'),
    dcc.Graph(figure=px.bar(result3, x='segment', y='product_count', title='Unique Product Counts per Segment')),

    html.H2('Query 4: Segment with the most increase in unique products in 2021 vs 2020'),
    html.Table([
        html.Tr([html.Th(col) for col in result4.columns])] + 
        [html.Tr([html.Td(result4.iloc[0][col]) for col in result4.columns])]
    ),

    html.H2('Query 5: Products with the highest and lowest manufacturing costs'),
    html.Table([
        html.Tr([html.Th(col) for col in result5.columns])] + 
        [html.Tr([html.Td(result5.iloc[i][col]) for col in result5.columns]) for i in range(len(result5))]
    ),

    html.H2('Query 6: Top 5 customers with highest average pre_invoice_discount_pct in 2021 in India'),
    dcc.Graph(figure=px.bar(result6, x='customer', y='average_discount_percentage', title='Top 5 Customers by Average Discount Percentage')),

    html.H2('Query 7: Gross sales amount for "Atliq Exclusive" for each month'),
    dcc.Graph(figure=px.line(result7, x='Month', y='Gross_sales_Amount', title='Monthly Gross Sales for Atliq Exclusive')),

    html.H2('Query 8: Quarter of 2020 with the maximum total_sold_quantity'),
    html.Table([
        html.Tr([html.Th(col) for col in result8.columns])] + 
        [html.Tr([html.Td(result8.iloc[0][col]) for col in result8.columns])]
    ),

    html.H2('Query 9: Channel with more gross sales in 2021 and percentage of contribution'),
    dcc.Graph(figure=px.pie(result9, names='channel', values='gross_sales_mln', title='Gross Sales by Channel')),

    html.H2('Query 10: Top 3 products in each division with high total_sold_quantity in 2021'),
    dcc.Graph(figure=px.bar(result10, x='division', y='total_sold_quantity', color='product', title='Top 3 Products by Division'))
])

if __name__ == '__main__':
    app.run_server(debug=True)
