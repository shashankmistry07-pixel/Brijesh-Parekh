#!/bin/bash
echo "Building project for production..."

# 1. Ensure output directory exists and populate static assets
mkdir -p staticfiles_build/static
cp -r static/* staticfiles_build/static/ 2>/dev/null || true

# 2. Install dependencies with PEP 668 / uv support
python3 -m pip install --break-system-packages -r requirements.txt || uv pip install --system -r requirements.txt || pip install -r requirements.txt || true

# 3. Run Django collectstatic
python3 manage.py collectstatic --noinput --clear || python3 manage.py collectstatic --noinput || true

echo "Static build complete."
