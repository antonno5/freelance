# Freelance

## Best freelance exchange ever... ever
### *Really the best

Freelance is the lightweight service for searching and ordering remote work. Simple for executors, convenient for customers

## Features
- The ability to choose one of three roles: executor, private customer and corporate customer
- Great opportunities for setting up a profile
- Customers: can post an order. Performers: can accept it. Very easy)
- Editing an order in real time

## Installation (debug mode)
Setup virtual environment and activate it
```shell
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
```

Install dependencies
```shell
pip install --upgrade pip
pip install -r requirements.txt
```

Apply Django migrations
```shell
python3 manage.py migrate
```

Run server
```shell
python3 manage.py runserver
```

Now the service is located at http://127.0.0.1:8000/ <br>
Enjoy)

## Usage
- Just register 2 accounts (one for executor and one for customer)
- You can also add some information about accounts in their profiles
- As the customer create an order
- As the executor accept the order