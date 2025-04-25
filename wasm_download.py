import os
import urllib.request
import site


def download():
    """
    Download WASM files from GitHub repository to standard location
    """
    # Base URL for GitHub repository
    base_url = "https://raw.githubusercontent.com/vitche/wasm_storage_timeline/main"
    wasm_url = f"{base_url}/storage_timeline.wasm"
    js_url = f"{base_url}/wasm_exec.js"

    # Determine the standard directory for WASM files
    if site.ENABLE_USER_SITE and os.path.exists(site.getusersitepackages()):
        base_dir = site.getusersitepackages()
    else:
        try:
            base_dir = site.getsitepackages()[0]
        except (IndexError, AttributeError):
            base_dir = os.getcwd()

    wasm_dir = os.path.join(base_dir, "wasm_storage_timeline")
    os.makedirs(wasm_dir, exist_ok=True)

    # File paths
    wasm_path = os.path.join(wasm_dir, "storage_timeline.wasm")
    js_path = os.path.join(wasm_dir, "wasm_exec.js")

    try:
        print(f"Downloading `storage_timeline.wasm` from {wasm_url}")
        # Create SSL context that doesn't verify certificates
        import ssl
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        # Download WASM file
        with urllib.request.urlopen(wasm_url, context=ssl_context) as response:
            wasm_content = response.read()
            with open(wasm_path, 'wb') as f:
                f.write(wasm_content)

        print(f"Downloading `wasm_exec.js` from {js_url}")
        # Download JS file
        with urllib.request.urlopen(js_url, context=ssl_context) as response:
            js_content = response.read()
            with open(js_path, 'wb') as f:
                f.write(js_content)

        print(f"WASM files downloaded successfully to {wasm_dir}")
    except Exception as e:
        print(f"Error downloading WASM files: {e}")
        print("Please download these files manually from:")
        print(f"  {wasm_url}")
        print(f"  {js_url}")
        print(f"And place them in: {wasm_dir}")
