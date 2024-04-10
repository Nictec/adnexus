**XDI is a modern and declarative DI and IoC framework using pydantic for config and data.**

## Key features

- **Fast:** Very high performance thanks to pydantic and preemptive wiring
- **Developer friendly:** Declarative Container definition to take the "Magic" out of DI
- **Good compatibility:** Can be used with almost every framework and supports async

## Basic Example

```python3
from pathlib import Path
from datetime import datetime

from pydantic import BaseModel
from adnexus.containers import DeclarativeContainer
from adnexus.config_old.builtin import TOMLConfigLoader
from adnexus.providers import FactoryProvider
from adnexus.markers import Provide
from adnexus.decorators import inject


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
    # the loaded config can be accessed by calling MyContainer.config.<name>
    config_loaders = [
        TOMLConfigLoader(Path("settings.toml"))]  # <-- This file must (obviously) exist for the example to work
    config_model = MyConfig

    injectables = [
        FactoryProvider(TestInjectable, "Bob"),
        FactoryProvider(UpstreamInjectable)
    ]


if __name__ == "__main__":
    container = MyContainer()
    container.wire([__name__])

    test()  # <-- dependencies are injected automatically
```