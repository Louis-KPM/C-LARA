migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

runserver:
	python3 manage.py runserver
	
qcluster:
	python3 manage.py qcluster

check:
	python3 manage.py check

superuser:
	python3 manage.py createsuperuser

collectstatic:
	python3 manage.py collectstatic

test:
	python3 manage.py test

count_lines:
	python3 count_lines.py

