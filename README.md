# WASM `Storage.Timeline`

A minimal, cross-language example demonstrating how to compile Go code for WebAssembly and expose a custom timeline-parsing function in multiple environments, notably:

• JavaScript/TypeScript in Node.js or React.js.  
• Python (using a small helper for WASM execution).  

This project is designed to:  
• Read records from a binary file.  
• Parse them into a friendly list of “timestamp + value” objects.  
• Provide those records to higher-level interfaces for usage on the web, in Node.js scripts, or in Python.

--------------------------------------------------------------------------------

## Table of Contents

1. [Features](#features)  
2. [Installation](#installation)  
3. [Node.js / React.js Usage](#nodejs--reactjs-usage)  
   1. [Build Process](#build-process)  
   2. [Running Locally](#running-locally)  
   3. [Browser Usage Example](#browser-usage-example)  
4. [Python Usage](#python-usage)  
   1. [Installation in Python Environment](#installation-in-python-environment)  
   2. [Import and Usage Example in Python](#import-and-usage-example-in-python)  
5. [License](#license)  
6. [Author](#author)  

--------------------------------------------------------------------------------

## Features

• Written in Go, compiled to WebAssembly, enabling usage in JavaScript and Python.  
• A minimal timeline-parsing function exposed via a “Timeline” object, which can take a binary file or binary data and produce structured records.  
• Adaptable for both browser-based projects (React.js, standard JS) and server-side (Node.js, Python).  

--------------------------------------------------------------------------------

## Installation

### Requirements  
1. [Go 1.12+](https://go.dev/dl/) (with WebAssembly support).  
2. [Node.js](https://nodejs.org/) (v14 or higher) if you plan to run/build in JavaScript.  
3. [http-server](https://www.npmjs.com/package/http-server) globally installed (or another HTTP server) if you want to serve locally in the browser.  
4. (Optional) Python 3 if you want to parse the timeline in Python.  

--------------------------------------------------------------------------------

## Node.js / React.js Usage

### Build Process

1. Ensure Go, Node.js, and any needed local dependencies are installed.  
2. Clone or download this repository, then from your terminal:  
   • Run “npm install” (if additional local dependencies appear in package.json).  
   • Build the WASM and copy wasm_exec.js by running:  
     › npm run build  
     or  
     › ./build.sh  

   This compiles main.go to storage_timeline.wasm and copies wasm_exec.js into your working directory.

### Running Locally

1. Serve the directory (for example using http-server):  
   › npm run start  
2. Open your web browser to:  
   http://localhost:8080/  

You can then browse or open an index.html that references “storage_timeline.wasm” and “wasm_exec.js”.

### Browser Usage Example

After building, you will have:

• storage_timeline.wasm  
• wasm_exec.js  
• main.js  

In a browser environment:

1. Include “wasm_exec.js” in a <script> tag.  
2. Include “main.js” in another <script> tag.  
3. Ensure “storage_timeline.wasm” is served from the same directory (or specify the path to it).  
4. Once the page loads, call “initialize()” to set up the WASM environment. Then you can handle your binary data with the exposed parse method.

Example (in your browser console or script):
  
--------------------------------------------------------------------------------
<script>
  // Ensure that storage_timeline.wasm and wasm_exec.js are available.
  // main.js exposes the Storage class globally under window.StorageTimeline.Storage.
  
  (async function() {
    await window.StorageTimeline.Storage.initialize();  
    const Schema = await window.StorageTimeline.Storage();  
    const TimeLine = await Schema();  
    const records = await TimeLine("test_data.bin");  
    console.log('Parsed Records:', records);
  })();
</script>
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------

## Python Usage

### Installation in Python Environment

To use this project within Python, you have a few options:

1. From source:  
   • Make sure you have Python 3 installed.  
   • (Optional) Create a new virtual environment:  
        python -m venv venv  
        source venv/bin/activate  
   • Install the current project:  
        python setup.py install  

2. Or, if you generate / have a wheel, you can install using pip:  
   • pip install wasm_storage_timeline-1.0.3-py3-none-any.whl  
     (Adjust version/filename as needed.)

### Import and Usage Example in Python

Once you have installed, you can parse timeline data from Python. Under the hood, the library uses Node.js to execute the WASM module through a helper class (wasm_execute.WASMExecutor).

--------------------------------------------------------------------------------
Example usage (pseudo-code):

    from wasm_execute import WASMExecutorFactory

    # Acquire a single executor instance (singleton)
    executor = WASMExecutorFactory.instance()

    # Load binary data
    with open("test_data.bin", "rb") as f:
        binary_data = f.read()

    # Parse into structured records
    records = executor.parse_timeline(binary_data)

    print("Parsed Records:", records)
--------------------------------------------------------------------------------

• The parse_timeline() method returns a Python list of records in JSON-compatible format.  
• If you need to download or update the WASM files, the setup process automatically attempts it. You can also manually call:  
    python -c "import wasm_download; wasm_download.download()"  

--------------------------------------------------------------------------------

## License

This project is licensed under [LGPL-3.0-or-later](https://www.gnu.org/licenses/lgpl-3.0.html). For more details, see the “license” field in [package.json](./package.json).

--------------------------------------------------------------------------------

## Author

Made with ♥ by Vitche Research Team Developer  

--------------------------------------------------------------------------------

Enjoy using “Storage.Timeline” in your web or Python projects! Feel free to open issues or pull requests if you have suggestions or improvements.

