# Hybrid Rocket Simulator Setup Guide

## 1. Install Prerequisites

Make sure the following are installed **independently** on your system:

- [Git](https://git-scm.com/)
- [GitHub Account](https://github.com/)
- [VS Code](https://code.visualstudio.com/) or another code editor
- [Python 3.8+](https://www.python.org/)
- JS, HTML, and CSS support/extensions in your editor (recommended)

---

## 2. Clone the Repository

Open the terminal in **VS Code** (or your editor of choice).  
Navigate to the folder where you want to store the project:

```bash
cd /path/to/your/folder
```

Then run:

```bash
git clone https://github.com/scp15156402/Hybrid-Rocket-Code-IITB-Rocket-Team.git
```

---

## 3. Open the Project

After cloning, **open the cloned folder** in VS Code.
Also open the terminal inside VS Code in that folder.

---

## 4. Create and Activate Virtual Environment

Create a virtual environment:

```bash
python -m venv venv
```

Then activate it:

* **For Windows:**

  ```bash
  venv\Scripts\activate
  ```

* **For macOS/Linux:**

  ```bash
  source venv/bin/activate
  ```

---

## 5. Install Required Packages

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## Setup Complete

---

## To Run the App

Run the Flask app:

```bash
python app.py
```

Then open your browser and go to:

```
http://127.0.0.1:5000
```

or whatever link Flask prints in the terminal.

---