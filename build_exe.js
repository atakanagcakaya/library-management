const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('Starting executable build process...');

// Check if Python is installed
try {
  console.log('Checking Python installation...');
  const pythonVersion = execSync('python --version').toString();
  console.log(`Python detected: ${pythonVersion}`);
} catch (error) {
  console.error('Python is not installed or not in PATH. Please install Python first.');
  process.exit(1);
}

// Install PyInstaller if not already installed
try {
  console.log('Installing PyInstaller...');
  execSync('python -m pip install pyinstaller', { stdio: 'inherit' });
  console.log('PyInstaller installed successfully.');
} catch (error) {
  console.error('Failed to install PyInstaller:', error.message);
  process.exit(1);
}

// Check if main.py exists
if (!fs.existsSync('main.py')) {
  console.error('main.py not found. Please make sure your main Python file is named "main.py".');
  process.exit(1);
}

// Check if icon file exists
const iconFile = 'app_icon.ico';
if (!fs.existsSync(iconFile)) {
  console.warn(`Warning: Icon file "${iconFile}" not found. The executable will use the default icon.`);
  console.log('Building executable without custom icon...');
  execSync('python -m PyInstaller --onefile --windowed main.py', { stdio: 'inherit' });
} else {
  console.log(`Building executable with custom icon "${iconFile}"...`);
  execSync(`python -m PyInstaller --onefile --windowed --icon=${iconFile} main.py`, { stdio: 'inherit' });
}

console.log('Build process completed.');
console.log('Your executable should be available in the "dist" folder.');