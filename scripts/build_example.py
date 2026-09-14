"""Rebuild synthetic SQL from ORM metadata; never reads an existing database."""
import os
from pathlib import Path
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DB_PASS', 'example_build_only')

import app.models
from app.database.engine import Base
from sqlalchemy.schema import CreateTable, CreateIndex
from sqlalchemy.dialects import postgresql

dialect = postgresql.dialect()
statements = ['-- Synthetic examples only. Generated from ORM models, not a database dump.']
for table in Base.metadata.sorted_tables:
    statements.append(str(CreateTable(table).compile(dialect=dialect)).strip() + ';')
    for index in sorted(table.indexes, key=lambda item: item.name):
        statements.append(str(CreateIndex(index).compile(dialect=dialect)) + ';')
statements.append("""
INSERT INTO platforms (id, platform, created_at, updated_at)
VALUES ('example-platform', 'Example Platform', '2026-01-01', '2026-01-01');
INSERT INTO users (id, platform_id, platform_user_id, created_at, max_storage_mb)
VALUES ('example-user', 'example-platform', 'example-member', '2026-01-01', 10240);
INSERT INTO folders (id, title, parent_id, user_id, created_at, updated_at, delete_at)
VALUES ('example-root', 'Example root', NULL, 'example-user', '2026-01-01', '2026-01-01', NULL),
       ('example-child', 'Example child', 'example-root', 'example-user', '2026-01-01', '2026-01-01', NULL),
       ('example-trash', 'Example deleted folder', 'example-root', 'example-user', '2026-01-01', '2026-01-01', '2026-01-02');
INSERT INTO items (id, name, description, located)
VALUES ('example-item', 'Example item', 'Synthetic practice record', 'Example location');
""".strip())
sql = '\n'.join(line.rstrip() for line in '\n\n'.join(statements).splitlines()) + '\n'
# The current schema uses portable types. Check all inserts and foreign keys in memory.
connection = sqlite3.connect(':memory:')
connection.execute('PRAGMA foreign_keys = ON')
connection.executescript(sql)
assert connection.execute('SELECT COUNT(*) FROM folders').fetchone()[0] == 3
assert connection.execute('PRAGMA foreign_key_check').fetchall() == []
assert connection.execute("SELECT COUNT(*) FROM folders WHERE delete_at IS NOT NULL").fetchone()[0] == 1
connection.close()
destination = ROOT / 'db-image/example.sql'
if '--check' in sys.argv:
    assert destination.read_text(encoding='utf-8') == sql, 'example.sql is out of date'
else:
    destination.write_text(sql, encoding='utf-8')
print(f'PASS: {len(Base.metadata.tables)} tables; synthetic inserts and foreign keys checked in SQLite.')
