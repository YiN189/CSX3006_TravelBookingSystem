-- ==============================================
-- CSX3006 Travel Booking System - Group 14
-- Presentation Queries for pgAdmin 4
-- ==============================================


-- ================================================
-- 🟢 BASIC SELECT QUERIES (Start Simple)
-- ================================================

-- Q1: View All Users
SELECT id, username, first_name, last_name, email, role, is_active
FROM accounts_user
ORDER BY id;

-- Q2: View All Hotels
SELECT id, name, city, star_rating, is_active
FROM partners_hotel
ORDER BY star_rating DESC;

-- Q3: View All Flights
SELECT id, flight_number, origin, destination, departure_time, arrival_time, price, seats_available, class_type
FROM partners_flight
ORDER BY departure_time;


-- ================================================
-- 🔵 CUSTOMER ROLE QUERIES
-- ================================================

-- Q4: Hotel Search with Minimum Price (JOIN + GROUP BY)
SELECT DISTINCT
    h.id,
    h.name,
    h.city,
    h.star_rating,
    MIN(rt.price_per_night) AS min_price,
    COUNT(rt.id) AS room_types_count
FROM partners_hotel h
LEFT JOIN partners_roomtype rt ON h.id = rt.hotel_id
WHERE h.is_active = TRUE
GROUP BY h.id, h.name, h.city, h.star_rating
ORDER BY h.star_rating DESC, min_price ASC;

-- Q5: Hotel Detail with Room Types (JOIN)
SELECT
    h.name AS hotel_name,
    h.city,
    h.star_rating,
    h.amenities,
    rt.name AS room_type,
    rt.price_per_night,
    rt.max_occupancy,
    rt.rooms_available,
    rt.bed_type
FROM partners_hotel h
LEFT JOIN partners_roomtype rt ON h.id = rt.hotel_id
WHERE h.id = 1 AND rt.is_active = TRUE;

-- Q6: Flight Search (JOIN with Filters)
SELECT
    f.flight_number,
    f.origin,
    f.destination,
    f.departure_time,
    f.arrival_time,
    f.price,
    f.seats_available,
    f.class_type,
    p.name AS airline_name
FROM partners_flight f
INNER JOIN partners_partner p ON f.partner_id = p.id
WHERE f.is_active = TRUE
ORDER BY f.departure_time ASC;

-- Q7: My Bookings (JOIN)
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
WHERE u.id = 3
ORDER BY b.created_at DESC;

-- Q8: Booking Detail with Payment Status (LEFT JOIN)
SELECT
    b.booking_id,
    b.booking_type,
    b.status AS booking_status,
    b.total_amount,
    b.created_at,
    p.status AS payment_status,
    p.payment_method,
    p.payment_date
FROM bookings_booking b
LEFT JOIN payments_payment p ON b.id = p.booking_id
WHERE b.user_id = 3;

-- Q9: User Profile (JOIN)
SELECT
    u.username, u.email, u.first_name, u.last_name, u.phone, u.role,
    up.date_of_birth, up.address, up.city, up.country
FROM accounts_user u
LEFT JOIN accounts_userprofile up ON u.id = up.user_id
WHERE u.id = 3;

-- Q10: Payment History (JOIN)
SELECT
    p.payment_id,
    p.amount,
    p.payment_method,
    p.status,
    p.payment_date,
    p.card_last_four,
    b.booking_id,
    b.booking_type
FROM payments_payment p
INNER JOIN bookings_booking b ON p.booking_id = b.id
WHERE p.user_id = 3
ORDER BY p.created_at DESC;

-- Q11: Payment Receipt Detail (Multi-Table JOIN)
SELECT
    p.payment_id,
    p.amount,
    p.payment_method,
    p.status,
    p.transaction_id,
    p.payment_date,
    p.card_last_four,
    p.card_holder_name,
    b.booking_id,
    b.booking_type,
    b.total_amount,
    u.username,
    u.email
FROM payments_payment p
INNER JOIN bookings_booking b ON p.booking_id = b.id
INNER JOIN accounts_user u ON p.user_id = u.id
WHERE p.user_id = 3;

-- Q12: Hotel Booking Details (Multi-Table JOIN)
SELECT
    hbd.check_in_date,
    hbd.check_out_date,
    hbd.number_of_rooms,
    hbd.number_of_guests,
    hbd.price_per_night,
    hbd.number_of_nights,
    h.name AS hotel_name,
    h.city,
    h.star_rating,
    rt.name AS room_type_name
