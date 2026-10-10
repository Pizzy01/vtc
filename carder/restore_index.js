const fs = require('fs');
const path = require('path');

const logPath = '/Users/mind4peace/.gemini/antigravity/brain/32d4bd08-8bb9-445a-af18-86d53bcf8225/.system_generated/logs/transcript.jsonl';
const lines = fs.readFileSync(logPath, 'utf8').split('\n');

const fileLines = {};

lines.forEach(lineStr => {
  if (!lineStr.trim()) return;
  try {
    const step = JSON.parse(lineStr);
    if (step.type === 'VIEW_FILE' && step.content && step.content.includes('index.html')) {
      const content = step.content;
      const matchRange = content.match(/Showing lines (\d+) to (\d+)/);
      if (matchRange) {
        const start = parseInt(matchRange[1]);
        const end = parseInt(matchRange[2]);
        
        const contentLines = content.split('\n');
        contentLines.forEach(l => {
          const m = l.match(/^(\d+): (.*)/);
          if (m) {
            const lineNum = parseInt(m[1]);
            const originalLine = m[2];
            if (lineNum >= start && lineNum <= end) {
              fileLines[lineNum] = originalLine;
            }
          }
        });
      }
    }
  } catch (e) {
    // ignore
  }
});

const totalLines = 2715;
let output = '';
let missing = 0;
for (let i = 1; i <= totalLines; i++) {
  if (fileLines[i] !== undefined) {
    output += fileLines[i] + '\n';
  } else {
    console.log('Missing line:', i);
    missing++;
  }
}

if (missing === 0) {
  fs.writeFileSync('/Users/mind4peace/Downloads/carder/index.html', output);
  console.log('Successfully reconstructed index.html!');
} else {
  console.log('Failed: missing lines count:', missing);
}
