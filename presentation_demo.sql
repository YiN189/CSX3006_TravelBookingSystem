-- ==============================================
-- CSX3006 Travel Booking System - Group 14
-- PRESENTATION DEMO SCRIPT
-- Pattern: SHOW → INSERT/UPDATE/DELETE → SHOW AGAIN
-- Run each block one at a time in pgAdmin 4
-- ==============================================


-- ████████████████████████████████████████████████
-- DEMO 1: USER REGISTRATION
-- ████████████████████████████████████████████████

-- Step 1: Show existing users BEFORE
SELECT id, username, first_name, last_name, email, role, is_active
FROM accounts_user
ORDER BY id;

-- Step 2: Register a new customer
INSERT INTO "accounts_user" ("password", "last_login", "is_superuser", "username",
 "first_name", "last_name", "is_staff", "is_active", "date_joined", "role",
 "email", "phone", "created_at", "updated_at")
VALUES ('pbkdf2_sha256$hashed_pw', NULL, FALSE, 'demo_customer', 'Jane', 'Smith',
 FALSE, TRUE, NOW(), 'customer', 'jane@demo.com', '0891112222', NOW(), NOW());

-- Step 3: Show users AFTER (new customer should appear)
SELECT id, username, first_name, last_name, email, role, is_active
FROM accounts_user
ORDER BY id;


-- ████████████████████████████████████████████████
-- DEMO 2: CREATE USER PROFILE
-- ████████████████████████████████████████████████

-- Step 1: Show existing profiles BEFORE
SELECT u.username, u.email, up.date_of_birth, up.address, up.city, up.country
FROM accounts_user u
LEFT JOIN accounts_userprofile up ON u.id = up.user_id
ORDER BY u.id;

-- Step 2: Create profile for the new user
INSERT INTO "accounts_userprofile" ("profile_picture", "date_of_birth", "address",
 "city", "country", "user_id")
VALUES (NULL, '1995-08-20', '456 Demo Street', 'Chiang Mai', 'Thailand',
 (SELECT id FROM accounts_user WHERE username = 'demo_customer'));

-- Step 3: Show profiles AFTER (new profile should appear)
SELECT u.username, u.email, up.date_of_birth, up.address, up.city, up.country
FROM accounts_user u
LEFT JOIN accounts_userprofile up ON u.id = up.user_id
ORDER BY u.id;


-- ████████████████████████████████████████████████
-- DEMO 3: PARTNER ADDS A NEW HOTEL
-- ████████████████████████████████████████████████

-- Step 1: Show existing hotels BEFORE
SELECT id, name, city, star_rating, is_active
FROM partners_hotel
ORDER BY id;

-- Step 2: Partner creates a new hotel
INSERT INTO "partners_hotel" ("name", "city", "address", "description", "star_rating",
 "main_image", "amenities", "check_in_time", "check_out_time", "email", "phone",
 "is_active", "created_at", "updated_at", "partner_id")
VALUES ('Riverside Resort', 'Phuket', '123 Beach Road', 'Beautiful beachfront resort',
 4, NULL, 'Pool, Beach Access, Spa, WiFi', '15:00:00', '11:00:00',
 'info@riverside.com', '076123456', TRUE, NOW(), NOW(), 1);

-- Step 3: Show hotels AFTER (new hotel should appear)
SELECT id, name, city, star_rating, is_active
FROM partners_hotel
ORDER BY id;


-- ████████████████████████████████████████████████
-- DEMO 4: ADD ROOM TYPES TO HOTEL
-- ████████████████████████████████████████████████

-- Step 1: Show existing room types BEFORE
SELECT rt.id, rt.name, rt.price_per_night, rt.max_occupancy, 
 rt.rooms_available, rt.bed_type, h.name AS hotel_name
FROM partners_roomtype rt
INNER JOIN partners_hotel h ON rt.hotel_id = h.id
ORDER BY h.name, rt.price_per_night;

-- Step 2: Add room types to the new hotel
INSERT INTO "partners_roomtype" ("name", "description", "price_per_night",
 "max_occupancy", "rooms_available", "room_size", "bed_type", "amenities",
 "image", "is_active", "created_at", "updated_at", "hotel_id")
