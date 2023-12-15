
## Defintions:
Denote the nodes ending in *A* "__A" as $A_i$ and the nodes ending in *Z* "__Z" as $Z_i$.
$l$ is the length of a sequence of steps repeated by each node.

## Assumptions:
(1) l is prime.
(2) Each $A_i$ is connected to one and only one $Z_i$ in a directional network and vice versa.
(3) $A_i$ will reach $Z_i$ in $n_i = l \cdot p_i$ steps.
(4) $Z_i$ will reach $A_i$ in $n_i$ steps.
(5) All $p_i$ are unique and prime.

## Proof:
A person starting on $A_i$ will land on $Z_i$ after $(2 \cdot N + 1) \cdot n_i$ steps, an odd multiple of the path length $n_i$. Suppose after $S$ steps, everybody starting on $A_i$ has landed on $Z_i$. We write

$S = (2 \cdot N_1 + 1) \cdot n_1$
$S = (2 \cdot N_2 + 2) \cdot n_2$
$...$

It is evident that $S$ has prime factors of $l$ and $p_1, p_2, ...$. Since all $p_i$ are prime (and therefore odd), any product of the $p_i$ will also be odd, and

$S = l \cdot p_1 \cdot p_2 \cdot ... = \text{lcm}(n_1, n_2, ...)$

is the minmimum number of steps which satisfies the requirement for all people starting on $A_i$ to land on $Z_i$.