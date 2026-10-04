from datetime import datetime


def get_deadline_status(due_date, due_time, status):

    if status == "Completed":
        return "Completed", "✅"

    deadline_datetime = datetime.strptime(
        f"{due_date} {due_time}",
        "%Y-%m-%d %H:%M"
    )

    now = datetime.now()

    difference = deadline_datetime - now
    total_seconds = difference.total_seconds()

    if total_seconds < 0:
        return "Overdue", "🔴"

    total_days = difference.days

    if total_days == 0:
        return "Due today", "🟠"

    if total_days == 1:
        return "Due tomorrow", "🟡"

    return f"Due in {total_days} days", "🟢"


def get_reminder_message(
    due_date,
    due_time,
    status
):

    if status == "Completed":
        return None

    deadline_datetime = datetime.strptime(
        f"{due_date} {due_time}",
        "%Y-%m-%d %H:%M"
    )

    now = datetime.now()

    difference = deadline_datetime - now

    total_hours = (
        difference.total_seconds() / 3600
    )

    if total_hours < 0:
        return "🔴 This deadline is overdue!"

    if total_hours <= 24:
        return "🚨 Deadline is within 24 hours!"

    if total_hours <= 48:
        return "⚠️ Deadline is within 2 days!"

    return None


def get_priority_icon(priority):

    if priority == "High":
        return "🔴"

    if priority == "Medium":
        return "🟠"

    return "🟢"
