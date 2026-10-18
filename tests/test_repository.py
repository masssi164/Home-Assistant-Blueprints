"""Repository consistency, privacy heuristics and dashboard/template checks."""
from pathlib import Path
import importlib.util
import json
import re
import subprocess
import sys

import pytest
from jinja2 import Environment, StrictUndefined
from .support import ROOT, CORE, RECIPE, Runner, load, expand

spec = importlib.util.spec_from_file_location('render_dashboard', ROOT/'tools/render_dashboard.py')
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


def public_files():
    return [p for p in ROOT.rglob('*') if p.is_file() and not any(
        part in ('.git','.pytest_cache','__pycache__','.venv','local') for part in p.relative_to(ROOT).parts)]


def values(obj):
    if isinstance(obj,dict):
        for v in obj.values(): yield from values(v)
    elif isinstance(obj,list):
        for v in obj: yield from values(v)
    elif isinstance(obj,str): yield obj


def test_all_yaml_and_json_parse():
    for p in public_files():
        if p.suffix == '.yaml' or p.suffix == '.yml': load(p)
        if p.suffix == '.json': json.loads(p.read_text())


def test_duplicate_yaml_keys_are_errors(tmp_path):
    p = tmp_path/'bad.yaml';p.write_text('a: 1\na: 2\n')
    with pytest.raises(ValueError, match='Duplicate YAML key'): load(p)


def test_jinja_templates_compile():
    env = Environment(undefined=StrictUndefined)
    for p in public_files():
        if p.suffix != '.yaml': continue
        for v in values(load(p)):
            if '{{' in v or '{%' in v: env.parse(v)


def test_no_identifying_machine_ids_in_public_sources():
    # Heuristic, not a substitute for human review. Only ID-shaped entity prefixes.
    identifier = re.compile(r'\b(?:sensor|binary_sensor|select|number|switch)\.[a-z0-9_]*_[a-f0-9]{12}_[a-z0-9_]+')
    forbidden_names = {'scripts.yaml','kaffee.yaml','secrets.yaml','.env'}
    for p in public_files():
        assert p.name not in forbidden_names, p
        assert not identifier.search(p.read_text(encoding='utf-8')), p


def test_native_dashboard_has_no_custom_cards():
    dashboard = load(ROOT/'dashboards/quick_start.yaml')
    assert not any(v.startswith('custom:') for v in values(dashboard))
    assert '__COFFEE_SCRIPT__' not in (ROOT/'dashboards/quick_start.yaml').read_text()


@pytest.mark.parametrize('style,file', [('native','quick_start.template.yaml'),('barista','barista.template.yaml')])
def test_all_dashboard_tokens_render_with_valid_domains(style,file):
    template = (ROOT/'dashboards'/file).read_text()
    mapping = json.loads((ROOT/'examples/dashboard_entities.example.json').read_text())
    rendered = renderer.render(template,mapping)
    assert not renderer.TOKEN.search(rendered)
    import yaml
    assert yaml.safe_load(rendered)['views']


@pytest.mark.parametrize('mapping', [{}, {'COFFEE_SCRIPT':'sensor.coffee'},
                                    {'COFFEE_SCRIPT':'script.x\nmalicious: true'},
                                    {'COFFEE_SCRIPT':'script.x','UNKNOWN':'script.z'}])
def test_renderer_rejects_missing_invalid_or_wrong_domain_values(mapping):
    with pytest.raises(ValueError):
        renderer.render('entity: __COFFEE_SCRIPT__',mapping)


def test_renderer_does_not_overwrite(tmp_path):
    mapping=tmp_path/'map.json'
    mapping.write_text((ROOT/'examples/dashboard_entities.example.json').read_text())
    output=tmp_path/'out.yaml';output.write_text('existing content')
    result=subprocess.run([sys.executable,str(ROOT/'tools/render_dashboard.py'),
                           '--mapping',str(mapping),'--output',str(output)],capture_output=True,text=True)
    assert result.returncode != 0
    assert output.read_text() == 'existing content'


def find_card(obj, primary):
    if isinstance(obj,dict):
        if obj.get('primary') == primary:return obj
        for v in obj.values():
            result=find_card(v,primary)
            if result:return result
    if isinstance(obj,list):
        for v in obj:
            result=find_card(v,primary)
            if result:return result
    return None


@pytest.mark.parametrize('counts,expected', [([0,0,0],'Noch keine Getränke'),
    ([10,10,1],'Gleichstand'), ([1,2,5],'Espresso/Ristretto'),
    (['unknown',2,4],'nicht verfügbar'), ([9,2,1],'Kaffee mit Milch')])
def test_favourite_statistics_handle_ties_zero_and_missing(counts,expected):
    card=find_card(load(ROOT/'dashboards/barista.template.yaml'),'🏆 Dein Lieblings-Getränk')
    keys=['__MILK_COUNTER_ENTITY__','__COFFEE_COUNTER_ENTITY__','__ESPRESSO_COUNTER_ENTITY__']
    state=dict(zip(keys,map(str,counts)))
    env=Environment(undefined=StrictUndefined)
    assert expected in env.from_string(card['secondary']).render(states=lambda e:state[e])


def test_source_statistical_guesses_removed():
    text=(ROOT/'dashboards/barista.template.yaml').read_text()
    assert '* 0.15' not in text and '/ 1000' not in text and '/ 2.5' not in text
    assert 'custom:mushroom-template-card' not in text
    assert 'custom:mushroom-legacy-template-card' in text


def test_relative_markdown_links_exist():
    for p in public_files():
        if p.suffix != '.md':continue
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if '://' in link or link.startswith('#') or link.startswith('mailto:'):continue
            target=link.split('#')[0]
            if target:assert (p.parent/target).exists(), (p.relative_to(ROOT),target)


def test_workflow_does_not_use_write_permissions_or_pr_target():
    wf=load(ROOT/'.github/workflows/validate.yml')
    assert wf['permissions'] == {'contents':'read'}
    assert 'pull_request_target' not in wf['on']
    assert 'homeassistant-schema' in wf['jobs']
    for job in wf['jobs'].values():
        for step in job.get('steps',[]):
            if 'uses' in step:
                assert re.search(r'@[0-9a-f]{40}$',step['uses']), step['uses']


def test_repository_links_target_real_destination():
    for name in ('README.md', 'blueprints/script/coffee_control/prepare_coffee.yaml',
                 'blueprints/script/coffee_control/coffee_recipe.yaml'):
        content = (ROOT/name).read_text(encoding='utf-8')
        assert 'masssi164/home-assistant-coffee-control' not in content
        assert 'masssi164/Home-Assistant-Blueprints' in content or 'masssi164%2FHome-Assistant-Blueprints' in content

def test_no_repository_bootstrap_scripts_or_secret_files():
    assert not (ROOT/'tools/publish.sh').exists()
    assert not (ROOT/'kaffee_einrichtung.private.yaml').exists()
    for p in public_files():
        assert not re.search(r'\b[a-f0-9]{32}\b', p.read_text(encoding='utf-8')), p
