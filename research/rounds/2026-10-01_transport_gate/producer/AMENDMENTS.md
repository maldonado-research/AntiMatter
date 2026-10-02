# Registration clarification after first numerical run

2 October 2026 UTC. The independent reviewer identified a missing qualification
in registered control 1: the zero modes equal `C^(1/2) ker(S^T)` when every
included reaction rate is strictly positive. With zero-rate channels the exact
statement is `C^(1/2) ker(S_active^T)`, equivalently
`C^(1/2) ker((S diag(sqrt(rho)))^T)`. Compatibility also applies only to active
reactions. Registration control 8 and the original implementation already use
the enlarged conserved space during rate shutdown. This amendment clarifies the
general claim; it changes no selected input, numerical criterion, code, or result.
The original registration and its recorded SHA-256 remain preserved.
