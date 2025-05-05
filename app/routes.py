from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from .db_manager import (
    insert_pending, get_pending, get_pending_by_id,
    set_pending_status, get_all_restaurants, insert_restaurant
)
from .scraper import HappyHourScraper
from .extractor import HappyHourExtractor
from .email_utils import send_approval_email, send_rejection_email


def register_routes(app):
    # Public routes
    @app.route('/')
    def home():
        restaurants = get_all_restaurants()
        return render_template('restaurants.html', restaurants=restaurants)

    @app.route('/submit-url', methods=['GET', 'POST'])
    def submit_url():
        if request.method == 'POST':
            name = request.form['name']
            url = request.form['url']
            email = request.form['email']
            comments = request.form.get('comments', '')
            insert_pending(name, url, email, comments)
            flash('Submission received and pending approval.', 'info')
            return redirect(url_for('submit_url'))
        return render_template('submit_form.html')

    # Admin routes
    @app.route('/admin')
    @login_required
    def admin_dashboard():
        pending = get_pending()
        return render_template('admin.html', submissions=pending)

    @app.route('/admin/approve/<int:submission_id>', methods=['POST'])
    @login_required
    def approve_submission(submission_id):
        pending = get_pending_by_id(submission_id)
        if not pending:
            flash('Submission not found.', 'error')
            return redirect(url_for('admin_dashboard'))
        set_pending_status(submission_id, 'approved')
        scraper = HappyHourScraper(pending['url'])
        raw = scraper.scrape_page()
        extractor = HappyHourExtractor()
        info = extractor.extract_happy_hour(raw)
        insert_restaurant(pending['name'], pending['url'], raw, info, '')
        #send_approval_email(pending['email'], pending['name'])
        app.logger.info(f"(stub) Approval email would be sent to {pending['email']}")
        flash('Approved and scraped successfully.', 'success')
        return redirect(url_for('admin_dashboard'))

    @app.route('/admin/reject/<int:submission_id>', methods=['POST'])
    @login_required
    def reject_submission_route(submission_id):
        pending = get_pending_by_id(submission_id)
        if not pending:
            flash('Submission not found.', 'error')
            return redirect(url_for('admin_dashboard'))
        set_pending_status(submission_id, 'rejected', 'Admin rejection')
        #send_rejection_email(pending['email'], pending['name'])
        app.logger.info(f"(stub) Rejection email would be sent to {pending['email']}")
        flash('Rejected submission.', 'warning')
        return redirect(url_for('admin_dashboard'))
