from setuptools import setup


def filter_requirements(fn):
    with open(fn) as fh:
        filtered_requirements = []
        for line in fh.readlines():
            if line[0] in ['#', ' ', '-']:
                continue
            filtered_requirements.append(line)
    return filtered_requirements


required = filter_requirements('requirements.txt')

required_test = filter_requirements('requirements-test.txt')

setup(
    name='eelifx',
    description='''
    EmptyEpsilon to Lifx Bridge
    ''',
    version='0.0.1',
    author='Chris Speck',
    author_email='cgspeck@gmail.com',
    url='https://www.chrisspeck.com/',
    packages=['eelifx'],
    install_requires=required,
    extras_require={
        'tests': required_test
    },
    entry_points='''
        [console_scripts]
        eelifx=eelifx.cli:root
    '''
)
