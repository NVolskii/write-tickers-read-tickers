# How to make it work

## SImple way
In order to make it work you need to use docker. Just download the latest docker version, clone the repo, proceed
inside, and execute in the shell:

```bash
docker-compose up
```

When everything is built and running, visit `http://127.0.0.1:5000` where you will see a link to page graps with ticker
data. Or, you can visit it directly through `http://127.0.0.1:5000/tickerboard/`.

## Not that simple way
If you don't want to use docker, you can go use virtual environment together with postgresql db. But first of all,
clone the repo and proceed inside. You have two parts of the project: `post_tickers` and `present_tickers`. I suggest
that you use single virtual environment for both of them, but you can also chose to use separate ones.

Execute in terminal:

```bash
python3 -m venv venv
source venv/bin/activate
```

I used python 3.10. I don't think, that anything can break if you use an older version (but not much older).
Install both requirements:

```bash
pip install -r post_tickers/requirements.txt
pip install -r present_tickers/requirements.txt
```

You can either make two `.env` files in the `post_tickers` and `present_tickers` directories, or export environment
variables. I suggest the first approach.

```bash
touch post_tickers/.env
touch present_tickers/.env
```

open those files in your text editor. You need to add the following parameters to theese files:

__post_tickers/.env__
```
TICK_EP=http://127.0.0.1:5000/ticker/
TICK_VAL_EP=http://127.0.0.1:5000/ticker_value/
TICK_VAL_BATCH_EP=http://127.0.0.1:5000/tickers_values/
```

__present_tickers/.env__
```
FLASK_APP=wsgi.py
FLASK_ENV=development
SQLALCHEMY_DATABASE_URI=<connection string to your postgres db>
```

after that is done you can run the project. Open another terminal window and execute:

```bash
source venv/bin/activate
cd present_tickers
flask run
```

And in one more terminal window execute:
```bash
source venv/bin/activate
cd post_tickers
python vals_generator.py
```

Now, you can open `127.0.0.1:5000` just like in the simple way, and follow the link.

# Dive into history
At first I thought about Flask on backend and any JS framework on frontend. But as far as I have no practice in JS, I
decided to see other options. Reading the description for candidate I learned about Dash. Everything became clear at
that moment: that's the choice.

# Description
I decided to make a common repository for both parts of the task: for data presenter and data producer.

On the presenter's side there are two (actually three, but it's not the point) methods for posting data to the database:
one for tickers initialization and one for batch data loading. There is also one method for loading tickers' values
one-by-one, but I decided to use batch loading instead, it seems to work faster, but I realize, that in general there
can be lots of data sources, so it is important to handle high load. The db that stores data is postgres, but I also
thought about Redis, which can store cached data for a ticker, that is shown at the moment, in order not to query
postgres for values each second, but decided not to over-engineer it. I also thought about using Dash's callback on
new post-requests with data, in order not to query the database each second, but it does not seem to be a working
possibility, so an easier way was preffered: the figure is just being updated each second. That's not an elegant
solution, but seems to work well under proposed conditions.

On the producer's side there is an asynchronous method for posting data, which is implemented to increment all values,
do a post-request and get responce during one-second period. Tickers' initialization, on the other hand, is done
synchronously, because it is an one-time task, that does not need performance.

Each of three parts: database and both services run in personal docker-containers. I decided not to change default
postgres settings, because for this task it does not make much sense. The same about web-server. At first I thought
gunicorn and even nginx, but then decided, that it will just be too much, and embeded flask web-server is enough.
On the other hand I thought at first to set aside SQL-alchemy and use raw queries over psycopg2 instead. But this
approach started to look ugly in the very beginnig, so I decided to use SQL-alchemy. The codebase of the project is
pretty straightforward in order not to lack readability. I hope I managed to achieve it.

Have a nice day!