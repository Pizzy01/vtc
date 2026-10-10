const fs = require('fs');
const path = require('path');

const logPath = '/Users/mind4peace/.gemini/antigravity/brain/32d4bd08-8bb9-445a-af18-86d53bcf8225/.system_generated/logs/transcript.jsonl';
const lines = fs.readFileSync(logPath, 'utf8').split('\n');

function decodeVal(val) {
  if (typeof val === 'string') {
    let s = val.trim();
    if (s.startsWith('"') && s.endsWith('"')) {
      try {
        return JSON.parse(s);
      } catch (e) {
        return s.substring(1, s.length - 1);
      }
    }
  }
  return val;
}

lines.forEach(lineStr => {
  if (!lineStr.trim()) return;
  try {
    const step = JSON.parse(lineStr);
    if (step.tool_calls) {
      step.tool_calls.forEach(tc => {
        if (tc.name === 'replace_file_content' || tc.name === 'write_to_file') {
          const file = decodeVal(tc.args.TargetFile);
          console.log(`Step ${step.step_index}: Tool=${tc.name} File=${file}`);
          if (tc.name === 'replace_file_content') {
            console.log(`  Target (first 100 chars):`, JSON.stringify(decodeVal(tc.args.TargetContent).substring(0, 100)));
            console.log(`  Replacement (first 100 chars):`, JSON.stringify(decodeVal(tc.args.ReplacementContent).substring(0, 100)));
          }
        }
      });
    }
  } catch (e) {
    // ignore
  }
});
