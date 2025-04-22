import site
import json
import os
import subprocess
import tempfile
import base64


class GoWasmRunner:
    """
    Class for running Go WebAssembly module through Node.js
    """

    def __init__(self):
        # Determine standard directory for WASM files
        if site.ENABLE_USER_SITE and os.path.exists(site.getusersitepackages()):
            base_dir = site.getusersitepackages()
        else:
            try:
                base_dir = site.getsitepackages()[0]
            except (IndexError, AttributeError):
                base_dir = os.getcwd()

        wasm_dir = os.path.join(base_dir, "wasm_storage_timeline")
        wasm_file = os.path.join(wasm_dir, "storage_timeline.wasm")
        wasm_exec = os.path.join(wasm_dir, "wasm_exec.js")

        if not (os.path.exists(wasm_file) and os.path.exists(wasm_exec)):
            raise FileNotFoundError(
                f"Could not find WASM files in {wasm_dir}. "
                "Ensure 'storage_timeline.wasm' and 'wasm_exec.js' are installed."
            )

        self.wasm_file_path = wasm_file
        self.wasm_exec_path = wasm_exec
        self.node_script_path = None
        self.initialize()

    def initialize(self):
        """Initializes Node.js environment for running Go WASM module"""
        # Create JavaScript code for loading and initializing Go WASM module
        node_script = """
        const fs = require('fs');

        // Load wasm_exec.js, which provides Go runtime for WASM
        const wasmExecPath = process.argv[2];
        eval(fs.readFileSync(wasmExecPath, 'utf8'));

        // Path to WASM file
        const wasmPath = process.argv[3];

        // Paths to input/output files
        const inputFilePath = process.argv[4];
        const outputFilePath = process.argv[5];
        const encodeType = process.argv[6] || ''; // 'base64' or empty string

        // Function to run main logic after loading WASM
        async function runWasm() {
            try {
                // Create Go environment
                const go = new Go();

                // Load and instantiate WASM module
                const wasmInstance = await WebAssembly.instantiate(
                    fs.readFileSync(wasmPath), 
                    go.importObject
                );

                // Run Go environment
                go.run(wasmInstance.instance);

                // Read data from file
                let inputData = fs.readFileSync(inputFilePath);

                // If base64 is specified, decode the data
                if (encodeType === 'base64') {
                    inputData = Buffer.from(inputData.toString(), 'base64');
                }

                // Call the parse function from Timeline
                const result = StorageTimeline.Timeline.parse(new Uint8Array(inputData));

                // Write result to output file
                fs.writeFileSync(outputFilePath, JSON.stringify(result, null, 2));

                process.exit(0);
            } catch (error) {
                console.error('Error in WASM execution:', error);
                process.exit(1);
            }
        }

        // Run main logic
        runWasm().catch(err => {
            console.error('Fatal error:', err);
            process.exit(1);
        });
        """

        # Create temporary file for Node.js script
        fd, self.node_script_path = tempfile.mkstemp(suffix='.js')
        os.write(fd, node_script.encode('utf-8'))
        os.close(fd)

    def parse_timeline(self, binary_data):
        """
        Process binary data using Go WASM module
        """
        try:
            # Encode binary data in base64 to avoid transfer issues
            encoded_data = base64.b64encode(binary_data)

            # Change Node.js script on the fly to pass data through file
            temp_input_file = tempfile.NamedTemporaryFile(delete=False, suffix='.bin')
            temp_input_path = temp_input_file.name
            temp_input_file.write(encoded_data)
            temp_input_file.close()

            temp_output_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
            temp_output_path = temp_output_file.name
            temp_output_file.close()

            # Run Node.js process with script and file paths
            process = subprocess.Popen(
                [
                    'node', self.node_script_path,
                    self.wasm_exec_path, self.wasm_file_path,
                    temp_input_path, temp_output_path, 'base64'
                ],
                stderr=subprocess.PIPE
            )

            # Wait for process completion
            _, stderr = process.communicate()

            if process.returncode != 0:
                # Execution error
                try:
                    error_message = stderr.decode('utf-8', errors='replace')
                except:
                    error_message = "Unknown error"

                raise Exception(f"Error processing WASM data: {error_message}")

            # Read result from file
            try:
                with open(temp_output_path, 'r') as f:
                    result_data = f.read()
                    return json.loads(result_data)
            except json.JSONDecodeError as json_err:
                raise Exception(f"JSON decoding error: {str(json_err)}. First 100 characters: {result_data[:100]}")
            finally:
                # Delete temporary files
                try:
                    os.unlink(temp_input_path)
                    os.unlink(temp_output_path)
                except:
                    pass

        except Exception as e:
            raise Exception(f"Error executing WASM: {str(e)}")

    def __del__(self):
        """Clean up temporary files when object is destroyed"""
        if self.node_script_path and os.path.exists(self.node_script_path):
            try:
                os.remove(self.node_script_path)
            except:
                pass
