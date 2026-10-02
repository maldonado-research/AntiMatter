"""Reproduce a bounded susceptibility comparison; not a wall-yield solver.

The unconstrained ideal-gas charge sum explains the number stated in
arXiv:2604.20762v1 Eq. (22). The constrained coefficient is imported as an
exact result of this round's separate SM charge projection diagnostic.
Neither number is a matched broken-phase susceptibility or a physical yield.
"""

from fractions import Fraction as F
import json
from pathlib import Path


def main():
    # Three quark generations share mu_q, mu_u and mu_d; lepton flavors remain
    # separate. These ideal susceptibility weights include the Higgs factor.
    species = [
        ("q", 18, F(1, 3)), ("u", 9, F(1, 3)), ("d", 9, F(1, 3)),
        ("l_e", 2, F(1)), ("l_mu", 2, F(1)), ("l_tau", 2, F(1)),
        ("e_e", 1, F(1)), ("e_mu", 1, F(1)), ("e_tau", 1, F(1)),
        ("H", 4, F(0)),
    ]
    free_chi = sum(F(weight, 6) * charge ** 2
                   for _, weight, charge in species)
    projected_chi = F(144, 79)
    result = {
        "scope": "Exact arithmetic comparator; no new independent projection or wall transport calculation",
        "paper_version": "arXiv:2604.20762v1",
        "paper_anchor": "Eq. (22), printed page 9",
        "free_ideal_gas_chi_B_plus_L_over_T_squared": str(free_chi),
        "constrained_diagnostic_chi_B_plus_L_over_T_squared": str(projected_chi),
        "constrained_ensemble": "Hypercharge neutrality and fixed Delta_i=B/3-L_i; equilibrated ideal symmetric SM",
        "coefficient_input": "../producer/DERIVATION.md exact projection output; not independently derived here",
        "projected_to_free_ratio": str(projected_chi / free_chi),
        "projected_to_free_ratio_decimal": float(projected_chi / free_chi),
        "rate_porting_status": "Not established: anomaly charge and diffusion/relaxation conventions also need matching",
    }
    destination = Path(__file__).with_name("SUSCEPTIBILITY_COMPARISON.json")
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
