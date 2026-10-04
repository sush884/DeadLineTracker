import sqlite3
from datetime import datetime

DATABASE_NAME = "deadlines.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS deadlines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            description TEXT,
            due_date TEXT NOT NULL,
            due_time TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_deadline(
    title,
    subject,
    description,
    due_date,
    due_time,
    priority
):
    connection = get_connection()
    cursor = connection.cursor()

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO deadlines (
            title,
            subject,
            description,
            due_date,
            due_time,
            priority,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        subject,
        description,
        due_date,
        due_time,
        priority,
        "Pending",
        created_at
    ))

    connection.commit()
    connection.close()


def get_deadlines():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            subject,
            description,
            due_date,
            due_time,
            priority,
            status,
            created_at
        FROM deadlines
        ORDER BY due_date ASC, due_time ASC
    """)

    deadlines = cursor.fetchall()

    connection.close()

    return deadlines


def delete_deadline(deadline_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM deadlines WHERE id = ?",
        (deadline_id,)
    )

    connection.commit()
    connection.close()


def mark_completed(deadline_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE deadlines
        SET status = 'Completed'
        WHERE id = ?
    """, (deadline_id,))

    connection.commit()
    connection.close()


def update_deadline(
    deadline_id,
    title,
    subject,
    description,
    due_date,
    due_time,
    priority
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE deadlines
        SET
            title = ?,
            subject = ?,
            description = ?,
            due_date = ?,
            due_time = ?,
            priority = ?
        WHERE id = ?
    """, (
        title,
        subject,
        description,
        due_date,
        due_time,
        priority,
        deadline_id
    ))

    connection.commit()
    connection.close()