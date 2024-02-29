SELECT ROUND(price/square, 0) as price_sot, ads.sector_number, sector_price_sot, ads.*
FROM ads LEFT JOIN
	(SELECT sector_number,
		ROUND(AVG(price/square), 0) as 'sector_price_sot'
	FROM ads
	WHERE sector_number in (51) and vri = 'ИЖС'
	GROUP BY sector_number) as S ON ads.sector_number = S.sector_number
WHERE ads.sector_number in (51) AND price/square <= sector_price_sot*0.8 and vri = 'ИЖС'