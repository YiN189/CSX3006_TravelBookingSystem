-- =====================================================
-- Travel Booking System - SQL DDL
-- Based on ER Diagram (11 Tables)
-- Database: PostgreSQL
-- =====================================================

-- =====================================================
-- 1. USER (Strong Entity)
-- =====================================================
CREATE TABLE accounts_user (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL UNIQUE,
    phone VARCHAR(15),
    role VARCHAR(20) NOT NULL DEFAULT 'customer' CHECK (role IN ('customer', 'partner', 'admin')),
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    date_joined TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 2. USER_PROFILE (Weak Entity - depends on USER)
-- =====================================================
CREATE TABLE accounts_userprofile (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE,
    profile_picture VARCHAR(100),
    date_of_birth DATE,
    address TEXT,
    city VARCHAR(100),
    country VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES accounts_user(id) ON DELETE CASCADE
);

-- =====================================================
-- 3. PARTNER 
-- =====================================================
CREATE TABLE partners_partner (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    partner_type VARCHAR(20) NOT NULL DEFAULT 'both' CHECK (partner_type IN ('hotel', 'flight', 'both')),
    description TEXT,
    logo VARCHAR(100),
    website VARCHAR(200),
    contact_email VARCHAR(254) NOT NULL,
    contact_phone VARCHAR(15),
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES accounts_user(id) ON DELETE CASCADE
);

-- =====================================================
-- 4. HOTEL (Strong Entity)
-- =====================================================
CREATE TABLE partners_hotel (
    id BIGSERIAL PRIMARY KEY,
    partner_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    description TEXT,
    star_rating INTEGER NOT NULL DEFAULT 3 CHECK (star_rating >= 1 AND star_rating <= 5),
    main_image VARCHAR(100),
    amenities TEXT,
    check_in_time TIME NOT NULL DEFAULT '14:00:00',
    check_out_time TIME NOT NULL DEFAULT '12:00:00',
    email VARCHAR(254),
    phone VARCHAR(15),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (partner_id) REFERENCES partners_partner(id) ON DELETE CASCADE
);

-- =====================================================
-- 5. ROOM_TYPE (Strong Entity)
-- =====================================================
CREATE TABLE partners_roomtype (
    id BIGSERIAL PRIMARY KEY,
    hotel_id BIGINT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price_per_night DECIMAL(10, 2) NOT NULL CHECK (price_per_night >= 0),
    max_occupancy INTEGER NOT NULL DEFAULT 2 CHECK (max_occupancy >= 1),
    rooms_available INTEGER NOT NULL DEFAULT 10 CHECK (rooms_available >= 0),
    room_size DECIMAL(6, 2),
    bed_type VARCHAR(100),
    amenities TEXT,
    image VARCHAR(100),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hotel_id) REFERENCES partners_hotel(id) ON DELETE CASCADE
);

-- =====================================================
-- 6. FLIGHT (Strong Entity)
-- =====================================================
CREATE TABLE partners_flight (
    id BIGSERIAL PRIMARY KEY,
    partner_id BIGINT NOT NULL,
    flight_number VARCHAR(20) NOT NULL UNIQUE,
    origin VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    departure_time TIMESTAMP NOT NULL,
    arrival_time TIMESTAMP NOT NULL,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    seats_available INTEGER NOT NULL DEFAULT 150 CHECK (seats_available >= 0),
    total_seats INTEGER NOT NULL DEFAULT 150 CHECK (total_seats >= 1),
    aircraft_type VARCHAR(100),
    airline_logo VARCHAR(100),
    class_type VARCHAR(50) NOT NULL DEFAULT 'Economy',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (partner_id) REFERENCES partners_partner(id) ON DELETE CASCADE
);

-- =====================================================
-- 7. BOOKING (Strong Entity)
-- =====================================================
CREATE TABLE bookings_booking (
    id BIGSERIAL PRIMARY KEY,
    booking_id VARCHAR(36) NOT NULL UNIQUE,  -- UUID stored as string
    user_id BIGINT NOT NULL,
    booking_type VARCHAR(20) NOT NULL CHECK (booking_type IN ('hotel', 'flight')),
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'cancelled', 'completed')),
    total_amount DECIMAL(10, 2) NOT NULL CHECK (total_amount >= 0),
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES accounts_user(id) ON DELETE CASCADE
);

