# Lab 5: Static Code Analysis Reflection

## 1. What Static Code Analysis Is and How It Differs From Program Execution
Static code analysis is the process of examining source code without executing it. It parses the code into an Abstract Syntax Tree (AST) and evaluates the structure, syntax, coding standards, and control flow against predefined rules and security heuristics.

In contrast, program execution (dynamic testing) runs the application in a specific runtime environment with concrete inputs and observes runtime behavior, outputs, and side effects. While dynamic execution tests only the specific code paths triggered by test inputs, static analysis analyzes all lines and branches across the codebase simultaneously. Furthermore, static analysis detects critical flaws—such as unexecuted vulnerable branches, hardcoded secrets, syntax errors, and style regressions—very early in the software development lifecycle before code is ever run or deployed.

## 2. What Pylint, Bandit, and Flake8 Each Detect
- **Pylint:** Serves as a comprehensive code quality and design reviewer. It detects logical flaws, programming errors, unused variables and arguments, dead imports, non-standard naming styles (such as camelCase instead of snake_case in Python), refactoring opportunities (such as unnecessary `else` branches following a `return`), and missing documentation (docstrings). It also calculates an aggregate code quality rating out of 10.
- **Bandit:** Serves as a Python-specific security scanner. It analyzes the AST to identify known vulnerability patterns and dangerous constructs categorized by Common Weakness Enumerations (CWEs). It specifically detects SQL injection vulnerabilities from string-formatted SQL queries (B608), plaintext hardcoded passwords and API tokens (B105), insecure subprocess executions involving `shell=True` or relative binary paths (B602, B607), and risky module imports (B404).
- **Flake8:** Acts as a style and syntax linter combining PyFlakes, pycodestyle, and McCabe complexity. It strictly checks adherence to the official Python style guide (PEP 8), flagging line length violations (> 79 characters), missing or excessive whitespace around operators and commas, incorrect blank line counts between function definitions, and undefined or unused imported names.

## 3. Issues Identified and Fixed in This Assignment
During analysis of `museum_catalog.py`, the tools revealed multiple critical, medium, and low severity issues:
- **SQL Injection (Bandit B608):** In `addArtifact`, input values were interpolated directly into the SQL string via string concatenation. This was resolved by switching to parameterized queries `(?, ?, ?, ?)` and adding input type and range validation.
- **Hardcoded Secret (Bandit B105):** `CURATOR_PASSWORD = "m4seum!"` stored a credential in plain text. It was completely removed as it was unused and represented an insecure practice.
- **Unsafe Shell Subprocess (Bandit B602, B607, B404):** `backupNote` invoked `subprocess.call("echo catalog backup complete", shell=True)`. This was replaced with Python's built-in `print("catalog backup complete")` and `import subprocess` was removed.
- **Runtime Crash on Missing Artifact (Bug):** `displayStatus` accessed `row[0]` without checking if `row` was `None`. A null check was added returning an informative `"artifact not found"` message to avoid `TypeError`.
- **Unused Parameter (Pylint W0613):** `curator` in `displayStatus` was accepted but never used. It was assigned a default value, documented for audit tracking, and referenced internally to retain backward compatibility without tool warnings.
- **Unused Import (Pylint W0611, Flake8 F401):** `import datetime` was imported but unused. It was removed.
- **Non-conforming Naming (Pylint C0103):** Function names (`addArtifact`, `displayStatus`, `totalValue`, `moveToDisplay`, `backupNote`) used camelCase. All were renamed to PEP 8 snake_case (`add_artifact`, `display_status`, `total_value`, `move_to_display`, `backup_note`).
- **PEP 8 Formatting (Flake8 E501, E225, E303):** Lines exceeding 79 characters were broken into multi-line statements, whitespace was added around assignment operators (`total = 0`), and blank lines were standardized.
- **Missing Docstrings (Pylint C0114, C0116):** Added descriptive docstrings to the module and all functions.
- **Unnecessary Else (Pylint R1705):** Removed redundant `else` after `return` in `display_status`.
- **Script Guard:** Wrapped top-level `main()` execution in `if __name__ == "__main__":`.

## 4. How Static Analysis Improved Code Quality, Security, and Maintainability
- **Code Quality:** Pylint score increased from **4.85/10 to 10.00/10**. Potential runtime crashes (e.g., querying nonexistent artifact IDs) were prevented through defensive null checks and strict input validation.
- **Security:** The application's attack surface was neutralized. The SQL injection vulnerability was completely eliminated through parameterization, plaintext credentials were removed, and shell execution hazards were eradicated.
- **Maintainability:** Adopting PEP 8 conventions, descriptive docstrings, consistent snake_case identifiers, and standardized line lengths makes the codebase clean, readable, and intuitive for other engineers to extend.

## 5. Limitations and Challenges Encountered While Interpreting Reports
- **Context-Free Flagging:** Bandit flags all uses of `import subprocess` (B404) regardless of context. Understanding that the program merely needed to print a confirmation notice allowed replacing the external command with standard Python `print()`, rather than applying complex subprocess hardening.
- **Interface Compatibility vs. Unused Argument Warnings:** Pylint flagged `curator` as unused in `displayStatus`. Simply deleting the argument would break callers that pass a curator string (such as `main()`). Deciding how to maintain the method signature while satisfying the linter required careful consideration.
- **Tool-Specific Threshold Differences:** Flake8 strictly enforces a 79-character line limit, whereas Pylint defaults to 100 characters. Designing multi-line SQL strings that satisfied both tools without hurting readability required deliberate formatting.
- **Complementary Nature to Testing:** Static analysis can verify syntax, types, and known vulnerability patterns, but it cannot verify whether business logic produces the expected values (e.g. verifying that `total_value` sums integers correctly). Dynamic testing remains necessary alongside static analysis.
