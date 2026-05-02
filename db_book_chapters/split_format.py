#!/usr/bin/env python3
"""Split and format the English lecture notes txt into per-chapter Markdown files."""

import re
import os

INPUT = "/home/csorfolydaniel/0db/db2/jegyzet_haladó_AB_Vassányi_István_2026.txt"
BASE = "/home/csorfolydaniel/0db/chapters"

CHAPTERS = [
    (148,  1132, "c1",  "1. Review of Core Database Skills"),
    (1133, 1510, "c2",  "2. Loose Coupling Based on Triggers and Jobs"),
    (1511, 2156, "c3",  "3. Replication, Log Shipping and Failover"),
    (2157, 2539, "c4",  "4. Data Quality and Master Data Management"),
    (2540, 2948, "c5",  "5. Columnstore and Partitioning"),
    (2949, 3480, "c6",  "6. Database Migration"),
    (3481, 3800, "c7",  "7. Cloud Database Technologies"),
    (3801, 4587, "c8",  "8. Special Data Types"),
    (4588, 4787, "c9",  "9. In-Memory Tables in SQL Server"),
    (4788, 4797, "c10", "10. Acknowledgments"),
    (4798, 5081, "c11", "11. Appendix A: SQL DML Examples for Self-Learning"),
    (5082, 5614, "c12", "12. Appendix B: Database Administration and Maintenance"),
]

KNOWN_H2 = {
    "Modeling", "Querying", "Programming", "Cursors", "Transaction management",
    "Problem scenario", "Solution", "A short overview on triggers",
    "Cases when the use of a DML trigger is recommended",
    "Tight coupling", "The loosely coupled system",
    "The log table and the trigger",
    "The stored procedure for processing new orders",
    "The stored procedure for processing the event log",
    "The scheduled job that calls the event log processor",
    "Replication concepts and architecture",
    "Snapshot replication", "Creating the publication",
    "Checking the publication", "Creating a push subscription",
    "Checking the subscription",
    "Transactional replication",
    "Replication between separate servers",
    "Configuring the distributor", "Configuring the publisher",
    "Adding the publication and the subscription",
    "Peer-to-Peer transactional replication",
    "Merge replication", "The publication", "The subscription",
    "Log shipping", "Failover clusters",
    "Data profiling", "SQL Server Data Quality Services",
    "Data cleansing projects", "Building your own Knowledge Base",
    "Columnstore", "Partitioning",
    "Migration between relational technologies",
    "Migration from relational to document store",
    "Data models: relational vs document store",
    "The demo application",
    "Running the demo app on localhost with a Postgres backend",
    "Document stores: Cloud Firestore overview",
    "Designing, creating and loading our Firestore document store",
    "Transactions on Firestore vs Postgres",
    "Using a Firestore transaction", "Batched writes",
    "Other Firestore features of interest not detailed here",
    "Overview", "Starting a new GCP project",
    "Migrating the Postgres database to GCP",
    "Implementing the demo app on GCP -> Cloud programming MSc course",
    "BigQuery overview and demo", "Mining the Northwind database",
    "Further reading",
    "Graph modeling", "Graph tables on SQL Server", "Performance",
    "GraphQL interfaces", "A native graph database: neo4j",
    "Technical issues", "Introduction", "The Cypher query language",
    "Importing data to Neo4j", "Storing images and BLOBs",
    "Database files", "Database performance", "Backups",
    "Maintenance plans", "Alerts", "Setting up database mail",
    "Enabling the mail profile in SQL server agent",
    "Creating an operator", "Adding the alert",
    "Overview of principals, privileges, schemas, roles",
    "Data security in SQL Server", "Sensitive data",
    "Areas of data security", "Configuring SSL",
    "Backup encryption", "Always encrypted",
}

