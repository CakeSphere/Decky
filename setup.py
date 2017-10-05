from setuptools import setup

setup(
    name='decky',
    packages=['decky'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    setup_requires=['libsass >= 0.6.0'],
    sass_manifests={
        'myapp': ('static/sass', 'static/css', '/static/css')
    }
)
