let goInstance = null;
// TODO: This is derived from the previous
let wasmInitialized = false;

const initialize = async function (wasmUrl = "storage_timeline.wasm") {

    if (typeof Go === "undefined") {
        throw new Error("wasm_exec.js not found or not loaded.");
    }

    // Avoid double-initialization
    if (wasmInitialized) {
        return;
    }

    goInstance = new Go();

    // Handle different environments for fetching WASM
    let wasmModule;
    if (typeof window !== "undefined") {
        // Browser environment
        wasmModule = await WebAssembly.instantiateStreaming(fetch(wasmUrl), goInstance.importObject);
    } else {
        // Node.js environment
        const fs = await import("fs/promises");
        const wasmBuffer = await fs.readFile(wasmUrl);
        wasmModule = await WebAssembly.instantiate(wasmBuffer, goInstance.importObject);
    }

    goInstance.run(wasmModule.instance);
    wasmInitialized = true;
};

const TimeLine = async function (uri) {
    if (!wasmInitialized) {
        throw new Error("WASM not initialized. Call initialize() first.");
    }
    if (!uri) {
        throw new Error("No data URL provided to load().");
    }

    let dataBytes;
    if (typeof window !== "undefined") {
        // Fetch in browser
        const response = await fetch(uri, {
            method: "GET",
            headers: {
                "Content-Type": "application/storage-timeline",
            },
        });

        const buffer = await response.arrayBuffer();
        dataBytes = new Uint8Array(buffer);
    } else {
        // Fetch in Node.js (using fs)
        const fs = await import("fs/promises");
        dataBytes = new Uint8Array(await fs.readFile(uri));
    }

    return window.StorageTimeline.Timeline.parse(dataBytes);
};

const Schema = async function () {
    return TimeLine;
};

const Storage = async function () {
    this.initialize = initialize;
    return Schema;
};

export default Storage;
