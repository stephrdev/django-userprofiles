test:
	flake8 userprofiles --ignore=E501,E128
	coverage run --branch --source=userprofiles `which django-admin.py` test --settings=test_project.settings userprofiles
	coverage report --show-missing --omit=userprofiles/test*
