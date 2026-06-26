from setuptools import setup

setup(
    name="anomaly-agent",
    version="1.0.0",
    py_modules=["main", "detector", "report", "agent"],
    install_requires=[
        "pandas",
        "rich",
        "click",
        "scipy",
        "ollama",
    ],
    entry_points={
        "console_scripts": [
            "anomaly-agent=main:analyze",
        ],
    },
)