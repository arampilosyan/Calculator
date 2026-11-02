# Advanced Calculator

A Python scientific calculator with a Streamlit interface, safe expression evaluation, unit conversion, constants, and calculation history.

## Features

- Arithmetic: `+`, `-`, `*`, `/`, `//`, `%`, `**`, parentheses
- Scientific functions: trigonometry, inverse trigonometry, logarithms, square root, factorial, hyperbolic functions, rounding
- Constants: `pi`, `e`, `tau`, `phi`, `inf`
- Unit conversion: length, mass, time, temperature, speed
- Session calculation history and a simple memory register
- Safe AST-based evaluator (does not use `eval`)
- Automated unit tests

## Requirements

- Python 3.10+
- pip

## Run on macOS / Linux

```bash
cd advanced_calculator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Run on Windows

```powershell
cd advanced_calculator
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The app opens in your browser, usually at `http://localhost:8501`.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Example expressions

```text
sqrt(144) + 5
sin(pi / 2)
log(1000) + ln(e)
factorial(5)
(25 ** 0.5) * 4
degrees(pi)
```

Angles are in radians. Use `degrees(x)` and `radians(x)` for conversion.

## Project structure

```text
advanced_calculator/
├── app.py
├── calculator.py
├── tests/
│   └── test_calculator.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## GitHub upload

Create a new empty repository on GitHub, then run these commands from this folder:

```bash
git init
git add .
git commit -m "Build advanced scientific calculator"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/advanced-calculator.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.

## Security note

Expressions are parsed with Python's AST and only a restricted set of numeric operations, constants, and approved math functions is permitted. This is intended as a local learning project, not a hardened multi-user computation service.
