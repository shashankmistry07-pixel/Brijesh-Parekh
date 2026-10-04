echo "Building project for production..."
python3 -m pip install -r requirements.txt
python3 manage.py collectstatic --noinput --clear
echo "Static build complete."
