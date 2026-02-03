# Travel Booking System - ER Entities

## 1. USER (Strong Entity)
```
USER
├── id (PK)
├── username
├── email
├── password
├── phone
├── role
├── created_at
└── updated_at
```

## 2. USER_PROFILE (Weak Entity)
```
USER_PROFILE
├── id (PK)
├── user_id (FK) → USER
├── profile_picture
├── date_of_birth
├── address
├── city
└── country
```

## 3. PARTNER (Weak Entity)
```
PARTNER
├── id (PK)
├── user_id (FK) → USER
├── name
├── partner_type
├── description
├── logo
├── website
├── contact_email
├── contact_phone
├── is_verified
├── created_at
└── updated_at
```

## 4. HOTEL (Strong Entity)
```
HOTEL
├── id (PK)
├── partner_id (FK) → PARTNER
├── name
├── city
├── address
├── description
├── star_rating
├── main_image
├── amenities
├── check_in_time
├── check_out_time
├── email
├── phone
├── is_active
├── created_at
└── updated_at
```

## 5. ROOM_TYPE (Strong Entity)
```
ROOM_TYPE
├── id (PK)
├── hotel_id (FK) → HOTEL
├── name
├── description
├── price_per_night
├── max_occupancy
├── rooms_available
├── room_size
├── bed_type
├── amenities
├── image
├── is_active
├── created_at
└── updated_at
```

## 6. FLIGHT (Strong Entity)
```
FLIGHT
├── id (PK)
├── partner_id (FK) → PARTNER
├── flight_number
├── origin
├── destination
├── departure_time
├── arrival_time
├── price
├── seats_available
├── total_seats
├── aircraft_type
├── airline_logo
├── class_type
├── is_active
├── created_at
└── updated_at
```

## 7. BOOKING (Strong Entity)
```
BOOKING
├── id (PK)
├── booking_id (UUID)
├── user_id (FK) → USER
├── booking_type
├── status
├── total_amount
├── notes
├── created_at
└── updated_at
```

## 8. HOTEL_BOOKING_DETAIL (Weak Entity)
```
HOTEL_BOOKING_DETAIL
├── id (PK)
├── booking_id (FK) → BOOKING
├── hotel_id (FK) → HOTEL
├── room_type_id (FK) → ROOM_TYPE
├── check_in_date
├── check_out_date
├── number_of_rooms
├── number_of_guests
├── price_per_night
└── number_of_nights
```

## 9. FLIGHT_BOOKING_DETAIL (Weak Entity)
```
FLIGHT_BOOKING_DETAIL
├── id (PK)
├── booking_id (FK) → BOOKING
├── flight_id (FK) → FLIGHT
├── number_of_passengers
├── price_per_seat
├── passenger_title
├── passenger_first_name
├── passenger_last_name
├── passenger_dob
└── passenger_passport
```

## 10. PAYMENT (Weak Entity)
```
PAYMENT
├── id (PK)
├── payment_id (UUID)
├── booking_id (FK) → BOOKING
├── user_id (FK) → USER
├── amount
├── payment_method
├── status
├── transaction_id
├── card_type
├── card_last_four
├── card_holder_name
├── bank_name
├── account_number
├── paypal_email
├── payment_date
├── notes
├── failure_reason
├── created_at
└── updated_at
```

## 11. PAYMENT_RECEIPT (Weak Entity)
```
PAYMENT_RECEIPT
├── id (PK)
├── receipt_id (UUID)
├── payment_id (FK) → PAYMENT
├── generated_at
└── downloaded_count
```

---

## Relationships

```
USER ──1:1── USER_PROFILE
USER ──1:0..1── PARTNER
USER ──1:N── BOOKING
PARTNER ──1:N── HOTEL
PARTNER ──1:N── FLIGHT
HOTEL ──1:N── ROOM_TYPE
BOOKING ──1:0..1── HOTEL_BOOKING_DETAIL
BOOKING ──1:0..1── FLIGHT_BOOKING_DETAIL
HOTEL_BOOKING_DETAIL ──N:1── ROOM_TYPE
FLIGHT_BOOKING_DETAIL ──N:1── FLIGHT
BOOKING ──1:1── PAYMENT
PAYMENT ──1:1── PAYMENT_RECEIPT
```
