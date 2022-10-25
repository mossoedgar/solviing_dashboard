import sys, os
sys.path.append("/root/solviing_dashboard/")
import __init__
from __init__ import init_app

app = init_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
