from setuptools import setup, find_packages

setup(
    name="phantom",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        # List your package dependencies here
        # Example: 'requests>=2.24.0',
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
            # Add other development dependencies here
        ],
    },
    entry_points={
        "console_scripts": [
            "your_command=your_package_name.module:function",
            # Define console scripts here
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
