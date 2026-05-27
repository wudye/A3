from app.core.setup_logging import setup_logging


logger = setup_logging(__name__)

def te():
    logger.info("test")
    logger.warning("why not work")
    return "from test temp nothinghappen"