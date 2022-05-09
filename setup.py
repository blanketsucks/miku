import setuptools

setuptools.setup(
    name='miku',
    author='blanketsucks',
    url='https://github.com/blanketsucks/miku',
    license='MIT',
    version='1.0.0',
    packages=['miku', 'miku.types'],
    install_requires=['aiohttp'],
    python_requires='>=3.8',
)