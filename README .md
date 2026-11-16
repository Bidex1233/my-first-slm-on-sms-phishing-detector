# SMS Phishing & Smishing Detector (Multi-Class NLP)

An end-to-end Machine Learning NLP classifier and interactive Streamlit web app built to detect SMS Phishing (Smishing), Spam, and Legitimate (Ham) messages—specifically engineered to catch Nigerian banking and social-engineering scams.

## Problem & Motivation
Standard SMS spam classifiers achieve >98% accuracy on Western datasets by relying heavily on literal URLs and phone numbers. However, on real-world conversational scams (BVN/ATM PIN requests, fake bank alerts, and OTP-forwarding traps without links), baseline models miss over 80% of threats.

## Methodology & Data Split
- **Training & Validation (Dataset_10191, 10,191 messages):** Split 75% Training / 25% Validation, stratified across ham, smishing, and spam.
- **Unseen Real-World Test Set (60 custom messages):** 30 realistic scam messages (Nigerian banking, NIN/BVN, and OTP social-engineering lures) + 30 legitimate messages. Kept strictly isolated from training and feature tuning.

## Results Progression
- **Baseline TF-IDF + URL/Phone Flags:** 53.33% Real-World Test Accuracy (17% Scam Recall)
- **Behavioral Feature Engineering + Threshold Tuning:** 81.67% Real-World Test Accuracy (73% Scam Recall, 88% Scam Precision)

## How to Run Locally
1. Install dependencies: `pip install -r requirements.txt`
2. Run the web app: `streamlit run app.py`
