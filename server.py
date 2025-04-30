from flask_app.controllers.users import Users
from flask_app.controllers.notes import Notes
from flask_app import app

if __name__ == "__main__":
    app.run(debug=True)