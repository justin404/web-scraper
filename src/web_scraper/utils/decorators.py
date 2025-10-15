"""
    Decorators
"""

class Singleton:
    """
    Credit: https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
    """
    def __init__(self, cls):
        self.clazz = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.clazz(*args, **kwargs)
        return self.instance
