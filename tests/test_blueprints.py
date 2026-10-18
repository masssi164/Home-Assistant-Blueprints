"""Static contracts and simulated branches of the actual distributed YAML."""
from copy import deepcopy

import pytest

from .support import (CORE, RECIPE, CORE_INPUTS, ON, STANDBY, READY, RUN,
                      INACTIVE, Input, Runner, expand, input_definitions, load)


def engine(*, args=None, **inputs):
    return Runner(expand(CORE, {**CORE_INPUTS, 'dry_run': False, **inputs}), args)


def test_default_is_no_device_writes():
    runner = Runner(expand(CORE, CORE_INPUTS))
    result = runner.run()
    assert not result.error
    assert result.response['status'] == 'dry_run'
    assert runner.machine_calls == []


def test_no_implicit_power_on_by_default():
    runner = engine()
    runner.states['select.coffee_power'] = STANDBY
    runner.states['sensor.coffee_operation'] = INACTIVE
    assert runner.run().error
    assert not runner.machine_calls


@pytest.mark.parametrize('beverage', ['Coffee', 'Espresso', 'Cappuccino', 'LatteMacchiato', 'HotWater'])
def test_all_original_beverage_programs(beverage):
    runner = engine(args={'beverage_type': beverage})
    assert not runner.run().error
    assert len(runner.starts) == 1
    data = runner.starts[0]['data']
    assert data['device_id'] == 'test-coffee-device'
    assert data['program_key'] == 'ConsumerProducts.CoffeeMaker.Program.Beverage.' + beverage
    assert data['validate'] is True
    assert data['options'] == []


def test_absent_runtime_beverage_defaults_to_coffee():
    runner = engine()
    assert not runner.run().error
    assert runner.starts[0]['data']['program_key'].endswith('.Coffee')


@pytest.mark.parametrize('beverage', ['', None, 'OtherProgram', 'coffee', 12, ['Coffee']])
def test_unknown_beverage_never_starts(beverage):
    runner = engine(args={'beverage_type': beverage})
    assert runner.run().error
    assert not runner.machine_calls


@pytest.mark.parametrize('entity', list(CORE_INPUTS.values()))
@pytest.mark.parametrize('value', ['unknown', 'unavailable'])
def test_unavailable_entities_fail_closed(entity, value):
    runner = engine()
    runner.states[entity] = value
    assert runner.run().error
    assert not runner.machine_calls


def test_offline_fails():
    runner = engine()
    runner.states['binary_sensor.coffee_connected'] = 'off'
    assert runner.run().error
    assert not runner.machine_calls


@pytest.mark.parametrize('entity', list(CORE_INPUTS.values()))
def test_cross_device_mapping_is_rejected(entity):
    runner = engine()
    runner.devices[entity] = 'other-device'
    assert runner.run().error
    assert not runner.machine_calls


def test_missing_device_registry_link_is_rejected():
    runner = engine()
    runner.devices.pop('binary_sensor.coffee_connected')
    assert runner.run().error
    assert not runner.machine_calls


def test_server_translated_states_fail_with_explanation():
    runner = engine()
    runner.states['select.coffee_power'] = 'Ein'
    result = runner.run()
    assert result.error and 'Local' in result.message
    assert not runner.machine_calls


@pytest.mark.parametrize('state', ['Run', 'Pause', 'DelayedStart'])
def test_busy_machine_not_queued(state):
    runner = engine()
    runner.states['sensor.coffee_operation'] = 'BSH.Common.EnumType.OperationState.' + state
    assert runner.run().error
    assert not runner.machine_calls


def test_local_control_blocks_start_and_power():
    runner = engine(auto_power_on=True)
    runner.states['binary_sensor.coffee_local_control'] = 'on'
    runner.states['select.coffee_power'] = STANDBY
    assert runner.run().error
    assert not runner.machine_calls


def test_remote_permission_is_required():
    runner = engine()
    runner.states['binary_sensor.coffee_remote_start'] = 'off'
    assert runner.run().error
    assert not runner.starts


def test_missing_ready_aborts_without_start():
    runner = engine()
    runner.states['sensor.coffee_operation'] = 'BSH.Common.EnumType.OperationState.ActionRequired'
    assert runner.run().error
    assert not runner.starts


