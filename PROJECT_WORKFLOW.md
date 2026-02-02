# Travel Booking System - Project Workflow Documentation

This document provides a comprehensive overview of your CSX3006 Database System project.

---

## 🏗️ Project Architecture

```mermaid
graph TB
    subgraph "Django Apps"
        A[accounts] --> B[partners]
        A --> C[bookings]
        C --> D[payments]
        B --> C
    end
    
    subgraph "Database Layer"
        E[(PostgreSQL)]
        F[Raw SQL Queries]
        G[Django ORM]
    end
    
    C --> E
    D --> E
    F --> E
    G --> E
```

---

## 📦 App Structure

| App | Purpose |
|-----|---------|
| **accounts** | User authentication, roles (Customer, Partner, Admin), profiles |
| **partners** | Hotel & Flight management by partner companies |
| **bookings** | Booking creation for hotels and flights |
| **payments** | Payment processing, receipts, refunds |
| **utils** | Raw SQL database manager |

---

## 🗄️ Database Schema (ER Diagram Overview)

```mermaid
erDiagram
    USER ||--o| USER_PROFILE : has
    USER ||--o| PARTNER : "becomes (if partner)"
    USER ||--o{ BOOKING : makes
    USER ||--o{ PAYMENT : makes
    
    PARTNER ||--o{ HOTEL : manages
    PARTNER ||--o{ FLIGHT : manages
    
    HOTEL ||--o{ ROOM_TYPE : has
    
    BOOKING ||--o| HOTEL_BOOKING_DETAIL : "has (if hotel)"
    BOOKING ||--o| FLIGHT_BOOKING_DETAIL : "has (if flight)"
    BOOKING ||--|| PAYMENT : "paid via"
    
    HOTEL_BOOKING_DETAIL }o--|| HOTEL : references
    HOTEL_BOOKING_DETAIL }o--|| ROOM_TYPE : references
    
    FLIGHT_BOOKING_DETAIL }o--|| FLIGHT : references
    FLIGHT_BOOKING_DETAIL ||--o{ PASSENGER : contains
    
    PAYMENT ||--o| PAYMENT_RECEIPT : generates
```

---

## 👥 User Roles

| Role | Description | Permissions |
|------|-------------|-------------|
| **Customer** | End users who book hotels/flights | Search, Book, Pay, View bookings |
| **Partner** | Business owners (hotels/airlines) | Manage hotels, flights, view bookings |
| **Admin** | System administrators | Full access via Django Admin |

---

## 🔄 Booking Workflow

### Hotel Booking Flow
```mermaid
sequenceDiagram
    participant C as Customer
    participant S as System
    participant DB as Database
    participant P as Payment
    
    C->>S: Search Hotels
    S->>DB: Query available hotels
    DB-->>S: Return results
    S-->>C: Display hotels
    
    C->>S: Select Room Type
    C->>S: Fill booking details
    S->>DB: Create Booking (pending)
    S->>DB: Reduce room availability
    S-->>C: Redirect to Payment
    
    C->>P: Submit Payment
    P->>DB: Process Payment
    alt Payment Success
        P->>DB: Update status to confirmed
        P-->>C: Show receipt
    else Payment Failed
        P-->>C: Show retry option
    end
```

### Flight Booking Flow
```mermaid
sequenceDiagram
    participant C as Customer
    participant S as System
    participant DB as Database
    
    C->>S: Search Flights
    S->>DB: Query available flights
    DB-->>S: Return results
    
    C->>S: Select Flight
    C->>S: Add Passenger Details
    S->>DB: Create Booking + Passengers
    S->>DB: Reduce seats available
    S-->>C: Redirect to Payment
```

---

## 📊 Key Models Summary

### accounts App
- **User**: Custom user with roles (customer/partner/admin)
- **UserProfile**: Extended user info (bio, address, etc.)

### partners App
- **Partner**: Business entity linked to partner user
- **Hotel**: Hotel properties with star rating, amenities
- **RoomType**: Room categories with pricing
- **Flight**: Flight schedules with pricing

### bookings App
- **Booking**: Main booking record (hotel or flight)
- **HotelBookingDetail**: Check-in/out dates, rooms, guests
- **FlightBookingDetail**: Passengers, price per seat
- **Passenger**: Individual passenger info for flights

### payments App
- **Payment**: Payment records with multiple methods
- **PaymentReceipt**: Generated receipts

---

## 🔧 Raw SQL Layer

Located in `utils/db_manager.py`:

| Class | Purpose |
|-------|---------|
| `DatabaseManager` | Execute raw SQL queries |
| `BookingQueries` | User bookings, hotel details, availability |
| `HotelQueries` | Hotel search, statistics |
| `ReportQueries` | Revenue reports, analytics |

### Example Raw SQL Query
```sql
SELECT b.booking_id, b.status, b.total_amount, u.username
FROM bookings_booking b
INNER JOIN accounts_user u ON b.user_id = u.id
WHERE u.id = %s
ORDER BY b.created_at DESC;
```

---

## 🌐 URL Structure

| URL Pattern | View | Purpose |
|-------------|------|---------|
| `/` | home | Landing page |
| `/accounts/login/` | login | User login |
| `/accounts/register/` | register | User registration |
| `/accounts/dashboard/` | dashboard | User dashboard |
| `/bookings/hotels/` | hotel_search | Search hotels |
| `/bookings/hotels/<id>/` | hotel_detail | Hotel details |
| `/bookings/flights/` | flight_search | Search flights |
| `/bookings/my-bookings/` | my_bookings | User's bookings |
| `/payments/<booking_id>/` | payment_page | Process payment |
| `/admin/` | Django Admin | Admin interface |

---

## 🚀 How to Run

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Start PostgreSQL (make sure it's running)

# 3. Run migrations
python manage.py migrate

# 4. Create superuser (if needed)
python manage.py createsuperuser

# 5. Start server
python manage.py runserver
```

---

## 📝 For Your Presentation

### Key Points to Highlight:
1. **Three-tier architecture**: Presentation (Templates) → Business Logic (Views) → Data (Models/PostgreSQL)
2. **Both ORM and Raw SQL**: Demonstrates understanding of both approaches
3. **Role-based access**: Customer, Partner, Admin with different permissions
4. **Relational database design**: Proper use of foreign keys, one-to-one, many-to-many relationships
5. **Transaction management**: Atomic operations for bookings

### Database Features Used:
- ✅ PostgreSQL database
- ✅ Foreign Key relationships
- ✅ Indexes for performance
- ✅ UUID for unique identifiers
- ✅ Raw SQL queries in `db_manager.py`
- ✅ Aggregate functions (SUM, COUNT, AVG)
- ✅ JOINs (INNER, LEFT)
- ✅ Subqueries