VALUES ('Ocean View Room', 'Room with stunning ocean view', 4500.00, 2, 15,
 40.00, 'King', 'WiFi, TV, Minibar, Balcony', NULL, TRUE, NOW(), NOW(),
 (SELECT id FROM partners_hotel WHERE name = 'Riverside Resort'));

INSERT INTO "partners_roomtype" ("name", "description", "price_per_night",
 "max_occupancy", "rooms_available", "room_size", "bed_type", "amenities",
 "image", "is_active", "created_at", "updated_at", "hotel_id")
VALUES ('Beach Villa', 'Private villa steps from the beach', 12000.00, 4, 3,
 90.00, 'King', 'WiFi, TV, Minibar, Private Pool, Kitchen', NULL, TRUE, NOW(), NOW(),
 (SELECT id FROM partners_hotel WHERE name = 'Riverside Resort'));

-- Step 3: Show room types AFTER (new rooms should appear)
SELECT rt.id, rt.name, rt.price_per_night, rt.max_occupancy, 
 rt.rooms_available, rt.bed_type, h.name AS hotel_name
FROM partners_roomtype rt
INNER JOIN partners_hotel h ON rt.hotel_id = h.id
ORDER BY h.name, rt.price_per_night;


-- ████████████████████████████████████████████████
-- DEMO 5: ADD A NEW FLIGHT
-- ████████████████████████████████████████████████

-- Step 1: Show existing flights BEFORE
SELECT id, flight_number, origin, destination, departure_time,
 arrival_time, price, seats_available, class_type
FROM partners_flight
ORDER BY departure_time;

-- Step 2: Add a new flight
INSERT INTO "partners_flight" ("flight_number", "origin", "destination",
 "departure_time", "arrival_time", "price", "seats_available", "total_seats",
 "aircraft_type", "airline_logo", "class_type", "is_active",
 "created_at", "updated_at", "partner_id")
VALUES ('TG202', 'Bangkok', 'Phuket', '2026-03-20 10:00:00',
 '2026-03-20 11:30:00', 3200.00, 160, 160, 'Airbus A320', NULL,
 'Economy', TRUE, NOW(), NOW(), 1);

-- Step 3: Show flights AFTER (new flight should appear)
SELECT id, flight_number, origin, destination, departure_time,
 arrival_time, price, seats_available, class_type
FROM partners_flight
ORDER BY departure_time;


-- ████████████████████████████████████████████████
-- DEMO 6: CUSTOMER SEARCHES FOR HOTELS (SELECT with JOIN)
-- ████████████████████████████████████████████████

-- Step 1: Search all hotels with minimum price
SELECT DISTINCT
    h.id, h.name, h.city, h.star_rating,
    MIN(rt.price_per_night) AS min_price,
    COUNT(rt.id) AS room_types_count
FROM partners_hotel h
LEFT JOIN partners_roomtype rt ON h.id = rt.hotel_id
WHERE h.is_active = TRUE
GROUP BY h.id, h.name, h.city, h.star_rating
ORDER BY h.star_rating DESC, min_price ASC;

-- Step 2: Search hotels in specific city (e.g., Bangkok)
SELECT DISTINCT
    h.id, h.name, h.city, h.star_rating,
    MIN(rt.price_per_night) AS min_price,
    COUNT(rt.id) AS room_types_count
FROM partners_hotel h
LEFT JOIN partners_roomtype rt ON h.id = rt.hotel_id
WHERE h.is_active = TRUE
    AND LOWER(h.city) LIKE LOWER('%Bangkok%')
GROUP BY h.id, h.name, h.city, h.star_rating
ORDER BY h.star_rating DESC, min_price ASC;


-- ████████████████████████████████████████████████
-- DEMO 7: VIEW HOTEL DETAIL WITH ROOMS
-- ████████████████████████████████████████████████

SELECT
    h.name AS hotel_name, h.city, h.star_rating, h.amenities,
    h.check_in_time, h.check_out_time,
    rt.name AS room_type, rt.price_per_night,
    rt.max_occupancy, rt.rooms_available, rt.bed_type
FROM partners_hotel h
LEFT JOIN partners_roomtype rt ON h.id = rt.hotel_id
WHERE h.id = 1 AND rt.is_active = TRUE;


