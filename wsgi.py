from app import app as application
import server

if __name__ == "__main__":
    application.run_server(port=5000, debug = True)