-- =====================================================
-- 8. HOTEL_BOOKING_DETAIL (Weak Entity - depends on BOOKING)
-- =====================================================
CREATE TABLE bookings_hotelbookingdetail (
    id BIGSERIAL PRIMARY KEY,
    booking_id BIGINT NOT NULL UNIQUE,
    hotel_id BIGINT NOT NULL,
    room_type_id BIGINT NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    number_of_rooms INTEGER NOT NULL DEFAULT 1 CHECK (number_of_rooms >= 1),
    number_of_guests INTEGER NOT NULL DEFAULT 1 CHECK (number_of_guests >= 1),
    price_per_night DECIMAL(10, 2) NOT NULL,
    number_of_nights INTEGER NOT NULL CHECK (number_of_nights >= 1),
    FOREIGN KEY (booking_id) REFERENCES bookings_booking(id) ON DELETE CASCADE,
    FOREIGN KEY (hotel_id) REFERENCES partners_hotel(id) ON DELETE CASCADE,
    FOREIGN KEY (room_type_id) REFERENCES partners_roomtype(id) ON DELETE CASCADE
);

-- =====================================================
-- 9. FLIGHT_BOOKING_DETAIL (Weak Entity - depends on BOOKING)
-- =====================================================
CREATE TABLE bookings_flightbookingdetail (
    id BIGSERIAL PRIMARY KEY,
    booking_id BIGINT NOT NULL UNIQUE,
    flight_id BIGINT NOT NULL,
    number_of_passengers INTEGER NOT NULL DEFAULT 1 CHECK (number_of_passengers >= 1),
    price_per_seat DECIMAL(10, 2) NOT NULL,
    passenger_title VARCHAR(10) NOT NULL DEFAULT 'Mr' CHECK (passenger_title IN ('Mr', 'Mrs', 'Ms', 'Dr')),
    passenger_first_name VARCHAR(100),
    passenger_last_name VARCHAR(100),
    passenger_dob DATE,
    passenger_passport VARCHAR(50),
    FOREIGN KEY (booking_id) REFERENCES bookings_booking(id) ON DELETE CASCADE,
    FOREIGN KEY (flight_id) REFERENCES partners_flight(id) ON DELETE CASCADE
);

-- =====================================================
-- 10. PAYMENT (Weak Entity - depends on BOOKING)
-- =====================================================
CREATE TABLE payments_payment (
    id BIGSERIAL PRIMARY KEY,
    payment_id VARCHAR(36) NOT NULL UNIQUE,  -- UUID stored as string
    booking_id BIGINT NOT NULL UNIQUE,
    user_id BIGINT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(20) NOT NULL CHECK (payment_method IN ('credit_card', 'debit_card', 'bank_transfer', 'paypal', 'cash')),
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'failed', 'refunded')),
    transaction_id VARCHAR(100) UNIQUE,
    card_type VARCHAR(20) CHECK (card_type IN ('visa', 'mastercard', 'amex', 'discover', 'other')),
    card_last_four VARCHAR(4),
    card_holder_name VARCHAR(100),
    bank_name VARCHAR(100),
    account_number VARCHAR(50),
    paypal_email VARCHAR(254),
    payment_date TIMESTAMP,
    notes TEXT,
    failure_reason TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings_booking(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES accounts_user(id) ON DELETE CASCADE
);

-- =====================================================
-- 11. PAYMENT_RECEIPT (Weak Entity - depends on PAYMENT)
-- =====================================================
CREATE TABLE payments_paymentreceipt (
    id BIGSERIAL PRIMARY KEY,
    receipt_id VARCHAR(36) NOT NULL UNIQUE,  -- UUID stored as string
    payment_id BIGINT NOT NULL UNIQUE,
    generated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    downloaded_count INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (payment_id) REFERENCES payments_payment(id) ON DELETE CASCADE
);

-- =====================================================
-- INDEXES (for better query performance)
-- =====================================================
CREATE INDEX idx_user_email ON accounts_user(email);
CREATE INDEX idx_user_role ON accounts_user(role);
CREATE INDEX idx_booking_user ON bookings_booking(user_id);
CREATE INDEX idx_booking_status ON bookings_booking(status);
CREATE INDEX idx_booking_type ON bookings_booking(booking_type);
CREATE INDEX idx_payment_status ON payments_payment(status);
CREATE INDEX idx_payment_method ON payments_payment(payment_method);
CREATE INDEX idx_hotel_city ON partners_hotel(city);
CREATE INDEX idx_flight_origin ON partners_flight(origin);
CREATE INDEX idx_flight_destination ON partners_flight(destination);
CREATE INDEX idx_flight_departure ON partners_flight(departure_time);
