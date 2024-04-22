
echo 'Building the project...'
echo 'Cleaning up the build directory...'
python3 -m pip install -r requirements.txt

echo 'Makemigrations...'
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo 'Collecting static files...'
python3 manage.py collectstatic --noinput --clear
