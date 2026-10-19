"""Build the pack from the content modules:  python3 -I content-src/build.py  (run from anywhere)."""
import importlib
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import dsl  # noqa: E402

MODULES = ['stage_iv_vi_naturals', 'stage_iv_vi_divisors', 'stage_iv_vi_fractions', 'stage_iv_vi_decimals', 'stage_iv_vi_percent_money', 'stage_iv_vi_measures', 'stage_iv_vi_algebra_data', 'stage_iv_vi_figures', 'stage_iv_vi_figures2', 'stage_iv_vi_thinking', 'stage_i_iii_numbers', 'stage_i_iii_numbers2', 'stage_i_iii_measures', 'stage_i_iii_data_thinking', 'stage_vii_viii_numbers', 'stage_vii_viii_algebra', 'stage_vii_viii_figures', 'stage_vii_viii_data_thinking', 'stage_media', 'stage_quests', 'stage_intros']

for m in MODULES:
    importlib.import_module(m)
dsl.write_all()
import subprocess  # noqa: E402
root = pathlib.Path(__file__).resolve().parent.parent
subprocess.run([sys.executable, '-I', str(root / 'tools/cognio.py'), 'fit', str(dsl.PACK)], check=True)
subprocess.run([sys.executable, '-I', str(root / 'tools/cognio.py'), 'pack', str(dsl.PACK), str(root / 'dist/courses/pl-primary-math-0.1.0.cognio')], check=True)
subprocess.run([sys.executable, '-I', str(root / 'tools/make_index.py')], check=True)
print(f'{len(dsl.SKILLS)} skills, {len(dsl.GENS)} generators, {sum(map(len, dsl.BANKS.values()))} bank tasks, '
      f'{sum(len(u.lessons) for us in dsl.PATHS.values() for u in us)} lessons')
