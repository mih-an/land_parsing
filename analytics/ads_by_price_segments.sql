SELECT sector_number as sec_num,
	COUNT(ads_id) as ads_count,
	ROUND(AVG(square), 1) as avg_square,
	ROUND(AVG(price/square), 0) as 'price_sot',
	SUM(CASE WHEN price <= 3000000 THEN 1 ELSE 0 END) AS less_3,
	SUM(CASE WHEN price > 3000000 and price <= 5000000 THEN 1 ELSE 0 END) AS 3_5,
	SUM(CASE WHEN price > 5000000 and price <= 8000000 THEN 1 ELSE 0 END) AS 5_8,
	SUM(CASE WHEN price > 8000000 and price <= 10000000 THEN 1 ELSE 0 END) AS 8_10,
	SUM(CASE WHEN price > 10000000 and price <= 12000000 THEN 1 ELSE 0 END) AS 10_12,
	SUM(CASE WHEN price > 12000000 and price <= 15000000 THEN 1 ELSE 0 END) AS 12_15,
	SUM(CASE WHEN price > 15000000 and price <= 20000000 THEN 1 ELSE 0 END) AS 15_20,
	SUM(CASE WHEN price > 20000000 and price <= 30000000 THEN 1 ELSE 0 END) AS 20_30,
	SUM(CASE WHEN price > 30000000 THEN 1 ELSE 0 END) AS 30_plus,

	ROUND(AVG(CASE WHEN price <= 3000000 THEN price/square ELSE NULL END), 0) AS less_3_p_s,
	ROUND(AVG(CASE WHEN price > 3000000 and price <= 5000000 THEN price/square ELSE NULL END), 0) AS 3_5_p_s,
	ROUND(AVG(CASE WHEN price > 5000000 and price <= 8000000 THEN price/square ELSE NULL END), 0) AS 5_8_p_s,
	ROUND(AVG(CASE WHEN price > 8000000 and price <= 10000000 THEN price/square ELSE NULL END), 0) AS 8_10_p_s,
	ROUND(AVG(CASE WHEN price > 10000000 and price <= 12000000 THEN price/square ELSE NULL END), 0) AS 10_12_p_s,
	ROUND(AVG(CASE WHEN price > 12000000 and price <= 15000000 THEN price/square ELSE NULL END), 0) AS 12_15_p_s,
	ROUND(AVG(CASE WHEN price > 15000000 and price <= 20000000 THEN price/square ELSE NULL END), 0) AS 15_20_p_s,
	ROUND(AVG(CASE WHEN price > 20000000 and price <= 30000000 THEN price/square ELSE NULL END), 0) AS 20_30_p_s,
	ROUND(AVG(CASE WHEN price > 30000000 THEN price/square ELSE NULL END), 0) AS 30_plus_p_s

FROM ads
WHERE sector_number in (51, 52, 53, 54, 55, 56, 57)
GROUP BY sector_number;