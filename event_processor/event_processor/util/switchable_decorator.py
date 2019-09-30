class SwitchableDecorator:
    def __init__(self, enabled_func, enabled):
        self._enabled = enabled
        self._enabled_func = enabled_func

    def __call__(self, target):
        return self._enabled_func(target) if self._enabled else target