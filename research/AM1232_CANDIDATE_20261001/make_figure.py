#!/usr/bin/env python3
"""Plot the conditional conservation bound from the archived source inputs."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--checkpoint-root', type=Path, default=Path(__file__).resolve().parent)
parser.add_argument('--output-dir', type=Path, required=True)
args = parser.parse_args()
result = json.loads((args.checkpoint_root/'source-duration/results.json').read_text())
parameters = result['parameters']
x = np.linspace(0, 1, 300)
y = 16*np.sqrt(parameters['rho_kin_16_GeV4']/(2*parameters['A_GeV4'])*(3*np.exp(2*x)-2))
fig, ax = plt.subplots(figsize=(7, 5.2))
fig.subplots_adjust(bottom=.25, top=.90, left=.13, right=.97)
ax.plot(x, y, color='#275c63', linewidth=2.2, label='Continuous necessary bound on n × η')
points = result['duration_bounds']
ax.scatter([p['Delta_N_ending_at_T_star'] for p in points],
           [p['bound_n_eta_ge'] for p in points], color='#b45f33', zorder=3)
for p in points:
    if p['Delta_N_ending_at_T_star'] in (0, .1, .5, 1):
        ax.annotate(f"n ≥ {p['minimum_integer_n_at_eta_1']}",
                    (p['Delta_N_ending_at_T_star'],p['bound_n_eta_ge']),
                    xytext=(8, 10) if p['Delta_N_ending_at_T_star']<1 else (-55,-18),
                    textcoords='offset points', fontsize=10,
                    bbox=dict(facecolor='white', edgecolor='none', pad=1))
ax.set(xlabel='Required interval ending at T* = 131.7 GeV (e-folds)',
       ylabel='Necessary winding × relative response efficiency',
       title='Source-only energy cost of sustained threshold motion', xlim=(-.025,1.12))
ax.grid(alpha=.2)
ax.legend(loc='upper left', frameon=False)
fig.text(.5, .035,
         'Fixed cosine; initial rest; no driver work. Integer labels assume η = 1.\n'
         'Fixed dimensionless speed threshold; no predicted baryon abundance.',
         ha='center', fontsize=9)
args.output_dir.mkdir(parents=True, exist_ok=True)
for suffix in ('pdf','svg','png'):
    fig.savefig(args.output_dir/f'source_duration_bound.{suffix}', dpi=180, bbox_inches='tight')
plt.close(fig)
print('Saved conditional duration-bound figure as PDF, SVG and PNG')
