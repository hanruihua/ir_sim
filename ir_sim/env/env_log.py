import logging

# Set the level of the root logger to INFO
logging.basicConfig(level=logging.WARNING)

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
w_handler = logging.StreamHandler()
e_handler = logging.FileHandler('sim_error.log')

w_handler.setLevel(logging.INFO)
e_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
w_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
e_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

w_handler.setFormatter(w_format)
e_handler.setFormatter(e_format)

# Add handlers to the logger
logger.addHandler(w_handler)
logger.addHandler(e_handler)

logger.warning('This is an error message')