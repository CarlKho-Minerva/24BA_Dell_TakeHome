import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def init_app():
    app = create_app()

    # Ensure required directories exist
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    logger.info(f"Ensuring upload directory exists: {app.config['UPLOAD_FOLDER']}")

    return app

if __name__ == "__main__":
    app = init_app()
    logger.info("Starting Dell File Comparator application...")
    app.run(debug=True)
