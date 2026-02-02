# utils/db_manager.py

from django.db import connection

class DatabaseManager:
    """
    Custom database manager for raw SQL queries
    """
    
    @staticmethod
    def execute_query(query, params=None):
        """
        Execute a SELECT query and return results
        """
        with connection.cursor() as cursor:
            cursor.execute(query, params or [])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    @staticmethod
    def execute_insert(query, params=None):
        """
        Execute INSERT query
        """
        with connection.cursor() as cursor:
            cursor.execute(query, params or [])
            return cursor.lastrowid
    
    @staticmethod
    def execute_update(query, params=None):
        """
        Execute UPDATE/DELETE query
        """
        with connection.cursor() as cursor:
            cursor.execute(query, params or [])
            return cursor.rowcount


# Example Queries
class BookingQueries:
    """
    All booking-related SQL queries
    """
    
    @staticmethod
    def get_user_bookings(user_id):
        """
        Get all bookings for a user with details
        """
        query = """
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
            WHERE u.id = %s
            ORDER BY b.created_at DESC
        """
        return DatabaseManager.execute_query(query, [user_id])
    
    @staticmethod
    def get_hotel_booking_details(booking_id):
        """
        Get hotel booking details with hotel and room info
        """
        query = """
            SELECT 
                hbd.*,
                h.name as hotel_name,
                h.city,
                rt.name as room_type_name,
                rt.price_per_night
            FROM bookings_hotelbookingdetail hbd
            INNER JOIN partners_hotel h ON hbd.hotel_id = h.id
            INNER JOIN partners_roomtype rt ON hbd.room_type_id = rt.id
            WHERE hbd.booking_id = %s
        """
        result = DatabaseManager.execute_query(query, [booking_id])
        return result[0] if result else None
    
    @staticmethod
    def get_flight_booking_details(booking_id):
        """
        Get flight booking details with flight info
        """
        query = """
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
                f.aircraft_type,
                p.name as partner_name
            FROM bookings_flightbookingdetail fbd
            INNER JOIN partners_flight f ON fbd.flight_id = f.id
            INNER JOIN partners_partner p ON f.partner_id = p.id
            WHERE fbd.booking_id = %s
        """
        result = DatabaseManager.execute_query(query, [booking_id])
        return result[0] if result else None
    
    @staticmethod
    def get_passengers_for_booking(flight_booking_id):
        """
        Get all passengers for a flight booking
        """
        query = """
            SELECT 
                p.id,
                p.title,
                p.first_name,
                p.last_name,
                p.date_of_birth,
                p.passport_number,
                CONCAT(p.title, ' ', p.first_name, ' ', p.last_name) as full_name
            FROM bookings_passenger p
            WHERE p.flight_booking_id = %s
            ORDER BY p.id
        """
        return DatabaseManager.execute_query(query, [flight_booking_id])
    
    @staticmethod
    def get_flight_booking_with_passengers(booking_id):
        """
        Get complete flight booking with all passengers (using JOIN)
        """
        query = """
            SELECT 
                b.booking_id,
                b.status,
                b.total_amount,
                b.created_at,
                f.flight_number,
                f.origin,
                f.destination,
                f.departure_time,
                f.arrival_time,
                fbd.number_of_passengers,
                fbd.price_per_seat,
                p.title as passenger_title,
                p.first_name as passenger_first_name,
                p.last_name as passenger_last_name,
                p.date_of_birth as passenger_dob,
                p.passport_number as passenger_passport
            FROM bookings_booking b
            INNER JOIN bookings_flightbookingdetail fbd ON b.id = fbd.booking_id
            INNER JOIN partners_flight f ON fbd.flight_id = f.id
            LEFT JOIN bookings_passenger p ON fbd.id = p.flight_booking_id
            WHERE b.booking_id = %s
            ORDER BY p.id
        """
        return DatabaseManager.execute_query(query, [booking_id])

    
    @staticmethod
    def get_available_rooms(hotel_id, check_in, check_out):
        """
        Get available rooms for a hotel on specific dates
        """
        query = """
            SELECT 
                rt.id,
                rt.name,
                rt.price_per_night,
                rt.max_occupancy,
                rt.rooms_available,
                rt.rooms_available - COALESCE(
                    (SELECT SUM(hbd.number_of_rooms)
                     FROM bookings_hotelbookingdetail hbd
                     INNER JOIN bookings_booking b ON hbd.booking_id = b.id
                     WHERE hbd.room_type_id = rt.id
                     AND b.status IN ('pending', 'confirmed')
                     AND hbd.check_in_date < %s
                     AND hbd.check_out_date > %s), 0
                ) as actually_available
            FROM partners_roomtype rt
            WHERE rt.hotel_id = %s
            AND rt.is_active = TRUE
            HAVING actually_available > 0
        """
        return DatabaseManager.execute_query(query, [check_out, check_in, hotel_id])
    
    @staticmethod
    def create_booking(user_id, booking_type, total_amount):
        """
        Create a new booking using raw SQL
        """
        query = """
            INSERT INTO bookings_booking 
            (booking_id, user_id, booking_type, status, total_amount, created_at, updated_at)
            VALUES (uuid_generate_v4(), %s, %s, 'pending', %s, NOW(), NOW())
            RETURNING id, booking_id
        """
        result = DatabaseManager.execute_query(query, [user_id, booking_type, total_amount])
        return result[0] if result else None


