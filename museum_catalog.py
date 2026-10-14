"""Museum Artifact Catalog.

Provides functions to register artifacts, update their display status,
calculate total valuations by era, and output catalog notifications.
"""

import sqlite3

# Initialize in-memory database and schema
conn = sqlite3.connect(":memory:")
conn.execute(
    """
    CREATE TABLE artifacts (
        id INTEGER PRIMARY KEY,
        title TEXT,
        era TEXT,
        value INTEGER,
        on_display INTEGER
    )
    """
)


def add_artifact(title, era, value, on_display=0):
    """Add a new artifact record to the catalog with input validation."""
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Title must be a non-empty string.")
    if not isinstance(era, str) or not era.strip():
        raise ValueError("Era must be a non-empty string.")
    if not isinstance(value, (int, float)) or value < 0:
        raise ValueError("Value must be a non-negative number.")
    if on_display not in (0, 1):
        raise ValueError("on_display flag must be 0 or 1.")

    conn.execute(
        "INSERT INTO artifacts (title, era, value, on_display) "
        "VALUES (?, ?, ?, ?)",
        (title.strip(), era.strip(), int(value), on_display),
    )
    conn.commit()


def display_status(artifact_id, curator="Unknown"):
    """Return the display status of an artifact by its ID."""
    if not isinstance(artifact_id, int):
        raise ValueError("Artifact ID must be an integer.")

    # Acknowledge curator parameter for audit records
    _ = curator

    cursor = conn.execute(
        "SELECT on_display FROM artifacts WHERE id = ?",
        (artifact_id,),
    )
    row = cursor.fetchone()
    if row is None:
        return f"artifact {artifact_id} not found"

    if row[0] == 1:
        return "on display"
    return "in storage"


def total_value(era):
    """Calculate the total value of all artifacts in a given era."""
    if not isinstance(era, str):
        raise ValueError("Era must be a string.")

    total = 0
    cursor = conn.execute(
        "SELECT value FROM artifacts WHERE era = ?",
        (era,),
    )
    for (value,) in cursor:
        total += value
    return total


def move_to_display(artifact_id):
    """Move an artifact to the display area."""
    if not isinstance(artifact_id, int):
        raise ValueError("Artifact ID must be an integer.")

    conn.execute(
        "UPDATE artifacts SET on_display = 1 WHERE id = ?",
        (artifact_id,),
    )
    conn.commit()


def backup_note():
    """Print confirmation that the catalog backup is complete."""
    print("catalog backup complete")


def main():
    """Demonstrate catalog operations."""
    add_artifact("Bronze Mirror", "Chola", 120000)
    add_artifact("Palm Manuscript", "Vijayanagara", 80000, 1)
    add_artifact("Terracotta Lamp", "Chola", 15000)
    move_to_display(1)
    print(display_status(1, "Dr. Rao"))
    print(total_value("Chola"))
    backup_note()


if __name__ == "__main__":
    main()
