# Travel Booking System - Database Design Documentation

## 1. System Scenario & Business Requirements

### 1.1 System Overview
The **Travel Booking System** is an online platform that allows customers to search, book, and pay for hotels and flights. The system connects three main stakeholders:
- **Customers** - End users who book travel services
- **Partners** - Hotel and airline companies that offer services
- **Administrators** - System managers who oversee operations

### 1.2 Business Rules & Constraints

#### User Management
- Each user must have a **unique email** and **username**
- Users are classified into three roles: `customer`, `partner`, or `admin`
- A user can have **at most one** user profile (optional extended information)
- A partner user is linked to **exactly one** Partner entity

#### Partner & Service Management
- A Partner can be a **Hotel Partner**, **Flight Partner**, or **Both**
- Each Partner can manage **multiple Hotels** and/or **multiple Flights**
- A Hotel can have **multiple Room Types** (e.g., Standard, Deluxe, Suite)
- Each Room Type belongs to **exactly one Hotel**

#### Booking Rules
- A customer can make **multiple bookings**
- Each booking is either a **hotel booking** OR a **flight booking** (not both)
- A hotel booking requires: room type, check-in/out dates, number of rooms
- A flight booking requires: flight selection, number of passengers, passenger info
- Booking status: `pending` → `confirmed` → `completed` or `cancelled`

#### Payment Rules
- Each booking has **exactly one payment** (1:1 relationship)
- Payment is required to confirm a booking
- Payment methods: Credit Card, Debit Card, Bank Transfer, PayPal, Cash
- A successful payment generates **one receipt**

#### Availability Management
- When a hotel booking is created, `rooms_available` decreases
- When a flight booking is created, `seats_available` decreases
- Cancellation restores availability

---

## 2. ER Model Design

### 2.1 Entities Overview

| Entity | Type | Description |
|--------|------|-------------|
| USER | Strong | System users (customers, partners, admins) |
| USER_PROFILE | Weak | Extended user information |
| PARTNER | Weak | Business partner profile |
| HOTEL | Strong | Hotel properties |
| ROOM_TYPE | Strong | Room categories within hotels |
| FLIGHT | Strong | Available flights |
| BOOKING | Strong | Reservations made by customers |
| HOTEL_BOOKING_DETAIL | Weak | Hotel-specific booking details |
| FLIGHT_BOOKING_DETAIL | Weak | Flight-specific booking details |
| PAYMENT | Weak | Payment transactions |
| PAYMENT_RECEIPT | Weak | Generated receipts |

### 2.2 Entity Attributes

#### USER (Strong Entity)
| Attribute | Key | Description |
|-----------|-----|-------------|
| user_id | PK | Unique identifier |
| username | Unique | Login username |
| email | Unique | User email address |
| password | | Encrypted password |
| phone | | Contact number |
| role | | customer/partner/admin |
| created_at | | Account creation date |

#### USER_PROFILE (Weak Entity)
| Attribute | Key | Description |
|-----------|-----|-------------|
| profile_id | PK | Unique identifier |
| user_id | FK | References USER |
| profile_picture | | Avatar image |
| date_of_birth | | User's DOB |
| address, city, country | | Location info |

#### PARTNER (Weak Entity)
| Attribute | Key | Description |
|-----------|-----|-------------|
| partner_id | PK | Unique identifier |
| user_id | FK | References USER (role='partner') |
| name | | Company name |
| partner_type | | hotel/flight/both |
| is_verified | | Admin verification status |

#### HOTEL (Strong Entity)
| Attribute | Key | Description |
|-----------|-----|-------------|
| hotel_id | PK | Unique identifier |
| partner_id | FK | References PARTNER |
| name | | Hotel name |
| city, address | | Location |
| star_rating | | 1-5 stars |
| amenities | | Facilities offered |
| check_in_time, check_out_time | | Standard times |

#### ROOM_TYPE (Strong Entity)
| Attribute | Key | Description |
|-----------|-----|-------------|
| roomtype_id | PK | Unique identifier |
| hotel_id | FK | References HOTEL |
| name | | Room category name |
| price_per_night | | Nightly rate |
| max_occupancy | | Guest capacity |
| rooms_available | | Current availability |

