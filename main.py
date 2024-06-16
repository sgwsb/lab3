import subprocess
import json


def run_curl_command(url):
    try:
        result = subprocess.run(['curl', '-s', '-w', '%{http_code}', url], capture_output=True, text=True)
        http_code = result.stdout[-3:]
        json_data = result.stdout[:-3]
        return http_code, json_data
    except Exception as e:
        print(f"Error running curl command: {e}")
        return None, None


def validate_response(http_code, json_data, required_keys):
    if http_code != '200':
        return False, f"Invalid HTTP response code: {http_code}"

    try:
        data = json.loads(json_data)
        if isinstance(data, list):  # Dla endpointów zwracających listy
            data = data[0] if data else {}
        for key in required_keys:
            if key not in data:
                return False, f"Missing key: {key}"
        return True, "All keys present"
    except json.JSONDecodeError:
        return False, "Invalid JSON response"
    except Exception as e:
        return False, f"Error validating response: {e}"


def run_tests():
    tests = [
        {
            "url": "https://jsonplaceholder.typicode.com/posts",
            "required_keys": ["userId", "id", "title"]
        },
        {
            "url": "https://jsonplaceholder.typicode.com/comments",
            "required_keys": ["postId", "id", "name"]
        },
        {
            "url": "https://jsonplaceholder.typicode.com/users",
            "required_keys": ["id", "name", "username"]
        }
    ]

    for i, test in enumerate(tests, start=1):
        print(f"Running Test {i} for URL: {test['url']}")
        http_code, json_data = run_curl_command(test['url'])
        passed, message = validate_response(http_code, json_data, test['required_keys'])
        if passed:
            print(f"Test {i}: PASSED - {message}")
        else:
            print(f"Test {i}: FAILED - {message}")


if __name__ == "__main__":
    run_tests()