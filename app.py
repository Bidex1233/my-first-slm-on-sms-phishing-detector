import re
import joblib
import numpy as np
import streamlit as st
from scipy.sparse import hstack

st.set_page_config(page_title='SMS Phishing Detector', layout='centered')

@st.cache_resource
def load_bundle():
    return joblib.load('sms_phishing_detector.joblib')

bundle = load_bundle()
model = bundle['model']
vectorizer = bundle['vectorizer']
threshold = bundle.get('threshold', 0.35)

def extract_rich_features(messages):
    text_vec = vectorizer.transform(messages)
    meta_rows = []
    for msg in messages:
        m = msg.lower()
        has_url = 1 if re.search(r'(https?://|www\.|\b[a-z0-9-]+\.(com|net|org|ng|co|io|ly|do)\b)', m) else 0
        has_email = 1 if re.search(r'[\w\.-]+@[\w\.-]+\.\w+', m) else 0
        has_phone = 1 if re.search(r'(\+?\d[\d\s-]{7,}\d)', m) else 0
        asks_secret = 1 if re.search(r'\b(pin|otp|cvv|bvn|nin|password|passcode|login|card details|card number|3 digits|verification code|6 digit|code)\b', m) else 0
        asks_action = 1 if re.search(r'\b(send|reply|forward|read me|give|enter|confirm|verify|click|pay|transfer)\b', m) else 0
        urgency_lure = 1 if re.search(r'\b(blocked|suspended|deactivated|expired|urgent|urgently|immediately|grant|giveaway|double|free|winner|claim|fee)\b', m) else 0
        meta_rows.append([has_url, has_email, has_phone, asks_secret, asks_action, urgency_lure])
    return hstack([text_vec, np.array(meta_rows, dtype=float)])

st.title('SMS Phishing & Smishing Detector')
st.write('Paste any SMS or WhatsApp message below to check for scam or phishing risk.')

user_msg = st.text_area('Message text:', height=130)

if st.button('Analyze Message'):
    if not user_msg.strip():
        st.warning('Please enter a message first.')
    else:
        features = extract_rich_features([user_msg])
        probs = model.predict_proba(features)[0]
        classes = list(model.classes_)
        ham_prob = probs[classes.index('ham')]
        scam_risk = 1.0 - ham_prob
        if scam_risk >= threshold:
            st.error(f'SCAM / PHISHING DETECTED (Risk: {scam_risk:.1%})')
        else:
            st.success(f'LOOKS SAFE (Risk: {scam_risk:.1%})')