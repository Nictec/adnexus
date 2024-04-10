import pytest
from starlette.requests import Request
from starlette.responses import Response

from adnexus.integrations.starlette import InjectedRoute

async def homepage(request: Request) -> Response:
    pass

@pytest.mark.asyncio
def test_injected_route():
    InjectedRoute("/", homepage)


