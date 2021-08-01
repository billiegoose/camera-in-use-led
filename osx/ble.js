#!/usr/bin/env node
var noble = require('noble-mac');

const cmd = process.argv[2];
var deviceName = "tinypico"
var serviceUUID = ["6e400001b5a3f393e0a9e50e24dcca9e"];
var characteristicUUIDs = [];

noble.on('stateChange', function(state) {
  if (state === 'poweredOn') {
    console.log(`Scanning for ${deviceName}...`);
    noble.startScanning();
  } else {
    console.log('Scanning stopped - is Bluetooth adapter connected / turned on?');
    noble.stopScanning();
  }
});

noble.on('discover', function(peripheral) {
  var advertisement = peripheral.advertisement;
  var localName = advertisement.localName;

  if (localName && localName.toLowerCase() == deviceName) {
    noble.stopScanning();

    console.log(`Connected to ${deviceName}`);

    connectToUart(peripheral);
  }
});

var uartReadChar = null;
var uartWriteChar = null;

function connectToUart(peripheral) {
  peripheral.once('disconnect', function() {
    console.log(`Disconnected.`);
    uartReadChar = null;
    uartWriteChar = null;
    process.exit(0);
  });

  peripheral.connect(function(err) {
      peripheral.discoverSomeServicesAndCharacteristics(
        serviceUUID,
        characteristicUUIDs, 
        function(err, services, characteristics) {
          for(i=0; i<characteristics.length; i++) {
            var char = characteristics[i];
            if (char.properties.includes('notify')) {
              uartReadChar = char;
              uartReadChar.subscribe(function(err) {
                console.log('subscribed')
                if (err) {
                  console.error(`Failed to subscribe to read characteristic: ${err}`);
                }

                uartWriteChar.write(Buffer.from(cmd, 'utf8'), false, function(err) {
                  if (err) {
                    console.error(`Failed to write data to write characteristic: ${err}`);
                  }
                });
              });
              uartReadChar.on('data', function(data) {
                res = data.toString('utf8');
                if (res === 'ack') {
                  uartReadChar.unsubscribe(function(err) {
                    if (err) {
                      console.error(`Failed to unsubscribe from read characteristic: ${err}`);
                    }
                    console.log('unsubscribed');
                    peripheral.disconnect();
                  });
                } else {
                  console.log(res);
                }
              });
            } else if (char.properties.includes('write')) {
              uartWriteChar = char;
            }
          }
        }
      );
  });
}
