let golangInstance = null;

const TimeLine = async function (uri) {
    if (!golangInstance) {
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

export default class Storage {
    async initialize(wasmUrl = "storage_timeline.wasm") {

        if (typeof Go === "undefined") {
            throw new Error("wasm_exec.js not found or not loaded.");
        }

        golangInstance = new Go();

        // Handle different environments for fetching WASM
        let wasmModule;
        if (typeof window !== "undefined") {
            // Browser environment
            wasmModule = await WebAssembly.instantiateStreaming(fetch(wasmUrl), golangInstance.importObject);
        } else {
            // Node.js environment
            const fs = await import("fs/promises");
            const wasmBuffer = await fs.readFile(wasmUrl);
            wasmModule = await WebAssembly.instantiate(wasmBuffer, golangInstance.importObject);
        }

        golangInstance.run(wasmModule.instance);
    }

    schema() {
        return Schema;
    }
}
