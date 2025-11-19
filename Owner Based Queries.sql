-- OWNER BASED QUERIES
  --****
 Select sum(cast(Balance as decimal(12,2))) as ToalSavings
from Saving 
Select  sum(cast(Amount as decimal(12,2))) as TotalLoan
from Loan where Status = 'Active'

--1) Total Balance per customer
Select  Saving.CustomerID, sum(cast(Balance as decimal(12,2))) as Balance, sum(cast(Amount as decimal(12,2))) as Loan
from Saving inner join Loan on Saving. CustomerID= Loan. CustomerID
group by Saving. CustomerID
order by Balance desc

--2) Tranaction acc to month
select CustomerId, Format(TransactionDate, 'MMMM-yyyy') as month,
sum(case when Transactiontype='Deposit' then Amount Else 0 End) as Deposits,
sum(case when Transactiontype='Withdrawal' then Amount Else 0 End) as Withdrawal
from [Transaction]
Group by CustomerID,Format(TransactionDate, 'MMMM-yyyy'), YEAR(TransactionDate),
    MONTH(TransactionDate)
ORDER BY 
    YEAR(TransactionDate) ASC,
    MONTH(TransactionDate) ASC;

--3) Customers Above Average Balance
select CustomerID, averagetable.AverageBalance, SUM(CAST(Balance AS DECIMAL(12,2))) AS TotalBalance
FROM Saving cross join 
 (SELECT Avg (TotalPerCustomer) as AverageBalance
  FROM
	(SELECT SUM(CAST(Balance AS DECIMAL(12,2))) AS TotalPerCustomer
     FROM Saving
	GROUP BY CustomerID) as sub
)as averagetable
GROUP BY CustomerID, averagetable.AverageBalance
HAVING SUM(CAST(Balance AS DECIMAL(12,2))) > averagetable.AverageBalance

