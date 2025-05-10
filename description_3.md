Strategy 3: Enhancing Outage Probability and Secrecy Rate
Strategy 3 is divided into two sub-strategies, 3.1 and 3.2, each defining the beamforming vector ( w ) and artificial noise vector ( z ) differently, with specific power constraints. Below, we detail each sub-strategy, including formulations and power allocations.
Common Notations

( h ): Channel vector from Alice to Bob, assumed ( h \sim \mathcal{CN}(0, I_N) ) for this strategy (i.e., each component has variance 1), so ( \mathbb{E}[|h|^2] = N ).
( g ): Channel vector from Alice to Eve, similarly distributed.
( N ): Number of antennas at Alice.
( \gamma ): Null space matrix of ( h ), satisfying ( h^H \gamma = 0 ).
( v ): Random vector, ( v \sim \mathcal{CN}(0, \frac{I_{N-1}}{N-1}) ).
( P_{\text{total}} ): Total average power available at Alice.
( \alpha ): Fraction of power allocation parameter, ( 0 \leq \alpha \leq 1 ).

Note: The channel distribution ( h \sim \mathcal{CN}(0, I_N) ) is assumed here to align with the user's power constraint formulations, differing from ( \mathcal{CN}(0, 2I_N) ) in earlier contexts.
Strategy 3.1
Beamforming Vector ( w )
[ w = \sqrt{\lambda} h ]

Instantaneous Power:Since ( h ) is a ( 1 \times N ) row vector, ( h^H ) is an ( N \times 1 ) column vector, making ( w ) an ( N \times 1 ) column vector. The power is:[|w|^2 = \left| \sqrt{\lambda} h^H \right|^2 = \lambda |h^H|^2 = \lambda |h|^2]Thus, the instantaneous power of ( w ) is ( \lambda |h|^2 ).

Average Power:With ( h \sim \mathcal{CN}(0, I_N) ), ( \mathbb{E}[|h|^2] = N ), so:[\mathbb{E}[|w|^2] = \lambda \mathbb{E}[|h|^2] = \lambda N]


Artificial Noise Vector ( z )
[ z = \sqrt{\mu} \frac{\gamma v}{|\gamma v|} ]

Instantaneous Power:Since ( \frac{\gamma v}{|\gamma v|} ) is normalized to unit norm:[|z|^2 = \left| \sqrt{\mu} \frac{\gamma v}{|\gamma v|} \right|^2 = \mu \left| \frac{\gamma v}{|\gamma v|} \right|^2 = \mu \cdot 1 = \mu]Thus, the instantaneous power of ( z ) is ( \mu ).

Average Power:Since ( |z|^2 = \mu ) is constant:[\mathbb{E}[|z|^2] = \mu]


Power Constraint
The total average power is:[\mathbb{E}[|w|^2] + \mathbb{E}[|z|^2] = \lambda N + \mu = P_{\text{total}}]

Power Allocation:
( \lambda = \frac{\alpha P_{\text{total}}}{N} )
( \mu = P_{\text{total}} - \lambda N )Substituting ( \lambda ):[\lambda N = \left( \frac{\alpha P_{\text{total}}}{N} \right) N = \alpha P_{\text{total}}][\mu = P_{\text{total}} - \lambda N = P_{\text{total}} - \alpha P_{\text{total}} = (1 - \alpha) P_{\text{total}}]Verify:[\lambda N + \mu = \alpha P_{\text{total}} + (1 - \alpha) P_{\text{total}} = P_{\text{total}}]This satisfies the constraint.



Thus:

( \mathbb{E}[|w|^2] = \alpha P_{\text{total}} )
( \mathbb{E}[|z|^2] = (1 - \alpha) P_{\text{total}} )

Strategy 3.2
Beamforming Vector ( w )
[ w = \sqrt{\lambda} h^H ]

Instantaneous Power:As in 3.1:[|w|^2 = \lambda |h|^2](Note: The query mentions "lambda*||h||^1", likely a typo for ( \lambda |h|^2 ), consistent with the norm squared.)

Average Power:[\mathbb{E}[|w|^2] = \lambda \mathbb{E}[|h|^2] = \lambda N]


Artificial Noise Vector ( z )
The query states ( z = \sqrt{\mu} h^H \left( \frac{\gamma v}{|\gamma v|} \right) ), with power ( \mu |h|^2 ). The notation is ambiguous since ( h^H ) ( ( N \times 1 ) ) times ( \frac{\gamma v}{|\gamma v|} ) ( ( N \times 1 ) ) isn’t directly defined. Assuming a typo or intent, we interpret it as:[ z = \sqrt{\mu} |h| \frac{\gamma v}{|\gamma v|} ]to match the power requirement.

Instantaneous Power:[|z|^2 = \left| \sqrt{\mu} |h| \frac{\gamma v}{|\gamma v|} \right|^2 = \mu |h|^2 \left| \frac{\gamma v}{|\gamma v|} \right|^2 = \mu |h|^2 \cdot 1 = \mu |h|^2]This matches the specified instantaneous power.

Average Power:[\mathbb{E}[|z|^2] = \mu \mathbb{E}[|h|^2] = \mu N]


Power Constraint
The total average power is:[\mathbb{E}[|w|^2] + \mathbb{E}[|z|^2] = \lambda N + \mu N = (\lambda + \mu) N = P_{\text{total}}]

Power Allocation:
( \lambda N = \alpha P_{\text{total}} ), so ( \lambda = \frac{\alpha P_{\text{total}}}{N} )
( \mu N = (1 - \alpha) P_{\text{total}} ), so ( \mu = \frac{(1 - \alpha) P_{\text{total}}}{N} )Verify:[\lambda N + \mu N = \alpha P_{\text{total}} + (1 - \alpha) P_{\text{total}} = P_{\text{total}}]This satisfies the constraint.



Thus:

( \mathbb{E}[|w|^2] = \alpha P_{\text{total}} )
( \mathbb{E}[|z|^2] = (1 - \alpha) P_{\text{total}} )

Key Differences

Strategy 3.1: ( z ) has constant instantaneous power ( \mu ), while ( w )’s power varies with ( |h|^2 ).
Strategy 3.2: Both ( w ) and ( z ) have powers proportional to ( |h|^2 ), scaling as ( \lambda |h|^2 ) and ( \mu |h|^2 ), respectively.

These differences impact the secrecy rate and outage probability, as the artificial noise’s behavior relative to the channel strength varies between the strategies. Simulations would be needed to quantify these effects, similar to prior strategies.
