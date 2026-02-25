from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_db_connection

app = Flask(__name__)

# ✅ Proper CORS setup for Vercel frontend
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://gst-billing-frontend.vercel.app"]
    }
}, supports_credentials=True)


@app.route("/api/bookings", methods=["POST"])
def save_booking():
    data = request.json

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO bookings
            (name, email, mobile, transport, passengers, days, total_amount, payment_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            data["name"],
            data["email"],
            data["mobile"],
            data["transport"],
            data["passengers"],
            data["days"],
            data["totalAmount"],
            "SUCCESS"
        ))

        conn.commit()

        return jsonify({"success": True}), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

    finally:
        try:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        except:
            pass


# ❌ IMPORTANT:
# Do NOT use app.run() for Railway production
# Railway uses gunicorn automatically