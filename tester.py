import pickle
import string

# Load trained brain and dictionary
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def clean_text(text):
    text = text.lower()
    text = "".join([ch for ch in text if ch not in string.punctuation])
    return text

while True:
    msg = input("\nEnter an email/message (or type quit): ")

    if msg.lower() == "quit":
        break

    msg = clean_text(msg)
    msg_vec = vectorizer.transform([msg])

    prediction = model.predict(msg_vec)

    if prediction[0] == 1:
        print("🚨 This looks like SCAM/SPAM")
    else:
        print("✅ This looks like REAL email")



