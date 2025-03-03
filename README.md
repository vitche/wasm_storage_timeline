# WASM `Storage.Timeline`

A minimal example demonstrating how to compile Go code for WebAssembly and expose a custom timeline-parsing function in the browser (or Node.js). This project is designed to:

• Read records from a binary file.  
• Parse them into a JavaScript-friendly structure.  
• Provide those records to a higher-level interface for usage in web environments or Node.js scripts.

## Installation

1. Make sure you have [Go 1.12+](https://go.dev/dl/) installed (the version must support WebAssembly).
2. Have [Node.js](https://nodejs.org/) (v14 or higher) installed.
3. Install [http-server](https://www.npmjs.com/package/http-server) globally or use any other static server you prefer.

---

## Build Process

Clone or download this repository. Then, from your terminal:

1. Run "npm install" (if you need any additional local dependencies).
2. Build the WASM and copy wasm_exec.js:  
   » npm run build  
   or  
   » ./build.sh

This compiles main.go to storage_timeline.wasm and copies wasm_exec.js into your working directory.

---

## Running Locally

To serve and test in the browser:

1. Execute:  
   » npm run start
2. Open your web browser to:  
   http://localhost:8080/

This will serve index.html (if present) or allow direct file browsing. You can then include and use the "storage_timeline.wasm" and "wasm_exec.js" in your web page.

---

## Usage

After building, you will have the following structure:  
• storage_timeline.wasm  
• wasm_exec.js  
• main.js

In a browser environment:

1. Include "wasm_exec.js" in a <script> tag.
2. Include "main.js" in another <script> tag.
3. Ensure "storage_timeline.wasm" is served from the same directory (or specify the path to it).
4. Once the page loads, call initialize() to set up the WASM environment. Afterward, you can handle your binary data with the exposed parse method.

For example, from the browser console or script:

```javascript
await window.StorageTimeline.Storage.initialize();  
const Schema = await window.StorageTimeline.Storage();  
const TimeLine = await Schema();  
const records = await TimeLine("test_data.bin");  
console.log('Parsed Records:', records);  
```

---

## License

This project is licensed under [LGPL-3.0-or-later](https://www.gnu.org/licenses/lgpl-3.0.html). For more details, see the "license" field in [package.json](./package.json).

---

Made with ♥ by Vitche Research Team Developer  