# Only match unambiguously SQL-specific patterns (avoid common English words)
SQL_START_RE = re.compile(
    r'^('
    r'select\s|select\s*\*|select\s+top\b|'
    r'insert\s+into\b|insert\s+\[|insert\s+\w+\s*\(|'
    r'update\s+\w+\s+set\b|update\s+\[|'
    r'delete\s+from\b|delete\s+\[|'
    r'merge\s+\w+\s+(as|using)\b|'
    r'create\s+(table|procedure|proc|trigger|function|index|view|database)\b|'
    r'alter\s+(table|procedure|database|authorization)\b|'
    r'drop\s+(table|procedure|trigger|function|view|index)\b|'
    r'truncate\s+table\b|'
    r'use\s+\w|go\s*$|declare\s+@|set\s+@|set\s+nocount\b|'
    r'exec(ute)?\s|exec(ute)?\s*\(|'
    r'begin\s+tran|begin\s+transaction|begin\s+try\b|begin\s+catch\b|'
    r'end\s+try\b|end\s+catch\b|'
    r'commit\s*$|commit\s+tran|rollback\s*$|rollback\s+tran|'
    r'raiserror\s*\(|throw\s*;|'
    r'waitfor\s+delay\b|waitfor\s+time\b|'
    r'if\s+@@|if\s+@\w|while\s+@@|while\s+@\w|while\s+exists\b|'
    r'print\s+[@\'\"]|'
    # SQL clauses that are unambiguous in context (multi-word)
    r'group\s+by\s|order\s+by\s|inner\s+join\s|left\s+(outer\s+)?join\s|'
    r'right\s+(outer\s+)?join\s|from\s+\[?\w+\]?\s+(inner|left|right|outer|join|where|as)\b|'
    r'from\s+\w+\s+\w+\s+(inner|left|right|outer|join|where|on)\b|'
    r'--|:r\s'
    r')',
    re.IGNORECASE | re.MULTILINE,
)

# A dash-prefixed label like "-Value of each order" that precedes SQL in the PDF extraction
SQL_LABEL_RE = re.compile(r'^-[A-Za-z]')

BULLET_MARKERS = {'•', '○', 'o', '▪'}
BULLET_LEVEL = {'•': 0, '○': 0, 'o': 1, '▪': 2}


def is_page_num(s):
    # standalone page numbers (1–3 digits) or chapter-number artifacts like "10."
    return bool(re.match(r'^\d{1,3}\.?$', s.strip()))


def is_chapter_heading(s):
    return bool(re.match(r'^\d{1,2}\.\s+[A-Z]', s))


def is_bullet_marker(s):
    return s.strip() in BULLET_MARKERS


def is_sql(s):
    return bool(SQL_START_RE.match(s.strip()))

def block_is_sql(content_lines):
    """True if the content block is SQL code (possibly starting with a dash label)."""
    if not content_lines:
        return False
    if is_sql(content_lines[0]):
        return True
    # Block starts with a -Label line followed by a SQL line
    if SQL_LABEL_RE.match(content_lines[0].strip()) and len(content_lines) > 1:
        return any(is_sql(l) for l in content_lines[1:])
    return False


def split_block(filtered):
    """Split a block into (leading_markers, content_lines, trailing_markers).

    PDF extraction places the next sub-bullet marker at the END of the
    previous content block (no blank line), so we must separate it out.
    """
    i = 0
    # Leading markers (bullet chars before any content)
    leading = []
    while i < len(filtered) and is_bullet_marker(filtered[i]):
        leading.append(filtered[i])
        i += 1

    # Trailing markers (bullet chars at the very end after content)
    j = len(filtered) - 1
    trailing = []
    while j > i and is_bullet_marker(filtered[j]):
        trailing.insert(0, filtered[j])
        j -= 1

    content = filtered[i:j + 1]
    return leading, content, trailing


def get_blocks(lines):
    """Group non-blank lines into blocks; blank lines become empty-list sentinels."""
    blocks = []
    current = []
    for raw in lines:
        s = raw.rstrip('\n').strip()
        if s:
            current.append(s)
        else:
            if current:
                blocks.append(current)
                current = []
            blocks.append([])
    if current:
        blocks.append(current)
    return blocks


def split_sql_from_prose(content):
    """If a block mixes prose then SQL, return (prose_lines, sql_lines); else (None, None)."""
    for i, line in enumerate(content):
        if i == 0:
            continue  # first line already checked by caller
        if is_sql(line) or (SQL_LABEL_RE.match(line.strip()) and i < len(content) - 1 and is_sql(content[i + 1])):
            return content[:i], content[i:]
    return None, None


