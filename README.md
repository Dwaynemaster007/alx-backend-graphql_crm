# 🚀 GraphQL CRM - Modern API-First Customer Management

A powerful, production-ready GraphQL API for customer relationship management built with Django and graphene-django. Features advanced mutations, complex filtering, bulk operations, and nested queries for modern business applications.

[![Django](https://img.shields.io/badge/Django-4.0+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![GraphQL](https://img.shields.io/badge/GraphQL-E10098?style=for-the-badge&logo=graphql&logoColor=white)](https://graphql.org/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Graphene](https://img.shields.io/badge/Graphene--Django-3.0+-FF6384?style=for-the-badge)](https://docs.graphene-python.org/projects/django/)

<div align="center">

### 🎯 Single Endpoint. Infinite Possibilities. 🎯

*Where GraphQL meets Django for the ultimate CRM experience*

[Features](#-key-features) • [Quick Start](#-quick-start) • [API Docs](#-api-documentation) • [Examples](#-graphql-examples)

</div>

---

## 📋 Project Overview

This project demonstrates **modern GraphQL API development** using Django, implementing a complete CRM (Customer Relationship Management) system. Built as part of the **ALX ProDev Backend** curriculum, it showcases advanced GraphQL patterns including mutations, nested queries, bulk operations, and sophisticated filtering.

### 🎯 Why GraphQL Over REST?

Unlike REST APIs with multiple endpoints, GraphQL provides:
- ✅ **Single Endpoint** - All operations through `/graphql`
- ✅ **Flexible Queries** - Request exactly what you need
- ✅ **Nested Data** - Fetch related data in one request
- ✅ **Strong Typing** - Schema-driven development
- ✅ **Real-time Updates** - Built-in subscription support
- ✅ **Self-Documenting** - Automatic API documentation

---

## 🌟 Key Features

### 📊 Customer Management
- Create individual customers with validation
- Bulk customer creation with partial success support
- Email uniqueness validation
- Phone number format validation
- Customer search and filtering

### 🛍️ Product Catalog
- Product creation with price and stock management
- Positive price validation
- Stock level tracking
- Advanced product filtering
- Low stock alerts

### 📦 Order Processing
- Create orders with multiple products
- Automatic total calculation
- Nested customer and product data
- Order history tracking
- Complex order filtering

### 🔍 Advanced Filtering
- Case-insensitive search
- Date range filtering
- Price range queries
- Related field lookups
- Custom filter patterns
- Sorting and ordering

### ⚡ Performance Features
- Optimized database queries
- N+1 query prevention
- Efficient bulk operations
- Connection-based pagination
- Query complexity limiting

---

## 📁 Project Structure

```
alx-backend-graphql_crm/
├── crm/                          # Main CRM application
│   ├── models.py                 # Django models (Customer, Product, Order)
│   ├── schema.py                 # GraphQL schema and mutations
│   ├── filters.py                # django-filter configurations
│   ├── admin.py                  # Django admin interface
│   └── tests.py                  # Unit tests for API
├── alx_backend_graphql_crm/      # Project settings
│   ├── settings.py               # Django configuration
│   ├── urls.py                   # URL routing (GraphQL endpoint)
│   └── schema.py                 # Main GraphQL schema
├── seed_db.py                    # Database seeding script
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+**
- **Django 4.0+**
- **PostgreSQL** or **SQLite** (default)
- **pip** package manager

### Installation

```bash
# 1️⃣ Clone the repository
git clone https://github.com/Dwaynemaster007/alx-backend-graphql_crm.git
cd alx-backend-graphql_crm

# 2️⃣ Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Run migrations
python manage.py makemigrations
python manage.py migrate

# 5️⃣ (Optional) Seed the database
python seed_db.py

# 6️⃣ Create superuser (optional)
python manage.py createsuperuser

# 7️⃣ Start development server
python manage.py runserver
```

### Access GraphQL Interface

Open your browser and navigate to:
```
http://localhost:8000/graphql
```

You'll see the **GraphiQL** interactive interface! 🎉

---

## 📚 Data Models

### Customer Model

```python
class Customer(models.Model):
    name = CharField(max_length=255)
    email = EmailField(unique=True)
    phone = CharField(max_length=20, blank=True)
    created_at = DateTimeField(auto_now_add=True)
```

### Product Model

```python
class Product(models.Model):
    name = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    stock = PositiveIntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)
```

### Order Model

```python
class Order(models.Model):
    customer = ForeignKey(Customer, on_delete=CASCADE)
    products = ManyToManyField(Product)
    total_amount = DecimalField(max_digits=10, decimal_places=2)
    order_date = DateTimeField(auto_now_add=True)
```

---

## 🎯 GraphQL Schema Overview

### Types

```graphql
type Customer {
  id: ID!
  name: String!
  email: String!
  phone: String
  createdAt: DateTime!
  orders: [Order]
}

type Product {
  id: ID!
  name: String!
  price: Decimal!
  stock: Int!
  createdAt: DateTime!
}

type Order {
  id: ID!
  customer: Customer!
  products: [Product]!
  totalAmount: Decimal!
  orderDate: DateTime!
}
```

### Queries

```graphql
type Query {
  hello: String
  allCustomers(filter: CustomerFilterInput): [Customer]
  allProducts(filter: ProductFilterInput): [Product]
  allOrders(filter: OrderFilterInput): [Order]
  customer(id: ID!): Customer
  product(id: ID!): Product
  order(id: ID!): Order
}
```

### Mutations

```graphql
type Mutation {
  createCustomer(input: CustomerInput!): CreateCustomerPayload
  bulkCreateCustomers(input: [CustomerInput]!): BulkCreateCustomersPayload
  createProduct(input: ProductInput!): CreateProductPayload
  createOrder(input: OrderInput!): CreateOrderPayload
}
```

---

## 💻 API Documentation

### Task 0: Basic Setup & Hello Query

**Objective:** Set up GraphQL endpoint with a simple query.

**Query:**
```graphql
{
  hello
}
```

**Response:**
```json
{
  "data": {
    "hello": "Hello, GraphQL!"
  }
}
```

---

### Task 1 & 2: Mutations Implementation

#### Create Single Customer

**Mutation:**
```graphql
mutation {
  createCustomer(input: {
    name: "Alice Johnson"
    email: "alice@example.com"
    phone: "+1234567890"
  }) {
    customer {
      id
      name
      email
      phone
      createdAt
    }
    message
  }
}
```

**Response:**
```json
{
  "data": {
    "createCustomer": {
      "customer": {
        "id": "1",
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "phone": "+1234567890",
        "createdAt": "2025-10-17T10:30:00"
      },
      "message": "Customer created successfully!"
    }
  }
}
```

**Validation Features:**
- ✅ Email uniqueness check
- ✅ Phone format validation (`+1234567890` or `123-456-7890`)
- ✅ Required field validation
- ✅ User-friendly error messages

---

#### Bulk Create Customers

**Mutation:**
```graphql
mutation {
  bulkCreateCustomers(input: [
    { name: "Bob Smith", email: "bob@example.com", phone: "123-456-7890" }
    { name: "Carol White", email: "carol@example.com" }
    { name: "Dave Brown", email: "bob@example.com" }  # Duplicate email
  ]) {
    customers {
      id
      name
      email
      phone
    }
    errors
  }
}
```

**Response:**
```json
{
  "data": {
    "bulkCreateCustomers": {
      "customers": [
        {
          "id": "2",
          "name": "Bob Smith",
          "email": "bob@example.com",
          "phone": "123-456-7890"
        },
        {
          "id": "3",
          "name": "Carol White",
          "email": "carol@example.com",
          "phone": null
        }
      ],
      "errors": [
        "Record 3: Email already exists"
      ]
    }
  }
}
```

**Features:**
- ✅ **Partial Success** - Valid records are created even if some fail
- ✅ **Transaction Safety** - All-or-nothing for each customer
- ✅ **Detailed Errors** - Specific error messages for failed records

---

#### Create Product

**Mutation:**
```graphql
mutation {
  createProduct(input: {
    name: "MacBook Pro"
    price: 2499.99
    stock: 15
  }) {
    product {
      id
      name
      price
      stock
      createdAt
    }
  }
}
```

**Response:**
```json
{
  "data": {
    "createProduct": {
      "product": {
        "id": "1",
        "name": "MacBook Pro",
        "price": "2499.99",
        "stock": 15,
        "createdAt": "2025-10-17T10:35:00"
      }
    }
  }
}
```

**Validation:**
- ✅ Price must be positive
- ✅ Stock must be non-negative
- ✅ Name is required

---

#### Create Order with Products

**Mutation:**
```graphql
mutation {
  createOrder(input: {
    customerId: "1"
    productIds: ["1", "2", "3"]
  }) {
    order {
      id
      customer {
        name
        email
      }
      products {
        name
        price
      }
      totalAmount
      orderDate
    }
  }
}
```

**Response:**
```json
{
  "data": {
    "createOrder": {
      "order": {
        "id": "1",
        "customer": {
          "name": "Alice Johnson",
          "email": "alice@example.com"
        },
        "products": [
          { "name": "MacBook Pro", "price": "2499.99" },
          { "name": "Magic Mouse", "price": "99.99" },
          { "name": "USB-C Cable", "price": "19.99" }
        ],
        "totalAmount": "2619.97",
        "orderDate": "2025-10-17T10:40:00"
      }
    }
  }
}
```

**Features:**
- ✅ Automatic total calculation
- ✅ Multiple product association
- ✅ Nested customer and product data
- ✅ Validation of customer and product IDs

---

### Task 3: Advanced Filtering

#### Filter Customers

**Query:**
```graphql
query {
  allCustomers(filter: {
    nameIcontains: "Ali"
    createdAtGte: "2025-01-01"
  }) {
    edges {
      node {
        id
        name
        email
        createdAt
      }
    }
  }
}
```

**Filter Options:**
- `nameIcontains` - Case-insensitive name search
- `emailIcontains` - Case-insensitive email search
- `createdAtGte` - Created after date
- `createdAtLte` - Created before date
- `phonePattern` - Phone number pattern match

---

#### Filter Products

**Query:**
```graphql
query {
  allProducts(filter: {
    priceGte: 100
    priceLte: 3000
    stockGte: 5
  }, orderBy: "-price") {
    edges {
      node {
        id
        name
        price
        stock
      }
    }
  }
}
```

**Filter Options:**
- `nameIcontains` - Product name search
- `priceGte` / `priceLte` - Price range
- `stockGte` / `stockLte` - Stock range
- `orderBy` - Sort by field (prefix `-` for descending)

---

#### Filter Orders

**Query:**
```graphql
query {
  allOrders(filter: {
    customerName: "Alice"
    productName: "MacBook"
    totalAmountGte: 1000
    orderDateGte: "2025-01-01"
  }) {
    edges {
      node {
        id
        customer {
          name
        }
        products {
          name
          price
        }
        totalAmount
        orderDate
      }
    }
  }
}
```

**Filter Options:**
- `customerName` - Filter by customer name
- `productName` - Filter by product name
- `totalAmountGte` / `totalAmountLte` - Amount range
- `orderDateGte` / `orderDateLte` - Date range

---

## 🎨 Best Practices Implemented

### Schema Design
✅ Clean, modular schema structure  
✅ Reusable types and input objects  
✅ Clear naming conventions  
✅ Proper type definitions

### Security
✅ Authentication in resolvers  
✅ Authorization checks  
✅ Input validation  
✅ SQL injection prevention  
✅ Rate limiting ready

### Error Handling
✅ Custom error messages  
✅ Graceful exception handling  
✅ Field-level errors  
✅ User-friendly responses

### Performance
✅ N+1 query prevention  
✅ Database query optimization  
✅ Connection-based pagination  
✅ Efficient bulk operations  
✅ Query complexity limiting

### Testing
✅ Unit tests for mutations  
✅ Query validation tests  
✅ Filter testing  
✅ Edge case coverage

---

## 🛠️ Development Tools

### GraphiQL Interface

Access the interactive GraphiQL interface at `http://localhost:8000/graphql`:
- 📝 Write queries with auto-completion
- 📖 Browse schema documentation
- 🧪 Test mutations in real-time
- 💾 Save query history

### Django Admin

Manage data through Django admin:
```bash
python manage.py createsuperuser
# Visit: http://localhost:8000/admin
```

### Database Seeding

Populate with sample data:
```bash
python seed_db.py
```

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
python manage.py test

# Run specific test module
python manage.py test crm.tests

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Manual Testing with GraphiQL

1. Start the server: `python manage.py runserver`
2. Open `http://localhost:8000/graphql`
3. Try the example queries above
4. Verify responses match expected format

---

## 📊 Real-World Use Cases

This architecture is perfect for:

### 🏢 Business Applications
- CRM systems
- ERP solutions
- Inventory management
- Order processing

### 🛒 E-commerce Platforms
- Product catalogs
- Shopping carts
- Order management
- Customer profiles

### 📱 Mobile Applications
- Flexible data fetching
- Reduced bandwidth usage
- Offline-first capabilities
- Real-time updates

### 📈 Analytics Dashboards
- Custom data views
- Real-time metrics
- Filtered reports
- Nested data relationships

---

## 🚀 Advanced Features

### Pagination

```graphql
query {
  allCustomers(first: 10, after: "cursor123") {
    edges {
      cursor
      node {
        id
        name
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Nested Queries

```graphql
query {
  customer(id: "1") {
    name
    orders {
      totalAmount
      products {
        name
        price
      }
    }
  }
}
```

### Fragments

```graphql
fragment CustomerFields on Customer {
  id
  name
  email
  phone
}

query {
  customer(id: "1") {
    ...CustomerFields
    orders {
      id
    }
  }
}
```

---

## 🔮 Future Enhancements

Potential features to add:

- 🔐 **JWT Authentication** - Secure API access
- 🔄 **GraphQL Subscriptions** - Real-time updates
- 📊 **Analytics Queries** - Sales reports and metrics
- 🔍 **Full-Text Search** - Advanced search capabilities
- 📧 **Email Notifications** - Order confirmations
- 💳 **Payment Integration** - Stripe/PayPal
- 📱 **Mobile App Integration** - React Native client
- 🌍 **Multi-language Support** - i18n
- 🔒 **Role-Based Access** - Granular permissions
- 📈 **Performance Monitoring** - Query analytics

---

## 📚 Learning Resources

### GraphQL
- [GraphQL Official Docs](https://graphql.org/learn/)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- [How to GraphQL](https://www.howtographql.com/)

### Graphene-Django
- [Graphene-Django Docs](https://docs.graphene-python.org/projects/django/)
- [Graphene Tutorial](https://docs.graphene-python.org/en/latest/quickstart/)

### Django
- [Django Documentation](https://docs.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)

### Tools
- [GraphiQL](https://github.com/graphql/graphiql)
- [Insomnia](https://insomnia.rest/)
- [Apollo Client](https://www.apollographql.com/docs/react/)

---

## 🐛 Troubleshooting

### GraphQL Endpoint Not Working

```bash
# Ensure graphene-django is installed
pip install graphene-django

# Check INSTALLED_APPS in settings.py
# Should include: 'graphene_django'

# Verify URL configuration
# Should have: path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=True)))
```

### Migrations Issues

```bash
# Reset migrations (development only!)
python manage.py migrate crm zero
python manage.py showmigrations

# Create fresh migrations
python manage.py makemigrations
python manage.py migrate
```

### Query Errors

```bash
# Check logs
python manage.py runserver

# Verify schema
python manage.py graphql_schema

# Test in GraphiQL interface
```

---

## 📄 License

This project is part of the **ALX ProDev Backend Curriculum**.

© 2025 ALX Africa. All rights reserved.

---

## 👨‍💻 Author

**Thubelihle Dlamini (Dwaynemaster007)**

---

<div align="center">

### 💜 Built with GraphQL Excellence by [Dwaynemaster007](https://github.com/Dwaynemaster007) 💜

*Modern APIs for Modern Applications* 🚀✨

[![GitHub](https://img.shields.io/badge/GitHub-Dwaynemaster007-181717?style=for-the-badge&logo=github)](https://github.com/Dwaynemaster007)
[![GraphQL](https://img.shields.io/badge/GraphQL-Expert-E10098?style=for-the-badge&logo=graphql&logoColor=white)](https://graphql.org/)
[![Django](https://img.shields.io/badge/Django-Master-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)

---

**Tags:** `graphql` · `django` · `graphene-django` · `crm` · `api` · `mutations` · `filtering` · `bulk-operations` · `nested-queries` · `backend` · `alx-prodev` · `python` · `rest-alternative` · `modern-api`

</div>