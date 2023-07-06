from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL configuration
mysql_host = 'localhost'
mysql_user = 'your_mysql_username'
mysql_password = 'your_mysql_password'
mysql_database = 'your_mysql_database'


def connect_to_mysql():
    """Establishes a connection to MySQL and returns the connection object."""
    conn = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )
    return conn


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/save_volume', methods=['POST'])
def save_volume():
    volume_values = request.form.getlist('volume')

    # Save volume values to MySQL
    conn = connect_to_mysql()
    cursor = conn.cursor()
    for i, volume in enumerate(volume_values, start=1):
        query = "INSERT INTO audio_volumes (audio_id, volume) VALUES (%s, %s)"
        values = (i, volume)
        cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

    return 'Volume values saved successfully.'


if __name__ == '__main__':
    app.run()