-- ████████████████████████████████████████████████
-- DEMO 8: CUSTOMER BOOKS A HOTEL
-- ████████████████████████████████████████████████

-- Step 1: Show bookings BEFORE
SELECT b.booking_id, b.booking_type, b.status, b.total_amount,
 b.created_at, u.username
FROM bookings_booking b
INNER JOIN accounts_user u ON b.user_id = u.id
ORDER BY b.created_at DESC;

-- Step 2: Show room availability BEFORE
SELECT id, name, rooms_available FROM partners_roomtype WHERE hotel_id = 1;

-- Step 3: Create hotel booking
INSERT INTO "bookings_booking" ("booking_id", "booking_type", "status",
 "total_amount", "notes", "created_at", "updated_at", "user_id")
VALUES ('demo1234567890demo1234567890demo12', 'hotel', 'pending', 7000.00,
 'Demo booking - high floor request', NOW(), NOW(),
 (SELECT id FROM accounts_user WHERE username = 'demo_customer'));

INSERT INTO "bookings_hotelbookingdetail" ("check_in_date", "check_out_date",
 "number_of_rooms", "number_of_guests", "price_per_night", "number_of_nights",
 "booking_id", "hotel_id", "room_type_id")
VALUES ('2026-04-01', '2026-04-03', 1, 2, 3500.00, 2,
 (SELECT id FROM bookings_booking WHERE booking_id = 'demo1234567890demo1234567890demo12'),
 1, 1);

-- Step 4: Reduce room availability
UPDATE partners_roomtype SET rooms_available = rooms_available - 1 WHERE id = 1;

-- Step 5: Show bookings AFTER (new booking should appear)
SELECT b.booking_id, b.booking_type, b.status, b.total_amount,
 b.created_at, u.username
FROM bookings_booking b
INNER JOIN accounts_user u ON b.user_id = u.id
ORDER BY b.created_at DESC;

-- Step 6: Show room availability AFTER (reduced by 1)
SELECT id, name, rooms_available FROM partners_roomtype WHERE hotel_id = 1;


-- ████████████████████████████████████████████████
-- DEMO 9: CUSTOMER BOOKS A FLIGHT
-- ████████████████████████████████████████████████

-- Step 1: Show flights with seat count BEFORE
SELECT id, flight_number, origin, destination, seats_available FROM partners_flight;

-- Step 2: Create flight booking
INSERT INTO "bookings_booking" ("booking_id", "booking_type", "status",
 "total_amount", "notes", "created_at", "updated_at", "user_id")
VALUES ('demo_flight_uuid_1234567890demo12', 'flight', 'pending', 2500.00,
 NULL, NOW(), NOW(),
 (SELECT id FROM accounts_user WHERE username = 'demo_customer'));

INSERT INTO "bookings_flightbookingdetail" ("number_of_passengers", "price_per_seat",
 "passenger_title", "passenger_first_name", "passenger_last_name",
 "passenger_dob", "passenger_passport", "booking_id", "flight_id")
VALUES (1, 2500.00, 'Ms', 'Jane', 'Smith', '1995-08-20', 'TH99887766',
 (SELECT id FROM bookings_booking WHERE booking_id = 'demo_flight_uuid_1234567890demo12'),
 1);

-- Step 3: Reduce seat availability
UPDATE partners_flight SET seats_available = seats_available - 1 WHERE id = 1;

-- Step 4: Show flights AFTER (seats reduced by 1)
SELECT id, flight_number, origin, destination, seats_available FROM partners_flight;

-- Step 5: Show all bookings for demo customer
SELECT b.booking_id, b.booking_type, b.status, b.total_amount, b.created_at
FROM bookings_booking b
INNER JOIN accounts_user u ON b.user_id = u.id
WHERE u.username = 'demo_customer'
ORDER BY b.created_at DESC;


-- ████████████████████████████████████████████████
-- DEMO 10: PROCESS PAYMENT
-- ████████████████████████████████████████████████

-- Step 1: Show payments BEFORE
SELECT p.payment_id, p.amount, p.payment_method, p.status,
 p.payment_date, u.username
