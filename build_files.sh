echo "Building project for production..."
pip install -r requirements.txt || python3 -m pip install -r requirements.txt || uv pip install -r requirements.txt
mkdir -p staticfiles_build/static
python3 manage.py collectstatic --noinput --clear
echo "Static build complete."
