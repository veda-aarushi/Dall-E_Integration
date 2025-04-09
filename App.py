# Import necessary libraries
import openai
import os  # for creating directories and file paths
import requests  # to download images from a URL
from flask import Flask, request, render_template, redirect, url_for  # Flask web framework
from dotenv import load_dotenv  # to load API key from .env

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create a Flask web app instance
app = Flask(__name__)

# Directory where images will be stored (inside /static so they are publicly accessible)
IMAGE_DIR = "static/images"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)  # Create the folder if it doesn't exist

# List to keep track of image filenames for the gallery
gallery = []

# Route for the main page ("/"), handling both GET and POST requests
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the prompt input from the form and add a UW theme prefix
        theme = "UW-themed "  # you can try other themes too
        prompt = request.form.get("prompt")
        prompt = theme + prompt

        if prompt:
            # Call DALL·E API
            response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="1024x1024"
            )

            # Get the image URL
            image_url = response.data[0].url

            # Download the image
            image_response = requests.get(image_url)

            # Save the image if download was successful
            if image_response.status_code == 200:
                filename = f"{prompt[:10].replace(' ', '')}{len(gallery)}.png"
                filepath = os.path.join(IMAGE_DIR, filename)

                with open(filepath, "wb") as f:
                    f.write(image_response.content)

                gallery.append(filename)
                return redirect(url_for("index"))

    return render_template("index.html", images=gallery)

# Run the app in debug mode if this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)
