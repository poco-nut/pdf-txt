print("Test script starting...")
print(f"Python version: {__import__('sys').version}")
print(f"Current dir: {__import__('os').getcwd()}")

# Try to import Flask
try:
    import flask
    print("Flask import OK")
except Exception as e:
    print(f"Flask import failed: {e}")

print("Test script finished.")