# Example usage

```sh
node osx/ble.js 'on,0,255,0,1' # Turn LED on, set color to bright green

node osx/ble.js 'off' # Turn LED off, set color to bright green

node osx/main.js # Monitors the webcam, turns LED red when in use, off when not in use
```

# Thanks

This is a hacked together mess from stack overflow and code examples from various sources:

- [MacOS - detect when camera is turned on/off](https://stackoverflow.com/questions/60535678/macos-detect-when-camera-is-turned-on-off/65098443#65098443)
- [Micropython BLE examples](https://github.com/micropython/micropython/tree/f6fd46c4024c28c827ccffd13dbe02b9ea74cfb8/examples/bluetooth)
- [bleterm2 source code](https://github.com/josschne/bleterm2/blob/f5eedccae85ac773f501e8f1c935c74f68d07148/index.js)

# License

MIT