'use strict';
const { execSync } = require('child_process');

try {
  const version = execSync('python --version', { encoding: 'utf8' }).trim();
  console.log(`ass-ade: Found ${version}`);
  console.log('ass-ade: Run "pip install ass-ade" if not already installed');
} catch {
  console.warn('ass-ade: Python not found. Install Python 3.12+ from https://python.org');
}
