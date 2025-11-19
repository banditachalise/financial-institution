--1) active loan amount on year
SELECT Status,
    YEAR(IssuedDate) AS Year,
    SUM(CAST(Amount AS DECIMAL(12,2))) AS TotalLoanAmount
FROM Loan
where Status='Active'
GROUP BY YEAR(IssuedDate), Status
ORDER BY Year;

--1.2)loan amount based on year
SELECT 
    YEAR(IssuedDate) AS Year,
    SUM(CAST(Amount AS DECIMAL(12,2))) AS TotalLoanAmount
FROM Loan
GROUP BY YEAR(IssuedDate)
ORDER BY Year;

--1.3) active loan count on years
SELECT 
    YEAR(IssuedDate) AS IssuedYear, Status,
    COUNT(*) AS ActiveLoans
FROM Loan
WHERE Status = 'Active'
GROUP BY YEAR(IssuedDate), Status
ORDER BY IssuedYear;


--2)  new members growth
select count (CustomerID) as NewMembers, Year(JoinedDate) AS JoinedYEAR
from Customer
group by year(JoinedDate)


--3) loans on sector
select LoanType, Year(IssuedDate) as LoanYear,
	count(LoanType) as TotalLoanIssued, 
	Sum(CAST(Amount AS DECIMAL(12,2)))as TotalLoanAmount
from Loan
group by LoanType, Year(IssuedDate)


SELECT  
    SUM(CASE WHEN ClosedDate <= LoanDueDate THEN 1 ELSE 0 END) AS OnTimeRepayments,
    SUM(CASE WHEN ClosedDate > LoanDueDate THEN 1 ELSE 0 END) AS LateRepayments
FROM Loan
WHERE Status = 'Closed';

-- Loan Repayment Rate
SELECT  
    SUM(CASE WHEN ClosedDate IS NOT NULL AND ClosedDate <= LoanDueDate THEN 1 ELSE 0 END) AS OnTimeRepayments,
    SUM(CASE WHEN ClosedDate IS NOT NULL AND ClosedDate > LoanDueDate THEN 1 ELSE 0 END) AS LateRepayments,
    SUM(CASE WHEN Status = 'Active' AND LoanDueDate < GETDATE() THEN 1 ELSE 0 END) AS PastDueActive,
    SUM(CASE WHEN Status = 'Active' AND LoanDueDate >= GETDATE() THEN 1 ELSE 0 END) AS ActiveNotDue
FROM Loan;
