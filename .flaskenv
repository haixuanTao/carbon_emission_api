FLASK_ENV=development
FLASK_APP=instagram_carbon_emission.app:create_app
SECRET_KEY=changeme
DATABASE_URI=sqlite:////tmp/instagram_carbon_emission.db
CELERY_BROKER_URL=amqp://guest:guest@localhost/
CELERY_RESULT_BACKEND_URL=amqp://guest:guest@localhost/
