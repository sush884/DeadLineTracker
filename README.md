# Deadline Tracker

A small Streamlit app for organizing deadlines. Items are stored locally in a
SQLite database (`deadlines.db`) in the project directory.

## Features

- Add deadlines with due dates, priority, and optional notes.
- Edit or delete items and mark them complete or reopen them.
- Filter by status or priority and search titles and notes.
- Sort by due date or priority and use Quick View for today's, this week's, or
  upcoming deadlines.
- See reminders for approaching deadlines, a completion progress bar, and
  separate completed-deadline history.
- Browse deadlines by selected date in the calendar view.
- See counts for open, due-today, and overdue items.

## Run locally

Python 3.10 or later is recommended.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

On macOS or Linux, activate the environment with
`source .venv/bin/activate` instead.

## Data and deployment

The database is created automatically on the first run. Back up `deadlines.db`
to preserve your data. For a hosted deployment, provide persistent storage for
the database file; ephemeral app filesystems will not retain deadlines across
restarts.

The `.streamlit/secrets.toml.example` file is a template for optional Streamlit
secrets. The app does not require any secrets or external services.
