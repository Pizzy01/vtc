const fs = require('fs');
const path = require('path');

const logPath = '/Users/mind4peace/.gemini/antigravity/brain/32d4bd08-8bb9-445a-af18-86d53bcf8225/.system_generated/logs/transcript.jsonl';
const content = fs.readFileSync(logPath, 'utf8');
const lines = content.split('\n');

let step9 = null;
let step11 = null;

lines.forEach(lineStr => {
  if (!lineStr.trim()) return;
  try {
    const step = JSON.parse(lineStr);
    if (step.step_index === 9) {
      step9 = step;
    }
    if (step.step_index === 11) {
      step11 = step;
    }
  } catch (e) {
    // ignore
  }
});

console.log('Step 9 found:', !!step9);
console.log('Step 11 found:', !!step11);

if (step9) {
  console.log('Step 9 content length:', step9.content ? step9.content.length : 0);
  console.log('Step 9 contains <truncated:', step9.content && step9.content.includes('<truncated'));
}
if (step11) {
  console.log('Step 11 content length:', step11.content ? step11.content.length : 0);
  console.log('Step 11 contains <truncated:', step11.content && step11.content.includes('<truncated'));
}
