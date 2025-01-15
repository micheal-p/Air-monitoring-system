from flask import Flask, request, jsonify
import requests
import sqlite3

app = Flask(__name__)

API_KEY = 'ab521e27ff857459416de82f16664698'

# Map Nigerian states to their major cities and their coordinates
STATE_TO_CITY_COORDINATES = {
    "Abia": {"city": "Umuahia", "lat": 5.5320, "lon": 7.4860},
    "Adamawa": {"city": "Yola", "lat": 9.2035, "lon": 12.4954},
    "Akwa Ibom": {"city": "Uyo", "lat": 5.0377, "lon": 7.9128},
    "Anambra": {"city": "Awka", "lat": 6.2100, "lon": 7.0700},
    "Bauchi": {"city": "Bauchi", "lat": 10.3103, "lon": 9.8439},
    "Bayelsa": {"city": "Yenagoa", "lat": 4.9267, "lon": 6.2674},
    "Benue": {"city": "Makurdi", "lat": 7.7337, "lon": 8.5214},
    "Borno": {"city": "Maiduguri", "lat": 11.8371, "lon": 13.1423},
    "Cross River": {"city": "Calabar", "lat": 4.9589, "lon": 8.3269},
    "Delta": {"city": "Asaba", "lat": 6.1981, "lon": 6.7316},
    "Ebonyi": {"city": "Abakaliki", "lat": 6.3249, "lon": 8.1137},
    "Edo": {"city": "Benin City", "lat": 6.3373, "lon": 5.6302},
    "Ekiti": {"city": "Ado Ekiti", "lat": 7.6211, "lon": 5.2214},
    "Enugu": {"city": "Enugu", "lat": 6.5244, "lon": 7.5189},
    "Gombe": {"city": "Gombe", "lat": 10.2897, "lon": 11.1673},
    "Imo": {"city": "Owerri", "lat": 5.4850, "lon": 7.0355},
    "Jigawa": {"city": "Dutse", "lat": 11.7583, "lon": 9.3382},
    "Kaduna": {"city": "Kaduna", "lat": 10.5092, "lon": 7.4323},
    "Kano": {"city": "Kano", "lat": 12.0022, "lon": 8.5919},
    "Katsina": {"city": "Katsina", "lat": 12.9895, "lon": 7.6006},
    "Kebbi": {"city": "Birnin Kebbi", "lat": 12.4539, "lon": 4.1973},
    "Kogi": {"city": "Lokoja", "lat": 7.8023, "lon": 6.7333},
    "Kwara": {"city": "Ilorin", "lat": 8.4966, "lon": 4.5421},
    "Lagos": {"city": "Lagos", "lat": 6.5244, "lon": 3.3792},
    "Nasarawa": {"city": "Lafia", "lat": 8.4923, "lon": 8.5157},
    "Niger": {"city": "Minna", "lat": 9.6130, "lon": 6.5569},
    "Ogun": {"city": "Abeokuta", "lat": 7.1557, "lon": 3.3488},
    "Ondo": {"city": "Akure", "lat": 7.2526, "lon": 5.1931},
    "Osun": {"city": "Osogbo", "lat": 7.7820, "lon": 4.5560},
    "Oyo": {"city": "Ibadan", "lat": 7.3775, "lon": 3.9470},
    "Plateau": {"city": "Jos", "lat": 9.8965, "lon": 8.8583},
    "Rivers": {"city": "Port Harcourt", "lat": 4.8156, "lon": 7.0498},
    "Sokoto": {"city": "Sokoto", "lat": 13.0059, "lon": 5.2476},
    "Taraba": {"city": "Jalingo", "lat": 8.8892, "lon": 11.3600},
    "Yobe": {"city": "Damaturu", "lat": 11.7480, "lon": 11.9639},
    "Zamfara": {"city": "Gusau", "lat": 12.1700, "lon": 6.6641},
    "FCT": {"city": "Abuja", "lat": 9.0765, "lon": 7.3986}

}

# Initialize the database
def init_db():
    conn = sqlite3.connect('air_quality.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS air_quality (
            id INTEGER PRIMARY KEY,
            state TEXT,
            city TEXT,
            aqi INTEGER,
            pm2_5 REAL,
            pm10 REAL,
            co REAL,
            no2 REAL,
            o3 REAL,
            so2 REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Save data to SQLite database
def save_to_db(state, city, data):
    try:
        conn = sqlite3.connect('air_quality.db')
        cursor = conn.cursor()
        
        components = data['list'][0]['components']
        main = data['list'][0]['main']

        cursor.execute('''
            INSERT INTO air_quality (state, city, aqi, pm2_5, pm10, co, no2, o3, so2)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (state, city, main['aqi'], components['pm2_5'], components['pm10'],
              components['co'], components['no2'], components['o3'], components['so2']))

        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

@app.route('/api/air-quality', methods=['GET'])
def get_air_quality():
    state = request.args.get('state')
    if not state:
        return jsonify({'error': 'State parameter is required'}), 400

    state_data = STATE_TO_CITY_COORDINATES.get(state.title())
    if not state_data:
        return jsonify({'error': 'State not found'}), 404

    city = state_data["city"]
    latitude = state_data["lat"]
    longitude = state_data["lon"]

    # Fetch air quality data for the state's city
    url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        save_to_db(state, city, data)
        
        # Prepare detailed data to return
        components = data['list'][0]['components']
        main = data['list'][0]['main']
        detailed_data = {
            "state": state,
            "city": city,
            "aqi": main['aqi'],
            "pm2_5": components['pm2_5'],
            "pm10": components['pm10'],
            "co": components['co'],
            "no2": components['no2'],
            "o3": components['o3'],
            "so2": components['so2'],
            "timestamp": data['list'][0]['dt']
        }
        return jsonify(detailed_data)
    else:
        return jsonify({'error': f'Failed to fetch air quality data. Status code: {response.status_code}'}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)