def test_explicit_power_on_then_one_start():
    runner = engine(auto_power_on=True)
    runner.states['select.coffee_power'] = STANDBY
    runner.states['sensor.coffee_operation'] = INACTIVE
    assert not runner.run().error
    assert [c['action'] for c in runner.machine_calls] == ['select.select_option','home_connect_alt.start_program']


def test_power_timeout_does_not_start():
    runner = engine(auto_power_on=True)
    runner.states['select.coffee_power'] = STANDBY
    runner.states['sensor.coffee_operation'] = INACTIVE
    runner.power_succeeds = False
    assert runner.run().error
    assert not runner.starts


def test_invalid_power_select_options_do_not_write():
    runner = engine(auto_power_on=True)
    runner.states['select.coffee_power'] = STANDBY
    runner.attrs['select.coffee_power']['options'] = ['Ein']
    assert runner.run().error
    assert not runner.machine_calls


def test_dry_run_does_not_power_on_even_when_enabled():
    runner = engine(dry_run=True, auto_power_on=True)
    runner.states['select.coffee_power'] = STANDBY
    runner.states['sensor.coffee_operation'] = INACTIVE
    assert not runner.run().error
    assert not runner.machine_calls


def test_caller_cannot_override_blueprint_configuration():
    runner = engine(args={'cfg_device': 'other', 'cfg_connection': 'binary_sensor.other',
                          'cfg_dry_run': False, 'cfg_allowed': ['Delete'], 'cfg_power': 'select.other'},
                    dry_run=True)
    assert not runner.run().error
    assert not runner.machine_calls
    assert runner.vars['cfg_device'] == 'test-coffee-device'


def test_no_start_ack_holds_lock_and_does_not_retry():
    runner = engine(finish_timeout=300)
    runner.start_succeeds = False
    result = runner.run()
    assert result.error
    assert len(runner.starts) == 1
    assert runner.delays == [{'seconds': 300}]


def test_finish_timeout_is_not_success():
    runner = engine()
    runner.finish_succeeds = False
    assert runner.run().error
    assert len(runner.starts) == 1


def test_api_error_is_not_suppressed_or_retried():
    runner = engine()
    runner.start_error = True
    with pytest.raises(RuntimeError, match='API failure'):
        runner.run()
    assert len(runner.starts) == 1


FILL = 'ConsumerProducts.CoffeeMaker.Option.FillQuantity'
BEANS = 'ConsumerProducts.CoffeeMaker.Option.BeanAmount'
TEMP = 'ConsumerProducts.CoffeeMaker.Option.CoffeeTemperature'

@pytest.mark.parametrize('options', [None, {}, '[]', [None], [{'key': FILL}],
    [{'key': 'Other', 'value': 5}], [{'key': FILL,'value':True}],
    [{'key': FILL,'value':0}], [{'key': FILL,'value':-10}], [{'key': FILL,'value':1001}],
    [{'key': FILL,'value':25.2}], [{'key': FILL,'value':'50'}],
    [{'key':FILL,'value':50},{'key':FILL,'value':100}],
    [{'key':BEANS,'value':'Strong'}], [{'key':TEMP,'value':85}],
    [{'key':FILL,'value':50,'extra':False}]])
def test_bad_options_rejected_without_machine_writes(options):
    runner = engine(args={'program_options': options})
    assert runner.run().error
    assert not runner.machine_calls


def test_explicit_recipe_options_reach_same_start_request():
    options = [{'key': FILL,'value':150},
               {'key':BEANS,'value':'ConsumerProducts.CoffeeMaker.EnumType.BeanAmount.Strong'},
               {'key':TEMP,'value':'ConsumerProducts.CoffeeMaker.EnumType.CoffeeTemperature.High'}]
    runner = engine(args={'program_options':options})
    assert not runner.run().error
    assert runner.starts[0]['data']['options'] == options


def test_coffee_options_are_rejected_for_hot_water():
    runner = engine(args={'beverage_type':'HotWater', 'program_options':[
        {'key':TEMP, 'value':'ConsumerProducts.CoffeeMaker.EnumType.CoffeeTemperature.High'}]})
    assert runner.run().error
    assert not runner.starts


