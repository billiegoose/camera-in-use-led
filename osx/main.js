#!/usr/bin/env node

const { spawn, spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const stream = spawn('log', ['stream'])

stream.stdout.on('data', (data) => {
  const line = data.toString('utf8');
  if (line.includes('Post event kCameraStreamStart')) {
    console.log("Camera start");
    spawnSync('node', [path.join(__dirname, 'ble.js'), 'on,255,0,0,0.1'], { stdio: 'inherit' })
  }
  if (line.includes('Post event kCameraStreamStop')) {
    console.log("Camera stop");
    spawnSync('node', [path.join(__dirname, 'ble.js'), 'off'], { stdio: 'inherit' })
  }
});

setInterval(() => {
  let { stdout } = spawnSync('node', [path.join(__dirname, 'ble.js'), 'bat'], { encoding: 'utf8', stdio: 'pipe' })
  const matches = /subscribed\n(.*)\nunsubscribed/g.exec(stdout)
  const voltage = matches[1];
  console.log(`battery voltage: ${voltage}`);
  fs.appendFileSync('battery.log', `${voltage}, ${Date.now()}\n`);
}, 60_000);
