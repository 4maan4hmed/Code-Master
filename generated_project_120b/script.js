// Calculator script
const display = document.getElementById('display');
const buttons = document.querySelectorAll('.btn');

let currentInput = '';
let previousInput = '';
let operator = null;

function updateDisplay(value) {
  display.value = value;
}

function clearEntry() {
  currentInput = '';
  updateDisplay('');
}

function resetCalculator() {
  currentInput = '';
  previousInput = '';
  operator = null;
  updateDisplay('0');
}

function calculate() {
  if (!operator) return;
  const a = parseFloat(previousInput);
  const b = parseFloat(currentInput);
  let result;
  switch (operator) {
    case '+':
      result = a + b;
      break;
    case '-':
      result = a - b;
      break;
    case '*':
      result = a * b;
      break;
    case '/':
      result = b !== 0 ? a / b : 'Error';
      break;
    default:
      result = 'Error';
  }
  updateDisplay(result);
  previousInput = String(result);
  currentInput = '';
  operator = null;
}

function handleDigit(digit) {
  if (digit === '.' && currentInput.includes('.')) return;
  currentInput += digit;
  updateDisplay(currentInput);
}

function handleOperator(op) {
  // If no current input but there is a previous result, just change operator
  if (currentInput === '' && previousInput !== '') {
    operator = op;
    return;
  }
  // If we already have a pending operation, compute it first
  if (previousInput && operator) {
    calculate();
    // After calculate, previousInput now holds the result, keep it
    operator = op;
    return;
  }
  // No pending operation – store current input as previous and await next number
  previousInput = currentInput;
  currentInput = '';
  operator = op;
}

// Attach click listeners
buttons.forEach(btn => {
  btn.addEventListener('click', () => {
    const action = btn.dataset.action;
    const value = btn.dataset.value;
    switch (action) {
      case 'digit':
        handleDigit(value);
        break;
      case 'operator':
        handleOperator(value);
        break;
      case 'clear':
        clearEntry();
        break;
      case 'reset':
        resetCalculator();
        break;
      case 'equals':
        calculate();
        break;
    }
  });
});

// Keyboard support
document.addEventListener('keydown', e => {
  const key = e.key;
  if ((key >= '0' && key <= '9') || key === '.') {
    e.preventDefault();
    handleDigit(key);
  } else if (['+', '-', '*', '/'].includes(key)) {
    e.preventDefault();
    handleOperator(key);
  } else if (key === 'Enter' || key === '=') {
    e.preventDefault();
    calculate();
  } else if (key === 'Backspace') {
    e.preventDefault();
    clearEntry();
  } else if (key === 'Escape') {
    e.preventDefault();
    resetCalculator();
  }
});

// Initialize
resetCalculator();
