const StorageTimeline = (() => {
    let wasmInitialized = false;
    let goInstance = null;

    const Timeline = {
        initilize: async function (wasmUrl = "storage_timeline.wasm") {
            if (typeof Go === "undefined") {
                throw new Error("wasm_exec.js not found or not loaded.");
            }

            // Avoid double-initialization
            if (wasmInitialized) {
                return;
            }

            // Create a new Go instance
            goInstance = new Go();

            // Load the WASM file over HTTP and instantiate it
            const result = await WebAssembly.instantiateStreaming(
                fetch(wasmUrl),
                goInstance.importObject
            );

            // Run the Go instance
            goInstance.run(result.instance);

            wasmInitialized = true;
        },

        // load fetches a data file and calls the WASM parse method
        load: async function (dataUrl) {
            if (!wasmInitialized) {
                throw new Error("WASM not initialized. Call initilize() first.");
            }
            if (!dataUrl) {
                throw new Error("No data URL provided to load().");
            }

            // Fetch the binary data
            const resp = await fetch(dataUrl);
            if (!resp.ok) {
                throw new Error(`Failed to fetch data file: ${resp.statusText}`);
            }

            // Convert response to ArrayBuffer -> Uint8Array
            const buf = await resp.arrayBuffer();
            const dataBytes = new Uint8Array(buf);

            // Now call the WASM parse function, which is exposed under:
            //   window.StorageTimeline.Timeline.parse(...)
            // per the Go main.go code
            return window.StorageTimeline.Timeline.parse(dataBytes);
        },
    };

    // Return our component
    return {
        Timeline,
    };
})();

export default StorageTimeline;
