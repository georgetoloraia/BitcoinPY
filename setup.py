from setuptools import setup, find_packages

setup(
    name="BitcoinPY",
    version="0.1.0",
    description="A Python implementation of a blockchain system with wallet and mining capabilities",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="George Toloraia",
    author_email="georgetoloraia@gmail.com",
    url="https://github.com/georgetoloraia/BitcoinPY",
    packages=find_packages(exclude=["tests", "docs"]),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    python_requires=">=3.7",
    install_requires=[
        "cryptography>=39.0.0",
        "flask>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=23.0",
            "flake8>=6.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "run_node=main:main",  # Run the main node from the `main.py` script
        ],
    },
    project_urls={
        "Bug Tracker": "https://github.com/georgetoloraia/BitcoinPY/issues",
        "Source Code": "https://github.com/georgetoloraia/BitcoinPY",
    },
)
