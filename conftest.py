from __future__ import annotations
import platform
from pathlib import Path
from datetime import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from _pytest.nodes import Item
from _pytest.runner import CallInfo

# Optional imports for Chrome
try:
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.chrome.options import Options as ChromeOptions
except ImportError:
    ChromeService = ChromeOptions = None

# Optional imports for Firefox
try:
    from selenium.webdriver.firefox.service import Service as FirefoxService
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
except ImportError:
    FirefoxService = FirefoxOptions = None

from utils.config_loader import CONFIG
from utils.logger import get_logger

# ----------------------------
# Directories for reports/screenshots
# ----------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def _create_driver():
    """
    Factory function to create and configure a Selenium WebDriver
    based on settings in config.json.

    Supports Edge, Chrome, Firefox.
    Handles headless mode, window size, and page load timeout.
    
    Returns:
        WebDriver: Configured WebDriver instance.
    """
    logger = get_logger("driver_factory")

    # Read browser settings from config
    browser = str(CONFIG.get("browser", "edge")).lower()
    timeout = int(CONFIG.get("timeout", 10))
    headless = bool(CONFIG.get("headless", False))
    window_size = str(CONFIG.get("window_size", "1920,1080"))

    # Parse window size
    try:
        width, height = map(int, CONFIG.get("window_size", "1920,1080").split(","))
    except Exception as exc:
        raise RuntimeError(
            "config.json: 'window_size' must be 'WIDTH,HEIGHT' (e.g. '1920,1080')"
            ) from exc

    logger.info(
        "Initializing WebDriver | browser=%s headless=%s window_size =%s timeout=%s",
                browser, headless, window_size, timeout
                )

    # ----------------------------
    # Edge driver setup
    # ----------------------------
    if browser == "edge":
        # Detect OS
        system = platform.system().lower()  # 'windows', 'linux', 'darwin'

        # Get driver path for the current OS
        edge_path = CONFIG.get("drivers", {}).get("edge", {}).get(system)
        if not edge_path:
            raise RuntimeError(f"Edge driver path not defined in config.json for {system}")
        if not Path(edge_path).exists():
            raise FileNotFoundError(f"Edge driver not found for {system} at: {edge_path}")

        # Configure Edge options
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument(f"--window-size={width},{height}")

        # Create Edge WebDriver
        service = EdgeService(executable_path=edge_path)
        drv = webdriver.Edge(service=service, options=options)

    # ----------------------------
    # Chrome driver setup
    # ----------------------------
    elif browser == "chrome" and ChromeService and ChromeOptions:
        chrome_path = CONFIG.get("drivers", {}).get("chrome", {}).get("path")
        if not chrome_path:
            raise RuntimeError("Chrome path driver not defined in config.json under drivers.chrome.path")
        if not Path(chrome_path).exists():
            raise FileNotFoundError(f"Chrome driver not found at: {chrome_path}")
        
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument(f"--window-size={width},{height}")

        service = ChromeService(executable_path=chrome_path)
        drv = webdriver.Chrome(service=service, options=options)
    
    # ----------------------------
    # Firefox driver setup
    # ----------------------------
    elif browser == "firefox" and FirefoxService and FirefoxOptions:
        gecko_path = CONFIG.get("drivers", {}).get("firefox", {}).get("path")
        if not gecko_path:
            raise RuntimeError("Firefox driver path not defined in config.json under drivers.firefox.path")     
        if not Path(gecko_path).exists():
            raise FileNotFoundError(f"Gecko driver not found at: {gecko_path}")
        
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument(f"--width={width}")
        options.add_argument(f"--height={height}")

        service = FirefoxService(executable_path=gecko_path)
        drv = webdriver.Firefox(service=service, options=options)

        drv.set_window_size(width, height)
    
    else:
        raise ValueError(f"Unsupported or misconfigured browser in config.json: {browser}")
    
    # Set timeouts and implicit wait
    try:
        drv.set_page_load_timeout(timeout)
    except (ValueError, WebDriverException):
        logger.debug("Driver did not accept set_page_load_timeout(%s)", timeout, exc_info=True)
    
    drv.implicitly_wait(2)
    return drv


# ----------------------------
# Hook to attach result to test item
# ----------------------------
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item: Item, call: CallInfo):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


# ----------------------------
# Fixture: WebDriver
# ----------------------------
@pytest.fixture(scope="function")
def driver(request):
    """
    Provides a WebDriver instance for each test function.
    Takes screenshots on failure.
    Ensures proper driver quit.
    """
    logger = get_logger("tests.driver")
    drv = _create_driver()

    logger.info("WebDriver started for test: %s | browser=%s | headless=%s", 
                request.node.name,
                str(CONFIG.get("browser", "edge")).lower(),
                CONFIG.get("headless", False))

    try:
        yield drv

    finally:
        # Capture screenshot if test failed
        failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
        if failed:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            browser = str(CONFIG.get("browser", "edge")).lower()
            headless = CONFIG.get("headless", False)
            fname = f"{request.node.name}_{browser}_{'headless' if headless else 'gui'}_{timestamp}.png"
            fpath = SCREENSHOTS_DIR / fname
            try:
                drv.save_screenshot(str(fpath))
                logger.error("Test FAILED. Screenshot saved: %s", fpath, exc_info=True)
            except WebDriverException:
                logger.exception("Could not save screenshot", exc_info=True)

        # Quit driver
        try:
            drv.quit()
            logger.info("WebDriver quit successfully")
        except WebDriverException:
            logger.exception("Error quitting WebDriver", exc_info=True)


# ----------------------------
# Fixture: WebDriverWait
# ----------------------------
@pytest.fixture(scope="function")
def wait(driver):
    """
    Provides a WebDriverWait instance for explicit waits.
    Reads timeout from config.json.
    """
    timeout = CONFIG.get("timeout", 10)

    if not isinstance(timeout, (int, float)) or timeout <= 0:
        raise RuntimeError(
            f"config.json: 'timeout' must be a positive number, got {timeout}"
            )
    
    logger = get_logger("tests.driver")
    logger.debug("Creating WebDriver | timeout=%s for driver id=%s", timeout, id(driver))

    return WebDriverWait(driver, timeout)
