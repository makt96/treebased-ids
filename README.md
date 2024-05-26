# Live Network Monitoring Dashboard with Intrusion Detection System

This project is a live network monitoring dashboard that leverages tree-based machine learning algorithms to detect intrusions in real-time. The system uses Flask and Socket.IO for real-time data updates, and Chart.js for data visualization. The dashboard provides various charts to visualize network data and sends notifications for suspicious activities.

## Introduction

The proposed Intrusion Detection System (IDS) utilizes tree-based ML algorithms including decision tree (DT), random forest (RF), extra trees (ET), and Extreme Gradient Boosting (XGBoost). The results from the implementation of the proposed IDS on standard datasets indicate that the system can identify various cyber-attacks in communication networks. Furthermore, the proposed ensemble learning and feature selection approaches enable the system to achieve a high detection rate and low computational cost simultaneously.

## Features

- Real-time network monitoring
- Various types of charts to visualize data
- Notification alerts for suspicious activities
- Utilizes advanced machine learning algorithms for intrusion detection

## Prerequisites

- Python 3.x
- Make (optional, but recommended for easy setup)

## Setup and Run

### Using Make

1. **Clone the repository:**
    ```sh
    git clone https://github.com/makt96/treebased-ids.git
    cd treebased-ids
    ```

2. **Run the setup and start the server:**
    ```sh
    make
    ```

### Without Make

1. **Clone the repository:**
    ```sh
    git clone https://github.com/makt96/treebased-ids.git
    cd treebased-ids
    ```

2. **Set up a virtual environment and install dependencies:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Run the Flask server:**
    ```sh
    FLASK_APP=app.py flask run
    ```

## Usage

Once the server is running, open your web browser and navigate to `http://127.0.0.1:5000` to view the live network monitoring dashboard.

## Directory Structure

```plaintext
treebased-ids/
├── app.py
├── requirements.txt
├── Makefile
├── README.md
├── static/
│   ├── css/
│   │   ├── index.css
│   │   ├── live.css
│   │   └── style.css
│   ├── images/
│   └── js/
│       └── live.js
├── templates/
│   ├── index.html
│   ├── live.html
│   └── results.html
├── uploads/
│   └── 2013-12-09-Whitehole-EK-traffic.pcap
├── .gitignore
├── analyze_traffic.py
├── analyze.py
├── debug.log
├── features.py
├── live_analysis.py
├── live_features.py
├── main.py
├── stk_model.pkl






## Additional Information

The machine learning models used in this project include:

- **Decision Tree (DT):** A non-parametric supervised learning method used for classification and regression.
- **Random Forest (RF):** An ensemble learning method that constructs multiple decision trees during training and outputs the mode of the classes for classification.
- **Extra Trees (ET):** Similar to Random Forest, but with more randomization, leading to a reduction in variance.
- **Extreme Gradient Boosting (XGBoost):** An optimized distributed gradient boosting library designed to be highly efficient, flexible, and portable.

## Further Development

### Potential Enhancements

- **Integration with More Data Sources:** Expanding the system to support more data sources for a comprehensive analysis.
- **Improved Visualization:** Adding more advanced visualizations and interactive charts to enhance data interpretation.
- **Enhanced ML Models:** Experimenting with more sophisticated machine learning models and feature selection techniques to improve detection accuracy.
- **Scalability:** Optimizing the system for better performance and scalability to handle larger datasets and more concurrent users.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. We welcome improvements, bug fixes, and new features.

## License

This project is licensed under the MIT License.

## Contact

For any inquiries or issues, please open an issue on the GitHub repository or contact the project maintainer at makt.cse@gmail.com.
