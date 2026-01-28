# B2B-Aforra-

# Store Inventory and Order Management

This is a Django backend project.

This project manages stores, products, inventory, and orders.

Main idea:
- Store has stock
- Store places order
- System checks stock
- Stock reduces after order confirmation

---

## What this project does

- Lists all stores  
- Shows inventory of a store  
- Creates orders for a store  
- Checks stock before confirming order  
- Reduces stock after order is confirmed  

---

## Models

### Store
- name
- location

### Category
- name

### Product
- title
- price
- category

### Inventory
- store
- product
- quantity  
- One store has only one inventory row per product

### Order
- store
- status (PENDING, CONFIRMED, REJECTED)
- created_at

### OrderItem
- order
- product
- quantity_requested

---

## Order Flow

1. Store checks inventory  
2. Store places order  
3. Backend checks stock  
4. If stock is enough  
   - Order is CONFIRMED  
   - Inventory quantity is reduced  
5. If stock is not enough  
   - Order is REJECTED  
   - Inventory is not changed  

---

## APIs

### List Stores
```
GET /stores/
```

### Store Inventory
```
GET /stores/<store_id>/inventory/
```

### Create Order
```
POST /orders/
```

### Store Orders
```
GET /stores/<store_id>/orders/
```

---

## Important

- Order creation uses `transaction.atomic()`
- This ensures:
  - Full order is saved
  - Or nothing is saved
- Prevents wrong inventory updates

---

## Technologies Used

- Python
- Django
- Django REST Framework
- PostgreSQL

---

## Run Project

```
python manage.py migrate
python manage.py runserver
```

---

## Author

Teja Vardhan
