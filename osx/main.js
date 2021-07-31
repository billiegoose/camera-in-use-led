const { spawn } = require('child_process');
const path = require('path');

const stream = spawn('log', ['stream'])

stream.stdout.on('data', (data) => {
  const line = data.toString('utf8');
  if (line.includes('Post event kCameraStreamStart')) {
    console.log("Camera start");
    spawn('node', [path.join(__dirname, 'ble.js'), 'on,255,0,0,0.1'], { stdio: 'inherit' })
  }
  if (line.includes('Post event kCameraStreamStop')) {
    console.log("Camera stop");
    spawn('node', [path.join(__dirname, 'ble.js'), 'off'], { stdio: 'inherit' })
  }
});
