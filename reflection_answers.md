# Lab 5: Static Code Analysis Reflection

## 1. Which Issues Were the Easiest to Fix, and Which Were the Hardest? Why?

The easiest issues to fix were the unused `datetime` import, inconsistent function naming, missing docstrings, and formatting violations. These changes were straightforward because they did not require changing the main functionality of the program. Removing the unused import, converting function names to snake_case, and correcting whitespace and line lengths made the code cleaner and easier to read.

The hardest issues were the SQL injection vulnerability and the potential runtime crash when an artifact ID did not exist. Fixing the SQL query required switching to parameterized queries and validating user inputs without affecting the existing database operations. The runtime issue required checking whether the database returned a record before accessing its values. Handling the unused `curator` argument also required care because removing it could affect existing function calls.

## 2. Did the Static Analysis Tools Report Any False Positives? If So, Describe One Example.

Some findings required checking the surrounding code before deciding how to fix them. For example, Bandit flagged the use of `subprocess`, including the call that used `shell=True`. Although the tool correctly identified a potentially risky pattern, the program only needed to print a backup confirmation message. Replacing the subprocess call with Python's built-in `print()` was a simpler and safer solution.

This was not necessarily a false positive because the original code did use a potentially unsafe pattern. It was an example of why tool warnings need to be interpreted in context rather than fixed blindly. The final Bandit report showed no remaining issues.

## 3. How Would You Integrate Static Analysis Tools Into Your Actual Software Development Workflow?

I would run Pylint, Bandit, and Flake8 regularly while developing Python applications, especially before committing changes. Pylint would help identify programming mistakes and maintainability issues, Flake8 would check coding style, and Bandit would help detect common security vulnerabilities.

For team projects, I would integrate these tools into a GitHub Actions workflow so that they run automatically whenever a pull request is created or updated. Pull requests could be reviewed before merging if the checks failed. I would also review the reported issues instead of blindly applying every suggested change, and run the application's tests after making fixes. This would help catch problems early and keep the codebase consistent as the project grows.

## 4. What Tangible Improvements Did You Observe in the Code Quality, Readability, or Potential Robustness After Applying the Fixes?

The code became more consistent and easier to understand after renaming functions to snake_case, adding docstrings, removing unused imports, and correcting formatting issues. The changes also made the code easier to maintain because the functions and their purposes are more clearly documented.

The parameterized SQL query reduced the risk of SQL injection, while input validation and a check for missing database records made the program more robust against invalid inputs. Replacing the unnecessary shell command with `print()` also removed an avoidable subprocess call.

After the changes, Pylint reported a score of 10.00/10, Bandit reported no issues, and Flake8 exited with code 0. These results indicate that the code meets the checks performed by the three tools. However, static analysis alone cannot guarantee that every possible runtime or logical error has been eliminated, so testing the program remains important.
