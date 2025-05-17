## Running the Program Using Python

### Step 1: Make sure Python is installed

- Download and install Python from https://www.python.org/downloads/.
- **Important:** During installation, check the box **“Add Python to PATH”** to make running Python easier.

---

### Step 2: Open the program folder

- Find the folder where you saved the program files.
- Make sure `main.py` is inside this folder.

---

### Step 3: Open Command Prompt (Windows) or Terminal (macOS/Linux)

- On Windows: Press `Win + R`, type `cmd`, and press Enter.
- On macOS/Linux: Open your Terminal app.

---

### Step 4: Navigate to the program folder

Type the following command, replacing the path with your actual folder path:

```bash
cd path\to\your\program\folder
````

For example:

```bash
cd C:\Users\YourName\PycharmProjects\ASCII APP
```

*Note: On macOS/Linux, use `/` instead of `\` in the path.*

---

### Step 5: Run the program

Type:

```bash
python main.py
```

and press Enter.

---

### Troubleshooting common errors:

#### 1. Python command not found

If you see an error like:

```
'python' is not recognized as an internal or external command,
operable program or batch file.
```

**Solution:**

* Python is not installed or not added to your PATH.
* If you have Python installed, add it to your system PATH:

  * Search for **“Environment Variables”** in Windows Search.
  * Open **Edit the system environment variables**.
  * Click **Environment Variables**.
  * Under **System variables**, find and select **Path**, then click **Edit**.
  * Click **New** and add the full path where Python is installed.
    Example:
    `C:\Users\YourUsername\AppData\Local\Programs\Python\Python313\`
    and also add:
    `C:\Users\YourUsername\AppData\Local\Programs\Python\Python313\Scripts\`
  * Click **OK** on all windows.
  * Restart your Command Prompt and try again.

*WARNING*

If it *still* says Python isn’t found after adding Python to PATH, try these steps:

1. **Check Python Installation**
   Make sure Python is really installed:

   * Open a new Command Prompt and type:

     ```
     python --version
     ```
   * If you get a version number, Python is installed correctly.
   * If not, maybe Python wasn’t installed properly. Try reinstalling it from [https://www.python.org/downloads/].

2. **Verify PATH Environment Variable**

   * Open Command Prompt and type:

     ```
     echo %PATH%
     ```
   * Look for the Python install folder and Scripts folder in the output.
   * If not present, try adding them again carefully.

3. **Try Using `py` Launcher**
   Windows usually installs a `py` launcher with Python:

   * In Command Prompt, type:

     ```
     py main.py
     ```
   * This often runs Python even if `python` command doesn’t work.

4. **Check for Conflicting Installations or Aliases**

   * Sometimes Windows Store or other apps interfere with `python` command.
   * You can check installed apps and remove conflicting Python apps or aliases.

5. **Restart Your Computer**

   * Environment variable changes sometimes require a full restart.

6. **Use Full Path to Python**

   * If nothing works, run Python using its full path, for example:

     ```
     "C:\Users\YourUsername\AppData\Local\Programs\Python\Python313\python.exe" main.py
     ```

---

#### 2. Permission denied or access errors

* Make sure you have permission to run scripts in the folder.
* Try running Command Prompt as Administrator (right-click → Run as administrator).

---

#### 3. Syntax errors or crashes when running the script

* Ensure you’re running the script with the correct Python version (preferably Python 3.7 or newer).
* Double-check that the script files are complete and not corrupted.
* If errors show missing modules, you may need to install dependencies:

```bash
pip install -r requirements.txt
```

(Only if your project has a `requirements.txt` file.)

---

#### 4. Program window opens and closes immediately

* Run the program from the Command Prompt instead of double-clicking the file.
* This way, you can see any error messages before the window closes.