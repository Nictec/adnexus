# XDI

XDI is a modern and declarative DI and IoC framework using pydantic for config and data.

Key features:
- Fast: Very high performance thanks to pydantic and preemptive wiring
- Developer friendly: Declarative Container definition to take the "Magic" out of DI
- Compatibility: Can be used with almost every framework and supports async

## Example
```python3
from pathlib import Path
from pydantic import BaseModel
from xdi.containers import DeclarativeContainer
from xdi.config.builtin import TOMLConfigLoader
from xdi.providers import FactoryProvider
from datetime import datetime
from xdi.markers import Provide
from xdi.decorators import inject


class UpstreamInjectable:
    def __init__(self):
        self.time = datetime.now()

    def get_time(self):
        return self.time

class TestInjectable:
    def __init__(self, name: str, timer: Provide[UpstreamInjectable]):
        self.timer = timer
        self.name = name

    def greet(self):
        print(self.timer.get_time())
        return f"Hello {self.name}"
    
    
@inject
def test(greeter: Provide[TestInjectable]):
    print(greeter.greet())


class MyConfig(BaseModel):
    listen_addr: str
    listen_port: int
    


class MyContainer(DeclarativeContainer):
    config_loaders = [TOMLConfigLoader(Path("settings.toml"))] # <-- This file must (obviously) exist for the example to work
    config_model = MyConfig

    injectables = [
        FactoryProvider(TestInjectable, "Nicholas"),
        FactoryProvider(UpstreamInjectable)
    ]

if __name__ == "__main__":
    container = MyContainer()
    container.wire([__name__])

    test() # <-- dependencies are automatically injected
```