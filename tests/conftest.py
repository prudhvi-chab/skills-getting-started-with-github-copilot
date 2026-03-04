import copy
import pytest

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities dictionary before each test.

    The application stores state in the global `activities` dict in
    `src.app`.  We take a deep copy of the original data the first time
    this fixture runs and then clear/restore it for every subsequent
    invocation.  This keeps tests deterministic and isolated.
    """

    # capture a pristine snapshot on first use
    if not hasattr(app_module, "_orig_activities"):
        app_module._orig_activities = copy.deepcopy(app_module.activities)

    # wipe and restore
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(app_module._orig_activities))

    yield
