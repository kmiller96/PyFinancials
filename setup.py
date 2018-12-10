from setuptools import setup

setup(
    name='PyFinancials',
    version='0.1.1',
    description="A framework that builds fully-working, editable financial models in Excel so you don't have to.",
    url='https://github.com/kmiller96/PyFinancials',
    author='Kale Miller',
    author_email='me@kalelewismiller.com',
    license='MIT',
    packages=['pyfinancials'],
    install_requires=[
        "openpyxl"
    ],
    zip_safe=False
)
