from setuptools import find_packages, setup

setup(
    name="lura",
    version="0.0.1",
    description="A viewer",
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["*.*"]},
    entry_points={
        "console_scripts": ["lura = lura.main:run"],
    },
)
