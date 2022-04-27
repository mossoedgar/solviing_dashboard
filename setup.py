from setuptools import find_packages
from cx_Freeze import setup, Executable


options = {
    'build_exe': {
        'includes': [
            'cx_Logging', 'idna'
        ],
        'packages': [
            'asyncio', 'flask', 'jinja2', 'dash', 'plotly', 'waitress', 'pandas', 'numpy', 'datetime', 'plotly','mysql', 'mysql.connector', 'pymysql', 'sqlalchemy', 'sys', 'os','webbrowser', 'threading'
        ],
        'excludes': ['tkinter'],
        'include_files': [
            './assets/'
        ]
    }
}

executables = [
    Executable('run.py',
               base=None,
               targetName='solviingDashboard.exe')
]

setup(
    name='solviingDashboard',
    packages=find_packages(),
    version='0.1.0',
    description='dashboard',
    executables=executables,
    options=options
)