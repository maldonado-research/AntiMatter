"""Write comparator data; registration must exist and match before execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import platform
import numpy as np
from transport import Network,S,C,Q,D,AMPLITUDE,BIAS,rk4

root = Path(__file__).resolve().parent
receipt = json.loads((root/'registration_receipt.json').read_text())
assert hashlib.sha256((root/'REGISTRATION.md').read_bytes()).hexdigest() == receipt['registration_sha256']
net = Network(S,C,np.ones(3))
uneven = Network(S,C,np.array([1.,2.,4.]))
zero = np.zeros(3)
cycle = AMPLITUDE*np.ones(3)
positive = net.propagate(zero,BIAS,1)
signed = net.propagate(positive,-BIAS,1)
washed = net.propagate(signed,zero,20)
stationary = net.stationary(BIAS)
cycle_stationary = uneven.stationary(cycle)
errors = []
for steps in [32,64,128]:
    approx = rk4(net,rk4(net,zero,BIAS,1,steps),-BIAS,1,steps)
    errors.append({'steps_per_segment':steps,'error_norm':float(np.linalg.norm(approx-signed))})
trajectory = []
for t in np.linspace(0,2,201):
    x = net.propagate(zero,BIAS,float(t)) if t <= 1 else net.propagate(positive,-BIAS,float(t-1))
    trajectory.append([float(t), *x.tolist(), *net.chemical_potential(x).tolist(),float(Q@x)])
data = {
    'scope':'illustrative dimensionless diagnostic, not candidate baryon yield',
    'run_at_utc':datetime.now(timezone.utc).isoformat(),
    'registration_receipt':receipt,
    'environment':{'python':platform.python_version(),'numpy':np.__version__},
    'inputs':{'S':S.tolist(),'C':C.tolist(),'amplitude':AMPLITUDE,
              'rates':[1,1,1],'uneven_rates':[1,2,4],'source_vector_d':D.tolist()},
    'positive_relaxation_eigenvalues':net.eigenvalues[net.positive].tolist(),
    'conserved_charge_nullity':net.charges().shape[1],
    'compatible_bias':net.compatibility(BIAS),
    'compatible_stationary_x':stationary.tolist(),
    'incompatible_cycle_bias':net.compatibility(cycle),
    'equal_rate_cycle_stationary_x':net.stationary(cycle).tolist(),
    'equal_rate_cycle_progress':net.progress(zero,cycle).tolist(),
    'uneven_rate_cycle_stationary_x':cycle_stationary.tolist(),
    'uneven_rate_cycle_progress':uneven.progress(cycle_stationary,cycle).tolist(),
    'positive_pulse_x_at_1':positive.tolist(),
    'zero_bias_after_positive_x_at_2':net.propagate(positive,zero,1).tolist(),
    'zero_integrated_signed_bias_x_at_2':signed.tolist(),
    'sign_reversed_x_at_2':net.propagate(net.propagate(zero,-BIAS,1),BIAS,1).tolist(),
    'freeze_at_2_x_at_22':Network(S,C,zero).propagate(signed,zero,20).tolist(),
    'washout_x_at_22':washed.tolist(),
    'washout_norm':float(np.linalg.norm(washed)),
    'trajectory_max_abs_mu_over_T':float(np.max(np.abs(np.asarray(trajectory)[:,4:7]))),
    'trajectory_max_charge_drift':float(np.max(np.abs(np.asarray(trajectory)[:,7]))),
    'independent_rk4_convergence':errors,
}
(root/'results.json').write_text(json.dumps(data,indent=2)+'\n')
np.savetxt(root/'signed_trajectory.csv',trajectory,delimiter=',',
           header='tau,x_A,x_B,x_C,mu_A_over_T,mu_B_over_T,mu_C_over_T,conserved_charge',comments='')
print(json.dumps({key:data[key] for key in ['zero_integrated_signed_bias_x_at_2',
                                         'washout_norm','trajectory_max_abs_mu_over_T',
                                         'independent_rk4_convergence']},indent=2))
