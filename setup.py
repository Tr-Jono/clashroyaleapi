from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name="clashroyaleapi",
    version="0.1.0",
    description="A Python wrapper for RoyaleAPI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Games/Entertainment"
    ],
    keywords="clash royale cr crapi royaleapi",
    url="https://github.com/Tr-Jono/clashroyaleapi",
    author="Tr-Jono",
    author_email="omgthisissouseless@gmail.com",
    license="GNU General Public License v3.0",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    include_package_data=True,
    zip_safe=False
)
