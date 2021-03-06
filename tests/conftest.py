import pytest
from pathlib import Path

from .context import deploy

def pytest_addoption(parser):
    """
    Define the commandline params that can be passed to pytest.
    """
    parser.addoption(
        "--hub-name",
        action="store",
        default="staging"
    )
    parser.addoption(
        "--cluster-name",
        action="store",
        default="2i2c"
    )
    parser.addoption(
        "--api-token",
        action="store",
        default="secret"
    )

@pytest.fixture()
def hub(request):
    """
    Fixture returning a Hub object.

    Uses the hub-name and cluster-name cmd params to identify the hub
    in hubs.yaml config file.
    """
    hub_name = request.config.getoption("--hub-name")
    cluster_name = request.config.getoption("--cluster-name")
    
    config_file_path = Path(__file__).parent.parent / "hubs.yaml"
    clusters = deploy.parse_clusters(config_file_path)
 
    cluster = next((cluster for cluster in clusters if cluster.spec['name'] == cluster_name), None)
    hubs = cluster.hubs
    hub = next((hub for hub in hubs if hub.spec['name'] == hub_name), None)

    return hub

@pytest.fixture()
def api_token(request):
    """
    Fixture returning the service api token passed as a cmd param.
    """
    return request.config.getoption("--api-token")
