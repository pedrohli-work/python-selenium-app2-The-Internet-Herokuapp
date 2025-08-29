import json
import os
from typing import Any, Dict
from utils.logger import get_logger

logger = get_logger(__name__)


def load_config() -> Dict[str, Any]:
    """
    Load the JSON configuration file from the 'config' directory.

    This function reads 'config.json' located two directories above the current
    file in the 'config' folder, parses it, and returns a dictionary with
    configuration settings.

    Raises:
        RuntimeError: If the configuration file is missing or contains invalid JSON.

    Returns:
        Dict[str, Any]: The configuration dictionary loaded from JSON.
    """
    # Build the absolute path to the config.json file
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "config",
        "config.json"
    )

    try:
        # Open and parse the JSON config file
        with open(config_path, "r", encoding="utf-8") as file:
            config = json.load(file)
            logger.debug("Configuration loaded successfully from %s", config_path)
            return config
  
    except FileNotFoundError as exc:
        # Handle missing config file
        logger.error("Config file not found: %s", config_path)
        raise RuntimeError(f"Config file not found: {config_path}") from exc
    
    except json.JSONDecodeError as exc:
        # Handle invalid JSON syntax in config file
        logger.error("Config file is not valid JSON: %s", config_path)
        raise RuntimeError(f"Config file is not valid JSON: {config_path}") from exc

# Load configuration at module import
CONFIG: Dict[str, Any] = load_config()
