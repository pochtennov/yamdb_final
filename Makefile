build:
	docker-compose up -d --build

setup:
	docker-compose exec web python manage.py migrate auth
	docker-compose exec web python manage.py migrate --run-syncdb
	docker-compose exec web python manage.py collectstatic --no-input

add-fixtures:
	docker-compose exec web python manage.py loaddata fixtures.json

createsu:
	docker-compose exec web python manage.py createsuperuser

stop:
	docker-compose stop