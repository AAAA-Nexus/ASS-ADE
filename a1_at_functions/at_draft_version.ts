// Extracted from C:/!ass-ade/scripts/check-python.js:5
// Component id: at.source.ass_ade.version  version: 0.1.0


try {
  const version = execSync('python --version', { encoding: 'utf8' }).trim();
  console.log(`ass-ade: Found ${version}`);
  console.log('ass-ade: Run "pip install ass-ade" if not already installed');
} catch {
  console.warn('ass-ade: Python not found. Install Python 3.12+ from https://python.org');
}
