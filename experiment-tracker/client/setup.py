from setuptools import setup, find_packages

setup(
    name="experiment-tracker-client",
    version="0.1.0",
    description="Client SDK for Experiment Tracker",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.8",
)
