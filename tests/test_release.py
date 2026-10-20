"""Keep beta publishing scoped, gated and consistent with the import URLs."""
import re
from urllib.parse import unquote

from .support import ROOT, load


def test_beta_version_and_release_notes_exist():
    tag = (ROOT / 'VERSION').read_text().strip()
    assert re.fullmatch(r'v\d+\.\d+\.\d+-beta\.[1-9]\d*', tag)
    assert (ROOT / 'releases' / f'{tag}.md').read_text().strip()


def test_imports_and_blueprint_sources_use_the_release_tag():
    tag = (ROOT / 'VERSION').read_text().strip()
    prefix = f'https://github.com/masssi164/Home-Assistant-Blueprints/blob/{tag}/'
    readme = unquote((ROOT / 'README.md').read_text())
    notes = unquote((ROOT / 'releases' / f'{tag}.md').read_text())
    for name in ('prepare_coffee.yaml', 'coffee_recipe.yaml'):
        path = f'blueprints/script/coffee_control/{name}'
        assert load(ROOT / path)['blueprint']['source_url'] == prefix + path
        assert 'blueprint_url=' + prefix + path in readme
        assert 'blueprint_url=' + prefix + path in notes


def test_release_requires_both_checks_and_main_repository():
    workflow = load(ROOT / '.github/workflows/release-beta.yml')
    assert workflow['permissions'] == {'contents': 'read'}
    assert set(workflow['on']) == {'push', 'workflow_dispatch'}
    assert workflow['on']['push']['branches'] == ['main']
    publish = workflow['jobs']['publish']
    assert set(publish['needs']) == {'static-and-simulated', 'homeassistant-schema'}
    assert publish['permissions'] == {'contents': 'write'}
    for job in workflow['jobs'].values():
        assert "github.ref == 'refs/heads/main'" in job['if']
        assert "github.repository == 'masssi164/Home-Assistant-Blueprints'" in job['if']
        for step in job.get('steps', []):
            if 'uses' in step:
                assert re.search(r'@[0-9a-f]{40}$', step['uses'])
                if step['uses'].startswith('actions/checkout@'):
                    assert step['with']['persist-credentials'] is False
    for name in ('static-and-simulated', 'homeassistant-schema'):
        assert workflow['jobs'][name].get('permissions', {'contents': 'read'}) == {'contents': 'read'}
    script = publish['steps'][-1]['run']
    assert '--prerelease --latest=false' in script
    assert '--target "$GITHUB_SHA"' in script
    assert 'ref_sha' in script
    assert 'gh release delete' not in script
    assert 'git push --force' not in script
