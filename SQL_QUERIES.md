# SQL Queries Documentation

## 1. User Bookings Query
```sql
SELECT 
    b.booking_id,
    b.booking_type,
    b.status,
    b.total_amount,
    b.created_at,
    u.username,
    u.email
FROM bookings_booking b
INNER JOIN accounts_user u ON b.user_id = u.id
WHERE u.id = ?
ORDER BY b.created_at DESC;
```

**Purpose:** Retrieve all bookings for a specific user
**Returns:** List of bookings with user information
**Indexes Used:** user_id (FK index)

## 2. Available Rooms Query
```sql
SELECT 
    rt.id,
    rt.name,
    rt.price_per_night,
    rt.rooms_available - COALESCE(
        (SELECT SUM(hbd.number_of_rooms)
         FROM bookings_hotelbookingdetail hbd
         INNER JOIN bookings_booking b ON hbd.booking_id = b.id
         WHERE hbd.room_type_id = rt.id
         AND b.status IN ('pending', 'confirmed')
         AND hbd.check_in_date < ?
         AND hbd.check_out_date > ?), 0
    ) as actually_available
FROM partners_roomtype rt
WHERE rt.hotel_id = ?
AND rt.is_active = TRUE
HAVING actually_available > 0;
```

**Purpose:** Find available rooms considering existing bookings
**Returns:** Rooms with actual availability
**Complex Features:** Subquery, date overlap check

## 3. Revenue Report Query
```sql
SELECT 
    DATE_TRUNC('month', created_at) as month,
    booking_type,
    COUNT(*) as booking_count,
    SUM(total_amount) as total_revenue
FROM bookings_booking
WHERE status IN ('confirmed', 'completed')
GROUP BY DATE_TRUNC('month', created_at), booking_type
ORDER BY month DESC;
```

**Purpose:** Monthly revenue analysis
**Returns:** Revenue grouped by month and booking type
**Features:** Aggregation, date functions

## 4. Hotel Search Query
```sql
SELECT DISTINCT
    h.id,
    h.name,
    h.city,
    h.star_rating,
    h.main_image,
    MIN(rt.price_per_night) as min_price,
    COUNT(rt.id) as room_types_count
FROM partners_hotel h
LEFT JOIN partners_roomtype rt ON h.id = rt.hotel_id
WHERE h.is_active = TRUE
AND h.city ILIKE ?
GROUP BY h.id, h.name, h.city, h.star_rating, h.main_image
ORDER BY h.star_rating DESC, min_price ASC;
```

**Purpose:** Search hotels with city filter
**Returns:** Hotels with minimum price and room type count
**Features:** LEFT JOIN, GROUP BY, pattern matching with ILIKE

## 5. Top Hotels Query
```sql
SELECT 
    h.id,
    h.name,
    h.city,
    COUNT(b.id) as booking_count,
    SUM(b.total_amount) as revenue
FROM partners_hotel h
INNER JOIN partners_roomtype rt ON h.id = rt.hotel_id
INNER JOIN bookings_hotelbookingdetail hbd ON rt.id = hbd.room_type_id
INNER JOIN bookings_booking b ON hbd.booking_id = b.id
WHERE b.status IN ('confirmed', 'completed')
GROUP BY h.id, h.name, h.city
ORDER BY revenue DESC
LIMIT 10;
```

**Purpose:** Get top performing hotels by revenue
**Returns:** Top 10 hotels with booking counts and revenue
**Features:** Multiple JOINs, aggregation, LIMIT

## 6. Customer Analytics Query
```sql
SELECT 
    u.id,
    u.username,
    u.email,
    COUNT(b.id) as total_bookings,
    SUM(b.total_amount) as total_spent,
    AVG(b.total_amount) as avg_booking_value,
    MAX(b.created_at) as last_booking_date
FROM accounts_user u
INNER JOIN bookings_booking b ON u.id = b.user_id
WHERE u.role = 'customer'
GROUP BY u.id, u.username, u.email
ORDER BY total_spent DESC
LIMIT 20;
```

**Purpose:** Analyze customer behavior and spending patterns
**Returns:** Top 20 customers with booking statistics
**Features:** Multiple aggregation functions (COUNT, SUM, AVG, MAX)

## 7. Flight Booking Details Query
```sql
SELECT 
    fbd.id,
    fbd.number_of_passengers,
    fbd.price_per_seat,
    f.flight_number,
    f.origin,
    f.destination,
    f.departure_time,
    f.arrival_time,
    f.class_type,
    p.name as partner_name
FROM bookings_flightbookingdetail fbd
INNER JOIN partners_flight f ON fbd.flight_id = f.id
INNER JOIN partners_partner p ON f.partner_id = p.id
WHERE fbd.booking_id = ?;
```

**Purpose:** Get flight booking details with airline partner info
**Returns:** Flight info with partner details
**Features:** Multiple INNER JOINs across 3 tables

## 8. Get Passengers for Flight Booking
```sql
SELECT 
    p.id,
    p.title,
    p.first_name,
    p.last_name,
    p.date_of_birth,
    p.passport_number,
    CONCAT(p.title, ' ', p.first_name, ' ', p.last_name) as full_name
FROM bookings_passenger p
WHERE p.flight_booking_id = ?
ORDER BY p.id;
```

**Purpose:** Get all passengers for a specific flight booking
**Returns:** List of passenger details
**Features:** String concatenation with CONCAT, ORDER BY

## 9. Complete Flight Booking with Passengers (Single Query)
```sql
SELECT 
    b.booking_id,
    b.status,
    b.total_amount,
    f.flight_number,
    f.origin,
    f.destination,
    f.departure_time,
    f.arrival_time,
    fbd.number_of_passengers,
    p.title as passenger_title,
    p.first_name as passenger_first_name,
    p.last_name as passenger_last_name,
    p.date_of_birth as passenger_dob,
    p.passport_number as passenger_passport
FROM bookings_booking b
INNER JOIN bookings_flightbookingdetail fbd ON b.id = fbd.booking_id
INNER JOIN partners_flight f ON fbd.flight_id = f.id
LEFT JOIN bookings_passenger p ON fbd.id = p.flight_booking_id
WHERE b.booking_id = ?
ORDER BY p.id;
```

**Purpose:** Get complete flight booking with all passenger details in one query
**Returns:** Booking details with flight info and all passengers
**Features:** 4-table JOIN (INNER + LEFT), combines booking, flight details, and passengers

