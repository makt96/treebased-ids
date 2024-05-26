# Live Network Monitoring Dashboard

This is a live network monitoring dashboard that uses Flask and Socket.IO for real-time data updates, and Chart.js for data visualization.

## Features

- Real-time network monitoring
- Various types of charts to visualize data
- Notification alerts for suspicious activities

## Prerequisites

- Python 3.x
- Make (optional, but recommended for easy setup)

## Setup and Run

### Using Make

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. Run the setup and start the server:
    ```sh
    make
    ```

### Without Make

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. Set up a virtual environment and install dependencies:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Run the Flask server:
    ```sh
    FLASK_APP=app.py flask run
    ```

## Usage

Once the server is running, open your web browser and navigate to `http://127.0.0.1:5000` to view the live network monitoring dashboard.

## License

This project is licensed under the MIT License.

