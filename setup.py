import setuptools

setuptools.setup(
    name="miku",
    author='blanketsucks',
    url='https://github.com/blanketsucks/miku',
    license='MIT',
    version='0.1',
    packages=[
        'miku',
        'miku.sync'
    ],
    install_requires=[
        'requests',
        'aiohttp',
    ],
    python_requires='>=3.8',
)