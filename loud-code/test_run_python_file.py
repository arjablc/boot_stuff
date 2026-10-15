from functions.run_python_file import run_python_file


print(run_python_file("calculator", "main.py"))
print("\n")
print(run_python_file("calculator", "main.py", ["3 + 5"]))
print("\n")
print(run_python_file("calculator", "tests.py"))
print("\n")
print(run_python_file("calculator", "../main.py"))
print("\n")
print(run_python_file("calculator", "nonexistent.py"))
print("\n")
print(run_python_file("calculator", "lorem.txt"))
print("\n")
