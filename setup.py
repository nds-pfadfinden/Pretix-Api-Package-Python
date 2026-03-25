from setuptools import find_packages, setup

setup(
    name="Pretix_Api",
    version="0.1",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    install_requires=["requests"],
)
