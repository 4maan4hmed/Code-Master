// script.js
// Calculator logic and UI event handling

/**
 * Calculator class handles the core arithmetic logic and state management.
 */
class Calculator {
  /**
   * @param {HTMLElement} displayElement - The element where the current value is shown.
   */
  constructor(displayElement) {
    this.displayElement = displayElement;
    this.clear();
  }

  /** Reset all calculator state. */
  clear() {
    this.currentInput = '';
    this.previousInput = '';
    this.operation = undefined;
  }

  /** Append a digit or decimal point to the current input.
   * @param {string} number - The character to append (e.g., "1", "2", ".").
   */
  appendNumber(number) {
    // Prevent multiple decimals
    if (number === '.' && this.currentInput.includes('.')) return;
    // Avoid leading zeros like "00" unless after a decimal point
    if (number === '0' && this.currentInput === '0') return;
    // If starting a new number after an operation, allow leading zero
    if (this.currentInput === '' && number === '.') {
      this.currentInput = '0.';
    } else {
      this.currentInput = this.currentInput.toString() + number.toString();
    }
  }

  /** Choose an arithmetic operation (+, -, *, /).
   * @param {string} operation - The operation symbol.
   */
  chooseOperation(operation) {
    if (this.currentInput === '' && this.previousInput === '') {
      // No number entered yet – nothing to do.
      return;
    }
    if (this.currentInput === '' && this.previousInput !== '') {
      // Allow changing the operation before entering the next number.
      this.operation = operation;
      return;
    }
    if (this.previousInput !== '') {
      this.compute();
    }
    this.operation = operation;
    this.previousInput = this.currentInput;
    this.currentInput = '';
  }

  /** Perform the pending computation and store the result in currentInput. */
  compute() {
    const prev = parseFloat(this.previousInput);
    const current = parseFloat(this.currentInput);
    if (isNaN(prev) || isNaN(current)) return;
    let computation = 0;
    switch (this.operation) {
      case '+':
        computation = prev + current;
        break;
      case '-':
        computation = prev - current;
        break;
      case '*':
        computation = prev * current;
        break;
      case '/':
        // Simple division by zero handling – show "Error"
        if (current === 0) {
          this.currentInput = 'Error';
          this.previousInput = '';
          this.operation = undefined;
          return;
        }
        computation = prev / current;
        break;
      default:
        return;
    }
    // Trim unnecessary decimal zeros (e.g., 5.0 -> 5)
    this.currentInput = Number.isInteger(computation) ? computation.toString() : computation.toString();
    this.previousInput = '';
    this.operation = undefined;
  }

  /** Update the display element with the current value. */
  updateDisplay() {
    // Show the current input if available, otherwise the previous input, otherwise 0.
    const text = this.currentInput || this.previousInput || '0';
    this.displayElement.textContent = text;
  }
}

// Wait for the DOM to be fully loaded before attaching listeners.
window.addEventListener('DOMContentLoaded', () => {
  const display = document.getElementById('display');
  if (!display) {
    console.error('Display element not found');
    return;
  }
  const calculator = new Calculator(display);

  // Helper to get the data-value attribute safely.
  const getValue = (el) => el.dataset.value;

  // Number buttons (including decimal). Excludes operators, equals, clear.
  const numberButtons = document.querySelectorAll('.button:not(.operator):not(.equals):not(.clear)');
  numberButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const value = getValue(button);
      if (value !== undefined) {
        calculator.appendNumber(value);
        calculator.updateDisplay();
      }
    });
  });

  // Operator buttons (+, -, *, /)
  const operatorButtons = document.querySelectorAll('.operator');
  operatorButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const op = getValue(button);
      if (op !== undefined) {
        calculator.chooseOperation(op);
        calculator.updateDisplay();
      }
    });
  });

  // Equals button
  const equalsButton = document.querySelector('.equals');
  if (equalsButton) {
    equalsButton.addEventListener('click', () => {
      calculator.compute();
      calculator.updateDisplay();
    });
  }

  // Clear button
  const clearButton = document.querySelector('.clear');
  if (clearButton) {
    clearButton.addEventListener('click', () => {
      calculator.clear();
      calculator.updateDisplay();
    });
  }

  // Optional: Keyboard support
  window.addEventListener('keydown', (e) => {
    const key = e.key;
    if ((key >= '0' && key <= '9') || key === '.') {
      e.preventDefault();
      calculator.appendNumber(key);
      calculator.updateDisplay();
    } else if (key === '+' || key === '-' || key === '*' || key === '/') {
      e.preventDefault();
      calculator.chooseOperation(key);
      calculator.updateDisplay();
    } else if (key === 'Enter' || key === '=') {
      e.preventDefault();
      calculator.compute();
      calculator.updateDisplay();
    } else if (key === 'Backspace') {
      e.preventDefault();
      // Simple backspace: remove last character from current input
      calculator.currentInput = calculator.currentInput.slice(0, -1);
      calculator.updateDisplay();
    } else if (key.toLowerCase() === 'c') {
      e.preventDefault();
      calculator.clear();
      calculator.updateDisplay();
    }
  });
});
