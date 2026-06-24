# Exit on error
set -o errexit

# Modify this line as needed for your package manager ( pip, poetry, etc. )
pip install -r requirements.txt


# Convert static asset files
python manage.py collectstatic --no-input


# Apply any outstanding database migrations
python manage.py migrate


# This automatically loads your 160 objects into the manual database during deployment
python manage.py loaddata datadump.json
