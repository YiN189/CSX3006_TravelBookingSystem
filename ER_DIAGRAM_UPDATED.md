# Updated ER Diagram (Without Separate Passenger Entity)

## Changes Made
- Removed **PASSENGER** entity
- Added passenger fields directly to **FLIGHT_BOOKING_DETAIL**

---

## ER Diagram (Text Version)

```
┌─────────────────┐          ┌─────────────────┐
│      USER       │          │   USER_PROFILE  │
├─────────────────┤    1:1   ├─────────────────┤
│ (user_id) PK    │──────────│ (profile_id) PK │
│ username        │   has    │ user_id (FK)    │
│ email           │          │ profile_picture │
│ phone           │          │ date_of_birth   │
│ role            │          │ address         │
│ created_at      │          │ city, country   │
└────────┬────────┘          └─────────────────┘
         │
    becomes (1:0..1)
         │
         ▼
┌─────────────────┐
│     PARTNER     │
├─────────────────┤
│ (partner_id) PK │
│ user_id (FK)    │
│ name            │
│ partner_type    │
│ contact_email   │
│ is_verified     │
└────────┬────────┘
         │
    manages (1:N)
         │
    ┌────┴────┐
    ▼         ▼
┌─────────┐  ┌─────────┐
│  HOTEL  │  │ FLIGHT  │
├─────────┤  ├─────────┤
│(hotel_id)│  │(flight_id)│
│partner_id│  │partner_id│
│  name   │  │flight_number│
│  city   │  │  origin  │
│star_rating│ │destination│
│ is_active│  │  price   │
└────┬────┘  │seats_avail│
     │       └─────┬─────┘
  has (1:N)        │
     │             │
     ▼             │
┌─────────────┐    │
│  ROOM_TYPE  │    │
├─────────────┤    │
│(roomtype_id)│    │
│ hotel_id(FK)│    │
│    name     │    │
│price_per_night│  │
│max_occupancy│    │
│rooms_available│  │
└─────────────┘    │
                   │
                   ▼
┌────────────────────────────────────────────────────────────────────┐
│                              BOOKING                               │
├────────────────────────────────────────────────────────────────────┤
│ (booking_id) PK | user_id (FK) | booking_type | status | total_amt│
└───────────┬─────────────────────────────────────────────┬──────────┘
            │                                             │
     has (1:0..1)                                  has (1:0..1)
            │                                             │
            ▼                                             ▼
┌───────────────────────┐         ┌──────────────────────────────────┐
│ HOTEL_BOOKING_DETAIL  │         │     FLIGHT_BOOKING_DETAIL        │
├───────────────────────┤         ├──────────────────────────────────┤
│ (id) PK               │         │ (id) PK                          │
│ booking_id (FK)       │         │ booking_id (FK)                  │
│ hotel_id (FK)         │         │ flight_id (FK)                   │
│ room_type_id (FK)     │         │ number_of_passengers             │
│ check_in_date         │         │ price_per_seat                   │
│ check_out_date        │         │ ─────────────────────────────    │
│ number_of_rooms       │         │ PASSENGER INFO:                  │
│ number_of_guests      │         │ passenger_title                  │
│ price_per_night       │         │ passenger_first_name             │
│ number_of_nights      │         │ passenger_last_name              │
└───────────────────────┘         │ passenger_dob                    │
                                  │ passenger_passport               │
                                  └──────────────────────────────────┘

BOOKING ──(paid_via 1:1)──► PAYMENT ──(generates 1:1)──► PAYMENT_RECEIPT

┌─────────────────┐          ┌─────────────────┐
│     PAYMENT     │   1:1    │ PAYMENT_RECEIPT │
├─────────────────┤──────────├─────────────────┤
│ (payment_id) PK │ generates│ (receipt_id) PK │
│ booking_id (FK) │          │ payment_id (FK) │
│ user_id (FK)    │          │ generated_at    │
│ amount          │          │ downloaded_count│
│ payment_method  │          └─────────────────┘
│ status          │
│ transaction_id  │
│ payment_date    │
└─────────────────┘
```

---

## Summary of Entities (11 Total - No Passenger)

| Entity | Primary Key | Foreign Keys |
|--------|-------------|--------------|
| USER | user_id | - |
| USER_PROFILE | profile_id | user_id |
| PARTNER | partner_id | user_id |
| HOTEL | hotel_id | partner_id |
| ROOM_TYPE | roomtype_id | hotel_id |
| FLIGHT | flight_id | partner_id |
| BOOKING | booking_id | user_id |
| HOTEL_BOOKING_DETAIL | id | booking_id, hotel_id, room_type_id |
| FLIGHT_BOOKING_DETAIL | id | booking_id, flight_id |
| PAYMENT | payment_id | booking_id, user_id |
| PAYMENT_RECEIPT | receipt_id | payment_id |

---

## Relationships

| Relationship | Cardinality | Description |
|--------------|-------------|-------------|
| USER - USER_PROFILE | 1:1 | Each user has one profile |
| USER - PARTNER | 1:0..1 | User can become a partner |
| USER - BOOKING | 1:N | User makes many bookings |
| PARTNER - HOTEL | 1:N | Partner manages many hotels |
| PARTNER - FLIGHT | 1:N | Partner provides many flights |
| HOTEL - ROOM_TYPE | 1:N | Hotel has many room types |
| BOOKING - HOTEL_BOOKING_DETAIL | 1:0..1 | Hotel booking details |
| BOOKING - FLIGHT_BOOKING_DETAIL | 1:0..1 | Flight booking details (includes passenger) |
| BOOKING - PAYMENT | 1:1 | Booking is paid via payment |
| PAYMENT - PAYMENT_RECEIPT | 1:1 | Payment generates receipt |
