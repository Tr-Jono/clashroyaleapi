from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name="clashroyaleapi",
    version="0.1.1",
    description="A RoyaleAPI Python wrapper.",
    long_description=long_description,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Games/Entertainment"
    ],
    keywords="clash royale cr crapi",
    url="https://github.com/Tr-Jono/clashroyaleapi",
    author="Trainer Jono",
    author_email="omgthisissouseless@gmail.com",
    license="GNU General Public License v3.0",
    packages=["royaleapi"],
    install_requires=[
        "requests"
    ],
    include_package_data=True,
    zip_safe=False
)
