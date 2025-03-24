from flask import Flask, render_template, redirect, url_for, request, flash, send_file
import os
import requests
import redis
from forms import LoginForm, UploadForm, ConfigForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Redis connection
redis_client = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)

# Pre-load config settings into Redis if not set
default_settings = {
    "error_message": "Oops! Something went wrong. Ups! Hier funktionert etwas nicht!",
    "initial_greeting": "Um den Chatbot nutzen zu können, müssen Sie bitte unserer Datenschutzerklärung zustimmen. \n\n To proceed, please agree to our chatbot's privacy policy.",
    "inactivity_timer": "60",
    "English_llm_models_training_list": "gemma3, gemma3:1b, deepseek-r1:1.5b, deepseek-r1:7b, llama3.2:1b, llama3.2:3b",
    "Deutsch_llm_models_training_list": "gemma3, gemma3:1b, deepseek-r1:1.5b, deepseek-r1:7b, llama3.2:1b, llama3.2:3b",
    "English_llm_models_training_instruction": "Read the text below, which could serve as an answer to various questions...",
    "Deutsch_llm_models_training_instruction": "Lies den folgenden Text, der als Antwort auf verschiedene Fragen dienen könnte. Bitte formuliere fünf bis zehn plausible Fragen..."
}

for key, value in default_settings.items():
    if not redis_client.get(key):
        redis_client.set(key, value)

@app.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = os.getenv('MEDIAWIKI_ADMIN')
        password = os.getenv('MEDIAWIKI_ADMIN_PASSWORD')

        if form.username.data == username and form.password.data == password:
            return redirect(url_for('admin_panel'))
        else:
            flash("Invalid credentials. Please try again.", "danger")

    return render_template("login.html", form=form)

@app.route("/admin", methods=["GET", "POST"])
def admin_panel():
    form = UploadForm()
    config_form = ConfigForm()

    # Load config from Redis
    config_data = {key: redis_client.get(key) for key in config_form.fields.keys()}

    if request.method == "POST":
        if "train" in request.form:
            response = requests.get("http://api/admin/build_intent_classifier/")
            flash(f"Intent Classifier Training Response: {response.text}", "info")

        elif "generate" in request.form:
            response = requests.get("http://api/llm/llm_training_data/")
            flash(f"Intent Classifier Training Response: {response.text}", "info")

        elif "export" in request.form:
            response = requests.get("http://api/admin/export/")
            with open("export.json", "wb") as f:
                f.write(response.content)
            return send_file("export.json", as_attachment=True)
        

        elif "update_config" in request.form:
            for field in config_form.fields.keys():
                value = request.form.get(field)
                redis_client.set(field, value)
            flash("Configuration updated successfully!", "success")
            return redirect(url_for('admin_panel'))

        elif form.validate_on_submit():
            file = form.file.data
            files = {'file': (file.filename, file.stream, 'multipart/form-data')}
            response = requests.post("http://api/admin/import/", files=files)
            flash(f"Import Response: {response.text}", "success")

    return render_template("admin.html", form=form, config_form=config_form, config_data=config_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
