Strategy 2: Constant Power Allocation for Beamforming and Artificial Noise

In this approach, we configure the beamforming vector ( w ) and artificial noise ( z ) to maintain constant instantaneous and average powers, enhancing the physical layer security by ensuring predictable power levels.

Beamforming Vector ( w )

The beamforming vector is defined as:

[ w = \sqrt{\lambda} \frac{h}{|h|} ]





( h ) represents the channel vector from the transmitter (Alice) to the legitimate receiver (Bob).



( \lambda ) is a constant power scaling factor.



Instantaneous Power: The power of ( w ) is:

[ |w|^2 = \left| \sqrt{\lambda} \frac{h}{|h|} \right|^2 = \lambda \left| \frac{h}{|h|} \right|^2 = \lambda \cdot 1 = \lambda ]





Average Power: The expected power is:

[ \mathbb{E}[|w|^2] = \mathbb{E}[\lambda] = \lambda ]

Since ( \lambda ) is a constant, the average power equals the instantaneous power, ensuring consistency.

Artificial Noise ( z )

The artificial noise vector is defined as:

[ z = \sqrt{\mu} \frac{\gamma v}{|\gamma v|} ]





( \gamma ) is the null space matrix of ( h ), ensuring ( h^H z = 0 ) (no interference at Bob).



( v ) is a random vector, typically drawn from a complex Gaussian distribution.



( \mu ) is a constant power scaling factor.



Instantaneous Power: The power of ( z ) is:

[ |z|^2 = \left| \sqrt{\mu} \frac{\gamma v}{|\gamma v|} \right|^2 = \mu \left| \frac{\gamma v}{|\gamma v|} \right|^2 = \mu \cdot 1 = \mu ]





Average Power: The expected power is:

[ \mathbb{E}[|z|^2] = \mathbb{E}[\mu] = \mu ]

As ( \mu ) is constant, the average power matches the instantaneous power.

Power Allocation Parameter ( \alpha )

The total power is split between the beamforming vector and artificial noise:





Total power available: ( P )



Power allocated to ( w ): ( \lambda )



Power allocated to ( z ): ( \mu )



Since ( P = \lambda + \mu ), the fraction of power allocated to ( w ) is:

[ \alpha = \frac{\lambda}{\lambda + \mu} ]





The fraction allocated to ( z ) is ( 1 - \alpha ).