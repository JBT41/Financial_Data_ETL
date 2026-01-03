# financeManager
The project:

The finance manager project is designed to autmatically pull transactional data from my bank account, and insert into a Database ready to be analysed
there are 3 compenants to the script, refreshing the access token, pulling the transactions, and inserting the transactions into the DB. This will be broken down
into 3 functions that will be called within the main function, it should avoid any hard coding for ease of use.

Python code: https://github.com/JBT41/financeManager/blob/main/blankfinanceManager.py

Goals

1.) Automatically refresh the access token (expires every 24hours)

2.) Automatically pull the previous days transactions from my bank account

3.) Automatically Insert the transactions into a Database

4.) Analyse the data using PowerBI or Grafana.

Technologies

1.) GoCardlessAPI

2.) Python

3.) Linux (ubuntu)

3.) MySql DB (MariaDB)




Now that you have authenticated the goCardLess api with your bank
you should have 2 very important keys
  1) access token
  2) refresh token
We can move onto the next step - creating the MariaDB structure
i have a Database called Bank and a table called Bills
probably not the best naming convention for a large scale application but effective for what i want

![image](https://github.com/user-attachments/assets/ca262f23-9b39-4d3c-86b7-8d4b3b5822f0)

The bills table is setup as below

![image](https://github.com/user-attachments/assets/f1ed1271-57ec-4241-8739-78707ac5b366)



using a simple select statement we can see an example of the data that we are going to be working with
its worth noting here that the "amount" is in a double format which is not effective for currency
this data was inserted before i fixed this blunder.

![image](https://github.com/user-attachments/assets/c102e7f3-6086-4c77-8bf7-80f469ac22c3)

We can start analysing some transactions now
for example we can look at our daily and total expendeture in december#

![image](https://github.com/user-attachments/assets/4d3bfaac-b4f0-4096-bfd6-06e1dabe8435)

![image](https://github.com/user-attachments/assets/6b67a711-7590-4933-b768-96615d7da501)


Here we have the cronjob we setup to automatically run the python script
this is currently ran on an ubuntu VM - but this will be moved to a Raspbery pi 4b
this is so the script can be ran everyday without my laptop being left on - Raspberry pi is much small form factor and significantly less power draw.

![image](https://github.com/user-attachments/assets/1cf17fc6-389c-438d-ac51-9756078fd3be)

You'll notice here that the cronjob is setup to run every second ( * * * * *).
this is because the script in that file location is just a test.

when we move to the PI the cronjob will need updating to (0 5 * * *).

0: Specifies the 0th minute of the hour.

5: Specifies the 5th hour of the day (which is 5 AM).

*: Specifies every day of the month.

*: Specifies every month.

*: Specifies every day of the week.

which will run the script every days at 05 am.


Next steps:

1) Containerize the application using Docker and deploy using Docker Compose on the Raspberry Pi
2) Build a dashboard using powerBI or grafrana to analyse the transactional data
3) Design and develop a script to semi-automate the curl requests required to link your bank to goCardless
4) Can a Java web app be created to automatically adjust my budget as bills are paid using the data inserted into the database?













