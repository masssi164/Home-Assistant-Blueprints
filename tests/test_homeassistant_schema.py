"""Real HA schemas, only when explicitly requested; never simulated as passed."""
import os
import asyncio
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
    # HA 2026.10 schema validators require a running event loop,
    # including when checking templates and conditions. This is a
    # validation-only test: it does not execute script actions.
    async def validate():
        BLUEPRINT_SCHEMA(load(path))
        SCRIPT_ENTITY_SCHEMA(expand(path, inputs))

    asyncio.run(validate())
