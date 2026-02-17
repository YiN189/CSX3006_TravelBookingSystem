-- ==============================================
-- CSX3006 Travel Booking System
-- Complete SQL Script
-- Database: PostgreSQL
-- ==============================================

-- ██████████████████████████████████████████████
-- PART A: CREATE TABLE SCRIPTS (DDL)
-- ██████████████████████████████████████████████

-- -----------------------------------------------
-- Table 1: accounts_user (Custom User Model)
-- Stores all users: customers, partners, admins
-- -----------------------------------------------
CREATE TABLE "accounts_user" (
    "id" BIGSERIAL PRIMARY KEY,
    "password" VARCHAR(128) NOT NULL,
    "last_login" TIMESTAMP NULL,
    "is_superuser" BOOLEAN NOT NULL,
    "username" VARCHAR(150) NOT NULL UNIQUE,
    "first_name" VARCHAR(150) NOT NULL,
    "last_name" VARCHAR(150) NOT NULL,
    "is_staff" BOOLEAN NOT NULL,
    "is_active" BOOLEAN NOT NULL,
    "date_joined" TIMESTAMP NOT NULL,
    "role" VARCHAR(20) NOT NULL,
    "email" VARCHAR(254) NOT NULL UNIQUE,
    "phone" VARCHAR(15) NULL,
    "created_at" TIMESTAMP NOT NULL,
    "updated_at" TIMESTAMP NOT NULL
);

