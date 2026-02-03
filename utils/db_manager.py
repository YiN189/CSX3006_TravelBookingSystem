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
            WHERE hbd.booking_id = %s
        """
        result = DatabaseManager.execute_query(query, [booking_id])
        return result[0] if result else None
    
    @staticmethod
    def get_flight_booking_details(booking_id):
        """
        Get flight booking details with passenger info (stored in FlightBookingDetail)
        """
        query = """
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
            WHERE fbd.booking_id = %s
        """
        result = DatabaseManager.execute_query(query, [booking_id])
        return result[0] if result else None
    
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
            AND rt.is_active = 1
        """
        return DatabaseManager.execute_query(query, [check_out, check_in, hotel_id])


class HotelQueries:
    """
    All hotel-related SQL queries
    """
    
    @staticmethod
    def search_hotels(city=None, min_price=None, max_price=None):
        """
        Search hotels with filters (SQLite compatible)
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
            WHERE h.is_active = 1
        """
        params = []
        
        if city:
            # SQLite: Use LIKE with LOWER() for case-insensitive search
            query += " AND LOWER(h.city) LIKE LOWER(%s)"
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
    def get_hotel_with_rooms(hotel_id):
        """
        Get hotel with all room types
        """
        query = """
            SELECT 
                h.id as hotel_id,
                h.name as hotel_name,
                h.city,
                h.star_rating,
                rt.id as room_type_id,
                rt.name as room_type_name,
                rt.price_per_night,
                rt.max_occupancy,
                rt.rooms_available
            FROM partners_hotel h
            LEFT JOIN partners_roomtype rt ON h.id = rt.hotel_id
            WHERE h.id = %s
            AND rt.is_active = 1
        """
        return DatabaseManager.execute_query(query, [hotel_id])
    
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
    Reporting and analytics queries (SQLite compatible)
    """
    
    @staticmethod
    def get_revenue_by_month():
        """
        Get monthly revenue report (SQLite compatible)
        """
        query = """
            SELECT 
                strftime('%Y-%m', created_at) as month,
                booking_type,
                COUNT(*) as booking_count,
                SUM(total_amount) as total_revenue
            FROM bookings_booking
            WHERE status IN ('confirmed', 'completed')
            AND created_at >= date('now', 'start of year')
            GROUP BY strftime('%Y-%m', created_at), booking_type
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
