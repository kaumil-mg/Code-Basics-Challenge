use retail_events_db;

-- Q1  
SELECT distinct 
	p.product_name,
    e.promo_type,
    e.base_price 
FROM 
	fact_events e 
join 
	dim_products p on e.product_code = p.product_code 
where 
	e.promo_type="BOGOF" and e.base_price>=500;

-- Q2
 select distinct 
	city, 
    count(store_id) 
from 
	dim_stores 
group by 
	city;
 
 -- Q3
-- alter table fact_events rename column `quantity_sold(after_promo)` to quantity_sold_ap;
-- alter table fact_events rename column `quantity_sold(before_promo)` to quantity_sold_bp;

SELECT DISTINCT
    c.campaign_name,
    SUM(e.quantity_sold_bp * e.base_price) AS revenue_before_promotion,
    SUM(e.quantity_sold_ap * e.base_price) AS revenue_after_promotion,
    (
        (
            SUM(e.quantity_sold_ap * e.base_price) -
            SUM(e.quantity_sold_bp * e.base_price)
        ) / NULLIF(SUM(e.quantity_sold_bp * e.base_price), 0)
    ) * 100 AS difference
FROM
    fact_events e
JOIN
    dim_campaigns c ON e.campaign_id = c.campaign_id
GROUP BY
    c.campaign_name;

-- Q4
select distinct 
	p.category, 
    ((sum(e.quantity_sold_ap)-sum(e.quantity_sold_bp))/nullif(sum(e.quantity_sold_bp),0))*100 as ISU 
from 
	fact_events e 
join 
	dim_products p on e.product_code = p.product_code 
join  
	dim_campaigns c on e.campaign_id=c.campaign_id 
where 
	c.campaign_name='Diwali'  
group by 
	p.category
order by ISU desc;


-- Q5
SELECT DISTINCT
	p.product_name,
    p.category,
    c.campaign_name,
    SUM(e.quantity_sold_bp * e.base_price) AS revenue_before_promotion,
    SUM(e.quantity_sold_ap * e.base_price) AS revenue_after_promotion,
    (
        (
            SUM(e.quantity_sold_ap * e.base_price) -
            SUM(e.quantity_sold_bp * e.base_price)
        ) / NULLIF(SUM(e.quantity_sold_bp * e.base_price), 0)
    ) * 100 AS IR
FROM
    fact_events e
JOIN
    dim_campaigns c ON e.campaign_id = c.campaign_id
JOIN
	dim_products p ON e.product_code=p.product_code
GROUP BY
    p.product_name
order by
	IR desc
LIMIT 5;

