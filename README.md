# 🚀 GraphQL CRM

A customer relationship management API built with **Django** and **Graphene**. It manages customers, products and orders through GraphQL queries and mutations, with filtering, bulk inserts and scheduled background jobs. It's part of the **ALX ProDev Backend** programme.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white)
![GraphQL](https://img.shields.io/badge/GraphQL-E10098?style=flat-square&logo=graphql&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=flat-square&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white)

## Features

- **GraphQL API** at `/graphql`, with the GraphiQL explorer
- **Queries**: `allCustomers`, `allProducts` and `allOrders` as Relay connections with filters
  - Customers: `nameIcontains`, `emailIcontains`, `createdAtGte`/`Lte`, `phonePattern`
  - Products: price and stock ranges
  - Orders: `totalAmountGte`/`Lte`, `orderDateGte`/`Lte`, `customerName`, `productName`, `productId`
- **Mutations**: `createCustomer`, `bulkCreateCustomers` (partial success with per-row errors), `createProduct`, `createOrder` (total calculated automatically), `updateLowStockProducts`
- **Scheduled jobs**
  - `django-crontab`: a heartbeat every 5 minutes, and a restock of low-stock products every 12 hours
  - **Celery Beat + Redis**: a weekly CRM report (customers, orders, revenue)
  - Shell and Python scripts in `crm/cron_jobs/` that clean up inactive customers and send order reminders

## Getting started

```bash
git clone https://github.com/Dwaynemaster007/alx-backend-graphql_crm.git
cd alx-backend-graphql_crm
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python seed_db.py            # sample customers and products
python manage.py runserver   # open http://localhost:8000/graphql
```

### Example queries

```graphql
mutation {
  createCustomer(name: "Alice", email: "alice@example.com", phone: "+1234567890") {
    customer { id name }
    message
  }
}

mutation {
  createOrder(customerId: "1", productIds: ["1", "2"]) {
    order { id totalAmount }
  }
}

query {
  allCustomers(nameIcontains: "ali") {
    edges { node { name email } }
  }
}
```

### Background jobs

```bash
python manage.py crontab add                 # install the cron jobs
celery -A crm worker -l info                 # needs Redis on localhost:6379
celery -A crm beat -l info
```

The cron jobs and the Celery report call the API at `http://localhost:8000/graphql` and write logs to `/tmp/`. See [`crm/CELERY.md`](crm/CELERY.md) for more on the Celery setup.

## Project structure

```
alx_backend_graphql_crm/   # settings, root schema, urls
crm/
  models.py                # Customer, Product, Order
  schema.py                # GraphQL types, queries and mutations
  filters.py               # django-filter FilterSets
  cron.py                  # django-crontab jobs
  tasks.py, celery.py      # Celery report task
  cron_jobs/               # standalone cron scripts
seed_db.py                 # sample data
```

## Author

**Thubelihle Dlamini**, [GitHub](https://github.com/Dwaynemaster007) · [LinkedIn](https://linkedin.com/in/thubelihledlamini)
