"""60-digit arithmetic check of the analytic duration inequality.

The stipulated constant |u| threshold is diagnostic, not a derived yield law
away from the frozen electroweak instant. It holds throughout a contiguous
interval that ends at T_star, after release of a field initially at rest.
"""
from decimal import Decimal, localcontext, ROUND_CEILING
import json
from pathlib import Path


def main():
    with localcontext() as ctx:
        ctx.prec = 60
        A = Decimal("620116096.5235525")
        kinetic16 = (Decimal(250) * Decimal("131.7") * Decimal("1.020689")
                     / (Decimal(16) * Decimal("0.0195"))) ** 2 / 2
        bounds = []
        for ds in ["0", "0.01", "0.1", "0.5", "1"]:
            delta = Decimal(ds)
            bound = 16 * (kinetic16 / (2 * A) * (3 * (2 * delta).exp() - 2)).sqrt()
            nmin = int(bound.to_integral_value(rounding=ROUND_CEILING))
            assert Decimal(nmin) >= bound
            assert Decimal(nmin - 1) < bound
            bounds.append({"Delta_N": ds, "n_eta_lower_bound": str(bound),
                           "minimum_n_eta1": nmin, "predecessor_fails": True})
        caps = []
        for n in [16, 35, 49, 71, 119]:
            kreq = kinetic16 * (Decimal(16) / Decimal(n)) ** 2
            duration = ((2 * A / kreq + 2) / 3).ln() / 2
            caps.append({"n": n, "eta": 1, "endpoint_allowed_by_2A": kreq <= 2 * A,
                         "max_backward_Delta_N": str(duration) if kreq <= 2 * A else None})
        output = {"precision_decimal_digits": 60, "rho_kin16_GeV4": str(kinetic16),
                  "bounds": bounds, "duration_caps": caps}
        target = Path(__file__).with_name("independent_duration_bounds.json")
        target.write_text(json.dumps(output, indent=2) + "\n")
        print(target)


if __name__ == "__main__":
    main()
