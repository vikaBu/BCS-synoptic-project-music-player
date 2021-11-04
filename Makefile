mypy:
	poetry run mypy music_player_python tests

lint:
	poetry run flake8 music_player_python tests

black:
	poetry run black .

black-check:
	poetry run black . --check
flake8:
	poetry run flake8