#### FLIGHT (Strong Entity)
| Attribute | Key | Description |
|-----------|-----|-------------|
| flight_id | PK | Unique identifier |
| partner_id | FK | References PARTNER |
| flight_number | Unique | Flight code |
| origin, destination | | Route |
| departure_time, arrival_time | | Schedule |
| price | | Per-seat price |
| seats_available | | Current availability |

#### BOOKING (Strong Entity)
| Attribute | Key | Description |
|-----------|-----|-------------|
| booking_id | PK, UUID | Unique booking reference |
| user_id | FK | References USER |
| booking_type | | hotel/flight |
| status | | pending/confirmed/cancelled/completed |
| total_amount | | Total price |
| created_at | | Booking timestamp |

#### HOTEL_BOOKING_DETAIL (Weak Entity)
| Attribute | Key | Description |
|-----------|-----|-------------|
| id | PK | Unique identifier |
| booking_id | FK | References BOOKING |
| hotel_id | FK | References HOTEL |
| roomtype_id | FK | References ROOM_TYPE |
| check_in_date, check_out_date | | Stay dates |
| number_of_rooms | | Rooms booked |
| price_per_night | | Rate at booking time |

#### FLIGHT_BOOKING_DETAIL (Weak Entity)
| Attribute | Key | Description |
|-----------|-----|-------------|
| id | PK | Unique identifier |
| booking_id | FK | References BOOKING |
| flight_id | FK | References FLIGHT |
| number_of_passengers | | Passenger count |
| price_per_seat | | Rate at booking time |
| passenger_title, first_name, last_name | | Passenger info |
| passenger_dob, passport | | Travel documents |

#### PAYMENT (Weak Entity)
| Attribute | Key | Description |
|-----------|-----|-------------|
| payment_id | PK, UUID | Unique payment ID |
| booking_id | FK | References BOOKING |
| user_id | FK | References USER |
| amount | | Payment amount |
| payment_method | | Method used |
| status | | pending/completed/failed/refunded |
| transaction_id | Unique | Transaction reference |

#### PAYMENT_RECEIPT (Weak Entity)
| Attribute | Key | Description |
|-----------|-----|-------------|
| receipt_id | PK, UUID | Unique receipt ID |
| payment_id | FK | References PAYMENT |
| generated_at | | Creation timestamp |
| download_count | | Times downloaded |

### 2.3 Relationships

| Relationship | Cardinality | Description |
|--------------|-------------|-------------|
| USER **has** USER_PROFILE | 1:1 (identifying) | Optional profile extension |
| USER **becomes** PARTNER | 1:0..1 | Partner users have partner profile |
| USER **makes** BOOKING | 1:N | Customers can have many bookings |
| PARTNER **owns** HOTEL | 1:N | Partner manages multiple hotels |
| PARTNER **provides** FLIGHT | 1:N | Partner manages multiple flights |
| HOTEL **has** ROOM_TYPE | 1:N | Hotel has multiple room types |
| BOOKING **identifies** HOTEL_BOOKING_DETAIL | 1:1 (identifying) | Hotel booking details |
| BOOKING **identifies** FLIGHT_BOOKING_DETAIL | 1:1 (identifying) | Flight booking details |
| ROOM_TYPE **for** HOTEL_BOOKING_DETAIL | 1:N | Room type can be in many bookings |
| FLIGHT **for** FLIGHT_BOOKING_DETAIL | 1:N | Flight can be in many bookings |
| BOOKING **has** PAYMENT | 1:1 | Each booking has one payment |
| PAYMENT **generates** PAYMENT_RECEIPT | 1:1 | Each payment has one receipt |

---

## 3. ER to Relational Model Transformation

### 3.1 Transformation Rules Applied

| Rule | Application |
|------|-------------|
| **Strong Entity** → Table | USER, HOTEL, ROOM_TYPE, FLIGHT, BOOKING become tables |
| **Weak Entity** → Table with FK | USER_PROFILE, PARTNER, details, PAYMENT, RECEIPT become tables with owner's FK |
| **1:1 Identifying** → FK becomes PK | USER_PROFILE.user_id, HOTEL_BOOKING_DETAIL.booking_id |
| **1:N Relationship** → FK on N-side | HOTEL.partner_id, FLIGHT.partner_id, BOOKING.user_id |
| **1:1 Non-identifying** → FK | PAYMENT.booking_id, RECEIPT.payment_id |

