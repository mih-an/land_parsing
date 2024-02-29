SELECT sector_number as sec_num,
	COUNT(ads_id) as ads_count,
	ROUND(AVG(square), 1) as avg_square,
	SUM(CASE WHEN square <= 5 THEN 1 ELSE 0 END) AS less_5_sot_count,
	SUM(CASE WHEN square > 5 and square <=6 THEN 1 ELSE 0 END) AS 5_6_sot_count,
	SUM(CASE WHEN square > 6 and square <=8 THEN 1 ELSE 0 END) AS 6_8_sot_count,
	SUM(CASE WHEN square > 8 and square <=10 THEN 1 ELSE 0 END) AS 8_10_sot_count,
	SUM(CASE WHEN square > 10 and square <=12 THEN 1 ELSE 0 END) AS 10_12_sot_count,
	SUM(CASE WHEN square > 12 and square <=15 THEN 1 ELSE 0 END) AS 12_15_sot_count,
	SUM(CASE WHEN square > 15 and square <=20 THEN 1 ELSE 0 END) AS 15_20_sot_count,
	SUM(CASE WHEN square > 20 and square <=30 THEN 1 ELSE 0 END) AS 20_30_sot_count,
	SUM(CASE WHEN square > 30 and square <=60 THEN 1 ELSE 0 END) AS 30_60_sot_count,
	SUM(CASE WHEN square > 60 THEN 1 ELSE 0 END) AS 60_plus_sot_count,
	ROUND(AVG(price/square), 0) as 'price_sot',
	ROUND(AVG(CASE WHEN square <= 5 THEN price/square ELSE NULL END), 0) AS less_5_price_sot,
	ROUND(AVG(CASE WHEN square > 5 and square <=6 THEN price/square ELSE NULL END), 0) AS 5_6_price_sot,
	ROUND(AVG(CASE WHEN square > 6 and square <=8 THEN price/square ELSE NULL END), 0) AS 6_8_price_sot,
	ROUND(AVG(CASE WHEN square > 8 and square <=10 THEN price/square ELSE NULL END), 0) AS 8_10_price_sot,
	ROUND(AVG(CASE WHEN square > 10 and square <=12 THEN price/square ELSE NULL END), 0) AS 10_12_price_sot,
	ROUND(AVG(CASE WHEN square > 12 and square <=15 THEN price/square ELSE NULL END), 0) AS 12_15_price_sot,
	ROUND(AVG(CASE WHEN square > 15 and square <=20 THEN price/square ELSE NULL END), 0) AS 15_20_price_sot,
	ROUND(AVG(CASE WHEN square > 20 and square <=30 THEN price/square ELSE NULL END), 0) AS 20_30_price_sot,
	ROUND(AVG(CASE WHEN square > 30 and square <=60 THEN price/square ELSE NULL END), 0) AS 30_60_price_sot,
	ROUND(AVG(CASE WHEN square > 60 THEN price/square ELSE NULL END), 0) AS 60_plus_price_sot

FROM ads
WHERE sector_number in (51, 52, 53, 54, 55, 56, 57)
GROUP BY sector_number;