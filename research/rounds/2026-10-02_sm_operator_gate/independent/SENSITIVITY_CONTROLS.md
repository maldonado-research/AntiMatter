# Post-primary conditional sensitivity controls

This is a separate extension after the primary exact matrix receipt was frozen.
An exploratory coefficient calculation preceded these controls. Its first
interpretation treated `0.9987045454` as an achieved yield ratio; the parent
clarified from the historical public input that it is instead the *required*
relative efficiency at winding 49. The final calculation below uses that
documented interpretation and does not present this extension as preregistered
research or alter the primary controls/receipt.

Read literal historical constants from the public, unchanged file
`/workspace/AntiMatter/research/AM1231/v1.23.1/v1.23.1_efficiency_energy_frontier.py`.
Do not execute that file and do not import the parallel producer.

1. Independently derive `C_ideal = (72/79)/(2 pi^2 g_*s/45)` with
   `g_*s = 106.75` as a separate entropy assumption.
2. Use `threshold_old = 16 sqrt(9.35462209607388)` and
   `eta_required_old = threshold_old/49`, confirming the rounded parent value.
3. Holding target yield, scalar kinetic normalization, and all other inherited
   inputs fixed, the necessary speed scales as `1/C`; hence
   `threshold_new = threshold_old (0.0195/C_ideal)` and
   `eta_required_new = threshold_new/49`.
4. Check the minimum integer both by the threshold and the independently
   recomputed conditional kinetic-energy inequality, including its predecessor.
5. Acknowledge that symmetric massless susceptibilities cannot replace the
   finite-temperature broken-phase response at `T_* = 131.7 GeV`. The result is
   normalization sensitivity only, and all historical operator/history
   assumptions remain conditional.
