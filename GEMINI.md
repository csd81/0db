# 0db - Advanced Database Management Course Materials

This repository contains lecture notes, exercises, and demonstration scripts for an advanced database management course focused on **Microsoft SQL Server** and **T-SQL**.

## Project Overview
The project is organized into two main modules covering core and advanced database topics. It uses the **Northwind** sample database as a primary example for data modeling and programming exercises.

### Main Technologies
*   **Database:** MS SQL Server
*   **Language:** T-SQL (Transact-SQL)
*   **Documentation:** LaTeX (for PDF notes), Markdown, and Plain Text

## Directory Structure

### `db1/` - Core SQL & T-SQL Materials
*   **`README.md`**: Overview of the Northwind database schema.
*   **`jegyzet_adatb-II.txt`**: Comprehensive lecture notes covering:
    *   Field-oriented vs. Record-oriented modeling.
    *   T-SQL procedural programming (variables, loops, logic).
    *   Error handling (`TRY...CATCH`).
    *   Server-side cursors and Analytic functions.
    *   Transaction management (ACID properties, isolation levels).
*   **`feladat1.sql` to `feladat26.sql`**: Practical exercises corresponding to the lecture notes.
*   **`install_northwind.sql`**: Script to set up the practice environment.

### `db2/` - Advanced Topics & Glossary
*   **`jegyzet_halado*`**: Advanced database management notes.
*   **`TERMS.md`**: An English-Hungarian database glossary for technical terminology.
*   **`order_processing_demo.sql`**: A demo of a complex business process (order placement) implemented with T-SQL logic and transaction handling.
*   **`images/`**: Diagrams and visual aids for the course notes.

## Key Learning Objectives
1.  **Modeling Flexibility:** Understanding when to use record-oriented models for highly dynamic data.
2.  **Programmability:** Mastering T-SQL to move business logic into the database layer for efficiency and security.
3.  **Performance & Analysis:** Using window functions and optimized queries for data analysis.
4.  **Concurrency:** Managing multi-user environments through isolation levels and deadlock prevention.

## Usage Instructions
1.  **Setup:** Execute `db1/install_northwind.sql` in SQL Server Management Studio (SSMS) to prepare the Northwind database.
2.  **Learning Path:** Follow the `jegyzet_adatb-II.txt` notes and implement the corresponding `feladat*.sql` exercises.
3.  **Advanced Study:** Review `db2/` for deeper architectural concepts and advanced T-SQL demos.

---
*Note: This repository is intended for educational purposes. Some SQL scripts contain intentional "broken" lines (commented out) to demonstrate common errors and their corrections.*
