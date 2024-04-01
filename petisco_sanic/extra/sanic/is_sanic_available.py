def is_sanic_available() -> bool:
    try:
        import sanic  # noqa
    except (RuntimeError, ImportError):
        return False
    return True
