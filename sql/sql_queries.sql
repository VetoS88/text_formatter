/*
Запросы, которые отобразят  всю  информацию по каждому платежу включая
дополнительное поле pmRest - сумму нераспределенного на оплаты остатка по этому платежу.  
*/

-- Универсальный, подходит для обоих разработанных струтур данных.
SELECT pmId, pmNumber, pmDate, pmSum, (pmSum-sum(COALESCE(trfSum, 0))) as pmRest
FROM payments LEFT JOIN transfers  ON pmNumber=trfPayment GROUP BY pmNumber ORDER BY pmid;




-- Запрос для базы данных со структурой описанной в файле
-- db_structure_additional_pmRest_trAccrual.sql
SELECT * FROM payments;



/*
Анализ выполнения для db_structure_additional_pmRest_trAccrual.sql
EXPLAIN(ANALYZE) SELECT pmId, pmNumber, pmDate, pmSum, (pmSum-sum(COALESCE(trfSum, 0))) as pmRest
FROM payments LEFT JOIN transfers  ON pmNumber=trfPayment GROUP BY pmNumber;

 HashAggregate  (cost=13.54..13.67 rows=9 width=33) (actual time=0.190..0.204 rows=9 loops=1)
   Group Key: payments.pmnumber
   ->  Hash Right Join  (cost=1.20..13.49 rows=9 width=33) (actual time=0.073..0.121 rows=13 loops=1)
         Hash Cond: ((transfers.trfpayment)::text = (payments.pmnumber)::text)
         ->  Seq Scan on transfers  (cost=0.00..11.60 rows=160 width=160) (actual time=0.005..0.018 rows=10 loops=1)
         ->  Hash  (cost=1.09..1.09 rows=9 width=19) (actual time=0.050..0.050 rows=9 loops=1)
               Buckets: 1024  Batches: 1  Memory Usage: 9kB
               ->  Seq Scan on payments  (cost=0.00..1.09 rows=9 width=19) (actual time=0.015..0.028 rows=9 loops=1)
 Planning time: 0.226 ms
 Execution time: 0.295 ms


Результат запроса.
SELECT pmId, pmNumber, pmDate, pmSum, (pmSum-sum(COALESCE(trfSum, 0))) as pmRest
FROM payments LEFT JOIN transfers  ON pmNumber=trfPayment GROUP BY pmNumber ORDER BY pmnumber;
 pmid | pmnumber |           pmdate           | pmsum  | pmrest
------+----------+----------------------------+--------+--------
    3 | 100      | 2017-04-25 13:26:20.739363 | 918.00 | 318.00
    4 | 25       | 2017-04-25 13:26:20.739363 | 588.00 |  88.00
    6 | 45       | 2017-04-25 13:26:20.739363 | 652.00 | 152.00
    7 | 55       | 2017-04-25 13:26:20.739363 | 949.00 | 949.00
    2 | 59       | 2017-04-25 13:26:20.739363 | 574.00 | 474.00
    1 | 7        | 2017-04-25 13:26:20.739363 | 968.00 | 968.00
    9 | 72       | 2017-04-25 13:26:20.739363 | 744.00 | 344.00
    8 | 8        | 2017-04-25 13:26:20.739363 | 965.00 | 415.00
    5 | 86       | 2017-04-25 13:26:20.739363 | 806.00 | 806.00
(9 rows)

*/


/*
Анализ выполнения для db_structure_additional_pmRest_trAccrual.sql
EXPLAIN(ANALYZE) SELECT * FROM payments;
 Seq Scan on payments  (cost=0.00..1.09 rows=9 width=24) (actual time=0.015..0.026 rows=9 loops=1)
 Planning time: 0.071 ms
 Execution time: 0.074 ms

Результат запроса.
SELECT * FROM payments ORDER BY pmnumber;
 pmid | pmnumber |           pmdate           | pmsum  | pmrest
------+----------+----------------------------+--------+--------
    3 | 100      | 2017-04-25 13:26:20.739363 | 918.00 | 318.00
    4 | 25       | 2017-04-25 13:26:20.739363 | 588.00 |  88.00
    6 | 45       | 2017-04-25 13:26:20.739363 | 652.00 | 152.00
    7 | 55       | 2017-04-25 13:26:20.739363 | 949.00 | 949.00
    2 | 59       | 2017-04-25 13:26:20.739363 | 574.00 | 474.00
    1 | 7        | 2017-04-25 13:26:20.739363 | 968.00 | 968.00
    9 | 72       | 2017-04-25 13:26:20.739363 | 744.00 | 344.00
    8 | 8        | 2017-04-25 13:26:20.739363 | 965.00 | 415.00
    5 | 86       | 2017-04-25 13:26:20.739363 | 806.00 | 806.00

*/