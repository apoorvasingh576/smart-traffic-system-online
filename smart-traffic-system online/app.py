from flask import Flask, render_template, request
from vehicle_detection import count_vehicles
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def home():

    vehicles = 0
    density = ""
    green_time = 0
    alert = ""
    image_uploaded = False

    if request.method == "POST":

        file = request.files["image"]

        if file:

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                file.filename
            )

            file.save(filepath)

            vehicles = count_vehicles(filepath)

            if vehicles <= 15:
                density = "Low"
                green_time = 15

            elif vehicles <= 25:
                density = "Medium"
                green_time = 30

            else:
                density = "High"
                green_time = 45

            if density == "High":
                alert = "🚨 Heavy Traffic Detected"

            elif density == "Medium":
                alert = "⚠️ Moderate Traffic"

            else:
                alert = "✅ Traffic Flow Normal"

            image_uploaded = True

    return render_template(
        "index.html",
        vehicles=vehicles,
        density=density,
        green_time=green_time,
        alert=alert,
        image_uploaded=image_uploaded
    )

if __name__ == "__main__":
    app.run(debug=True)