import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WTFormsValidation-aresius", # Replace with your own username
    version="0.1",
    author="János Márkus",
    author_email="aresius423@gmail.com",
    description="A python library for generating client side validation functions from WTForms for FormValidation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Aresius423/WTFormsValidation",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
