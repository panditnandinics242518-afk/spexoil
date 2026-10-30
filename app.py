
import os
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv


# Load environment variables from the .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "change-this-secret"
)


# --------------------------------------------------
# MongoDB Connection
# --------------------------------------------------

enquiries = None

mongo_uri = os.getenv("MONGO_URI", "").strip()
database_name = os.getenv("MONGO_DB", "spexoil_website")

if mongo_uri:
    try:
        client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=3000
        )

        # Check whether MongoDB is reachable
        client.admin.command("ping")

        # Select the database and enquiries collection
        enquiries = client[database_name]["enquiries"]

        print("MongoDB connected successfully.")

    except PyMongoError as error:
        print("MongoDB connection error:", error)


# --------------------------------------------------
# Company Information
# --------------------------------------------------

COMPANY = {
    "name": "SILVERSTREAM LUBRICANTS PVT. LTD.",
    "brand": "SPEXOIL",
    "email": "silverstreamlubricants@gmail.com",
    "phone": "+91 80802 26123",
    "whatsapp": "918080226123",

    "factory": (
        "Plot No. 407, Sector-1, K.S.E.Z, Kandla, "
        "Gandhidham (Kutch), Gujarat, India - 370230"
    ),

    "office": (
        "Shop No. 214, 2nd Floor, Milan Mall, Near Milan Subway, "
        "Santacruz West, Maharashtra, India - 400054"
    )
}


# --------------------------------------------------
# Product Categories
# --------------------------------------------------

CATEGORIES = [
    (
        "Automotive Oils",
        "automotive-oils",
        "Engine oils, gear oils, hydraulic oils and automotive fluids",
        "https://www.spexoil.com/uploads/admin/product/ge-20w50_1725964624.png"
    ),
    (
        "Industrial Oils",
        "industrial-oils",
        "Industrial lubricant products for specialised applications",
        "https://www.spexoil.com/uploads/admin/product/transformer-oils_1725964345.png"
    ),
    (
        "Grease",
        "grease",
        "Grease range for industrial lubrication requirements",
        "https://www.spexoil.com/uploads/admin/product/industrial-specialty-grease_1725966116.png"
    ),
    (
        "Other Industrial Products",
        "other-industrial-products",
        "Coolant, brake fluid, fork oil and other products",
        "https://www.spexoil.com/uploads/admin/product/gear-oil-ep-140_1725965036.png"
    ),
    (
        "Base Oil",
        "base-oil",
        "Base oil for lubricant manufacturing applications",
        "https://www.spexoil.com/uploads/admin/product/transformer-oils_1725964345.png"
    )
]


# --------------------------------------------------
# Automotive Product List
# --------------------------------------------------

AUTO_PRODUCTS = [
    "4T 20W40 (SN GRADE) - Engine Oil",
    "TURBO 4T 20W40 (SL GRADE) - Engine Oil",
    "GEAR OIL 80W90",
    "GEAR OIL 85W140",
    "PREMIUM MG 20W40 - Engine Oil",
    "GE 20W50 - Engine Oil",
    "5W30 API SN/CJ",
    "CI4+ 15W40",
    "CF 4 15W40",
    "CH 4 15W40",
    "Active 4T 10W30",
    "GOLD 2T - Engine Oil",
    "GEAR OIL EP 90",
    "GEAR OIL EP 140",
    "Hydraulic Oil - 22/32/46/68/100/150/220/320/460",
    "Hydraulic Oil Plus - 22/32/46/68/100",
    "Coolant",
    "Brake Fluid DOT 3 / DOT 4",
    "Transmissions ATF TQ",
    "Fork Oil"
]


# --------------------------------------------------
# Share Common Data with All Templates
# --------------------------------------------------

@app.context_processor
def inject():
    return {
        "company": COMPANY,
        "categories": CATEGORIES
    }


# --------------------------------------------------
# Home Page
# --------------------------------------------------

@app.route("/")
def home():
    return render_template(
        "index.html",
        title="Home"
    )


# --------------------------------------------------
# About Page
# --------------------------------------------------

@app.route("/about")
def about():
    return render_template(
        "about.html",
        title="About Us"
    )


# --------------------------------------------------
# Products Page
# --------------------------------------------------

@app.route("/products")
def products():
    return render_template(
        "products.html",
        title="Products",
        auto_products=AUTO_PRODUCTS
    )


# --------------------------------------------------
# Factory Page
# --------------------------------------------------

@app.route("/factory")
def factory():
    return render_template(
        "factory.html",
        title="Our Factory"
    )


# --------------------------------------------------
# Values Page
# --------------------------------------------------

@app.route("/values")
def values():
    return render_template(
        "values.html",
        title="Our Values"
    )


# --------------------------------------------------
# Investor Page
# --------------------------------------------------

@app.route("/investor")
def investor():
    return render_template(
        "investor.html",
        title="Investor"
    )


# --------------------------------------------------
# Certificates Page
# --------------------------------------------------

@app.route("/certificates")
def certificates():
    return render_template(
        "certificates.html",
        title="Certificates"
    )


# --------------------------------------------------
# Contact Page and Enquiry Form
# --------------------------------------------------

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        # Collect and clean the submitted form data
        data = {
            field: request.form.get(field, "").strip()
            for field in (
                "name",
                "phone",
                "email",
                "subject",
                "message"
            )
        }

        # Record the enquiry submission time in UTC
        data["created_at"] = datetime.utcnow()

        # Check that all required fields are filled in
        required_fields = (
            "name",
            "phone",
            "email",
            "message"
        )

        if not all(data[field] for field in required_fields):
            flash(
                "Please fill in all required fields.",
                "error"
            )

        # Check the MongoDB connection
        elif enquiries is None:
            flash(
                "MongoDB is not connected yet. Please check "
                "your .env file and Atlas settings.",
                "error"
            )

        else:
            try:
                # Save the enquiry in MongoDB
                enquiries.insert_one(data)

                flash(
                    "Thank you! Your enquiry has been submitted.",
                    "success"
                )

                # Redirect to prevent accidental form resubmission
                return redirect(url_for("contact"))

            except PyMongoError:
                flash(
                    "Could not save your enquiry right now. "
                    "Please try again later.",
                    "error"
                )

    return render_template(
        "contact.html",
        title="Contact Us"
    )


# --------------------------------------------------
# Run the Flask Application
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
