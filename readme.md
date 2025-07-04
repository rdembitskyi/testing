# Testing App

This is a simple testing application to do a demo of file analysis using Flask. It provides both synchronous and asynchronous endpoints for file analysis.


# How to run

# 1. Install dependencies
```bash
pip install -r requirements.txt
```

# 2. Run the application
```bash
python main.py
```

# 3. Test case number 1

Go to /utils/test_file_generator.py to generate one or more test files. 

Or add test files manually

Run the tests by going to /analyzer/file_scanner.py and running the script.

Results will be saved in the `results` directory.

# 4. Test case number 2
Submit a file to the analyzer API endpoint `/analyze_sync` using a tool like Postman or curl.

```bash
curl -X POST http://127.0.0.1:5000/analyze_sync -F "file=@test_file_6748.txt"
```

# 5. Test case number 3
Submit a file to the analyzer API endpoint `/analyze_async` using a tool like Postman or curl.

```bash
curl -X POST http://127.0.0.1:5000/analyze_async -F "file=@test_file_6748.txt"
```

Get the results by going to `/results/<task_id>` where `<task_id>` is the ID returned from the async analysis request.

```bash
curl get http://127.0.0.1:5000/results/task_id
```