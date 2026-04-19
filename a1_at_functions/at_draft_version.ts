// Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_version.ts:5
// Component id: at.source.a1_at_functions.version  version: 0.1.0

try {
  const version = execSync('python --version', { encoding: 'utf8' }).trim();
  console.log(`ass-ade: Found ${version}`);
  console.log('ass-ade: Run "pip install ass-ade" if not already installed');
} catch {
  console.warn('ass-ade: Python not found. Install Python 3.12+ from https://python.org');
}