def format_chapter(lines, title):
    # Title body without the "N. " prefix, for detecting repeated heading lines
    title_body = re.sub(r'^\d+\.\s*', '', title).strip()
    blocks = get_blocks(lines)
    out = [f"# {title}", ""]

    pending_level = None   # bullet indent level for next content item
    in_sql = False
    sql_buf = []

    def flush_sql():
        nonlocal in_sql, sql_buf
        if sql_buf:
            if out and out[-1] != "":
                out.append("")
            out.append("```sql")
            out.extend(sql_buf)
            out.append("```")
            out.append("")
            sql_buf.clear()
        in_sql = False

    def emit_sql(text):
        nonlocal in_sql
        sl = re.sub(r'^-(?!-)\s*', '-- ', text)
        if not in_sql:
            in_sql = True
        sql_buf.append(sl)

    for block in blocks:
        # ── blank sentinel ─────────────────────────────────────────────────
        if not block:
            if not in_sql:
                if out and out[-1] != "":
                    out.append("")
            continue

        # Strip page numbers
        filtered = [l for l in block if not is_page_num(l)]
        if not filtered:
            continue

        # Split into leading markers / content / trailing markers
        leading, content, trailing = split_block(filtered)

        # Update pending_level from leading markers (set the level for this content)
        if leading:
            if in_sql:
                flush_sql()
            level_from_leading = max(BULLET_LEVEL.get(m.strip(), 0) for m in leading)
            pending_level = level_from_leading

        if not content:
            # Block was only markers — trailing update pending_level for next block
            if trailing:
                pending_level = max(BULLET_LEVEL.get(m.strip(), 0) for m in trailing)
            continue

        # ── process content ───────────────────────────────────────────────

        # Skip chapter headings and repeated title body lines
        if is_chapter_heading(content[0]) or content[0].strip() == title_body:
            content = content[1:]
        if not content:
            if trailing:
                pending_level = max(BULLET_LEVEL.get(m.strip(), 0) for m in trailing)
            continue

        # Detect known section heading in first content line
        if content[0] in KNOWN_H2:
            if in_sql:
                flush_sql()
            if out and out[-1] != "":
                out.append("")
            out.append(f"## {content[0]}")
            out.append("")
            content = content[1:]
            # After a heading, the remaining content (if any) is a new paragraph
            # at no bullet indent; reset pending_level to None unless leading set it
            if not leading:
                pending_level = None

        if not content:
            if trailing:
                pending_level = max(BULLET_LEVEL.get(m.strip(), 0) for m in trailing)
            continue

        # Detect SQL block
        if block_is_sql(content):
            for l in content:
                emit_sql(l)
            pending_level = None
            if trailing:
                pending_level = max(BULLET_LEVEL.get(m.strip(), 0) for m in trailing)
            continue

        # Mixed prose-then-SQL block (e.g. explanation followed immediately by code)
        prose_part, sql_part = split_sql_from_prose(content)
        if sql_part is not None:
            if in_sql:
                flush_sql()
            if prose_part:
                level = pending_level
                indent = "  " * level + "- " if level is not None else ""
                out.append(f"{indent}{' '.join(prose_part)}")
                pending_level = None
            for l in sql_part:
                emit_sql(l)
            if trailing:
                pending_level = max(BULLET_LEVEL.get(m.strip(), 0) for m in trailing)
            continue

        # Regular content
        if in_sql:
            flush_sql()

        joined = " ".join(content)
        level = pending_level
        indent = "  " * level + "- " if level is not None else ""
        out.append(f"{indent}{joined}")
        pending_level = None   # consumed

        # Trailing markers set pending_level for the NEXT content block
        if trailing:
            pending_level = max(BULLET_LEVEL.get(m.strip(), 0) for m in trailing)

    if in_sql:
        flush_sql()

    result = "\n".join(out)
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result.strip() + "\n"


def main():
    with open(INPUT, encoding="utf-8") as f:
        all_lines = f.readlines()
    total = len(all_lines)

    for start, end, dirname, title in CHAPTERS:
        dirpath = os.path.join(BASE, dirname)
        os.makedirs(dirpath, exist_ok=True)

        chapter_lines = all_lines[start - 1 : min(end, total)]
        md = format_chapter(chapter_lines, title)

        outpath = os.path.join(dirpath, f"{dirname}.md")
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(md)

        print(f"  {dirname}/  {len(chapter_lines):4d} src → {len(md.splitlines()):4d} md lines")


if __name__ == "__main__":
    main()
