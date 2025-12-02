#!/usr/bin/env python3
"""
Entrypoint wrapper for the bot. This tries several common entry functions
so deployments work even if the bot module uses a different convention.
"""
import importlib
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

def call_entry(module_name="bot"):
    try:
        mod = importlib.import_module(module_name)
    except Exception as e:
        logger.exception("Failed to import %s: %s", module_name, e)
        sys.exit(1)

    # Try common runnable function names
    for fn in ("main", "run", "start", "bot"):
        obj = getattr(mod, fn, None)
        if callable(obj):
            logger.info("Calling %s.%s()", module_name, fn)
            try:
                obj()
                return
            except Exception:
                logger.exception("Exception when calling %s.%s()", module_name, fn)
                sys.exit(1)

    # Try app.run() pattern (common in frameworks)
    app = getattr(mod, "app", None)
    if app is not None and hasattr(app, "run"):
        logger.info("Calling %s.app.run()", module_name)
        try:
            app.run()
            return
        except Exception:
            logger.exception("Exception when calling app.run()")
            sys.exit(1)

    logger.error(
        "No runnable entrypoint found in module '%s'. Expected one of: main/run/start/bot or app.run().",
        module_name,
    )
    sys.exit(1)

if __name__ == "__main__":
    call_entry()