FROM bookings_hotelbookingdetail hbd
INNER JOIN partners_hotel h ON hbd.hotel_id = h.id
INNER JOIN partners_roomtype rt ON hbd.room_type_id = rt.id
WHERE hbd.booking_id = 1;

-- Q13: Flight Booking with Passenger Info (Multi-Table JOIN)
SELECT
    fbd.passenger_title,
    fbd.passenger_first_name,
    fbd.passenger_last_name,
    fbd.passenger_dob,
    fbd.passenger_passport,
    fbd.number_of_passengers,
    fbd.price_per_seat,
    f.flight_number,
    f.origin,
    f.destination,
    f.departure_time,
    f.arrival_time,
    f.class_type,
    p.name AS airline_name
FROM bookings_flightbookingdetail fbd
INNER JOIN partners_flight f ON fbd.flight_id = f.id
INNER JOIN partners_partner p ON f.partner_id = p.id
WHERE fbd.booking_id = 2;


-- ================================================
-- 🟠 PARTNER ROLE QUERIES
-- ================================================

-- Q14: Partner Dashboard Statistics (Subqueries + Aggregation)
SELECT
    p.name AS partner_name,
    p.partner_type,
    p.is_verified,
    (SELECT COUNT(*) FROM partners_hotel h WHERE h.partner_id = p.id) AS total_hotels,
    (SELECT COUNT(*) FROM partners_flight f WHERE f.partner_id = p.id) AS total_flights
FROM partners_partner p
WHERE p.user_id = 2;

-- Q15: Partner's Hotels with Room Count
SELECT
    h.name, h.city, h.star_rating, h.is_active,
    (SELECT COUNT(*) FROM partners_roomtype rt WHERE rt.hotel_id = h.id) AS room_type_count
FROM partners_hotel h
WHERE h.partner_id = 1
ORDER BY h.created_at DESC;

-- Q16: Partner's Room Types for a Hotel
SELECT rt.name, rt.price_per_night, rt.max_occupancy, rt.rooms_available, rt.bed_type, rt.is_active
FROM partners_roomtype rt
WHERE rt.hotel_id = 1
ORDER BY rt.price_per_night ASC;

-- Q17: Partner's Flights
SELECT f.flight_number, f.origin, f.destination, f.departure_time, f.arrival_time, f.price, f.seats_available, f.class_type, f.is_active
FROM partners_flight f
INNER JOIN partners_partner p ON f.partner_id = p.id
WHERE p.user_id = 2
ORDER BY f.departure_time ASC;


-- ================================================
-- 🔴 ADMIN ROLE QUERIES
-- ================================================

-- Q18: User Statistics (CASE + Aggregation)
SELECT
    COUNT(*) AS total_users,
    SUM(CASE WHEN role = 'customer' THEN 1 ELSE 0 END) AS customers,
    SUM(CASE WHEN role = 'partner' THEN 1 ELSE 0 END) AS partners,
    SUM(CASE WHEN role = 'admin' THEN 1 ELSE 0 END) AS admins
FROM accounts_user;

-- Q19: Partner Statistics
SELECT
    COUNT(*) AS total_partners,
    SUM(CASE WHEN is_verified = TRUE THEN 1 ELSE 0 END) AS verified_partners
FROM partners_partner;

-- Q20: Booking Statistics
SELECT
    COUNT(*) AS total_bookings,
    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS pending,
    SUM(CASE WHEN status = 'confirmed' THEN 1 ELSE 0 END) AS confirmed,
    SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled
FROM bookings_booking;

-- Q21: Revenue Report
SELECT
    COALESCE(SUM(total_amount), 0) AS total_revenue,
    COALESCE(AVG(total_amount), 0) AS avg_booking_value
FROM bookings_booking
WHERE status IN ('confirmed', 'completed');

-- Q22: Top Customers (GROUP BY + ORDER BY)
SELECT
    u.username,
    u.email,
    COUNT(b.id) AS booking_count,
    COALESCE(SUM(b.total_amount), 0) AS total_spent
FROM accounts_user u
LEFT JOIN bookings_booking b ON u.id = b.user_id
WHERE u.role = 'customer'
GROUP BY u.id, u.username, u.email
ORDER BY total_spent DESC
LIMIT 5;

-- Q23: Recent Bookings (JOIN + LIMIT)
SELECT b.booking_id, b.booking_type, b.status, b.total_amount, b.created_at, u.username
FROM bookings_booking b
INNER JOIN accounts_user u ON b.user_id = u.id
ORDER BY b.created_at DESC
LIMIT 10;

