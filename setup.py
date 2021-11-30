import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vpack",
    version="0.0.10",
    author="Volltin",
    author_email="volltin@live.com",
    description="A package containing many useful utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/volltin/vpack",
    project_urls={
        "Bug Tracker": "https://github.com/volltin/vpack/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "colorama",
        "pygments"
    ]
)
