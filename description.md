Strategies for Enhancing Outage Probability and Secrecy Rate in Physical Layer Security
This document outlines two strategies to enhance outage probability and secrecy rate in physical layer security using artificial noise. The goal is to secure communication between a transmitter (Alice) and a legitimate receiver (Bob) against an eavesdropper (Eve). Both strategies leverage beamforming and artificial noise, with detailed mathematical formulations and Python implementation guidelines.
Common Parameters and Notations

Channel Models:

( h ): Channel vector from Alice to Bob, ( h \sim \mathcal{CN}(0, 2I_N) )
( g ): Channel vector from Alice to Eve, ( g \sim \mathcal{CN}(0, 2I_N) )
( N ): Number of antennas at Alice


Signal Model:

Transmitted signal: ( x = w s + z )
( s ): Data symbol with ( |s|^2 = 1 )
( w ): Beamforming vector
( z ): Artificial noise vector




Power Constraints:

Total power: ( P = \text{SNR} \times \sigma_n^2 ), where ( \sigma_n^2 ) is the natural noise variance
( \alpha ): Fraction of power allocated to ( w )
( 1 - \alpha ): Fraction of power allocated to ( z )


Secrecy Rate:

Instantaneous secrecy rate:[R_s = \max\left(0, \log_2\left(1 + \frac{|h^H w|^2}{\sigma_n^2}\right) - \mathbb{E}_g\left[\log_2\left(1 + \frac{|g^H w|^2}{|g^H z|^2 + \sigma_n^2}\right)\right]\right)]
( \mathbb{E}_g ) is approximated via Monte Carlo simulation over ( g ).


Outage Probability:

( P_{\text{out}} = \Pr(R_s > R) ), where ( R ) is a constant threshold rate and the x axis is SNR




Strategy 1: Constant Power Allocation
Description
This strategy uses a fixed power allocation between the beamforming vector ( w ) and artificial noise ( z ). The artificial noise is designed to be orthogonal to ( h ), ensuring no interference at Bob.
Implementation Details

Beamforming Vector:[w = \sqrt{\lambda} \frac{h^H}{|h|^2}]

( \lambda ): Power scaling factor
Instantaneous power: ( |w|^2 = \frac{\lambda}{|h|^2} )


Artificial Noise:[z = \sqrt{\mu} \frac{\gamma v}{|\gamma v|}]

( v \sim \mathcal{CN}(0, \frac{I_{N-1}}{N-1}) )
( \gamma ): Null space matrix of ( h ), ensuring ( h^H z = 0 )
( \mu ): Power scaling factor
Instantaneous power: ( |z|^2 = \mu )


Power Allocation:

Expected power:
( \mathbb{E}[|w|^2] = \mathbb{E}\left[\frac{\lambda}{|h|^2}\right] = \frac{\lambda}{2(N-1)} ) (since ( \mathbb{E}[1/|h|^2] = 1/(2(N-1)) ))
( \mathbb{E}[|z|^2] = \mu )


Total power: ( \mathbb{E}[|w|^2] + \mathbb{E}[|z|^2] = \alpha P + (1 - \alpha) P = P )
Solving:[\frac{\lambda}{2(N-1)} = \alpha P \quad \text{and} \quad \mu = (1 - \alpha) P][\lambda = 2(N-1) \alpha P \quad \text{and} \quad \mu = (1 - \alpha) P]


Secrecy Rate Calculation:

Bob’s rate: ( R_b = \log_2\left(1 + \frac{|h^H w|^2}{\sigma_n^2}\right) )
Eve’s rate (Monte Carlo over ( g )):[R_e \approx \frac{1}{M} \sum_{m=1}^M \log_2\left(1 + \frac{|g_m^H w|^2}{|g_m^H z|^2 + \sigma_n^2}\right)]
Secrecy rate: ( R_s = \max(0, R_b - R_e) )


Simulation:

SNR range: -5 to 20 dB
Monte Carlo over ( h ) and ( g ) to compute average secrecy rate and outage probability




Strategy 1.2: Variable Power Allocation
Description
This strategy adjusts the instantaneous power of the artificial noise based on ( h ), making ( |z|^2 = \frac{\mu}{|h|^2} ), while keeping the beamforming vector similar to Strategy 1.
Implementation Details

Beamforming Vector:[w = \sqrt{\lambda} \frac{h^H}{|h|^2}]

Same as Strategy 1


Artificial Noise:[z = \sqrt{\mu} \frac{\gamma v}{|h|}]

( v \sim \mathcal{CN}(0, \frac{I_{N-1}}{N-1}) )
( \gamma ): Null space matrix of ( h )
Instantaneous power: ( |z|^2 = \mu \frac{|\gamma v|^2}{|h|^2} )


Power Allocation:

Expected power:
( \mathbb{E}[|w|^2] = \frac{\lambda}{2(N-1)} = \alpha P )
( \mathbb{E}[|z|^2] = \mu \mathbb{E}\left[\frac{|\gamma v|^2}{|h|^2}\right] )
Since ( \mathbb{E}[|\gamma v|^2] = 1 ) and ( \mathbb{E}[1/|h|^2] = 1/(2(N-1)) ):[\mathbb{E}[|z|^2] = \mu \cdot \frac{1}{2(N-1)} = (1 - \alpha) P]
Solving:[\lambda = 2(N-1) \alpha P \quad \text{and} \quad \mu = 2(N-1) (1 - \alpha) P]




Secrecy Rate Calculation:

Same as Strategy 1, with updated ( z )
( R_b = \log_2\left(1 + \frac{|h^H w|^2}{\sigma_n^2}\right) )
( R_e ) via Monte Carlo over ( g )
( R_s = \max(0, R_b - R_e) )


Simulation:

SNR range: -5 to 20 dB
Monte Carlo over ( h ) and ( g ) for average secrecy rate and outage probability
