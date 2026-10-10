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

const edits = [];

lines.forEach(lineStr => {
  if (!lineStr.trim()) return;
  try {
    const step = JSON.parse(lineStr);
    if (step.tool_calls) {
      step.tool_calls.forEach(tc => {
        if (tc.name === 'replace_file_content') {
          const file = decodeVal(tc.args.TargetFile);
          if (file && (file.includes('ibr-luxury.html') || file.includes('index.html'))) {
            edits.push({
              step_index: step.step_index,
              target: decodeVal(tc.args.TargetContent),
              replacement: decodeVal(tc.args.ReplacementContent)
            });
          }
        }
      });
    }
  } catch (e) {
    // ignore
  }
});

// Sort edits in descending order of step_index to reverse them chronologically
edits.sort((a, b) => b.step_index - a.step_index);

console.log(`Found ${edits.length} edits to reverse.`);

// Read the customized content from ibr-luxury.html
let content = fs.readFileSync('/Users/mind4peace/Downloads/carder/ibr-luxury.html', 'utf8');

// Apply reversals
edits.forEach((edit, idx) => {
  const rep = edit.replacement;
  const tar = edit.target;
  
  // Normalize line endings to avoid \r\n issues
  const normContent = content.replace(/\r\n/g, '\n');
  const normRep = rep.replace(/\r\n/g, '\n');
  const normTar = tar.replace(/\r\n/g, '\n');
  
  if (normContent.includes(normRep)) {
    // Perform replacement on normalized content
    content = normContent.replace(normRep, normTar);
    console.log(`Reversing step ${edit.step_index} (${idx + 1}/${edits.length}): Success!`);
  } else {
    console.warn(`Reversing step ${edit.step_index} (${idx + 1}/${edits.length}): WARNING - Replacement content not found!`);
    console.warn(`Expected replacement text:\n${rep}\n`);
  }
});

// Save the restored content to index.html
fs.writeFileSync('/Users/mind4peace/Downloads/carder/index.html', content);
console.log('Done! Reconstructed original index.html.');
