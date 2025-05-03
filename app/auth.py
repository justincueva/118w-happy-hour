from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask import render_template, request, redirect, url_for, flash

login_manager = LoginManager()

class Admin(UserMixin):
    pass


def init_login(app):
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        if str(user_id) == str(app.config['ADMIN_ID']):
            user = Admin()
            user.id = user_id
            return user
        return None

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD']:
                user = Admin()
                user.id = app.config['ADMIN_ID']
                login_user(user)
                return redirect(url_for('admin_dashboard'))
            flash('Invalid credentials', 'error')
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home'))