def test_modes_and_single_core_call_contract():
    assert load(CORE)['mode'] == 'single'
    assert load(RECIPE)['mode'] == 'single'
    config = expand(RECIPE, {'engine_script':'script.coffee_engine'})
    runner = Runner(config)
    assert not runner.run().error
    assert len(runner.machine_calls) == 1
    assert runner.machine_calls[0]['action'] == 'script.coffee_engine'
    assert runner.machine_calls[0]['data'] == {'beverage_type':'Coffee','program_options':[]}


def test_recipe_customization_builds_native_options_list():
    runner = Runner(expand(RECIPE, {'engine_script':'script.coffee_engine',
        'fill_quantity':150, 'beverage_type':'Espresso'}))
    assert not runner.run().error
    assert runner.machine_calls[0]['data']['program_options'] == [{'key':FILL,'value':150}]


def test_recipe_self_reference_and_missing_engine_are_blocked():
    for entity in ('script.test_script','script.missing'):
        runner = Runner(expand(RECIPE, {'engine_script':entity}))
        assert runner.run().error
        assert not runner.machine_calls


def test_input_references_resolve_and_selectors_exist():
    for path, supplied in ((CORE, CORE_INPUTS), (RECIPE, {'engine_script':'script.coffee_engine'})):
        bp = load(path)
        assert bp['blueprint']['domain'] == 'script'
        assert all('selector' in spec for spec in input_definitions(bp).values())
        expand(path, supplied)


def test_integer_valued_float_quantity_normalized_for_api():
    runner=engine(args={'program_options':[{'key':FILL,'value':150.0}]})
    assert not runner.run().error
    value=runner.starts[0]['data']['options'][0]['value']
    assert type(value) is int and value == 150


@pytest.mark.parametrize('entity', ['binary_sensor.coffee_remote_start','binary_sensor.coffee_local_control'])
def test_non_binary_safety_state_aborts(entity):
    runner=engine(auto_power_on=True)
    runner.states[entity]='not-a-binary-state'
    assert runner.run().error
    assert not runner.machine_calls


def test_connection_loss_during_readiness_wait_does_not_start():
    runner=engine()
    runner.states['binary_sensor.coffee_remote_start']='off'
    runner.wait_changes['Begrenzt auf Fernstartbereitschaft warten']={'binary_sensor.coffee_connected':'off'}
    assert runner.run().error
    assert not runner.starts


def test_connection_loss_during_cycle_is_not_success():
    runner=engine()
    runner.wait_changes['Gemeinsame single-Sperre bis zum beobachteten Laufende halten']={'binary_sensor.coffee_connected':'off'}
    assert runner.run().error
    assert len(runner.starts)==1


@pytest.mark.parametrize('state', ['Run', 'Pause', 'DelayedStart'])
def test_other_activity_while_waiting_is_not_queued(state):
    runner = engine()
    runner.states['binary_sensor.coffee_remote_start'] = 'off'
    runner.wait_changes['Begrenzt auf Fernstartbereitschaft warten'] = {
        'sensor.coffee_operation': 'BSH.Common.EnumType.OperationState.' + state}
    assert runner.run().error
    assert runner.vars['wait'].completed, 'Busy change should terminate the wait immediately'
    assert not runner.starts


@pytest.mark.parametrize('wait_alias', [
    'Begrenzt auf Fernstartbereitschaft warten',
    'Start anhand des Betriebszustands beobachten',
    'Gemeinsame single-Sperre bis zum beobachteten Laufende halten',
])
def test_timeout_cannot_turn_into_success_by_a_late_state(wait_alias):
    runner = engine()
    runner.forced_timeouts.add(wait_alias)
    assert runner.run().error
    if wait_alias == 'Begrenzt auf Fernstartbereitschaft warten':
        assert not runner.starts
    else:
        assert len(runner.starts) == 1


def test_power_timeout_cannot_be_masked_by_late_on_state():
    runner = engine(auto_power_on=True)
    runner.states['select.coffee_power'] = STANDBY
    runner.states['sensor.coffee_operation'] = INACTIVE
    runner.forced_timeouts.add('')  # Power wait has no alias.
    assert runner.run().error
    assert not runner.starts
