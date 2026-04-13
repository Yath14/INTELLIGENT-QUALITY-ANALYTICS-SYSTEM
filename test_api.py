import requests
import time

time.sleep(2)

test_data = {
    'loc': 24,
    'v_g': 5,
    'ev_g': 1,
    'iv_g': 3,
    'n': 63,
    'v': 309.13
}

try:
    response = requests.post('http://127.0.0.1:8000/predict', json=test_data)
    print(f'Status Code: {response.status_code}')
    result = response.json()
    if response.status_code == 200:
        print(f'Is Defect: {result.get("is_defect")}')
        print(f'Risk Score: {result.get("probability")}%')
        print(f'Status: {result.get("status")}')
    else:
        print(f'Error from backend: {result.get("error")}')
        print(f'Detail: {result.get("detail")}')
except Exception as e:
    print(f'Error: {e}')
