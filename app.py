import os
import subprocess
import requests
import json
from fastapi import FastAPI, Query
from datetime import datetime

app = FastAPI()

DATA_DIR = "/data"

@app.post("/run")
def run_task(task: str):
    try:
        # Task A1: Install uv and run datagen.py
        if "install uv" in task.lower() and "run" in task.lower():
            subprocess.run(["pip", "install", "uv"], check=True)
            url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
            response = requests.get(url)
            with open("datagen.py", "w", encoding="utf-8") as file:
                file.write(response.text)
            user_email = "example email"
            subprocess.run(["python", "datagen.py", user_email], check=True)
            return {"status": "success", "message": "Task A1 completed successfully"}

        # Task A2: Format /data/format.md using prettier
        elif "format" in task.lower() and "prettier" in task.lower():
            file_path = f"{DATA_DIR}/format.md"
            if not os.path.exists(file_path):
                return {"status": "error", "message": "File not found"}
            subprocess.run(["prettier", "--write", file_path], check=True)
            return {"status": "success", "message": "Task A2 completed successfully"}

        # Task A3: Count Wednesdays in /data/dates.txt
        elif "wednesday" in task.lower() or "count days" in task.lower():
            file_path = f"{DATA_DIR}/dates.txt"
            if not os.path.exists(file_path):
                return {"status": "error", "message": "File not found"}
            with open(file_path, "r", encoding="utf-8") as file:
                dates = file.readlines()
            wednesday_count = sum(1 for date in dates if datetime.strptime(date.strip(), "%Y-%m-%d").weekday() == 2)
            with open(f"{DATA_DIR}/dates-wednesdays.txt", "w", encoding="utf-8") as file:
                file.write(str(wednesday_count))
            return {"status": "success", "message": "Task A3 completed successfully"}

        # Task A4: Sort contacts in /data/contacts.json
        elif "sort contacts" in task.lower():
            file_path = f"{DATA_DIR}/contacts.json"
            if not os.path.exists(file_path):
                return {"status": "error", "message": "File not found"}
            with open(file_path, "r", encoding="utf-8") as file:
                contacts = json.load(file)
            sorted_contacts = sorted(contacts, key=lambda x: (x["last_name"], x["first_name"]))
            with open(f"{DATA_DIR}/contacts-sorted.json", "w", encoding="utf-8") as file:
                json.dump(sorted_contacts, file, indent=4)
            return {"status": "success", "message": "Task A4 completed successfully"}
        # Task A5: Write first line of 10 most recent .log files
        elif "recent logs" in task.lower():
            log_dir = f"{DATA_DIR}/logs"
            if not os.path.exists(log_dir):
                return {"status": "error", "message": "Log directory not found"}
            log_files = sorted(
                [f for f in os.listdir(log_dir) if f.endswith(".log")],
                key=lambda f: os.path.getmtime(os.path.join(log_dir, f)),
                reverse=True
            )[:10]
            lines = []
            for log_file in log_files:
                with open(os.path.join(log_dir, log_file), "r", encoding="utf-8") as file:
                    first_line = file.readline().strip()
                    lines.append(first_line)
            with open(f"{DATA_DIR}/logs-recent.txt", "w", encoding="utf-8") as file:
                file.write("\n".join(lines))
            return {"status": "success", "message": "Task A5 completed successfully"}
       # Task A6: Extract H1 titles from Markdown files
        elif "index markdown" in task.lower():
            docs_dir = f"{DATA_DIR}/docs"
            if not os.path.exists(docs_dir):
                return {"status": "error", "message": "Docs directory not found"}
            index = {}
            for doc_file in os.listdir(docs_dir):
                if doc_file.endswith(".md"):
                    with open(os.path.join(docs_dir, doc_file), "r", encoding="utf-8") as file:
                        for line in file:
                            if line.startswith("# "):  # First H1 occurrence
                                index[doc_file] = line[2:].strip()
                                break
            with open(f"{DATA_DIR}/docs/index.json", "w", encoding="utf-8") as file:
                json.dump(index, file, indent=4)
            return {"status": "success", "message": "Task A6 completed successfully"}

        return {"status": "error", "message": "Task not recognized"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/read")
def read_file(path: str = Query(..., description="File path to read")):
    if not os.path.exists(path):
        return {"status": "error", "message": "File not found"}
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    return {"status": "success", "content":content}