how do I set an env var so that it gets picked up by python 
To set an environment variable that can be picked up by a Python script, you can follow these steps depending on your operating system.

### On Unix-like systems (Linux, macOS)

1. **Temporary (for the current session):**
   ```sh
   export MY_VAR="my_value"
   ```
   Then run your Python script in the same terminal session:
   ```sh
   python my_script.py
   ```

2. **Permanent (for all sessions):**
   Add the `export` line to your shell profile file (e.g., `~/.bashrc` for Bash, `~/.zshrc` for Zsh):
   ```sh
   echo 'export MY_VAR="my_value"' >> ~/.bashrc
   source ~/.bashrc
   ```

### On Windows

1. **Temporary (for the current session):**
   ```cmd
   set MY_VAR=my_value
   ```
   Then run your Python script in the same command prompt:
   ```cmd
   python my_script.py
   ```

2. **Permanent (for all sessions):**
   Set the environment variable through the System Properties:
   - Open the Start Search, type in "env", and select "Edit the system environment variables".
   - Click the "Environment Variables" button.
   - In the "System variables" section, click "New..." and add your variable name and value.

### Accessing the Environment Variable in Python

In your Python script, you can access the environment variable using the `os` module:

```python
import os

my_var = os.getenv('MY_VAR')
print(f'MY_VAR: {my_var}')
```

This will print the value of `MY_VAR` that you set in your environment. If `MY_VAR` is not set, `os.getenv('MY_VAR')` will return `None`.

### Example

**Setting the environment variable temporarily (Unix-like systems):**
```sh
export MY_VAR="Hello, World!"
python my_script.py
```

**Python script (my_script.py):**
```python
import os

my_var = os.getenv('MY_VAR')
print(f'MY_VAR: {my_var}')
```

Output:
```
MY_VAR: Hello, World!
```

This method ensures that your Python script can read any environment variables you set in your operating system.
