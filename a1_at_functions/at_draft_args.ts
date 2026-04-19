// Extracted from C:/!ass-ade/bin/ass-ade.js:5
// Component id: at.source.ass_ade.args  version: 0.1.0

const { execFileSync } = require('child_process');

const args = process.argv.slice(2);

try {
  execFileSync('python', ['-m', 'ass_ade', ...args], {
    stdio: 'inherit',
    env: { ...process.env }
  });
} catch (err) {
  if (err.status) process.exit(err.status);
  // Python not found
  console.error('Error: Python 3.12+ is required. Install from https://python.org');
  console.error('Then: pip install ass-ade');
  process.exit(1);
}
