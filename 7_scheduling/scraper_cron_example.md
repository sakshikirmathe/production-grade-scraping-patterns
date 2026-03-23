# ⏰ Scraper Scheduling Guide

This guide explains how to run your scraping scripts automatically on a schedule using:

* [x] Cron (Linux/macOS)
* [x] Windows Task Scheduler
* [x] GitHub Actions (cloud-based)

---

## 🐧 Linux/macOS — Cron Job

### 1. Make your script executable

```bash
chmod +x path/to/your_scraper.py
```

### 2. Add Python shebang at top (optional)

```bash
#!/usr/bin/env python3
```

### 3. Edit cron

```bash
crontab -e
```

### 4. Example: Run scraper every day at 7 AM

```bash
0 7 * * * /usr/bin/python3 /absolute/path/to/your_scraper.py >> /absolute/path/to/logfile.log 2>&1
```

### ⏱️ Cron Format

```
# ┌──────── minute (0 - 59)
# │ ┌────── hour (0 - 23)
# │ │ ┌──── day of month (1 - 31)
# │ │ │ ┌── month (1 - 12)
# │ │ │ │ ┌ day of week (0 - 6)
# │ │ │ │ │
# * * * * *
```

---

## 🪟 Windows — Task Scheduler

### 1. Open Task Scheduler

Search **"Task Scheduler"** in Start menu

### 2. Create Basic Task

* Name: `Daily Scraper`
* Trigger: `Daily`
* Start time: `07:00 AM`
* Action: `Start a Program`

### 3. Program/script

```
C:\Path\To\python.exe
```

### 4. Add Arguments

```
"C:\Path\To\your_scraper.py"
```

### 5. Optional (Recommended)

* **Start in:**

```
C:\Path\To\your_script_folder
```

* **Add logging:**

```bat
python your_scraper.py >> logfile.txt 2>&1
```

---

## ☁️ GitHub Actions — Scheduled Cloud Runs

### 1. Create workflow file

```
.github/workflows/scheduled_scraper.yml
```

### 2. Add the following configuration

```yaml
name: Scheduled Scraper

on:
  schedule:
    - cron: "0 6 * * *"  # Runs daily at 6 AM UTC

jobs:
  run-scraper:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repo
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.10

      - name: Install Dependencies
        run: pip install -r requirements.txt

      - name: Run Scraper
        run: python path/to/your_scraper.py
```

### ⏰ Timezone Note

GitHub Actions uses **UTC time**.

💡 Example:
To run at **7:00 AM IST**, use:

```
cron: "30 1 * * *"
```

---

## 🧪 Virtual Environment (Recommended)

Use virtual environments to avoid dependency issues:

### Linux/macOS

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 📝 Tips

* Always use **absolute paths** in cron jobs
* Add **logging** to debug failures
* Ensure dependencies are installed before scheduling
* Use **virtual environments** for clean setups
* For cloud runs, consider storing outputs (CSV/DB)

---

## 🚀 Use Cases

* Daily job scraping
* Price tracking
* News aggregation
* Data pipelines
* Automated reporting

---

Happy Scraping! 🕷️