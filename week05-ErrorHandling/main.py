from gui import LoginInterface
from backend import Backend

if __name__ == "__main__":
    backend = Backend()
    ui = LoginInterface(backend.verify_credentials)
    ui.main_loop()