SELECT sector_number as sec_num,
	ROUND(AVG(price/square), 0) as 'price_sot',
	COUNT(ads_id) as ads_count,
	ROUND(AVG(square), 1) as avg_square,
	SUM(CASE WHEN ads_owner = 'Собственник' THEN 1 ELSE 0 END) AS owner_ads_count,
	ROUND(AVG(CASE WHEN ads_owner = 'Собственник' THEN price/square ELSE NULL END), 0) AS owner_price_sotka,
  SUM(CASE WHEN ads_owner = 'Риелтор' THEN 1 ELSE 0 END) AS rieltor_ads_count,
	ROUND(AVG(CASE WHEN ads_owner = 'Риелтор' THEN price/square ELSE NULL END), 0) AS rieltor_price_sotka,
	SUM(CASE WHEN ads_owner = 'Агентство недвижимости' THEN 1 ELSE 0 END) AS agency_ads_count,
	ROUND(AVG(CASE WHEN ads_owner = 'Агентство недвижимости' THEN price/square ELSE NULL END), 0) AS agency_price_sotka,
	SUM(CASE WHEN ads_owner = 'Застройщик' THEN 1 ELSE 0 END) AS developer_ads_count,
	ROUND(AVG(CASE WHEN ads_owner = 'Застройщик' THEN price/square ELSE NULL END), 0) AS developer_price_sotka,
  SUM(CASE WHEN ads_owner = '' THEN 1 ELSE 0 END) AS empty_owner_ads_count,
	ROUND(AVG(CASE WHEN ads_owner = '' THEN price/square ELSE NULL END), 0) AS empty_owner_price_sotka
FROM ads
WHERE sector_number in (51, 52, 53, 54, 55, 56, 57)
GROUP BY sector_number;