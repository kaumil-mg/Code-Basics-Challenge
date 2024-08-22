# Q1 Provide the list of markets in which customer "Atliq Exclusive" operates its business in the APAC region.

SELECT DISTINCT market FROM dim_customer WHERE customer = 'Atliq Exclusive' AND region = 'APAC';

# Q2 What is the percentage of unique product increase in 2021 vs. 2020? The final output contains these fields,
-- unique_products_2020
-- unique_products_2021
-- percentage_chg

WITH product_counts AS (
    SELECT 
        COUNT(DISTINCT product_code) AS unique_products,
        fiscal_year
    FROM fact_sales_monthly
    WHERE fiscal_year IN (2020, 2021)
    GROUP BY fiscal_year
)
SELECT 
    MAX(CASE WHEN fiscal_year = 2020 THEN unique_products ELSE 0 END) AS unique_products_2020,
    MAX(CASE WHEN fiscal_year = 2021 THEN unique_products ELSE 0 END) AS unique_products_2021,
    (MAX(CASE WHEN fiscal_year = 2021 THEN unique_products ELSE 0 END) - MAX(CASE WHEN fiscal_year = 2020 THEN unique_products ELSE 0 END)) * 100.0 / MAX(CASE WHEN fiscal_year = 2020 THEN unique_products ELSE 0 END) AS percentage_chg
FROM product_counts;

# Q3 Report with all the unique product counts for each segment

SELECT segment, COUNT(DISTINCT dp.product_code) AS product_count
FROM dim_product dp
JOIN fact_sales_monthly fsm ON dp.product_code = fsm.product_code
GROUP BY segment
ORDER BY product_count DESC;

# Q4 Segment with the most increase in unique products in 2021 vs 2020

WITH product_counts AS (
    SELECT 
        segment,
        COUNT(DISTINCT CASE WHEN fiscal_year = 2020 THEN dp.product_code ELSE NULL END) AS product_count_2020,
        COUNT(DISTINCT CASE WHEN fiscal_year = 2021 THEN dp.product_code ELSE NULL END) AS product_count_2021
    FROM dim_product dp
    JOIN fact_sales_monthly fsm ON dp.product_code = fsm.product_code
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

# Q5. Products with the highest and lowest manufacturing costs

(select dp.product,fmc.manufacturing_cost from dim_product dp join fact_manufacturing_cost fmc on dp.product_code = fmc.product_code order by fmc.manufacturing_cost desc limit 1)
union all 
(select dp.product,fmc.manufacturing_cost from dim_product dp join fact_manufacturing_cost fmc on dp.product_code = fmc.product_code order by fmc.manufacturing_cost asc limit 1);

# Q6. Top 5 customers who received an average high pre_invoice_discount_pct for the fiscal year 2021 in the Indian market
SELECT 
    dc.customer_code,
    dc.customer,
    AVG(fpid.pre_invoice_discount_pct) AS average_discount_percentage
FROM dim_customer dc
JOIN fact_pre_invoice_deductions fpid ON dc.customer_code = fpid.customer_code
WHERE fpid.fiscal_year = 2021 AND dc.market = 'India'
GROUP BY dc.customer_code, dc.customer
ORDER BY average_discount_percentage DESC
LIMIT 5;

# Q7. Gross sales amount for the customer “Atliq Exclusive” for each month
SELECT 
    EXTRACT(MONTH FROM fsm.date) AS Month,
    EXTRACT(YEAR FROM fsm.date) AS Year,
    SUM(fp.gross_price * fsm.sold_quantity) AS Gross_sales_Amount
FROM fact_sales_monthly fsm
JOIN fact_gross_price fp ON fsm.product_code = fp.product_code AND fsm.fiscal_year = fp.fiscal_year
JOIN dim_customer dc ON fsm.customer_code = dc.customer_code
WHERE dc.customer = 'Atliq Exclusive'
GROUP BY EXTRACT(YEAR FROM fsm.date), EXTRACT(MONTH FROM fsm.date)
ORDER BY Year, Month;


# Q8. Quarter of 2020 with the maximum total_sold_quantity

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

# Q9. Channel that brought more gross sales in the fiscal year 2021 and the percentage of contribution
WITH total_sales AS (
    SELECT 
        dc.channel,
        SUM(fp.gross_price * fsm.sold_quantity) / 1e6 AS gross_sales_mln,
        SUM(SUM(fp.gross_price * fsm.sold_quantity)) OVER () AS total_sales
    FROM fact_sales_monthly fsm
    JOIN fact_gross_price fp ON fsm.product_code = fp.product_code AND fsm.fiscal_year = fp.fiscal_year
    JOIN dim_customer dc ON fsm.customer_code = dc.customer_code
    WHERE fsm.fiscal_year = 2021
    GROUP BY dc.channel
)
SELECT 
    channel,
    gross_sales_mln,
    (gross_sales_mln / total_sales) * 100 AS percentage
FROM total_sales
ORDER BY gross_sales_mln DESC
LIMIT 1;


# Q10. Top 3 products in each division with the highest total_sold_quantity in fiscal year 2021

WITH ranked_products AS (
    SELECT 
        dp.division,
        dp.product_code,
        dp.product,
        SUM(fsm.sold_quantity) AS total_sold_quantity,
        RANK() OVER (PARTITION BY dp.division ORDER BY SUM(fsm.sold_quantity) DESC) AS rank_order
    FROM dim_product dp
    JOIN fact_sales_monthly fsm ON dp.product_code = fsm.product_code
    WHERE fsm.fiscal_year = 2021
    GROUP BY dp.division, dp.product_code, dp.product
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