-- Q24: Payment Statistics (Advanced Aggregation)
SELECT
    COUNT(*) AS payment_count,
    COALESCE(SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END), 0) AS total_revenue,
    COALESCE(SUM(CASE WHEN status = 'refunded' THEN amount ELSE 0 END), 0) AS total_refunded,
    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed,
    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) AS failed
FROM payments_payment;

-- Q25: Payments by Method (GROUP BY)
SELECT
    payment_method,
    COUNT(*) AS count,
    COALESCE(SUM(amount), 0) AS total
FROM payments_payment
GROUP BY payment_method
ORDER BY total DESC;

-- Q26: Recent Payments with Details
SELECT p.payment_id, p.amount, p.payment_method, p.status, p.payment_date, u.username, b.booking_id, b.booking_type
FROM payments_payment p
INNER JOIN accounts_user u ON p.user_id = u.id
INNER JOIN bookings_booking b ON p.booking_id = b.id
ORDER BY p.created_at DESC
LIMIT 10;


-- ================================================
-- 🟣 BONUS: REPORTING QUERIES
-- ================================================

-- Q27: Monthly Revenue Report (TO_CHAR + GROUP BY)
SELECT
    TO_CHAR(created_at, 'YYYY-MM') AS month,
    booking_type,
    COUNT(*) AS booking_count,
    SUM(total_amount) AS total_revenue
FROM bookings_booking
WHERE status IN ('confirmed', 'completed')
GROUP BY TO_CHAR(created_at, 'YYYY-MM'), booking_type
ORDER BY month DESC;

-- Q28: Top Hotels by Revenue (Multi-Table JOIN)
SELECT
    h.name, h.city,
    COUNT(b.id) AS booking_count,
    SUM(b.total_amount) AS revenue
FROM partners_hotel h
INNER JOIN partners_roomtype rt ON h.id = rt.hotel_id
INNER JOIN bookings_hotelbookingdetail hbd ON rt.id = hbd.room_type_id
INNER JOIN bookings_booking b ON hbd.booking_id = b.id
WHERE b.status IN ('confirmed', 'completed')
GROUP BY h.id, h.name, h.city
ORDER BY revenue DESC
LIMIT 10;

-- Q29: Customer Analytics (GROUP BY + Aggregation)
SELECT
    u.username,
    u.email,
    COUNT(b.id) AS total_bookings,
    SUM(b.total_amount) AS total_spent,
    AVG(b.total_amount) AS avg_booking_value,
    MAX(b.created_at) AS last_booking_date
FROM accounts_user u
INNER JOIN bookings_booking b ON u.id = b.user_id
WHERE u.role = 'customer'
GROUP BY u.id, u.username, u.email
ORDER BY total_spent DESC
LIMIT 20;

-- Q30: Available Rooms with Date Overlap Check (Subquery)
SELECT
    rt.id, rt.name, rt.price_per_night, rt.max_occupancy, rt.rooms_available,
    rt.rooms_available - COALESCE(
        (SELECT SUM(hbd.number_of_rooms)
         FROM bookings_hotelbookingdetail hbd
         INNER JOIN bookings_booking b ON hbd.booking_id = b.id
         WHERE hbd.room_type_id = rt.id
         AND b.status IN ('pending', 'confirmed')
         AND hbd.check_in_date < '2026-03-05'
         AND hbd.check_out_date > '2026-03-01'), 0
    ) AS actually_available
FROM partners_roomtype rt
WHERE rt.hotel_id = 1 AND rt.is_active = TRUE;

-- Q31: Hotel Statistics (LEFT JOINs + Aggregation)
SELECT
    h.name, h.city,
    COUNT(DISTINCT rt.id) AS total_room_types,
    SUM(rt.rooms_available) AS total_rooms,
    COUNT(DISTINCT b.id) AS total_bookings,
    COALESCE(SUM(b.total_amount), 0) AS total_revenue
FROM partners_hotel h
LEFT JOIN partners_roomtype rt ON h.id = rt.hotel_id
LEFT JOIN bookings_hotelbookingdetail hbd ON rt.id = hbd.room_type_id
LEFT JOIN bookings_booking b ON hbd.booking_id = b.id AND b.status = 'confirmed'
WHERE h.id = 1
GROUP BY h.id, h.name, h.city;


-- ==============================================
-- END OF PRESENTATION QUERIES
-- ==============================================
