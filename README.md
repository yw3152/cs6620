#Flask Transactions API

This is a simple Flask-based web service API for inputting transactions and generating reports.

#Instructions

##Environment Setup
- Python3
- pip


#Solution Approach:
API Design:
- Two endpoints: POST /transactions for data input and GET /report for reporting.
- Data is parsed using Pandas, and transactions are appened to a global DataFrame.

##Assumptions:
Input CSV data is well-formed and matches the expected schema (Date, Type, Amount($), Memo).

#Shortcomings:
1. In-Memory Storage:
	- All data is stored in memory, and it resets when the server restarts
	- Not scalable for large datasets or production use
2. Error Handling:
	- No validation of CSV data, such as format errors or invalid types
3. 