FROM payments_payment p
INNER JOIN accounts_user u ON p.user_id = u.id
ORDER BY p.created_at DESC;

-- Step 2: Create payment for hotel booking
INSERT INTO "payments_payment" ("payment_id", "amount", "payment_method", "status",
 "transaction_id", "card_type", "card_last_four", "card_holder_name",
 "bank_name", "account_number", "paypal_email", "payment_date",
 "created_at", "updated_at", "notes", "failure_reason", "booking_id", "user_id")
VALUES ('demo_payment_uuid_12345678901234', 7000.00, 'credit_card', 'completed',
 'TXN-DEMO123ABC', 'visa', '9876', 'Jane Smith', NULL, NULL, NULL, NOW(),
 NOW(), NOW(), NULL, NULL,
 (SELECT id FROM bookings_booking WHERE booking_id = 'demo1234567890demo1234567890demo12'),
 (SELECT id FROM accounts_user WHERE username = 'demo_customer'));

-- Step 3: Update booking status to confirmed
UPDATE bookings_booking SET status = 'confirmed', updated_at = NOW()
WHERE booking_id = 'demo1234567890demo1234567890demo12';

-- Step 4: Show payments AFTER
SELECT p.payment_id, p.amount, p.payment_method, p.status,
 p.payment_date, u.username
FROM payments_payment p
INNER JOIN accounts_user u ON p.user_id = u.id
ORDER BY p.created_at DESC;

-- Step 5: Show booking status changed to confirmed
SELECT b.booking_id, b.booking_type, b.status, b.total_amount
FROM bookings_booking b
WHERE b.booking_id = 'demo1234567890demo1234567890demo12';


-- ████████████████████████████████████████████████
-- DEMO 11: GENERATE RECEIPT
-- ████████████████████████████████████████████████

-- Step 1: Show receipts BEFORE
SELECT pr.receipt_id, pr.generated_at, pr.downloaded_count,
 p.payment_id, p.amount
FROM payments_paymentreceipt pr
INNER JOIN payments_payment p ON pr.payment_id = p.id
ORDER BY pr.generated_at DESC;

-- Step 2: Create receipt
INSERT INTO "payments_paymentreceipt" ("receipt_id", "generated_at",
 "downloaded_count", "payment_id")
VALUES ('demo_receipt_uuid_123456789012345',  NOW(), 0,
 (SELECT id FROM payments_payment WHERE payment_id = 'demo_payment_uuid_12345678901234'));

-- Step 3: Show receipts AFTER
SELECT pr.receipt_id, pr.generated_at, pr.downloaded_count,
 p.payment_id, p.amount
FROM payments_paymentreceipt pr
INNER JOIN payments_payment p ON pr.payment_id = p.id
ORDER BY pr.generated_at DESC;

-- Step 4: Increment download count (simulate download)
UPDATE payments_paymentreceipt SET downloaded_count = downloaded_count + 1
WHERE receipt_id = 'demo_receipt_uuid_123456789012345';

-- Step 5: Show updated download count
SELECT receipt_id, downloaded_count FROM payments_paymentreceipt
WHERE receipt_id = 'demo_receipt_uuid_123456789012345';


-- ████████████████████████████████████████████████
-- DEMO 12: VIEW BOOKING DETAILS (Multi-Table JOIN)
-- ████████████████████████████████████████████████

-- Hotel booking details
SELECT
    b.booking_id, b.status, b.total_amount,
    hbd.check_in_date, hbd.check_out_date,
    hbd.number_of_rooms, hbd.number_of_guests,
    hbd.price_per_night, hbd.number_of_nights,
    h.name AS hotel_name, h.city,
    rt.name AS room_type
FROM bookings_booking b
INNER JOIN bookings_hotelbookingdetail hbd ON b.id = hbd.booking_id
INNER JOIN partners_hotel h ON hbd.hotel_id = h.id
INNER JOIN partners_roomtype rt ON hbd.room_type_id = rt.id
WHERE b.booking_id = 'demo1234567890demo1234567890demo12';

-- Flight booking details
SELECT
    b.booking_id, b.status, b.total_amount,
    fbd.passenger_title, fbd.passenger_first_name,
    fbd.passenger_last_name, fbd.passenger_passport,
    f.flight_number, f.origin, f.destination,
    f.departure_time, f.arrival_time, f.class_type,
    p.name AS airline_name
