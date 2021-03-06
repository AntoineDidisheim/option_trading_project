SELECT
    SP500_CONST_SECIDS.STOCK_KEY,
    SP500_CONST_SECIDS.TICKER,
    SP500_CONST_SECIDS.GV_KEY,
    'S&P 500'                  AS INDEX_NAME,
    SECURITY_PRICE.CLOSE_PRICE AS s_close,
    SECURITY_PRICE.ADJUSTMENT_FACTOR_2,
    SECURITY_PRICE.SHARES_OUTSTANDING,
    OPTION_PRICE.DELTA,
    OPTION_PRICE.STRIKE,
    OPTION_PRICE.DATE,
    OPTION_PRICE.IMPLIED_VOLATILITY,
    OPTION_PRICE.EXPIRATION,
    OPTION_PRICE.BEST_OFFER,
    OPTION_PRICE.BEST_BID,
    OPTION_PRICE.CALL_PUT,
    OPTION_PRICE.VOLUME,
    OPTION_PRICE.OPEN_INTEREST,
    OPTION_VOLUME.VOLUME AS TOTAL_VOLUME,
    OPTION_VOLUME.OPEN_INTEREST AS TOTAL_OPEN_INTEREST,
    OPTION_PRICE.OPTION_ID,
    DATEDIFF(DAY, OPTION_PRICE.DATE, OPTION_PRICE.EXPIRATION) AS T,
    DATE_PART(week, OPTION_PRICE.DATE)                        AS dw,
    YEAR(OPTION_PRICE.DATE) AS YY
FROM
    SP500_CONST_SECIDS
INNER JOIN
    "OPTION_PRICE"
ON
    SP500_CONST_SECIDS.SECURITY_ID = OPTION_PRICE.SECURITY_ID
AND SP500_CONST_SECIDS.EFFECTIVE_DATE = OPTION_PRICE.DATE
INNER JOIN
    "SECURITY_PRICE"
ON
    SECURITY_PRICE.DATE = OPTION_PRICE.DATE
AND OPTION_PRICE.SECURITY_ID = SECURITY_PRICE.SECURITY_ID
INNER JOIN
    "OPTION_VOLUME"
ON
OPTION_VOLUME.SECURITY_ID = OPTION_PRICE.SECURITY_ID
AND OPTION_VOLUME.DATE
= OPTION_PRICE.DATE
AND OPTION_VOLUME.CALL_PUT
= OPTION_PRICE.CALL_PUT
WHERE T <=31 AND YY = 2019
UNION
SELECT
    SP500_CONST_SECIDS_V1.STOCK_KEY,
    SP500_CONST_SECIDS_V1.TICKER,
    SP500_CONST_SECIDS_V1.GV_KEY,
    'S&P 500'                  AS INDEX_NAME,
    SECURITY_PRICE.CLOSE_PRICE AS s_close,
    SECURITY_PRICE.ADJUSTMENT_FACTOR_2,
    SECURITY_PRICE.SHARES_OUTSTANDING,
    OPTION_PRICE.DELTA,
    OPTION_PRICE.STRIKE,
    OPTION_PRICE.DATE,
    OPTION_PRICE.IMPLIED_VOLATILITY,
    OPTION_PRICE.EXPIRATION,
    OPTION_PRICE.BEST_OFFER,
    OPTION_PRICE.BEST_BID,
    OPTION_PRICE.CALL_PUT,
    OPTION_PRICE.VOLUME,
    OPTION_PRICE.OPEN_INTEREST,
    OPTION_VOLUME.VOLUME AS TOTAL_VOLUME,
    OPTION_VOLUME.OPEN_INTEREST AS TOTAL_OPEN_INTEREST,
    OPTION_PRICE.OPTION_ID,
    DATEDIFF(DAY, OPTION_PRICE.DATE, OPTION_PRICE.EXPIRATION) AS T,
    DATE_PART(week, OPTION_PRICE.DATE)                        AS dw,
    YEAR(OPTION_PRICE.DATE) AS YY
FROM
    SP500_CONST_SECIDS_V1
INNER JOIN
    "OPTION_PRICE"
ON
    SP500_CONST_SECIDS_V1.SECURITY_ID = OPTION_PRICE.SECURITY_ID
AND SP500_CONST_SECIDS_V1.EFFECTIVE_DATE = OPTION_PRICE.DATE
INNER JOIN
    "SECURITY_PRICE"
ON
    SECURITY_PRICE.DATE = OPTION_PRICE.DATE
AND OPTION_PRICE.SECURITY_ID = SECURITY_PRICE.SECURITY_ID
INNER JOIN
    "OPTION_VOLUME"
ON
OPTION_VOLUME.SECURITY_ID = OPTION_PRICE.SECURITY_ID
AND OPTION_VOLUME.DATE
= OPTION_PRICE.DATE
AND OPTION_VOLUME.CALL_PUT
= OPTION_PRICE.CALL_PUT
WHERE T <=31 AND YY = 2019