class HotelQueries:
    """
    All hotel-related SQL queries
    """
    
    @staticmethod
    def search_hotels(city=None, min_price=None, max_price=None):
        """
        Search hotels with filters
        """
        query = """
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
        """
        params = []
        
        if city:
            query += " AND h.city ILIKE %s"
            params.append(f'%{city}%')
        
        if min_price:
            query += " AND rt.price_per_night >= %s"
            params.append(min_price)
        
        if max_price:
            query += " AND rt.price_per_night <= %s"
            params.append(max_price)
        
        query += """
            GROUP BY h.id, h.name, h.city, h.star_rating, h.main_image
            ORDER BY h.star_rating DESC, min_price ASC
        """
        
        return DatabaseManager.execute_query(query, params)
    
    @staticmethod
    def get_hotel_statistics(hotel_id):
        """
        Get statistics for a specific hotel
        """
        query = """
            SELECT 
                h.name,
                h.city,
                COUNT(DISTINCT rt.id) as total_room_types,
                SUM(rt.rooms_available) as total_rooms,
                COUNT(DISTINCT b.id) as total_bookings,
                COALESCE(SUM(b.total_amount), 0) as total_revenue
            FROM partners_hotel h
            LEFT JOIN partners_roomtype rt ON h.id = rt.hotel_id
            LEFT JOIN bookings_hotelbookingdetail hbd ON rt.id = hbd.room_type_id
            LEFT JOIN bookings_booking b ON hbd.booking_id = b.id AND b.status = 'confirmed'
            WHERE h.id = %s
            GROUP BY h.id, h.name, h.city
        """
        result = DatabaseManager.execute_query(query, [hotel_id])
        return result[0] if result else None


class ReportQueries:
    """
    Reporting and analytics queries
    """
    
    @staticmethod
    def get_revenue_by_month():
        """
        Get monthly revenue report
        """
        query = """
            SELECT 
                DATE_TRUNC('month', created_at) as month,
                booking_type,
                COUNT(*) as booking_count,
                SUM(total_amount) as total_revenue
            FROM bookings_booking
            WHERE status IN ('confirmed', 'completed')
            AND created_at >= DATE_TRUNC('year', CURRENT_DATE)
            GROUP BY DATE_TRUNC('month', created_at), booking_type
            ORDER BY month DESC
        """
        return DatabaseManager.execute_query(query)
    
    @staticmethod
    def get_top_hotels():
        """
        Get top performing hotels
        """
        query = """
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
            LIMIT 10
        """
        return DatabaseManager.execute_query(query)
    
    @staticmethod
    def get_customer_analytics():
        """
        Get customer behavior analytics
        """
        query = """
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
            LIMIT 20
        """
        return DatabaseManager.execute_query(query)