FROM bookings_booking b
INNER JOIN bookings_flightbookingdetail fbd ON b.id = fbd.booking_id
INNER JOIN partners_flight f ON fbd.flight_id = f.id
INNER JOIN partners_partner p ON f.partner_id = p.id
WHERE b.booking_id = 'demo_flight_uuid_1234567890demo12';


-- ████████████████████████████████████████████████
-- DEMO 13: REFUND PAYMENT
-- ████████████████████████████████████████████████

-- Step 1: Show payment status BEFORE
SELECT payment_id, amount, status, notes
FROM payments_payment
WHERE payment_id = 'demo_payment_uuid_12345678901234';

-- Step 2: Process refund
UPDATE payments_payment
SET status = 'refunded', notes = 'Refund: Changed travel plans',
 updated_at = NOW()
WHERE payment_id = 'demo_payment_uuid_12345678901234';

-- Step 3: Cancel booking
UPDATE bookings_booking SET status = 'cancelled', updated_at = NOW()
WHERE booking_id = 'demo1234567890demo1234567890demo12';

-- Step 4: Restore room availability
UPDATE partners_roomtype SET rooms_available = rooms_available + 1 WHERE id = 1;

-- Step 5: Show payment status AFTER (now refunded)
SELECT payment_id, amount, status, notes
FROM payments_payment
WHERE payment_id = 'demo_payment_uuid_12345678901234';

-- Step 6: Show booking status AFTER (now cancelled)
SELECT booking_id, status, total_amount
FROM bookings_booking
WHERE booking_id = 'demo1234567890demo1234567890demo12';

-- Step 7: Show rooms restored
SELECT id, name, rooms_available FROM partners_roomtype WHERE id = 1;


-- ████████████████████████████████████████████████
-- DEMO 14: UPDATE HOTEL (Partner)
-- ████████████████████████████████████████████████

-- Step 1: Show hotel BEFORE
SELECT id, name, star_rating, amenities FROM partners_hotel WHERE id = 1;

-- Step 2: Update hotel
UPDATE partners_hotel
SET name = 'Grand Palace Hotel Premium',
 amenities = 'WiFi, Pool, Spa, Gym, Restaurant, Rooftop Bar',
 updated_at = NOW()
WHERE id = 1;

-- Step 3: Show hotel AFTER
SELECT id, name, star_rating, amenities FROM partners_hotel WHERE id = 1;


-- ████████████████████████████████████████████████
-- DEMO 15: UPDATE USER PROFILE
-- ████████████████████████████████████████████████

-- Step 1: Show profile BEFORE
SELECT u.username, u.first_name, u.last_name, u.email, u.phone,
 up.address, up.city, up.country
FROM accounts_user u
LEFT JOIN accounts_userprofile up ON u.id = up.user_id
WHERE u.username = 'demo_customer';

-- Step 2: Update profile
UPDATE accounts_user
SET phone = '0899999999', updated_at = NOW()
WHERE username = 'demo_customer';

UPDATE accounts_userprofile
SET address = '789 Updated Street', city = 'Phuket'
WHERE user_id = (SELECT id FROM accounts_user WHERE username = 'demo_customer');

-- Step 3: Show profile AFTER
SELECT u.username, u.first_name, u.last_name, u.email, u.phone,
 up.address, up.city, up.country
FROM accounts_user u
LEFT JOIN accounts_userprofile up ON u.id = up.user_id
WHERE u.username = 'demo_customer';


-- ████████████████████████████████████████████████
-- DEMO 16: DELETE HOTEL (Partner)
-- ████████████████████████████████████████████████

-- Step 1: Show hotels BEFORE
SELECT id, name, city, star_rating FROM partners_hotel ORDER BY id;

-- Step 2: Delete the demo hotel (must delete room types first due to FK)
DELETE FROM partners_roomtype
WHERE hotel_id = (SELECT id FROM partners_hotel WHERE name = 'Riverside Resort');

DELETE FROM partners_hotel WHERE name = 'Riverside Resort';

