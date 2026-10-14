# Lab 5: Static Code Analysis Reflection

## 1. Which Issues Were the Easiest to Fix, and Which Were the Hardest? Why?

The easiest issues to fix were the unused import, function naming, missing docstrings, and formatting mistakes. These did not require major changes to the program. I just had to remove unnecessary code, rename functions using snake_case, and correct the spacing and line lengths.

The harder issues were the SQL injection vulnerability and the crash that occurred when an artifact ID was not found. For the SQL issue, I had to change the query to use parameters instead of directly combining user inputs with the SQL statement. For the missing artifact issue, I added a check before accessing the database result so that the program could handle it properly. I also had to be careful while fixing the unused `curator` argument so that existing function calls would continue to work.

## 2. Did the Static Analysis Tools Report Any False Positives? If So, Describe One Example.

Some warnings needed a closer look before deciding what to change. For example, Bandit flagged the use of `subprocess` and the `shell=True` argument. In this program, the command was only being used to print a backup confirmation message. I replaced it with Python's `print()` function, which was simpler and avoided running an unnecessary shell command.

I would not consider this a completely false warning because using `shell=True` can be risky in other situations. It showed me that the warnings need to be understood in the context of the program rather than fixed without checking what the code actually does.

## 3. How Would You Integrate Static Analysis Tools Into Your Actual Software Development Workflow?

I would run Pylint, Bandit, and Flake8 while developing a project and before committing my changes. Pylint helps find code quality issues, Flake8 checks formatting, and Bandit helps identify common security risks.

For a team project, I would set them up in GitHub Actions so that the checks run automatically whenever someone creates or updates a pull request. This would help the team catch problems before merging code. I would also run the existing tests after fixing any issues to make sure the changes have not affected the program's functionality.

## 4. What Tangible Improvements Did You Observe in the Code Quality, Readability, or Potential Robustness After Applying the Fixes?

The code became easier to read after I fixed the function names, removed unused imports, added docstrings, and corrected the formatting. The SQL query is also safer now because it uses parameters instead of directly combining input values with the query.

Adding input validation and checking whether a database record exists helped the program handle invalid inputs and missing records more appropriately. Replacing the subprocess call with `print()` also removed an unnecessary operation.

After making the changes, Pylint gave a score of 10.00/10, Bandit reported no issues, and Flake8 finished with exit code 0. This showed that the code passed the checks performed by these tools. However, I also understood that passing static analysis does not guarantee that the program is free of every bug, so testing is still necessary.
