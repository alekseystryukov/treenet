import sys
import os

sys.path.append(os.getcwd())

if __name__ == "__main__":
    from app import app
    app.run(debug=True, host="0.0.0.0", port=3000)
