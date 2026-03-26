Scam / Spam Detection Using Machine Learning

Overview
This project detects scam or spam messages using Machine Learning.
It uses TF-IDF for text feature extraction and Logistic Regression for classification.
A Flask web application allows users to test messages in real time.
All predictions are stored in an SQLite database and can be exported as CSV.

Technologies Used
- Python
- TF-IDF Vectorization
- Logistic Regression
- Flask
- SQLite
- HTML & CSS

How to Run
1. Install dependencies:
   pip install -r requirements.txt

2. Train the model:
   python trainer.py

3. Start the web app:
   python app.py

Open the browser at:
http://127.0.0.1:5000

Features
- Scam / Safe prediction with confidence
- Clean web interface
- History logging using SQLite
- Export results as CSV

Note
This is a student project for educational purposes.
Predictions are probabilistic and may not be 100% accurate.

