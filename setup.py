from setuptools import setup

setup(
    name="SikuliPlusLibrary",
    version="0.1.0",
    license="Apache-2.0",
    author="Leonardo Sextare",
    author_email="leonardosextare@gmail.com",
    keywords="robotframework testing testautomation sikuli sikulix sikulilibrary",
    description="Robot Framework library for GUI automation using image recognition (wrapper of SikuliLibrary).",
    packages=["SikuliPlusLibrary"],
    install_requires=[
        "robotframework",
        "SikuliLibrary",
    ],
)