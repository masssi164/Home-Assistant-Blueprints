"""Small, explicit test double for the YAML used here; NOT a Home Assistant runtime."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import yaml
from jinja2 import StrictUndefined
from jinja2.nativetypes import NativeEnvironment
from jinja2.sandbox import SandboxedEnvironment

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / 'blueprints/script/coffee_control/prepare_coffee.yaml'
RECIPE = ROOT / 'blueprints/script/coffee_control/coffee_recipe.yaml'

class Input(str):
    """A blueprint input reference."""

class Loader(yaml.SafeLoader):
    """Reject duplicate YAML keys instead of silently keeping the last one."""

    def construct_mapping(self, node: yaml.MappingNode, deep: bool = False) -> dict:
        result = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in result:
                raise ValueError(f'Duplicate YAML key: {key}')
            result[key] = self.construct_object(value_node, deep=deep)
        return result

Loader.add_constructor('!input', lambda loader, node: Input(loader.construct_scalar(node)))

def load(path: Path) -> Any:
    return yaml.load(path.read_text(encoding='utf-8'), Loader=Loader)

def input_definitions(blueprint: dict) -> dict:
    result = {}
    for key, value in blueprint['blueprint'].get('input', {}).items():
        if 'input' in value:
            result.update(value['input'])
        else:
            result[key] = value
    return result

def expand(path: Path, supplied: dict) -> dict:
    bp = load(path)
    definitions = input_definitions(bp)
    unknown = set(supplied) - set(definitions)
    if unknown:
        raise ValueError(f'Unknown inputs: {unknown}')
    values = {k: deepcopy(v['default']) for k, v in definitions.items() if 'default' in v}
    values.update(supplied)
    missing = set(definitions) - set(values)
    if missing:
        raise ValueError(f'Missing inputs: {missing}')

    def visit(value: Any) -> Any:
        if isinstance(value, Input):
            return deepcopy(values[str(value)])
        if isinstance(value, dict):
            return {k: visit(v) for k, v in value.items()}
        if isinstance(value, list):
            return [visit(v) for v in value]
        return value
    return visit({k: v for k, v in bp.items() if k != 'blueprint'})

CORE_INPUTS = {
    'connection_entity': 'binary_sensor.coffee_connected',
    'power_entity': 'select.coffee_power',
    'operation_entity': 'sensor.coffee_operation',
    'remote_start_entity': 'binary_sensor.coffee_remote_start',
    'local_control_entity': 'binary_sensor.coffee_local_control',
}
ON = 'BSH.Common.EnumType.PowerState.On'
STANDBY = 'BSH.Common.EnumType.PowerState.Standby'
READY = 'BSH.Common.EnumType.OperationState.Ready'
RUN = 'BSH.Common.EnumType.OperationState.Run'
INACTIVE = 'BSH.Common.EnumType.OperationState.Inactive'

class Environment(SandboxedEnvironment, NativeEnvironment):
    pass

@dataclass
class Stop(Exception):
    message: str
    error: bool = False
    response: Any = None

class Runner:
    """Executes this project's finite YAML subset using native Jinja and fake states.

    Waits inject specified fake state changes. No clocks, HA event loop, entity registry,
    backend schema, network traffic, cloud API or real appliances are emulated.
    """
    def __init__(self, config: dict, args: dict | None = None):
        self.config = config
        self.vars = dict(args or {})
        self.vars['this'] = SimpleNamespace(entity_id='script.test_script')
        self.states = {
            'binary_sensor.coffee_connected': 'on', 'select.coffee_power': ON,
            'sensor.coffee_operation': READY, 'binary_sensor.coffee_remote_start': 'on',
            'binary_sensor.coffee_local_control': 'off', 'script.coffee_engine': 'off'
        }
        self.devices = {e: 'test-coffee-device' for e in CORE_INPUTS.values()}
        self.attrs = {'select.coffee_power': {'options': [ON, STANDBY]}}
        self.calls: list[dict] = []
        self.delays: list[dict] = []
        self.wait_changes: dict[str, dict[str, str]] = {}
        self.forced_timeouts: set[str] = set()
        self.power_succeeds = True
        self.start_succeeds = True
        self.finish_succeeds = True
        self.start_error = False
        self.env = Environment(undefined=StrictUndefined)
        self.env.globals.update(
            states=lambda e: self.states.get(e, 'unknown'),
            is_state=lambda e, s: self.states.get(e, 'unknown') == s,
            has_value=lambda e: self.states.get(e, 'unknown') not in ('unknown', 'unavailable'),
            state_attr=lambda e, a: self.attrs.get(e, {}).get(a),
            device_id=lambda e: self.devices.get(e)
        )

    def render(self, value: Any) -> Any:
        if isinstance(value, str) and ('{{' in value or '{%' in value):
            return self.env.from_string(value).render(self.vars)
        if isinstance(value, list):
            return [self.render(v) for v in value]
        if isinstance(value, dict):
            return {k: self.render(v) for k, v in value.items()}
        return value

    def condition(self, c: Any) -> bool:
        if isinstance(c, dict):
            assert c['condition'] == 'template'
            c = c['value_template']
        value = self.render(c)
        assert isinstance(value, bool), f'Condition is not a native bool: {value!r}'
        return value

    def execute(self, steps: list) -> None:
        for step in steps:
            if 'variables' in step:
                for name, value in step['variables'].items():
                    self.vars[name] = self.render(value)
            elif 'if' in step:
                if all(self.condition(c) for c in step['if']):
                    self.execute(step['then'])
                else:
                    self.execute(step.get('else', []))
            elif 'wait_template' in step:
                template = step['wait_template']
                if not self.condition(template):
                    alias = step.get('alias', '')
                    if alias in self.wait_changes:
                        self.states.update(self.wait_changes[alias])
                    elif 'Laufende' in alias and self.finish_succeeds:
                        self.states['sensor.coffee_operation'] = READY
                completed = self.condition(template) and step.get('alias', '') not in self.forced_timeouts
                self.vars['wait'] = SimpleNamespace(completed=completed)
                if not completed and not step.get('continue_on_timeout', True):
                    raise Stop('Timeout', error=True)
            elif 'action' in step:
                call = self.render(step)
                self.calls.append(call)
                if call['action'] == 'select.select_option' and self.power_succeeds:
                    self.states[call['target']['entity_id']] = call['data']['option']
                    self.states['sensor.coffee_operation'] = READY
                if call['action'] == 'home_connect_alt.start_program':
                    if self.start_error:
                        raise RuntimeError('Simulated API failure')
                    if self.start_succeeds:
                        self.states['sensor.coffee_operation'] = RUN
            elif 'delay' in step:
                self.delays.append(self.render(step['delay']))
            elif 'stop' in step:
                raise Stop(str(self.render(step['stop'])), step.get('error', False),
                           self.vars.get(step.get('response_variable', '')))
            else:
                raise AssertionError(f'Unsupported simulation step: {step}')

    def run(self) -> Stop:
        try:
            self.execute(self.config['sequence'])
        except Stop as stop:
            return stop
        return Stop('End of sequence')

    @property
    def machine_calls(self) -> list[dict]:
        return [c for c in self.calls if c['action'] != 'persistent_notification.create']

    @property
    def starts(self) -> list[dict]:
        return [c for c in self.calls if c['action'] == 'home_connect_alt.start_program']
