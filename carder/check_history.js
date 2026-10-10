const fs = require('fs');
const glob = require('path');

const historyDir = '/Users/mind4peace/Library/Application Support/Code/User/History/';
const folders = fs.readdirSync(historyDir);

folders.forEach(folder => {
  const entryPath = glob.join(historyDir, folder, 'entries.json');
  if (fs.existsSync(entryPath)) {
    try {
      const data = JSON.parse(fs.readFileSync(entryPath, 'utf8'));
      if (data.resource) {
        console.log(`Folder: ${folder} -> ${data.resource}`);
      }
    } catch (e) {
      // ignore
    }
  }
});
