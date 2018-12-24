from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="clashroyaleapi",
    python_requies=">=3.6",
    version="0.2.0",
    description="A sync Python 3.6+ wrapper for RoyaleAPI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Games/Entertainment"
    ],
    keywords="clash royale cr crapi royaleapi",
    url="https://github.com/Tr-Jono/clashroyaleapi",
    author="Tr-Jono",
    author_email="omgthisissouseless@gmail.com",
    license="GNU General Public License v3.0",
    packages=find_packages(),
    install_requires=[
        "dataclasses; python_version<'3.7'",
        "requests"
    ],
    include_package_data=True,
    zip_safe=False
)
