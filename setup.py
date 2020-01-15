import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="virtualvideo", # Replace with your own username
    version="0.1.0",
    author="Flashs",
    description="""virtualvideo allows you to write simple programs
                   that feed images to a v4l2loopback device""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="(GPL-3)",
    url="https://github.com/Flashs/virtualvideo",
    packages=setuptools.find_packages(),
    classifiers=[
        "v4l2loopback",
        "ffmpeg",
    ],
    install_requires=[
          'ffmpeg-python',
          "numpy"
    ],
    python_requires='>=3.6',
)