### 3.2 Relational Schema

```
USER = (user_id, email, username, password, phone, role, created_at)

USER_PROFILE = (profile_id, user_id, profile_picture, date_of_birth, address, city, country)
  FK: user_id → USER(user_id)

PARTNER = (partner_id, user_id, name, partner_type, is_verified)
  FK: user_id → USER(user_id)

HOTEL = (hotel_id, partner_id, name, city, address, star_rating, amenities)
  FK: partner_id → PARTNER(partner_id)

ROOM_TYPE = (roomtype_id, hotel_id, name, price_per_night, max_occupancy, rooms_available)
  FK: hotel_id → HOTEL(hotel_id)

FLIGHT = (flight_id, partner_id, flight_number, origin, destination, departure_time, arrival_time, price, seats_available)
  FK: partner_id → PARTNER(partner_id)

BOOKING = (booking_id, user_id, booking_type, status, total_amount, created_at)
  FK: user_id → USER(user_id)

HOTEL_BOOKING_DETAIL = (id, booking_id, hotel_id, roomtype_id, check_in_date, check_out_date, number_of_rooms, price_per_night)
  FK: booking_id → BOOKING(booking_id)
  FK: hotel_id → HOTEL(hotel_id)
  FK: roomtype_id → ROOM_TYPE(roomtype_id)

FLIGHT_BOOKING_DETAIL = (id, booking_id, flight_id, number_of_passengers, price_per_seat, passenger_title, passenger_first_name, passenger_last_name, passenger_dob, passenger_passport)
  FK: booking_id → BOOKING(booking_id)
  FK: flight_id → FLIGHT(flight_id)

PAYMENT = (payment_id, booking_id, user_id, amount, payment_method, status, transaction_id)
  FK: booking_id → BOOKING(booking_id)
  FK: user_id → USER(user_id)

PAYMENT_RECEIPT = (receipt_id, payment_id, generated_at, download_count)
  FK: payment_id → PAYMENT(payment_id)
```

### 3.3 Relationship Transformation Summary

| Relationship | Type | Transformation |
|--------------|------|----------------|
| USER has USER_PROFILE | 1:1 (identifying) | user_id becomes PK/FK in USER_PROFILE |
| USER makes BOOKING | 1:N | user_id added as FK in BOOKING |
| USER manages PAYMENT | 1:N | user_id added as FK in PAYMENT |
| BOOKING has PAYMENT | 1:1 | booking_id added as FK in PAYMENT |
| BOOKING identifies HOTEL_BOOKING_DETAIL | 1:1 (identifying) | booking_id becomes PK/FK |
| BOOKING identifies FLIGHT_BOOKING_DETAIL | 1:1 (identifying) | booking_id becomes PK/FK |
| PARTNER owns HOTEL | 1:N | partner_id added as FK in HOTEL |
| PARTNER provides FLIGHT | 1:N | partner_id added as FK in FLIGHT |
| HOTEL has ROOM_TYPE | 1:N | hotel_id added as FK in ROOM_TYPE |
| ROOM_TYPE for HOTEL_BOOKING_DETAIL | 1:N | roomtype_id added as FK |
| FLIGHT for FLIGHT_BOOKING_DETAIL | 1:N | flight_id added as FK |
| PAYMENT generates PAYMENT_RECEIPT | 1:1 | payment_id added as FK |

---

## 4. Key Design Decisions

### 4.1 Booking Type Polymorphism
Instead of separate Hotel and Flight booking tables, we use:
- One `BOOKING` table with `booking_type` discriminator
- Separate detail tables (`HOTEL_BOOKING_DETAIL`, `FLIGHT_BOOKING_DETAIL`)
- This allows unified booking management while maintaining type-specific data

### 4.2 Price Snapshot
We store `price_per_night` and `price_per_seat` in booking details to:
- Preserve historical pricing at time of booking
- Prevent price changes from affecting existing bookings

### 4.3 Availability Tracking
- `rooms_available` in ROOM_TYPE
- `seats_available` in FLIGHT
- Updated via transactions on booking create/cancel

---

## 5. Legend

- **PK** = Primary Key (underlined in diagrams)
- **FK** = Foreign Key (italicized in diagrams)
- **1:N** = One-to-Many relationship
- **1:1** = One-to-One relationship
