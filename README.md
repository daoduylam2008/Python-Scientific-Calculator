# Python Scientific Calculator

A desktop scientific calculator built with Python and Tkinter, supporting standard arithmetic, trigonometric functions, and advanced equation solving.

## Features

- **Standard Arithmetic** — addition, subtraction, multiplication, division, exponentiation
- **Scientific Functions** — sin, cos, tan, cotangent, square root, cube root, π
- **Equation Solving Modes:**
  - Linear equations (`ax + b = 0`)
  - Quadratic equations (`ax² + bx + c = 0`)
  - Cubic equations (`ax³ + bx² + cx + d = 0`)
  - Systems of 2 equations with 2 unknowns (`x`, `y`)
  - Systems of 3 equations with 3 unknowns (`x`, `y`, `z`)

## Requirements

- Python 3.x
- `tkinter` (included in the Python standard library)
- `numpy` (auto-installed on first run if missing)

## Download & Installation

### Option 1: Clone with Git
```bash
git clone https://github.com/daoduylam2008/Python-Scientific-Calculator.git
cd your-repo-name
```

### Option 2: Download ZIP
1. Go to the repository page on GitHub.
2. Click the green **Code** button.
3. Select **Download ZIP**.
4. Extract the ZIP file to a folder of your choice.

### Option 3: Direct file download
Download `main.py` directly and place it in a folder on your machine.

---

Once downloaded:

1. Ensure Python 3 is installed — download it from [python.org](https://www.python.org/downloads/) if needed.
2. Run the script — `numpy` will be installed automatically if not present.

```bash
python main.py
```

## Usage

### Standard Calculations
Type an expression directly using the on-screen buttons or your keyboard and press `=` to evaluate. Supported operators include `+`, `-`, `*`, `/`, `^` (exponent), `√` (square root), and `π`.

### Equation Modes
Select a mode using the mode button to populate a template in the input field, then replace the placeholder coefficients (`a`, `b`, `c`, etc.) with numbers and press `=`.

| Mode | Template |
|------|----------|
| Standard | _(blank)_ |
| Quadratic | `ax^(2) + bx + c` |
| Cubic | `ax^(3) + bx^2 + cx + d` |
| 2-variable system | `ax + by = c` / `dx + ey = f` |
| 3-variable system | `ax + by + cz = d` / ... |

### Keyboard Shortcut
Press **Enter** to evaluate the current expression (equivalent to pressing `=`).

### Buttons
| Button | Action |
|--------|--------|
| `AC` | Clear all input |
| `DEL` | Delete the last character |
| `=0` | Append `=0` (for equation solving) |
| `x` | Insert variable `x` |

## Project Structure

```
main.py
├── Mathematical helpers     # sin, cos, tan, cotg, cbrt
├── Equation solvers         # Linear, quadratic, cubic, systems
├── TextWithVar              # Custom Tkinter Text widget with StringVar binding
├── Calculator (Frame)       # Main UI class
└── main()                   # Entry point
```

## Notes

- Trigonometric functions expect input in **degrees**.
- The calculator uses Python's `eval()` for standard expression parsing — avoid inputting untrusted expressions.
- Cubic equation solving uses an approximation method and may have reduced accuracy for some edge cases.