-- -----------------------------------------------
-- Table 2: accounts_userprofile (Extended User Profile)
-- -----------------------------------------------
CREATE TABLE "accounts_userprofile" (
    "id" BIGSERIAL PRIMARY KEY,
    "profile_picture" VARCHAR(100) NULL,
    "date_of_birth" DATE NULL,
    "address" TEXT NULL,
    "city" VARCHAR(100) NULL,
    "country" VARCHAR(100) NULL,
    "user_id" BIGINT NOT NULL UNIQUE REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- -----------------------------------------------
-- Table 3: partners_partner (Partner Companies)
-- -----------------------------------------------
CREATE TABLE "partners_partner" (
    "id" BIGSERIAL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "partner_type" VARCHAR(20) NOT NULL,
    "description" TEXT NULL,
    "logo" VARCHAR(100) NULL,
    "website" VARCHAR(200) NULL,
    "contact_email" VARCHAR(254) NOT NULL,
    "contact_phone" VARCHAR(15) NULL,
    "is_verified" BOOLEAN NOT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "updated_at" TIMESTAMP NOT NULL,
    "user_id" BIGINT NOT NULL UNIQUE REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- -----------------------------------------------
-- Table 4: partners_hotel (Hotels)
-- -----------------------------------------------
CREATE TABLE "partners_hotel" (
    "id" BIGSERIAL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "city" VARCHAR(100) NOT NULL,
    "address" TEXT NOT NULL,
    "description" TEXT NULL,
    "star_rating" INTEGER NOT NULL,
    "main_image" VARCHAR(100) NULL,
    "amenities" TEXT NULL,
    "check_in_time" TIME NOT NULL,
    "check_out_time" TIME NOT NULL,
    "email" VARCHAR(254) NULL,
    "phone" VARCHAR(15) NULL,
    "is_active" BOOLEAN NOT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "updated_at" TIMESTAMP NOT NULL,
    "partner_id" BIGINT NOT NULL REFERENCES "partners_partner" ("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE INDEX "partners_hotel_partner_id_7ecd2582" ON "partners_hotel" ("partner_id");

-- -----------------------------------------------
-- Table 5: partners_roomtype (Room Types for Hotels)
-- -----------------------------------------------
CREATE TABLE "partners_roomtype" (
    "id" BIGSERIAL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "description" TEXT NULL,
    "price_per_night" DECIMAL NOT NULL,
    "max_occupancy" INTEGER NOT NULL,
    "rooms_available" INTEGER NOT NULL,
    "room_size" DECIMAL NULL,
    "bed_type" VARCHAR(100) NULL,
    "amenities" TEXT NULL,
    "image" VARCHAR(100) NULL,
    "is_active" BOOLEAN NOT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "updated_at" TIMESTAMP NOT NULL,
    "hotel_id" BIGINT NOT NULL REFERENCES "partners_hotel" ("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE INDEX "partners_roomtype_hotel_id_d13ecb70" ON "partners_roomtype" ("hotel_id");

-- -----------------------------------------------
-- Table 6: partners_flight (Flights)
-- -----------------------------------------------
CREATE TABLE "partners_flight" (
    "id" BIGSERIAL PRIMARY KEY,
    "flight_number" VARCHAR(20) NOT NULL UNIQUE,
    "origin" VARCHAR(100) NOT NULL,
    "destination" VARCHAR(100) NOT NULL,
    "departure_time" TIMESTAMP NOT NULL,
    "arrival_time" TIMESTAMP NOT NULL,
    "price" DECIMAL NOT NULL,
    "seats_available" INTEGER NOT NULL,
    "total_seats" INTEGER NOT NULL,
    "aircraft_type" VARCHAR(100) NULL,
    "airline_logo" VARCHAR(100) NULL,
    "class_type" VARCHAR(50) NOT NULL,
    "is_active" BOOLEAN NOT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "updated_at" TIMESTAMP NOT NULL,
    "partner_id" BIGINT NOT NULL REFERENCES "partners_partner" ("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE INDEX "partners_flight_partner_id_65127e6b" ON "partners_flight" ("partner_id");

-- -----------------------------------------------
-- Table 7: bookings_booking (Main Booking Record)
-- -----------------------------------------------
CREATE TABLE "bookings_booking" (
    "id" BIGSERIAL PRIMARY KEY,
    "booking_id" CHAR(32) NOT NULL UNIQUE,
    "booking_type" VARCHAR(20) NOT NULL,
    "status" VARCHAR(20) NOT NULL,
    "total_amount" DECIMAL NOT NULL,
    "notes" TEXT NULL,
    "created_at" TIMESTAMP NOT NULL,
    "updated_at" TIMESTAMP NOT NULL,
    "user_id" BIGINT NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE INDEX "bookings_booking_user_id_834dfc23" ON "bookings_booking" ("user_id");

-- -----------------------------------------------
-- Table 8: bookings_hotelbookingdetail (Hotel Booking Details)
-- -----------------------------------------------
CREATE TABLE "bookings_hotelbookingdetail" (
    "id" BIGSERIAL PRIMARY KEY,
    "check_in_date" DATE NOT NULL,
    "check_out_date" DATE NOT NULL,
    "number_of_rooms" INTEGER NOT NULL,
    "number_of_guests" INTEGER NOT NULL,
    "price_per_night" DECIMAL NOT NULL,
    "number_of_nights" INTEGER NOT NULL,
    "booking_id" BIGINT NOT NULL UNIQUE REFERENCES "bookings_booking" ("id") DEFERRABLE INITIALLY DEFERRED,
    "hotel_id" BIGINT NOT NULL REFERENCES "partners_hotel" ("id") DEFERRABLE INITIALLY DEFERRED,
    "room_type_id" BIGINT NOT NULL REFERENCES "partners_roomtype" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- -----------------------------------------------
-- Table 9: bookings_flightbookingdetail (Flight Booking + Passenger Info)
-- -----------------------------------------------
CREATE TABLE "bookings_flightbookingdetail" (
    "id" BIGSERIAL PRIMARY KEY,
    "number_of_passengers" INTEGER NOT NULL,
    "price_per_seat" DECIMAL NOT NULL,
    "passenger_title" VARCHAR(10) NOT NULL,
    "passenger_first_name" VARCHAR(100) NULL,
    "passenger_last_name" VARCHAR(100) NULL,
    "passenger_dob" DATE NULL,
    "passenger_passport" VARCHAR(50) NULL,
    "booking_id" BIGINT NOT NULL UNIQUE REFERENCES "bookings_booking" ("id") DEFERRABLE INITIALLY DEFERRED,
    "flight_id" BIGINT NOT NULL REFERENCES "partners_flight" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- -----------------------------------------------
-- Table 10: payments_payment (Payment Records)
-- -----------------------------------------------
CREATE TABLE "payments_payment" (
    "id" BIGSERIAL PRIMARY KEY,
    "payment_id" CHAR(32) NOT NULL UNIQUE,
    "amount" DECIMAL NOT NULL,
    "payment_method" VARCHAR(20) NOT NULL,
    "status" VARCHAR(20) NOT NULL,
    "transaction_id" VARCHAR(100) NULL UNIQUE,
    "card_type" VARCHAR(20) NULL,
    "card_last_four" VARCHAR(4) NULL,
    "card_holder_name" VARCHAR(100) NULL,
    "bank_name" VARCHAR(100) NULL,
    "account_number" VARCHAR(50) NULL,
    "paypal_email" VARCHAR(254) NULL,
    "payment_date" TIMESTAMP NULL,
    "created_at" TIMESTAMP NOT NULL,
    "updated_at" TIMESTAMP NOT NULL,
    "notes" TEXT NULL,
    "failure_reason" TEXT NULL,
    "booking_id" BIGINT NOT NULL UNIQUE REFERENCES "bookings_booking" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" BIGINT NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE INDEX "payments_pa_created_3147e3_idx" ON "payments_payment" ("created_at" DESC);
CREATE INDEX "payments_pa_status_7ad4af_idx" ON "payments_payment" ("status");
CREATE INDEX "payments_pa_payment_5c92d7_idx" ON "payments_payment" ("payment_method");

-- -----------------------------------------------
-- Table 11: payments_paymentreceipt (Receipts)
-- -----------------------------------------------
CREATE TABLE "payments_paymentreceipt" (
    "id" BIGSERIAL PRIMARY KEY,
    "receipt_id" CHAR(32) NOT NULL UNIQUE,
    "generated_at" TIMESTAMP NOT NULL,
    "downloaded_count" INTEGER NOT NULL,
    "payment_id" BIGINT NOT NULL UNIQUE REFERENCES "payments_payment" ("id") DEFERRABLE INITIALLY DEFERRED
);


-- ██████████████████████████████████████████████
-- PART B: SAMPLE DATA (INSERT statements)
-- ██████████████████████████████████████████████

-- B1: Insert Admin User
INSERT INTO "accounts_user" ("password", "last_login", "is_superuser", "username", "first_name", "last_name", "is_staff", "is_active", "date_joined", "role", "email", "phone", "created_at", "updated_at")
VALUES ('pbkdf2_sha256$hashed_password', NULL, TRUE, 'admin', 'System', 'Admin', TRUE, TRUE, '2026-01-01 00:00:00', 'admin', 'admin@travel.com', '0812345678', '2026-01-01 00:00:00', '2026-01-01 00:00:00');

-- B2: Insert Partner User
INSERT INTO "accounts_user" ("password", "last_login", "is_superuser", "username", "first_name", "last_name", "is_staff", "is_active", "date_joined", "role", "email", "phone", "created_at", "updated_at")
VALUES ('pbkdf2_sha256$hashed_password', NULL, FALSE, 'partner1', 'Hotel', 'Manager', FALSE, TRUE, '2026-01-05 00:00:00', 'partner', 'partner@travel.com', '0898765432', '2026-01-05 00:00:00', '2026-01-05 00:00:00');

-- B3: Insert Customer User
INSERT INTO "accounts_user" ("password", "last_login", "is_superuser", "username", "first_name", "last_name", "is_staff", "is_active", "date_joined", "role", "email", "phone", "created_at", "updated_at")
VALUES ('pbkdf2_sha256$hashed_password', NULL, FALSE, 'customer1', 'John', 'Doe', FALSE, TRUE, '2026-01-10 00:00:00', 'customer', 'john@email.com', '0891234567', '2026-01-10 00:00:00', '2026-01-10 00:00:00');

-- B4: Insert User Profiles
INSERT INTO "accounts_userprofile" ("profile_picture", "date_of_birth", "address", "city", "country", "user_id")
VALUES (NULL, '1990-05-15', '123 Main St', 'Bangkok', 'Thailand', 3);

-- B5: Insert Partner Profile
INSERT INTO "partners_partner" ("name", "partner_type", "description", "logo", "website", "contact_email", "contact_phone", "is_verified", "created_at", "updated_at", "user_id")
VALUES ('Grand Hotels Group', 'both', 'Premium hotel and flight partner', NULL, 'https://grandhotels.com', 'partner@travel.com', '0898765432', TRUE, '2026-01-05 00:00:00', '2026-01-05 00:00:00', 2);

-- B6: Insert Hotel
INSERT INTO "partners_hotel" ("name", "city", "address", "description", "star_rating", "main_image", "amenities", "check_in_time", "check_out_time", "email", "phone", "is_active", "created_at", "updated_at", "partner_id")
VALUES ('Grand Palace Hotel', 'Bangkok', '999 Sukhumvit Road', 'A luxury 5-star hotel in downtown Bangkok', 5, NULL, 'WiFi, Pool, Spa, Gym, Restaurant', '14:00:00', '12:00:00', 'info@grandpalace.com', '026541234', TRUE, '2026-01-06 00:00:00', '2026-01-06 00:00:00', 1);

-- B7: Insert Room Types
INSERT INTO "partners_roomtype" ("name", "description", "price_per_night", "max_occupancy", "rooms_available", "room_size", "bed_type", "amenities", "image", "is_active", "created_at", "updated_at", "hotel_id")
VALUES ('Deluxe Room', 'Spacious room with city view', 3500.00, 2, 10, 35.00, 'King', 'WiFi, TV, Minibar', NULL, TRUE, '2026-01-06 00:00:00', '2026-01-06 00:00:00', 1);

INSERT INTO "partners_roomtype" ("name", "description", "price_per_night", "max_occupancy", "rooms_available", "room_size", "bed_type", "amenities", "image", "is_active", "created_at", "updated_at", "hotel_id")
VALUES ('Suite', 'Premium suite with panoramic view', 8500.00, 4, 5, 65.00, 'King', 'WiFi, TV, Minibar, Jacuzzi, Lounge', NULL, TRUE, '2026-01-06 00:00:00', '2026-01-06 00:00:00', 1);

-- B8: Insert Flight
INSERT INTO "partners_flight" ("flight_number", "origin", "destination", "departure_time", "arrival_time", "price", "seats_available", "total_seats", "aircraft_type", "airline_logo", "class_type", "is_active", "created_at", "updated_at", "partner_id")
VALUES ('TG101', 'Bangkok', 'Chiang Mai', '2026-03-15 08:00:00', '2026-03-15 09:15:00', 2500.00, 150, 180, 'Boeing 737', NULL, 'Economy', TRUE, '2026-01-07 00:00:00', '2026-01-07 00:00:00', 1);

-- B9: Insert Sample Hotel Booking
INSERT INTO "bookings_booking" ("booking_id", "booking_type", "status", "total_amount", "notes", "created_at", "updated_at", "user_id")
VALUES ('a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4', 'hotel', 'confirmed', 7000.00, 'Honeymoon trip', '2026-02-01 10:00:00', '2026-02-01 10:05:00', 3);

INSERT INTO "bookings_hotelbookingdetail" ("check_in_date", "check_out_date", "number_of_rooms", "number_of_guests", "price_per_night", "number_of_nights", "booking_id", "hotel_id", "room_type_id")
VALUES ('2026-03-01', '2026-03-03', 1, 2, 3500.00, 2, 1, 1, 1);

-- B10: Insert Sample Flight Booking
INSERT INTO "bookings_booking" ("booking_id", "booking_type", "status", "total_amount", "notes", "created_at", "updated_at", "user_id")
VALUES ('b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5', 'flight', 'confirmed', 2500.00, NULL, '2026-02-02 14:00:00', '2026-02-02 14:05:00', 3);

INSERT INTO "bookings_flightbookingdetail" ("number_of_passengers", "price_per_seat", "passenger_title", "passenger_first_name", "passenger_last_name", "passenger_dob", "passenger_passport", "booking_id", "flight_id")
VALUES (1, 2500.00, 'Mr', 'John', 'Doe', '1990-05-15', 'TH12345678', 2, 1);

-- B11: Insert Sample Payment
INSERT INTO "payments_payment" ("payment_id", "amount", "payment_method", "status", "transaction_id", "card_type", "card_last_four", "card_holder_name", "bank_name", "account_number", "paypal_email", "payment_date", "created_at", "updated_at", "notes", "failure_reason", "booking_id", "user_id")
VALUES ('c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6', 7000.00, 'credit_card', 'completed', 'TXN-ABC123DEF456', 'visa', '4242', 'John Doe', NULL, NULL, NULL, '2026-02-01 10:05:00', '2026-02-01 10:05:00', '2026-02-01 10:05:00', NULL, NULL, 1, 3);

-- B12: Insert Sample Receipt
INSERT INTO "payments_paymentreceipt" ("receipt_id", "generated_at", "downloaded_count", "payment_id")
VALUES ('d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1', '2026-02-01 10:06:00', 1, 1);


-- ██████████████████████████████████████████████
-- PART C: SQL QUERIES PER SCREEN/FUNCTION
-- (Numbered to match PPT presentation slides)
-- ██████████████████████████████████████████████

-- ================================================
-- CUSTOMER ROLE SCREENS
-- ================================================

-- -----------------------------------------------
-- #1: Register Screen (accounts/register.html)
-- Function: Create new user account
-- SQL Type: INSERT
-- -----------------------------------------------
-- When a customer registers, these 2 INSERTs run:

-- 1a. Insert new user
INSERT INTO "accounts_user" ("password", 
"is_superuser", "username", "first_name", 
"last_name", "is_staff", "is_active", "date_joined",
 "role", "email", "phone", "created_at", "updated_at")
VALUES ('pbkdf2_sha256$hashed_pw', FALSE, 'newcustomer', 'Jane', 'Smith', FALSE, TRUE, '2026-02-13 00:00:00', 'customer', 'jane@email.com', '0891112222', '2026-02-13 00:00:00', '2026-02-13 00:00:00');

-- 1b. Create user profile automatically
INSERT INTO "accounts_userprofile" ("profile_picture", "date_of_birth", "address", "city", "country", "user_id")
VALUES (NULL, NULL, NULL, NULL, NULL, 4);


-- -----------------------------------------------
-- #2: Login Screen (accounts/login.html)
-- Function: Authenticate user credentials
-- SQL Type: SELECT
-- -----------------------------------------------
SELECT id, username, password, role, is_active
FROM accounts_user
WHERE username = 'customer1';

-- After login, update last_login:
UPDATE accounts_user SET last_login = '2026-02-13 15:00:00' WHERE id = 3;


-- -----------------------------------------------
-- #3: Homepage (home.html)
-- Function: Display welcome page with navigation
-- SQL Type: SELECT (counts for display)
-- -----------------------------------------------
SELECT COUNT(*) as total_hotels FROM partners_hotel WHERE is_active = TRUE;
SELECT COUNT(*) as total_flights FROM partners_flight WHERE is_active = TRUE;


-- -----------------------------------------------
-- #4: Customer Dashboard (accounts/dashboard.html)
-- Function: Show customer overview and stats
-- SQL Type: SELECT
-- -----------------------------------------------
SELECT
    (SELECT COUNT(*) FROM accounts_user) as total_users,
    (SELECT COUNT(*) FROM accounts_user WHERE role = 'customer') as total_customers,
    (SELECT COUNT(*) FROM accounts_user WHERE role = 'partner') as total_partners;


-- -----------------------------------------------
-- #5: Hotel Search (bookings/hotels/search.html)
-- Function: Search hotels with city filter
-- SQL Type: SELECT with JOIN, GROUP BY
-- Uses: RAW SQL in utils/db_manager.py → HotelQueries.search_hotels()
-- -----------------------------------------------
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
    AND LOWER(h.city) LIKE LOWER('%Bangkok%')
GROUP BY h.id, h.name, h.city, h.star_rating, h.main_image
ORDER BY h.star_rating DESC, min_price ASC;


-- -----------------------------------------------
-- #6: Hotel Detail (bookings/hotels/detail.html)
-- Function: Show hotel info and available room types
-- SQL Type: SELECT with JOIN
-- Uses: RAW SQL in utils/db_manager.py → HotelQueries.get_hotel_with_rooms()
-- -----------------------------------------------
SELECT
    h.id as hotel_id,
    h.name as hotel_name,
    h.city,
    h.star_rating,
    h.description,
    h.amenities,
    h.check_in_time,
    h.check_out_time,
    rt.id as room_type_id,
    rt.name as room_type_name,
    rt.price_per_night,
    rt.max_occupancy,
    rt.rooms_available,
    rt.bed_type,
    rt.amenities as room_amenities
FROM partners_hotel h
LEFT JOIN partners_roomtype rt ON h.id = rt.hotel_id
WHERE h.id = 1
AND rt.is_active = TRUE;


-- -----------------------------------------------
-- #7: Hotel Booking Form (bookings/hotels/booking_form.html)
-- Function: Create hotel booking
-- SQL Type: INSERT + UPDATE (transaction)
-- -----------------------------------------------
-- 7a. Create main booking record
INSERT INTO "bookings_booking" ("booking_id", "booking_type", "status", "total_amount", "notes", "created_at", "updated_at", "user_id")
VALUES ('new_uuid_value', 'hotel', 'pending', 7000.00, 'Special request: high floor', '2026-02-13 15:00:00', '2026-02-13 15:00:00', 3);

-- 7b. Create hotel booking details
INSERT INTO "bookings_hotelbookingdetail" ("check_in_date", "check_out_date", "number_of_rooms", "number_of_guests", "price_per_night", "number_of_nights", "booking_id", "hotel_id", "room_type_id")
VALUES ('2026-04-01', '2026-04-03', 1, 2, 3500.00, 2, 3, 1, 1);

-- 7c. Reduce room availability
UPDATE partners_roomtype SET rooms_available = rooms_available - 1 WHERE id = 1;


-- -----------------------------------------------
-- #8: Flight Search (bookings/flights/search.html)
-- Function: Search flights with origin/destination/date filters
-- SQL Type: SELECT with WHERE filters
-- -----------------------------------------------
SELECT
    f.id,
    f.flight_number,
    f.origin,
    f.destination,
    f.departure_time,
    f.arrival_time,
    f.price,
    f.seats_available,
    f.class_type,
    f.aircraft_type,
    p.name as airline_name
FROM partners_flight f
INNER JOIN partners_partner p ON f.partner_id = p.id
WHERE f.is_active = TRUE
    AND f.departure_time >= '2026-02-13 00:00:00'
    AND LOWER(f.origin) LIKE LOWER('%Bangkok%')
    AND LOWER(f.destination) LIKE LOWER('%Chiang Mai%')
ORDER BY f.departure_time ASC;


-- -----------------------------------------------
-- #9: Flight Detail (bookings/flights/detail.html)
-- Function: Show flight details
-- SQL Type: SELECT
-- -----------------------------------------------
SELECT
    f.id,
    f.flight_number,
    f.origin,
    f.destination,
    f.departure_time,
    f.arrival_time,
    f.price,
    f.seats_available,
    f.total_seats,
    f.class_type,
    f.aircraft_type,
    p.name as partner_name
FROM partners_flight f
INNER JOIN partners_partner p ON f.partner_id = p.id
WHERE f.id = 1 AND f.is_active = TRUE;


-- -----------------------------------------------
-- #10: Flight Booking Form (bookings/flights/booking_form.html)
-- Function: Create flight booking with passenger info
-- SQL Type: INSERT + UPDATE (transaction)
-- -----------------------------------------------
-- 10a. Create main booking record
INSERT INTO "bookings_booking" ("booking_id", "booking_type", "status", "total_amount", "notes", "created_at", "updated_at", "user_id")
VALUES ('new_flight_uuid', 'flight', 'pending', 2500.00, NULL, '2026-02-13 15:30:00', '2026-02-13 15:30:00', 3);

-- 10b. Create flight booking detail with passenger info
INSERT INTO "bookings_flightbookingdetail" ("number_of_passengers", "price_per_seat", "passenger_title", "passenger_first_name", "passenger_last_name", "passenger_dob", "passenger_passport", "booking_id", "flight_id")
VALUES (1, 2500.00, 'Mr', 'John', 'Doe', '1990-05-15', 'TH12345678', 4, 1);

-- 10c. Reduce seat availability
UPDATE partners_flight SET seats_available = seats_available - 1 WHERE id = 1;


-- -----------------------------------------------
-- #11: My Bookings (bookings/my_bookings.html)
-- Function: List all bookings for current user
-- SQL Type: SELECT with JOIN (RAW SQL)
-- Uses: RAW SQL in utils/db_manager.py → BookingQueries.get_user_bookings()
-- -----------------------------------------------
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

-- Get hotel booking details (RAW SQL)
-- Uses: BookingQueries.get_hotel_booking_details()
SELECT
    hbd.id,
    hbd.check_in_date,
    hbd.check_out_date,
    hbd.number_of_rooms,
    hbd.number_of_guests,
    hbd.price_per_night,
    hbd.number_of_nights,
    h.name as hotel_name,
    h.city,
    h.star_rating,
    rt.name as room_type_name,
    rt.price_per_night as room_price
FROM bookings_hotelbookingdetail hbd
INNER JOIN partners_hotel h ON hbd.hotel_id = h.id
INNER JOIN partners_roomtype rt ON hbd.room_type_id = rt.id
WHERE hbd.booking_id = 1;


-- -----------------------------------------------
-- #12: Booking Detail (bookings/booking_detail.html)
-- Function: View single booking details
-- SQL Type: SELECT with JOIN
-- -----------------------------------------------
SELECT
    b.booking_id,
    b.booking_type,
    b.status,
    b.total_amount,
    b.notes,
    b.created_at,
    p.status as payment_status,
    p.payment_method,
    p.payment_date
FROM bookings_booking b
LEFT JOIN payments_payment p ON b.id = p.booking_id
WHERE b.booking_id = 'a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4'
AND b.user_id = 3;

-- Get flight booking details (RAW SQL)
-- Uses: BookingQueries.get_flight_booking_details()
SELECT
    fbd.id,
    fbd.number_of_passengers,
    fbd.price_per_seat,
    fbd.passenger_title,
    fbd.passenger_first_name,
    fbd.passenger_last_name,
    fbd.passenger_dob,
    fbd.passenger_passport,
    f.flight_number,
    f.origin,
    f.destination,
    f.departure_time,
    f.arrival_time,
    f.class_type,
    f.aircraft_type,
    p.name as partner_name
FROM bookings_flightbookingdetail fbd
INNER JOIN partners_flight f ON fbd.flight_id = f.id
INNER JOIN partners_partner p ON f.partner_id = p.id
WHERE fbd.booking_id = 2;


-- -----------------------------------------------
-- #13: Cancel Booking (bookings/booking_cancel.html)
-- Function: Cancel booking and restore availability
-- SQL Type: UPDATE (transaction)
-- -----------------------------------------------
-- 13a. Update booking status to cancelled
UPDATE bookings_booking SET status = 'cancelled', updated_at = '2026-02-13 16:00:00'
WHERE booking_id = 'a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4' AND user_id = 3;

-- 13b. Restore hotel room availability
UPDATE partners_roomtype
SET rooms_available = rooms_available + (
    SELECT hbd.number_of_rooms FROM bookings_hotelbookingdetail hbd
    INNER JOIN bookings_booking b ON hbd.booking_id = b.id
    WHERE b.booking_id = 'a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4'
)
WHERE id = (
    SELECT hbd.room_type_id FROM bookings_hotelbookingdetail hbd
    INNER JOIN bookings_booking b ON hbd.booking_id = b.id
    WHERE b.booking_id = 'a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4'
);

-- 13c. Restore flight seat availability (for flight bookings)
UPDATE partners_flight
SET seats_available = seats_available + (
    SELECT fbd.number_of_passengers FROM bookings_flightbookingdetail fbd
    INNER JOIN bookings_booking b ON fbd.booking_id = b.id
    WHERE b.booking_id = 'b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5'
)
WHERE id = (
    SELECT fbd.flight_id FROM bookings_flightbookingdetail fbd
    INNER JOIN bookings_booking b ON fbd.booking_id = b.id
    WHERE b.booking_id = 'b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5'
);


-- -----------------------------------------------
-- #14: Payment Form (payments/payment_form.html)
-- Function: Process payment for a booking
-- SQL Type: INSERT
-- -----------------------------------------------
INSERT INTO "payments_payment" ("payment_id", "amount", "payment_method", "status", "transaction_id", "card_type", "card_last_four", "card_holder_name", "payment_date", "created_at", "updated_at", "booking_id", "user_id")
VALUES ('new_payment_uuid', 7000.00, 'credit_card', 'pending', 'TXN-NEW123ABC', 'visa', '4242', 'John Doe', NULL, '2026-02-13 15:05:00', '2026-02-13 15:05:00', 1, 3);


-- -----------------------------------------------
-- #15: Payment Success (payments/payment_success.html)
-- Function: Mark payment as completed, confirm booking
-- SQL Type: UPDATE
-- -----------------------------------------------
-- 15a. Update payment status to completed
UPDATE payments_payment
SET status = 'completed', payment_date = '2026-02-13 15:05:00', updated_at = '2026-02-13 15:05:00'
WHERE payment_id = 'new_payment_uuid';

-- 15b. Update booking status to confirmed
UPDATE bookings_booking
SET status = 'confirmed', updated_at = '2026-02-13 15:05:00'
WHERE id = (SELECT booking_id FROM payments_payment WHERE payment_id = 'new_payment_uuid');


-- -----------------------------------------------
-- #16: Payment History (payments/payment_history.html)
-- Function: View all payments for current user
-- SQL Type: SELECT with JOIN and filters
-- -----------------------------------------------
SELECT
    p.payment_id,
    p.amount,
    p.payment_method,
    p.status,
    p.payment_date,
    p.card_type,
    p.card_last_four,
    b.booking_id,
    b.booking_type,
    b.status as booking_status
FROM payments_payment p
INNER JOIN bookings_booking b ON p.booking_id = b.id
WHERE p.user_id = 3
ORDER BY p.created_at DESC;

-- With status filter:
SELECT * FROM payments_payment WHERE user_id = 3 AND status = 'completed' ORDER BY created_at DESC;

-- With payment method filter:
SELECT * FROM payments_payment WHERE user_id = 3 AND payment_method = 'credit_card' ORDER BY created_at DESC;


-- -----------------------------------------------
-- #17: Payment Receipt (payments/receipt.html)
-- Function: Generate and display payment receipt
-- SQL Type: SELECT + INSERT/UPDATE
-- -----------------------------------------------
-- 17a. Get payment details for receipt
SELECT
    p.payment_id,
    p.amount,
    p.payment_method,
    p.status,
    p.transaction_id,
    p.payment_date,
    p.card_type,
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
WHERE p.payment_id = 'c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6'
AND p.user_id = 3;

-- 17b. Create or get receipt (PostgreSQL upsert)
INSERT INTO "payments_paymentreceipt" ("receipt_id", "generated_at", "downloaded_count", "payment_id")
VALUES ('new_receipt_uuid', '2026-02-13 15:10:00', 0, 1)
ON CONFLICT ("payment_id") DO NOTHING;

-- 17c. Increment download count
UPDATE payments_paymentreceipt SET downloaded_count = downloaded_count + 1 WHERE payment_id = 1;


-- -----------------------------------------------
-- #18: Refund Request (payments/refund_request.html)
-- Function: Process refund for completed payment
-- SQL Type: UPDATE (transaction)
-- -----------------------------------------------
-- 18a. Update payment status to refunded
UPDATE payments_payment
SET status = 'refunded', notes = 'Refund requested: Changed travel plans', updated_at = '2026-02-13 16:00:00'
WHERE payment_id = 'c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6' AND status = 'completed';

-- 18b. Cancel the associated booking
UPDATE bookings_booking SET status = 'cancelled', updated_at = '2026-02-13 16:00:00'
WHERE id = (SELECT booking_id FROM payments_payment WHERE payment_id = 'c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6');

-- 18c. Restore hotel room availability (for hotel bookings)
UPDATE partners_roomtype
SET rooms_available = rooms_available + 1
WHERE id = (
    SELECT hbd.room_type_id FROM bookings_hotelbookingdetail hbd
    WHERE hbd.booking_id = (SELECT booking_id FROM payments_payment WHERE payment_id = 'c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6')
);


-- -----------------------------------------------
-- #19: User Profile (accounts/profile.html)
-- Function: View and update user profile
-- SQL Type: SELECT + UPDATE
-- Role: All users
-- -----------------------------------------------
-- 19a. Get user with profile
SELECT
    u.id, u.username, u.email, u.first_name, u.last_name, u.phone, u.role,
    up.profile_picture, up.date_of_birth, up.address, up.city, up.country
FROM accounts_user u
LEFT JOIN accounts_userprofile up ON u.id = up.user_id
WHERE u.id = 3;

-- 19b. Update user info
UPDATE accounts_user SET first_name = 'John', last_name = 'Doe', email = 'john.updated@email.com', phone = '0899999999'
WHERE id = 3;

-- 19c. Update user profile
UPDATE accounts_userprofile SET date_of_birth = '1990-05-15', address = '456 New Street', city = 'Bangkok', country = 'Thailand'
WHERE user_id = 3;


-- ================================================
-- PARTNER ROLE SCREENS
-- ================================================

-- -----------------------------------------------
-- #20: Partner Dashboard (partners/dashboard.html)
-- Function: Partner overview with statistics
-- SQL Type: SELECT with aggregation
-- -----------------------------------------------
SELECT
    p.name as partner_name,
    p.partner_type,
    p.is_verified,
    (SELECT COUNT(*) FROM partners_hotel h WHERE h.partner_id = p.id) as total_hotels,
    (SELECT COUNT(*) FROM partners_flight f WHERE f.partner_id = p.id) as total_flights,
    (SELECT COUNT(*) FROM bookings_booking b
     INNER JOIN bookings_hotelbookingdetail hbd ON b.id = hbd.booking_id
     INNER JOIN partners_hotel h ON hbd.hotel_id = h.id
     WHERE h.partner_id = p.id) as hotel_bookings,
    (SELECT COUNT(*) FROM bookings_booking b
     INNER JOIN bookings_flightbookingdetail fbd ON b.id = fbd.booking_id
     INNER JOIN partners_flight f ON fbd.flight_id = f.id
     WHERE f.partner_id = p.id) as flight_bookings
FROM partners_partner p
WHERE p.user_id = 2;


-- -----------------------------------------------
-- #21: Partner Profile (partners/profile.html)
-- Function: View and edit partner profile
-- SQL Type: SELECT + UPDATE
-- -----------------------------------------------
-- 21a. Get partner profile
SELECT p.id, p.name, p.partner_type, p.description, p.logo, p.website, p.contact_email, p.contact_phone, p.is_verified
FROM partners_partner p WHERE p.user_id = 2;

-- 21b. Update partner profile
UPDATE partners_partner
SET name = 'Grand Hotels Group Updated', description = 'Updated description', website = 'https://updated.com', contact_phone = '0891111111'
WHERE user_id = 2;


-- -----------------------------------------------
-- #22: Hotel List (partners/hotels/list.html)
-- Function: List all hotels for current partner
-- SQL Type: SELECT
-- -----------------------------------------------
SELECT h.id, h.name, h.city, h.star_rating, h.is_active, h.created_at,
    (SELECT COUNT(*) FROM partners_roomtype rt WHERE rt.hotel_id = h.id) as room_type_count
FROM partners_hotel h
INNER JOIN partners_partner p ON h.partner_id = p.id
WHERE p.user_id = 2
ORDER BY h.created_at DESC;


-- -----------------------------------------------
-- #23: Create Hotel (partners/hotels/form.html)
-- Function: Add a new hotel
-- SQL Type: INSERT
-- -----------------------------------------------
INSERT INTO "partners_hotel" ("name", "city", "address", "description", "star_rating", "main_image", "amenities", "check_in_time", "check_out_time", "email", "phone", "is_active", "created_at", "updated_at", "partner_id")
VALUES ('Riverside Resort', 'Phuket', '123 Beach Road', 'Beautiful beachfront resort', 4, NULL, 'Pool, Beach Access, Spa', '15:00:00', '11:00:00', 'info@riverside.com', '076123456', TRUE, '2026-02-13 15:00:00', '2026-02-13 15:00:00', 1);


-- -----------------------------------------------
-- #24: Edit Hotel (partners/hotels/form.html)
-- Function: Update hotel details
-- SQL Type: UPDATE
-- -----------------------------------------------
UPDATE partners_hotel
SET name = 'Grand Palace Hotel Premium', star_rating = 5, description = 'Updated luxury hotel', amenities = 'WiFi, Pool, Spa, Gym, Restaurant, Rooftop Bar', updated_at = '2026-02-13 16:00:00'
WHERE id = 1 AND partner_id = 1;


-- -----------------------------------------------
-- #25: Delete Hotel (partners/hotels/delete.html)
-- Function: Remove a hotel
-- SQL Type: DELETE
-- -----------------------------------------------
DELETE FROM partners_hotel WHERE id = 2 AND partner_id = 1;


-- -----------------------------------------------
-- #26: Room Type List (partners/rooms/list.html)
-- Function: List room types for a specific hotel
-- SQL Type: SELECT
-- -----------------------------------------------
SELECT rt.id, rt.name, rt.price_per_night, rt.max_occupancy, rt.rooms_available, rt.bed_type, rt.is_active
FROM partners_roomtype rt
INNER JOIN partners_hotel h ON rt.hotel_id = h.id
INNER JOIN partners_partner p ON h.partner_id = p.id
WHERE h.id = 1 AND p.user_id = 2
ORDER BY rt.price_per_night ASC;


-- -----------------------------------------------
-- #27: Create Room Type (partners/rooms/form.html)
-- Function: Add a new room type to a hotel
-- SQL Type: INSERT
-- -----------------------------------------------
INSERT INTO "partners_roomtype" ("name", "description", "price_per_night", "max_occupancy", "rooms_available", "room_size", "bed_type", "amenities", "image", "is_active", "created_at", "updated_at", "hotel_id")
VALUES ('Family Room', 'Perfect for families with children', 5000.00, 4, 8, 50.00, 'Twin', 'WiFi, TV, Minibar, Crib available', NULL, TRUE, '2026-02-13 15:00:00', '2026-02-13 15:00:00', 1);


-- -----------------------------------------------
-- #28: Edit Room Type (partners/rooms/form.html)
-- Function: Update room type details
-- SQL Type: UPDATE
-- -----------------------------------------------
UPDATE partners_roomtype
SET name = 'Deluxe Room Premium', price_per_night = 4000.00, rooms_available = 12, amenities = 'WiFi, TV, Minibar, Room Service', updated_at = '2026-02-13 16:00:00'
WHERE id = 1 AND hotel_id = 1;


-- -----------------------------------------------
-- #29: Delete Room Type (partners/rooms/delete.html)
-- Function: Remove a room type
-- SQL Type: DELETE
-- -----------------------------------------------
DELETE FROM partners_roomtype WHERE id = 3 AND hotel_id = 1;


-- -----------------------------------------------
-- #30: Flight List (partners/flights/list.html)
-- Function: List all flights for current partner
-- SQL Type: SELECT
-- -----------------------------------------------
SELECT f.id, f.flight_number, f.origin, f.destination, f.departure_time, f.arrival_time, f.price, f.seats_available, f.total_seats, f.class_type, f.is_active
FROM partners_flight f
INNER JOIN partners_partner p ON f.partner_id = p.id
WHERE p.user_id = 2
ORDER BY f.departure_time ASC;


-- -----------------------------------------------
-- #31: Create Flight (partners/flights/form.html)
-- Function: Add a new flight
-- SQL Type: INSERT
-- -----------------------------------------------
INSERT INTO "partners_flight" ("flight_number", "origin", "destination", "departure_time", "arrival_time", "price", "seats_available", "total_seats", "aircraft_type", "airline_logo", "class_type", "is_active", "created_at", "updated_at", "partner_id")
VALUES ('TG202', 'Bangkok', 'Phuket', '2026-03-20 10:00:00', '2026-03-20 11:30:00', 3200.00, 160, 160, 'Airbus A320', NULL, 'Economy', TRUE, '2026-02-13 15:00:00', '2026-02-13 15:00:00', 1);


-- -----------------------------------------------
-- #32: Edit Flight (partners/flights/form.html)
-- Function: Update flight details
-- SQL Type: UPDATE
-- -----------------------------------------------
UPDATE partners_flight
SET price = 2800.00, seats_available = 145, class_type = 'Economy', updated_at = '2026-02-13 16:00:00'
WHERE id = 1 AND partner_id = 1;


-- -----------------------------------------------
-- #33: Delete Flight (partners/flights/delete.html)
-- Function: Remove a flight
-- SQL Type: DELETE
-- -----------------------------------------------
DELETE FROM partners_flight WHERE id = 2 AND partner_id = 1;


-- ================================================
-- ADMIN ROLE SCREENS
-- ================================================

-- -----------------------------------------------
-- #34: Admin Dashboard (admin/dashboard.html)
-- Function: System-wide statistics and overview
-- SQL Type: SELECT with aggregation (multiple queries)
-- -----------------------------------------------
-- 34a. User statistics
SELECT
    COUNT(*) as total_users,
    SUM(CASE WHEN role = 'customer' THEN 1 ELSE 0 END) as customers,
    SUM(CASE WHEN role = 'partner' THEN 1 ELSE 0 END) as partners,
    SUM(CASE WHEN role = 'admin' THEN 1 ELSE 0 END) as admins,
    SUM(CASE WHEN created_at >= CURRENT_DATE - INTERVAL '30 days' THEN 1 ELSE 0 END) as new_users_this_month
FROM accounts_user;

-- 34b. Partner statistics
SELECT
    COUNT(*) as total_partners,
    SUM(CASE WHEN is_verified = TRUE THEN 1 ELSE 0 END) as verified_partners
FROM partners_partner;

SELECT COUNT(*) as total_hotels, SUM(CASE WHEN is_active = TRUE THEN 1 ELSE 0 END) as active_hotels FROM partners_hotel;
SELECT COUNT(*) as total_flights, SUM(CASE WHEN is_active = TRUE THEN 1 ELSE 0 END) as active_flights FROM partners_flight;

-- 34c. Booking statistics
SELECT
    COUNT(*) as total_bookings,
    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending_bookings,
    SUM(CASE WHEN status = 'confirmed' THEN 1 ELSE 0 END) as confirmed_bookings,
    SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) as cancelled_bookings,
    SUM(CASE WHEN created_at >= CURRENT_DATE - INTERVAL '7 days' THEN 1 ELSE 0 END) as bookings_this_week,
    SUM(CASE WHEN created_at >= CURRENT_DATE - INTERVAL '30 days' THEN 1 ELSE 0 END) as bookings_this_month
FROM bookings_booking;

-- 34d. Revenue statistics
SELECT
    COALESCE(SUM(total_amount), 0) as total_revenue
FROM bookings_booking
WHERE status IN ('confirmed', 'completed');

SELECT
    COALESCE(SUM(total_amount), 0) as revenue_this_month
FROM bookings_booking
WHERE status IN ('confirmed', 'completed') AND created_at >= CURRENT_DATE - INTERVAL '30 days';

SELECT COALESCE(AVG(total_amount), 0) as avg_booking_value FROM bookings_booking;

-- 34e. Recent bookings
SELECT b.booking_id, b.booking_type, b.status, b.total_amount, b.created_at, u.username
FROM bookings_booking b
INNER JOIN accounts_user u ON b.user_id = u.id
ORDER BY b.created_at DESC LIMIT 10;

-- 34f. Top customers
SELECT u.username, u.email,
    COUNT(b.id) as booking_count,
    COALESCE(SUM(b.total_amount), 0) as total_spent
FROM accounts_user u
LEFT JOIN bookings_booking b ON u.id = b.user_id
WHERE u.role = 'customer'
GROUP BY u.id, u.username, u.email
ORDER BY total_spent DESC LIMIT 5;


-- -----------------------------------------------
-- #35: Payment Statistics (payments/statistics.html)
-- Function: Admin payment analytics dashboard
-- SQL Type: SELECT with aggregation
-- -----------------------------------------------
-- 35a. Overall payment statistics (last 30 days)
SELECT
    COUNT(*) as payment_count,
    COALESCE(SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END), 0) as total_revenue,
    COALESCE(SUM(CASE WHEN status = 'refunded' THEN amount ELSE 0 END), 0) as total_refunded,
    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_count,
    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed_count,
    SUM(CASE WHEN status = 'refunded' THEN 1 ELSE 0 END) as refunded_count
FROM payments_payment
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days';

-- 35b. Payments by method
SELECT payment_method, COUNT(*) as count, COALESCE(SUM(amount), 0) as total
FROM payments_payment
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY payment_method ORDER BY total DESC;

-- 35c. Payments by status
SELECT status, COUNT(*) as count, COALESCE(SUM(amount), 0) as total
FROM payments_payment
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY status;

-- 35d. Recent payments with details
SELECT p.payment_id, p.amount, p.payment_method, p.status, p.payment_date, u.username, b.booking_id, b.booking_type
FROM payments_payment p
INNER JOIN accounts_user u ON p.user_id = u.id
INNER JOIN bookings_booking b ON p.booking_id = b.id
ORDER BY p.created_at DESC LIMIT 10;


-- ================================================
-- BONUS: REPORTING QUERIES (from utils/db_manager.py)
-- ================================================

-- -----------------------------------------------
-- R1: Monthly Revenue Report
-- Uses: RAW SQL in utils/db_manager.py → ReportQueries.get_revenue_by_month()
-- -----------------------------------------------
SELECT
    TO_CHAR(created_at, 'YYYY-MM') as month,
    booking_type,
    COUNT(*) as booking_count,
    SUM(total_amount) as total_revenue
FROM bookings_booking
WHERE status IN ('confirmed', 'completed')
AND created_at >= DATE_TRUNC('year', CURRENT_DATE)
GROUP BY TO_CHAR(created_at, 'YYYY-MM'), booking_type
ORDER BY month DESC;


-- -----------------------------------------------
-- R2: Top Performing Hotels
-- Uses: RAW SQL in utils/db_manager.py → ReportQueries.get_top_hotels()
-- -----------------------------------------------
SELECT
    h.id, h.name, h.city,
    COUNT(b.id) as booking_count,
    SUM(b.total_amount) as revenue
FROM partners_hotel h
INNER JOIN partners_roomtype rt ON h.id = rt.hotel_id
INNER JOIN bookings_hotelbookingdetail hbd ON rt.id = hbd.room_type_id
INNER JOIN bookings_booking b ON hbd.booking_id = b.id
WHERE b.status IN ('confirmed', 'completed')
GROUP BY h.id, h.name, h.city
ORDER BY revenue DESC LIMIT 10;


-- -----------------------------------------------
-- R3: Customer Analytics
-- Uses: RAW SQL in utils/db_manager.py → ReportQueries.get_customer_analytics()
-- -----------------------------------------------
SELECT
    u.id, u.username, u.email,
    COUNT(b.id) as total_bookings,
    SUM(b.total_amount) as total_spent,
    AVG(b.total_amount) as avg_booking_value,
    MAX(b.created_at) as last_booking_date
FROM accounts_user u
INNER JOIN bookings_booking b ON u.id = b.user_id
WHERE u.role = 'customer'
GROUP BY u.id, u.username, u.email
ORDER BY total_spent DESC LIMIT 20;


-- -----------------------------------------------
-- R4: Available Rooms with Date Overlap Check
-- Uses: RAW SQL in utils/db_manager.py → BookingQueries.get_available_rooms()
-- -----------------------------------------------
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
    ) as actually_available
FROM partners_roomtype rt
WHERE rt.hotel_id = 1 AND rt.is_active = TRUE;


-- -----------------------------------------------
-- R5: Hotel Statistics
-- Uses: RAW SQL in utils/db_manager.py → HotelQueries.get_hotel_statistics()
-- -----------------------------------------------
SELECT
    h.name, h.city,
    COUNT(DISTINCT rt.id) as total_room_types,
    SUM(rt.rooms_available) as total_rooms,
    COUNT(DISTINCT b.id) as total_bookings,
    COALESCE(SUM(b.total_amount), 0) as total_revenue
FROM partners_hotel h
LEFT JOIN partners_roomtype rt ON h.id = rt.hotel_id
LEFT JOIN bookings_hotelbookingdetail hbd ON rt.id = hbd.room_type_id
LEFT JOIN bookings_booking b ON hbd.booking_id = b.id AND b.status = 'confirmed'
WHERE h.id = 1
GROUP BY h.id, h.name, h.city;


-- ==============================================
-- END OF SQL SCRIPT
-- ==============================================
