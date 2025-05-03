
````markdown
# Happy Hour App

A Flask application for crowdsourcing and displaying local restaurant happy-hour information. Users can submit URLs, admins can approve/reject, and approved listings are scraped and displayed publicly.

Quick Start

Prerequisites
Python 3.11.x installed and on your `PATH`  
SQLite (optional, for inspecting the database)  

1. Clone the Repository
```bash
git clone https://github.com/your-org/happy-hour-app.git
cd happy-hour-app
````

### 2. Create & Activate a Virtual Environment

```bash
python3.11 -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows (PowerShell)
# venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configuration

1. Copy the example environment file:

   ```bash
   cp .env.example .env
   ```
2. Open `.env` and set at minimum:

   ```dotenv
   SECRET_KEY=your-secret-key
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=password
   ```

   > **Note:** Email settings can remain blank if you’re stubbing out mail.

### 5. Initialize the Database

```bash
python create_tables.py
```

This will create the `pending_urls` and `restaurants` tables in `happy_hour.db`.

### 6. Configure Flask Environment

```bash
export FLASK_APP=main.py
export FLASK_ENV=development

# Windows (PowerShell):
# $Env:FLASK_APP = "main.py"
# $Env:FLASK_ENV = "development"
```

### 7. Run the Development Server

```bash
flask run
```

You should see:

```
 * Serving Flask app "main.py"
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/
```

---

## 🔍 Verify Endpoints

1. **Home / Listings**
   Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
   – Should show “No restaurants to display yet.”

2. **Submit URL**
   Visit [http://127.0.0.1:5000/submit-url](http://127.0.0.1:5000/submit-url)
   – Fill out the form → “Submission received and pending approval.”

3. **Admin Login**
   Visit [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login)
   – Use the credentials from your `.env` (`ADMIN_USERNAME` / `ADMIN_PASSWORD`).

4. **Admin Dashboard**
   Visit [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin)
   – You should see pending submissions with Approve/Reject buttons.
   – Approving a submission scrapes it and adds it to the public listing.

After approving, revisit **Home** (`/`) to see the newly added restaurant.

---

## Common Errors

* **Forgot to run `create_tables.py`** → “no such table” errors
* **Missing or mis-configured `.env`** → KeyErrors on login or app config
* **TemplateNotFound** → Ensure your `templates/` directory at project root contains:
  `base.html`, `submit_form.html`, `login.html`, `admin.html`, `restaurants.html`
* **Static files 404** → Verify your CSS files live in `static/` at project root, or adjust `static_folder` in `create_app()`

---

## Next Steps

* Secure environment variables for production
* Remove mail stubs and configure real SMTP settings
* Add unit tests (e.g. with `pytest`) and CI configuration
* Consider Dockerizing or adding a `runtime.txt` for Heroku

---

