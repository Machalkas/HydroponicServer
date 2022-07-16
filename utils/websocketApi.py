from typing import Any, Callable, Optional


class WebsocketApi:
    def __init__(self) -> None:
        self.handlers = {}
    
    def route(self, action: str):
        def wrapper(handler: Callable):
            self.handlers[action] = handler
        return wrapper
    
    def get_handler(self, action: str) -> Optional[Callable]:
        return self.handlers.get(action)
    
    def call_handler(self, child_self, request: dict) -> Optional[Any]:
        action = request.get("action")
        handler = self.get_handler(action)
        if handler is None:
            return None
        return handler(child_self, request)

        
