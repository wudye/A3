from app.core.setup_development_logging import setup_development_logging


logger = setup_development_logging(__name__)

def te():
    logger.info("test")
    logger.warning("why not work")
    return "from test temp nothinghappen"