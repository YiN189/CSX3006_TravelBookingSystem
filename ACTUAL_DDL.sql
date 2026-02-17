-- ==============================================
-- Travel Booking System - Actual Django DDL
-- Generated from Django Migrations
-- Database: PostgreSQL
-- ==============================================

-- ACCOUNTS APP
BEGIN;
--
-- Create model User
--
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


--
-- Create model UserProfile
--
CREATE TABLE "accounts_userprofile" (
    "id" BIGSERIAL PRIMARY KEY,
    "bio" TEXT NULL,
    "profile_picture" VARCHAR(100) NULL,
    "date_of_birth" DATE NULL,
    "address" TEXT NULL,
    "city" VARCHAR(100) NULL,
    "country" VARCHAR(100) NULL,
    "postal_code" VARCHAR(20) NULL,
    "user_id" BIGINT NOT NULL UNIQUE REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED
);

COMMIT;

-- PARTNERS APP
BEGIN;
--
-- Create model Partner
--
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

--
-- Create model Hotel
--
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

--
-- Create model Flight
--
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

--
-- Create model RoomType
--
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

CREATE INDEX "partners_hotel_partner_id_7ecd2582" ON "partners_hotel" ("partner_id");
CREATE INDEX "partners_flight_partner_id_65127e6b" ON "partners_flight" ("partner_id");
CREATE INDEX "partners_roomtype_hotel_id_d13ecb70" ON "partners_roomtype" ("hotel_id");
COMMIT;

-- BOOKINGS APP
BEGIN;
--
-- Create model Booking
--
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

--
-- Create model FlightBookingDetail
--
CREATE TABLE "bookings_flightbookingdetail" (
    "id" BIGSERIAL PRIMARY KEY,
    "number_of_passengers" INTEGER NOT NULL,
    "price_per_seat" DECIMAL NOT NULL,
    "booking_id" BIGINT NOT NULL UNIQUE REFERENCES "bookings_booking" ("id") DEFERRABLE INITIALLY DEFERRED,
    "flight_id" BIGINT NOT NULL REFERENCES "partners_flight" ("id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create model HotelBookingDetail
--
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

--
-- Create model Passenger
--
CREATE TABLE "bookings_passenger" (
    "id" BIGSERIAL PRIMARY KEY,
    "title" VARCHAR(10) NOT NULL,
    "first_name" VARCHAR(100) NOT NULL,
    "last_name" VARCHAR(100) NOT NULL,
    "date_of_birth" DATE NOT NULL,
    "passport_number" VARCHAR(50) NULL,
    "flight_booking_id" BIGINT NOT NULL REFERENCES "bookings_flightbookingdetail" ("id") DEFERRABLE INITIALLY DEFERRED
);

CREATE INDEX "bookings_booking_user_id_834dfc23" ON "bookings_booking" ("user_id");
CREATE INDEX "bookings_flightbookingdetail_flight_id_afa79097" ON "bookings_flightbookingdetail" ("flight_id");
CREATE INDEX "bookings_hotelbookingdetail_hotel_id_bc54dfd3" ON "bookings_hotelbookingdetail" ("hotel_id");
CREATE INDEX "bookings_hotelbookingdetail_room_type_id_7996c5ab" ON "bookings_hotelbookingdetail" ("room_type_id");
CREATE INDEX "bookings_passenger_flight_booking_id_4504ab1a" ON "bookings_passenger" ("flight_booking_id");
COMMIT;

-- PAYMENTS APP
BEGIN;
--
-- Create model Payment
--
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

--
-- Create model PaymentReceipt
--
CREATE TABLE "payments_paymentreceipt" (
    "id" BIGSERIAL PRIMARY KEY,
    "receipt_id" CHAR(32) NOT NULL UNIQUE,
    "generated_at" TIMESTAMP NOT NULL,
    "downloaded_count" INTEGER NOT NULL,
    "payment_id" BIGINT NOT NULL UNIQUE REFERENCES "payments_payment" ("id") DEFERRABLE INITIALLY DEFERRED
);

--
-- Create index payments_pa_created_3147e3_idx on field(s) -created_at of model payment
--
CREATE INDEX "payments_pa_created_3147e3_idx" ON "payments_payment" ("created_at" DESC);
--
-- Create index payments_pa_status_7ad4af_idx on field(s) status of model payment
--
CREATE INDEX "payments_pa_status_7ad4af_idx" ON "payments_payment" ("status");
--
-- Create index payments_pa_payment_5c92d7_idx on field(s) payment_method of model payment
--
CREATE INDEX "payments_pa_payment_5c92d7_idx" ON "payments_payment" ("payment_method");
CREATE INDEX "payments_payment_user_id_f9db060a" ON "payments_payment" ("user_id");
COMMIT;
