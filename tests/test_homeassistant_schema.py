"""Real HA schemas, only when explicitly requested; never simulated as passed."""
import os
import pytest
from .support import CORE, RECIPE, CORE_INPUTS, expand, load

pytestmark = [pytest.mark.homeassistant,
              pytest.mark.skipif(os.getenv('REQUIRE_HOME_ASSISTANT') != '1',
                                 reason='Actual HA schema check requires explicit HA environment')]

@pytest.mark.parametrize('path,inputs', [(CORE, CORE_INPUTS),
                                        (RECIPE, {'engine_script':'script.coffee_engine'})])
def test_actual_homeassistant_schemas(path, inputs):
    # A missing dependency MUST fail, not skip, in the designated CI job.
    from homeassistant.components.blueprint.schemas import BLUEPRINT_SCHEMA
    from homeassistant.components.script.config import SCRIPT_ENTITY_SCHEMA
    BLUEPRINT_SCHEMA(load(path))
    SCRIPT_ENTITY_SCHEMA(expand(path, inputs))
