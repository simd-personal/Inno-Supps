#!/usr/bin/env python3
"""
Script to update database models for SQLite compatibility
"""

import re

# Read the current database.py file
with open('database.py', 'r') as f:
    content = f.read()

# Replace UUID columns with uuid_column() helper
content = re.sub(r'id = Column\(UUID\(as_uuid=True\), primary_key=True, default=uuid\.uuid4\)', 'id = uuid_column()', content)

# Replace UUID foreign keys with uuid_foreign_key() helper
content = re.sub(r'Column\(UUID\(as_uuid=True\), ForeignKey\("([^"]+)"\)', r'uuid_foreign_key("\1")', content)

# Replace Vector columns with Text for SQLite
content = re.sub(r'Column\(Vector\(1536\)', 'Column(Text', content)

# Replace postgresql.UUID with String(36)
content = re.sub(r'postgresql\.UUID\(as_uuid=True\)', 'String(36)', content)

# Write the updated content back
with open('database.py', 'w') as f:
    f.write(content)

print("Database models updated for SQLite compatibility!")
