let golangInstance = null;

const TimeLine = async function (uri) {
    if (!golangInstance) {
        throw new Error("WASM not initialized. Call initialize() first.");
    }
    if (!uri) {
        throw new Error("No data URL provided to load().");
    }

    const response = await fetch(uri, {
        method: "GET",
        headers: {
            "Content-Type": "application/storage-timeline",
        },
    });
    const buffer = await response.arrayBuffer();
    const dataBytes = new Uint8Array(buffer);

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
        let wasmModule = await WebAssembly.instantiateStreaming(fetch(wasmUrl), golangInstance.importObject);
        golangInstance.run(wasmModule.instance);
    }

    schema() {
        return Schema;
    }
}
