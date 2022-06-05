# Why?
This project is my solution to technical task of an interview. More information coming soon.

# Project Description
## Preface
At first I wanted to implement something like producer-consumer layout, but finally decided that it will be
an overengeneering for the task. For now I implemented data generator as a service which incapsulates getting data from
somewhere, leaving us with resulting values in a database. Perhaps I will change it later.
## Current solution
Right now there is not much done about the project. Data generation is pretty straightforward: every second one hundred
values for all tickers are generated and written to the database. Timestamp for each new value is generated on the
db-side, which is, in my opinion, the correct way to do it. Data presenter lacks most core features:
* it cannot update plots in realtime
* it cannot change the ticker through selection
* it gets all the data from the db to make a plot
Everything will be fixed in later commits 
