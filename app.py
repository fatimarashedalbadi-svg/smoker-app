from flask import Flask, render_template, request
import pickle
import numpy as np
app = Flask(__name__)
# Load model + scaler
model = pickle.load(open("smoker_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get inputs
        age = float(request.form["age"])
        sex = request.form["sex"]
        bmi = float(request.form["bmi"])
        children = float(request.form["children"])
        region = request.form["region"]
        charges = float(request.form["charges"])
        # Encoding 
        sex_map = {"male": 0, "female": 1}
        region_map = {
            "southwest": 0,
            "southeast": 1,
            "northwest": 2,
            "northeast": 3
        }
        sex = sex_map[sex]
        region = region_map[region]
        features = np.array([[age, sex, bmi, children, region, charges]])
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]
        result = "Smoker" if prediction == 1 else "Non-Smoker"
        return render_template("index.html", prediction_text=result)

    except Exception as e:
        return render_template("index.html", prediction_text=f"Error: {str(e)}")
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)