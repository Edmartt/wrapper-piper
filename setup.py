from setuptools import find_packages, setup

setup(
        name='wrapper piper',
        version='1.0',
        long_description=__doc__,
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=['Flask']
    )

install_requires=[
    'Flask>=0.2',
    'SQLAlchemy>=0.6',
    'BrokenPackage>=0.7,<=1.0',
    'blinker==1.6.2',
    'click==8.1.3',
    'Flask==2.3.2',
    'gunicorn==20.1.0',
    'itsdangerous==2.1.2',
    'Jinja2==3.1.2',
    'MarkupSafe==2.1.3',
    'psycopg2-binary==2.9.6',
    'redis==4.6.0',
    'rq==1.15.1',
    'Werkzeug==2.3.6'
]
