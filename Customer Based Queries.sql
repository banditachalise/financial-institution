--CUSTOMER BASED QUERIES

--1) toal balance of customer id acrross difrrent table
select c.CustomerID, Name, Savings, Loan
from Customer c
left join
(Select CustomerID , sum(CAST(Balance AS DECIMAL(12,2)))  as Savings 
from Saving
group by CustomerID)s 
on s.CustomerID = c.CustomerID
left join 
(Select CustomerID, sum(CAST(Amount AS DECIMAL(12,2))) as Loan 
from Loan 
where Status='Active'
group by CustomerID)l 
on l.CustomerID= c.CustomerID
order by Savings ASC

--2)saving above 12000
select Customer.CustomerID, Name, Balance as SavingAmount, Type
from Saving inner join Customer
on Customer.CustomerID = Saving.CustomerID
where Balance>12000 

--3) monthly transaction for cutomer
select CustomerID, FORMAT(TransactionDate, 'yyyy-MM') as month, sum (Amount) as TotalAmount
from [Transaction]
group by CustomerID, FORMAT(TransactionDate, 'yyyy-MM')
order by month asc

--4) customer with active loans
Select Customer.CustomerID, Name, LoanType, Status
from Loan
join Customer on Customer.CustomerID = Loan. CustomerID
where Status= 'Active'

--5) deposits> withdrawals
select CustomerID, Amount, Sum(case when TransactionType= 'Deposit' then Amount else 0 end) as Deposit,
Sum(case when TransactionType= 'Withdrawal' then Amount else 0 end) as Withdrawal
from [Transaction]
group by CustomerID, Amount
having Sum(case when TransactionType= 'Deposit' then Amount else 0 end) <
Sum(case when TransactionType= 'Withdrawal' then Amount else 0 end) 