-- Step 3: Show hotels AFTER (Riverside Resort removed)
SELECT id, name, city, star_rating FROM partners_hotel ORDER BY id;


-- ████████████████████████████████████████████████
-- DEMO 17: ADMIN DASHBOARD STATISTICS
-- ████████████████████████████████████████████████

-- User statistics
SELECT
    COUNT(*) AS total_users,
    SUM(CASE WHEN role = 'customer' THEN 1 ELSE 0 END) AS customers,
    SUM(CASE WHEN role = 'partner' THEN 1 ELSE 0 END) AS partners,
    SUM(CASE WHEN role = 'admin' THEN 1 ELSE 0 END) AS admins
FROM accounts_user;

-- Booking statistics
SELECT
    COUNT(*) AS total_bookings,
    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS pending,
    SUM(CASE WHEN status = 'confirmed' THEN 1 ELSE 0 END) AS confirmed,
    SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled
FROM bookings_booking;

-- Revenue
SELECT
    COALESCE(SUM(total_amount), 0) AS total_revenue,
    COALESCE(AVG(total_amount), 0) AS avg_booking_value
FROM bookings_booking
WHERE status IN ('confirmed', 'completed');

-- Top customers
SELECT u.username, u.email,
    COUNT(b.id) AS booking_count,
    COALESCE(SUM(b.total_amount), 0) AS total_spent
FROM accounts_user u
LEFT JOIN bookings_booking b ON u.id = b.user_id
WHERE u.role = 'customer'
GROUP BY u.id, u.username, u.email
ORDER BY total_spent DESC LIMIT 5;

-- Payment breakdown by method
SELECT payment_method, COUNT(*) AS count,
 COALESCE(SUM(amount), 0) AS total
FROM payments_payment
GROUP BY payment_method ORDER BY total DESC;


-- ████████████████████████████████████████████████
-- DEMO 18: CLEANUP (Run after presentation)
-- Removes all demo data to restore original state
-- ████████████████████████████████████████████████

-- Delete demo receipts
DELETE FROM payments_paymentreceipt
WHERE payment_id IN (SELECT id FROM payments_payment
 WHERE payment_id = 'demo_payment_uuid_12345678901234');

-- Delete demo payments
DELETE FROM payments_payment WHERE payment_id = 'demo_payment_uuid_12345678901234';

-- Delete demo booking details
DELETE FROM bookings_hotelbookingdetail
WHERE booking_id IN (SELECT id FROM bookings_booking
 WHERE booking_id IN ('demo1234567890demo1234567890demo12'));

DELETE FROM bookings_flightbookingdetail
WHERE booking_id IN (SELECT id FROM bookings_booking
 WHERE booking_id IN ('demo_flight_uuid_1234567890demo12'));

-- Delete demo bookings
DELETE FROM bookings_booking
WHERE booking_id IN ('demo1234567890demo1234567890demo12', 'demo_flight_uuid_1234567890demo12');

-- Delete demo room types (for Riverside Resort if not already deleted)
DELETE FROM partners_roomtype
WHERE hotel_id IN (SELECT id FROM partners_hotel WHERE name = 'Riverside Resort');

-- Delete demo hotel
DELETE FROM partners_hotel WHERE name = 'Riverside Resort';

-- Delete demo flight
DELETE FROM partners_flight WHERE flight_number = 'TG202';

-- Delete demo user profile
DELETE FROM accounts_userprofile
WHERE user_id = (SELECT id FROM accounts_user WHERE username = 'demo_customer');

-- Delete demo user
DELETE FROM accounts_user WHERE username = 'demo_customer';

-- Restore hotel name if changed
UPDATE partners_hotel SET name = 'Grand Palace Hotel',
 amenities = 'WiFi, Pool, Spa, Gym, Restaurant'
WHERE id = 1;

-- Verify cleanup: should show original data only
SELECT '--- Users ---' AS section;
SELECT id, username, role FROM accounts_user ORDER BY id;
SELECT '--- Hotels ---' AS section;
SELECT id, name, city FROM partners_hotel ORDER BY id;
SELECT '--- Flights ---' AS section;
SELECT id, flight_number FROM partners_flight ORDER BY id;


-- ==============================================
-- END OF PRESENTATION DEMO
-- ==============================================
