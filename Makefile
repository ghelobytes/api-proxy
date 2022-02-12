
run:
	uvicorn main:app --host 0.0.0.0 --port 8008 --reload

setup_uvicorn:
	pip install uvicorn[standard]
