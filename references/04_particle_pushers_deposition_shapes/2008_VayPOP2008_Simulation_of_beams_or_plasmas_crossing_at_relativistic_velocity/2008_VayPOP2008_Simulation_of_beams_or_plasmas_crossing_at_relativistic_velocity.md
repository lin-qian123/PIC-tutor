# Simulation of beams or plasmas crossing at relativistic velocity

J.-L. Vay

Citation: Phys. Plasmas 15, 056701 (2008); doi: 10.1063/1.2837054 View online: http://dx.doi.org/10.1063/1.2837054   
View Table of Contents: http://pop.aip.org/resource/1/PHPAEN/v15/i5 Published by the AIP Publishing LLC.

# Additional information on Phys. Plasmas

Journal Homepage: http://pop.aip.org/ Journal Information: http://pop.aip.org/about/about_the_journal Top downloads: http://pop.aip.org/features/most_downloaded Information for Authors: http://pop.aip.org/authors

# Simulation of beams or plasmas crossing at relativistic velocitya…

J.-L. Vayb Lawrence Berkeley National Laboratory, Berkeley, California 94720, USA Received 16 November 2007; accepted 20 December 2007; published online 12 February 2008-

This paper addresses the numerical issues related to the modeling of beams or plasmas crossing at relativistic velocity using the particle-in-cell method. Issues related to the use of the standard Boris particle pusher are identified and a novel pusher which circumvents them is proposed, whose effectiveness is demonstrated on single particle tests. A procedure for solving the fields is proposed, which retains electrostatic, magnetostatic, and inductive field effects in the direction of the mean velocity of the species, is fully explicit and simpler than the full Darwin approximation. Finally, results are given, from a calculation using the novel features, of an ultrarelativistic beam interacting with a background of electrons. $\circledcirc$ 2008 American Institute of Physics. DOI: 10.1063/1.2837054

# I. INTRODUCTION

It was shown recently1 that for a certain class of problems involving objects made of matter or light- propagating near or at the speed of light, the range of space and time scales spanned by the system depends strongly on the velocity of the frame of reference with regard to the system we assume in the entire paper that the frame of reference is inertial-. For commonly used methods in computer physics simulations, which rely on a discretization of space and time into small contiguous chunks, such as, for example, the ubiquitous particle-in-cell method in plasma physics, the implication is a difference of orders of magnitude on the number of mathematical operations needed to solve a problem, based solely on the choice of the frame of reference.

Since the principle of relativity implies that the laws of physics are the same regardless of the chosen frame of reference, and that the particle-in-cell method is based on the discretization of the fundamental laws of particle motion and electromagnetism, we might think that the solution is simple: just do the calculation in the frame which minimizes the range of space and time scales. In practice, however, the discretized equations may not preserve some fundamental properties of the continuous equations which may lead to unacceptably large errors. For example, when electric fields are transformed from one inertial frame to another using the Lorentz transformation, part of the electric field transforms into magnetic field and vice versa. When combined with Newton’s law of motion with the Lorentz force, part of the force exerted on particles from the electric field cancels with part of the force exerted by the magnetic field, so that the motion of the particles is identical in both frames. For particle-in-cell calculations involving relativistic species, it implies eventually that the particle pusher preserves the property of electric field and magnetic field cancellation in the Lorentz force term, either exactly or to such degree that the associated errors can be neglected. We have found that the commonly used Boris algorithm, a second-order leapfrog integrator of the equations of motion,2 does not preserve this property and may thus lead to large errors when calculating the orbits of relativistic species. We present an alternative formulation of the second-order leapfrog solver that preserves this property, and contrast numerical results with the Boris scheme on a few simple test cases. For the fields, we restrict this paper to the case where waves and retardation can be neglected and present a system that is simpler than the Darwin set of equations, under the provision of an additional approximation. The fully electromagnetic system involves additional complications and is left for later studies. We finally present an application of the new particle pusher and the field solver to the modeling of the interaction of an ultrarelativistic beam with a background of electrons.

# II. PUSHING PARTICLES

# A. Cancellation of electric and magnetic fields contributions in the Lorentz force

The equations of motion for a particle of mass $m$ and charge $q$ in electric and magnetic fields $\mathbf { E }$ and $\mathbf { B }$ may be written

$$
\frac { d { \bf x } } { d t } = { \bf v } ,
$$

$$
\frac { d ( \gamma \mathbf { v } ) } { d t } = \frac { q } { m } ( \mathbf { E + v \times B } ) ,
$$

where $\mathbf { X } , \ \mathbf { V } .$ , and $\scriptstyle \gamma = 1 / { \sqrt { 1 - { v ^ { 2 } } / { c ^ { 2 } } } }$ are, respectively, the position, velocity, and relativistic factor of the particle, $t$ is time, and $c$ is the speed of light. A centered finite-difference discretization of the system is given by

$$
\frac { \mathbf { x } ^ { i + 1 / 2 } - \mathbf { x } ^ { i - 1 / 2 } } { \Delta t } = \mathbf { v } ^ { i } ,
$$

$$
\frac { \gamma ^ { i + 1 } \mathbf v ^ { i + 1 } - \gamma ^ { i } \mathbf v ^ { i } } { \Delta t } = \frac { q } { m } ( \mathbf E ^ { i + 1 / 2 } + \overline { { \mathbf v } } ^ { i + 1 / 2 } \times \mathbf B ^ { i + 1 / 2 } ) .
$$

In order to close the system, $\overline { { \mathbf { V } } } ^ { i + 1 / 2 }$ must be expressed as a function of the other quantities. The solution proposed by Boris2 is given by

$$
\overline { { \mathbf { v } } } ^ { i + 1 / 2 } = \frac { \gamma ^ { i } \mathbf { v } ^ { i } + \gamma ^ { i + 1 } \mathbf { v } ^ { i + 1 } } { 2 \overline { { \gamma } } ^ { i + 1 / 2 } } .
$$

The systems 4- and 5- can be solved very efficiently following Boris’ method, where the electric field push is decoupled from the magnetic push, avoiding having to solve explicitly for $\overline { { \gamma } } ^ { i + 1 / 2 }$ .2 With the Boris scheme, the relativistic factor of the particle at time $i + 1 / 2$ is given by

$$
\begin{array} { l }  { \displaystyle { \overline { { \gamma } } ^ { i + 1 / 2 } = \sqrt { 1 + \left( \gamma ^ { i } { \bf v } ^ { i } + \frac { q \Delta t } { 2 m } { \bf E } ^ { i + 1 / 2 } \right) } } } \\ { { \displaystyle ~ = \sqrt { 1 + \left( \gamma ^ { i + 1 } { \bf v } ^ { i + 1 } - \frac { q \Delta t } { 2 m } { \bf E } ^ { i + 1 / 2 } \right) } . } } \end{array}
$$

Let us now assume that the particle is submitted to constant nonzero electric and magnetic fields in such a way that their mutual contributions cancel, i.e., $\mathbf { E } + \mathbf { v } \times \mathbf { B } = 0$ . If the particle pusher does a correct cancellation of the electric field and magnetic field contributions in the Lorentz force term, there should be no force acting on the particle and its velocity should stay unchanged. However, if we apply this condition to systems 4-–6-, by setting $\mathbf { E } + \mathbf { v } ^ { i } \times \mathbf { B } = \mathbf { E } + \mathbf { v } ^ { i + 1 } \times \mathbf { B }$ ${ } = 0$ and $\gamma ^ { i + 1 } \mathbf { v } ^ { i + 1 } { = } \gamma ^ { i } \mathbf { v } ^ { i }$ , we find that the system admits a solution only if $\mathbf { E } ^ { i + 1 / 2 } { = } \mathbf { B } ^ { i + 1 / 2 } { = } 0$ . Consequently, the particle will undergo a spurious force in the general case, where E $\neq 0$ and $\mathbf { B } \neq 0$ .

Let us now consider, in place of Eq. 5-, the following velocity average:

$$
\overline { { \mathbf { v } } } ^ { i + 1 / 2 } = \frac { \mathbf { v } ^ { i } + \mathbf { v } ^ { i + 1 } } { 2 } ,
$$

so that Eq. 4- becomes

$$
\frac { \gamma ^ { i + 1 } \mathbf { v } ^ { i + 1 } - \gamma ^ { i } \mathbf { v } ^ { i } } { \Delta t } = \frac { q } { m } \Bigg ( \mathbf { E } ^ { i + 1 / 2 } + \frac { \mathbf { v } ^ { i } + \mathbf { v } ^ { i + 1 } } { 2 } \times \mathbf { B } ^ { i + 1 / 2 } \Bigg ) .
$$

Setting ${ \bf { E } } ^ { i + 1 / 2 } + { \bf { v } } ^ { i } \times { \bf { B } } ^ { i + 1 / 2 } = { \bf { E } } ^ { i + 1 / 2 } + { \bf { v } } ^ { i + 1 } \times { \bf { B } } ^ { i + 1 / 2 } = 0$ and $\gamma ^ { i + 1 } \mathbf { v } ^ { i + 1 } { = } \gamma ^ { i } \mathbf { v } ^ { i }$ does not lead to any constraint on the values of the electric or magnetic field nor the velocity. Consequently, the velocity update given by Eq. 8- is free of the spurious force observed with the Boris velocity update.

# B. A new leapfrog pusher

Solving Eq. 8- presents no major difficulty. Setting $\mathbf { u }$ $= \gamma \mathbf { v }$ and

$$
\mathbf { u } ^ { \prime } = \mathbf { u } ^ { \mathrm { i } } + \frac { q \Delta t } { m } \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \mathopen { } \mathclose \bgroup \left( \mathbf { E } ^ { i + 1 / 2 } + \frac { \mathbf { v } ^ { i } } { 2 } \times \mathbf { B } ^ { i + 1 / 2 } \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \aftergroup \egroup \right) ,
$$

Eq. 8- becomes

$$
\mathbf { u } ^ { i + 1 } = \mathbf { u } ^ { \prime } + \frac { q \Delta t } { m } \bigg ( \frac { \mathbf { u } ^ { i + 1 } } { 2 \gamma ^ { i + 1 } } \times \mathbf { B } ^ { i + 1 / 2 } \bigg ) .
$$

Solving Eq. 10- together with $\gamma ^ { i + 1 } = \sqrt { 1 + ( u ^ { i + 1 } / c ) ^ { 2 } }$ yields a detailed demonstration is given in Appendix A

$$
\gamma ^ { i + 1 } = \sqrt { \frac { \sigma + \sqrt { \sigma ^ { 2 } + 4 ( \tau ^ { 2 } + u ^ { * 2 } ) } } { 2 } } ,
$$

$$
\mathbf { u } ^ { i + 1 } = s [ \mathbf { u } ^ { \prime } + ( \mathbf { u } ^ { \prime } \cdot \mathbf { t } ) \mathbf { t } + \mathbf { u } ^ { \prime } \times \mathbf { t } ] ,
$$

where $\boldsymbol { \tau } = ( q \Delta t / 2 m ) \mathbf { B } ^ { i + 1 / 2 } , \quad \boldsymbol { u } ^ { * } = \mathbf { u } ^ { \prime } \cdot \boldsymbol { \tau } / c , \quad \sigma = \gamma ^ { \prime 2 } - \boldsymbol { \tau } ^ { 2 } ,$ $\gamma ^ { \prime }$ $= \sqrt { 1 + u ^ { \prime 2 } / c ^ { 2 } } , \mathbf { t } = \pmb { \tau } / \gamma ^ { i + 1 }$ , and $s { = } 1 / \left( 1 { + } t ^ { 2 } \right)$ . Finally, we define the velocities at half time steps, when the positions are known. We set

$$
\begin{array} { l } { { \displaystyle { \bf u } ^ { i + 1 / 2 } = { \bf u } ^ { i } + \frac { q \Delta t } { 2 m } ( { \bf E } ^ { i + 1 / 2 } + { \bf v } ^ { i } \times { \bf B } ^ { \mathrm { i + 1 / 2 } } ) } \ ~ } \\ { { \displaystyle ~ = { \bf u } ^ { i + 1 } - \frac { q \Delta t } { 2 m } ( { \bf E } ^ { i + 1 / 2 } + { \bf v } ^ { i + 1 } \times { \bf B } ^ { \mathrm { i + 1 / 2 } } ) } , } \end{array}
$$

which is convenient computationally since the algorithm breaks into the following sequence for two half steps:

First half step: Get $\mathbf { u } ^ { i + 1 / 2 }$ from $\mathbf { u } ^ { i }$ using Eq. 13-.

Second half step: Get $\mathbf { u } ^ { i + 1 }$ from $\mathbf { u } ^ { i + 1 / 2 }$ using Eqs. 11- and 12- and $\mathbf { u } ^ { \prime } = \mathbf { u } ^ { i + 1 / 2 } + \big ( q \Delta t / 2 m \big ) \mathbf { E } ^ { i + 1 / 2 }$ .

Under some circumstances, this choice also provides the correct gyroradius for a particle rotating in a constant magnetic field, as discussed in Appendix B.

# C. Single particle tests of the new pusher 1. Constant uniform magnetic field in the laboratory frame

A particle was initialized with a velocity $v _ { x } = v _ { 0 } = 1 0 ^ { - 2 } c$ in a constant magnetic field $B _ { z }$ . The time step was set to $\Delta t { = } 1 0 ^ { - 2 } \times 2 \pi / \omega _ { c }$ and the position of the particle recorded for 100 steps. The positions in $\hat { x }$ and $\hat { y }$ normalized to the cyclotron radius $R _ { c } = v _ { 0 } / \omega _ { c } )$ are contrasted in Fig. 1 against the analytical results for the new pusher, the Boris pusher, and the Boris pusher with $\tan \left( \omega _ { c } \Delta t \right) / \omega _ { c } \Delta t$ correction. The calculation was done also in a frame moving at $\gamma _ { f } = 2$ with regard to the laboratory in the direction of $\hat { y }$ , transforming the initial parameters according to the Lorentz transformation. While the new pusher tracks very accurately the analytical result in both frames, the results from the Boris pusher with or without the $\tan \left( \omega _ { c } \Delta t \right) / \omega _ { c } \Delta t$ correction depart from the analytical result. For both versions of the Boris pusher, errors are very significant for $\gamma _ { f } = 3$ and grow very quickly as $\gamma _ { f }$ increases.The results from the new pusher for high values of $\gamma _ { f }$ were limited only by the precision of the machine. Running in double precision, we observed a slight departure from the analytical result starting around $\gamma _ { f } = 1 0 ^ { 5 }$ , for which the maximum velocity in $\hat { x }$ is about $1 0 ^ { - 7 }$ the velocity in $\hat { y }$ , which leads to 14 significant figures needed in the evaluation of the relativistic factor $\gamma$ of the particles, at which roundoff errors start to be non-negligible.

# 2. Constant uniform electric field in the laboratory frame

An electron was initialized with no initial velocity in the laboratory, and pushed through a constant electric field $E _ { x }$ $= 1 ~ \mathrm { k V / m }$ with a time step of $\Delta t { = } 1$ ns, for 100 steps. The same physical system was then modeled in a frame moving at $\gamma _ { f } = 1 0 0$ with respect to the laboratory in the direction of $\hat { y }$ .

![](images/d4206cd28a6341a1ac033b8cccf2b3b1d7ce25b90d8808a4fea389e480a3ceb3.jpg)  
FIG. 1. Color online- $X$ and $Y$ positions vs time step of a particle rotating in a constant magnetic field $B _ { z }$ as computed in the laboratory left- or in a frame moving along $\hat { y }$ at $\gamma _ { f } = 2$ right-.

The results from the new pusher, the Boris pusher, and the Boris pusher with $\tan \left( \omega _ { c } \Delta t \right) / \omega _ { c } \Delta t$ correction are given in Fig. 2 and contrasted with the analytic solution. Again, all three movers track the analytic solution well in the laboratory frame, but only the new pusher is accurate in the moving frame calculation.

# III. SOLVING FOR THE FIELDS

Assuming that waves and retardation effects are negligible, Maxwell’s equations reduce to Darwin’s equations.3,4 However, the numerical solution of the Darwin set of equations leads to an implicit scheme which has been reported to be expensive to solve.5 We seek a simpler system by making the following additional assumption: for each species, we assume that the electrostatic approximation is sufficient when the fields are computed in a comoving frame such that, in a frame moving at relativistic velocity $- v _ { z }$ with regard to the species, we can make the approximations $v _ { z } \gg v _ { x } , v _ { y } ,$ , and $\partial / \partial t \approx v _ { z } \partial / \partial z$ . As a result, we get

$$
\frac { \partial ^ { 2 } \phi } { c ^ { 2 } \partial t ^ { 2 } } - \frac { \partial ^ { 2 } \phi } { \partial x ^ { 2 } } - \frac { \partial ^ { 2 } \phi } { \partial y ^ { 2 } } - \frac { \partial ^ { 2 } \phi } { \partial z ^ { 2 } } \approx - \frac { \partial ^ { 2 } \phi } { \partial x ^ { 2 } } - \frac { \partial ^ { 2 } \phi } { \partial y ^ { 2 } } - \frac { \partial ^ { 2 } \phi } { \partial ( \gamma z ) ^ { 2 } } = \frac { \rho } { \epsilon _ { 0 } } ,
$$

$$
\mathbf { E } = - \frac { \partial \mathbf { A } } { \partial t } - \nabla \phi \approx \left\{ \frac { \partial \phi } { \partial x } , \frac { \partial \phi } { \partial y } , ( 1 + \beta ^ { 2 } ) \frac { \partial \phi } { \partial z } \right\} ,
$$

$$
\mathbf { B } = \pmb { \nabla } \times \mathbf { A } \approx \left\{ \frac { v _ { z } \partial \phi } { c ^ { 2 } \partial y } , - \frac { v _ { z } \partial \phi } { c ^ { 2 } \partial x } , 0 \right\} ,
$$

where $\scriptstyle { \beta = v _ { z } / c }$ and $\gamma { = } 1 / \sqrt { 1 { - } \beta ^ { 2 } }$ . Thus, for $N$ species, the field calculation is reduced to $N$ solves of the Poisson equation 15- where the scale along $\hat { z }$ is stretched by the factor $\gamma$ . Typically, for our applications, $N { = } 1$ or 2, and solving $N$ times Eq. 15- is much less expensive than solving the Darwin set of equations.

# IV. APPLICATION TO THE MODELING OF AN ULTRARELATIVISTIC BEAM INTERACTING WITH A BACKGROUND OF ELECTRONS

In high-energy physics accelerators, beams travel at near the speed of light and the force from their own magnetic field almost entirely offsets the one from their own electric field. They also interact with electron clouds which do not move appreciably in the laboratory frame. According to Ref. 1, the modeling from first principles of the interaction of the beam with the electron cloud is more efficient if performed in a frame moving at a relativistic velocity which is a fraction of the beam velocity in the laboratory frame. In such a frame, both the beam’s and the electron cloud’s self-magnetic fields cancel almost entirely their respective self-electric field. Consequently, whether one is to perform a simulation from first principles of the interaction of the beam with the electron clouds in the laboratory frame or in a moving frame, the modeling offers the right conditions for the applications of the present new particle pusher and field solver.

![](images/ec7d3b44413520bec9881909f5a06caf554f1ccd2ae2da06f92204d6f345d646.jpg)  
FIG. 2. Color online- $X$ and $Y$ positions vs time step of a particle accelerated by a constant electric field $E _ { x }$ as computed in the laboratory left- or in a frame moving along $\hat { y }$ at $\gamma _ { f } = 1 0 0$ right-.

TABLE I. Parameters used for simplified configuration of LHC at injection.   

<table><tr><td>Electron cloud density</td><td></td><td>1014 m-3</td></tr><tr><td>Bunch population</td><td>pe Nb</td><td>1.1×10l1</td></tr><tr><td>Beta functions</td><td>βxy</td><td>66.0, 71.54 m</td></tr><tr><td>rms bunch length</td><td>J</td><td>0.13 m</td></tr><tr><td>rms beam size</td><td>xy</td><td>0.884 mm</td></tr><tr><td>rms momentum spread</td><td>δrms</td><td>0</td></tr><tr><td>Circumference</td><td>C</td><td>26.659 km</td></tr><tr><td>Nominal tunes</td><td>Qx.y</td><td>64.28, 59.31</td></tr><tr><td>Relativistic factor</td><td>Y</td><td>479.6</td></tr><tr><td>Pipe radius</td><td>Rp</td><td>2.2 cm (with flat tops at ±1.8 cm)</td></tr><tr><td>Initial beam position offset</td><td>Sy</td><td>0.1 gy</td></tr><tr><td>Dipole field (electrons only)</td><td>By0</td><td>8.39 T</td></tr></table>

We consider a simplified model of a beam interacting with an electron cloud in the Large Hadron Collider LHC-, setting the beam parameters as prescribed right after its injection into the ring see Table I-. In the experiment, the beam is forced onto a near circular trajectory by a vertical constant magnetic field applied by a succession of magnetic dipoles. However, since the circumference of the ring is large compared to the beam length, we do not apply the dipole magnetic field on the beam in the simulations, which is assumed to propagate on a straight line. However, since the effect of the magnetic dipole field on the background of electrons is large, it is applied onto the electron motion. In the experiment, the beam is also focused transversely by a periodic succession of magnetic quadrupoles which we replaced in our simplified model by a continuous azimuthal magnetic field.

We performed a first-principles simulation using the particle-in-cell code WARP, 6 in which we have implemented the new particle pusher and the field solve procedure described above, using the numerical parameters given in Table II. The calculation was made in a frame moving at $\gamma { \approx } 1 6 . 5$ . We tried first a calculation using the Boris algorithm with or without the $\tan \left( \omega _ { c } \Delta t \right) / \omega _ { c } \Delta t$ correction. In both cases, both the beam and the electron macroparticles were lost at an unphysically fast rate. Using the new particle pusher, the beam interacted with the electrons and underwent a hoselike instability, as expected on physical grounds. The history of the fractional emittance in the vertical direction is plotted in Fig. 3. It is contrasted to the one obtained by running WARP in a quasistatic mode,7–9 where the particle positions were pushed in the laboratory frame using linear maps which contain the effect of the continuous focusing built-in, while the electrons were pushed in the laboratory frame using the Boris pusher. Both the quasistatic calculation in the laboratory frame and the particle-in-cell calculation in the moving frame predicted the same growth rate and saturation level of the emittance.

TABLE II. Simulation parameters.   

<table><tr><td>No.of macro-protons</td><td>Np</td><td>3×105</td></tr><tr><td>No.of macro-electrons</td><td>Ne</td><td>~2×106</td></tr><tr><td>Transverse size of the grid</td><td>LxXLy</td><td>4.4 cm×4.4cm</td></tr><tr><td>No.of grid points</td><td>Nx×Ny</td><td>128×128</td></tr><tr><td>Bunch/grid extension in z</td><td>L</td><td>±40</td></tr><tr><td>No.of slices</td><td>Nz</td><td>128</td></tr><tr><td>No.of electron cloud stations</td><td>Nstn</td><td>3000</td></tr><tr><td>No.of turns</td><td>N</td><td>1</td></tr><tr><td>No.of processors</td><td>Nproc</td><td>32</td></tr></table>

# V. CONCLUSION

We showed that the modeling of relativistic systems involves the issue of cancellation of electric and magnetic field contributions in the Lorentz force. We demonstrated that the Boris particle pusher does not cancel the two components exactly and showed on single test particles that this might lead to large errors in the calculation of particles trajectories. We derived a new leapfrog particle pusher which exactly satisfies the cancellation property and demonstrated its effectiveness in single particle tests. We also presented a procedure for solving the fields which retains electrostatic, magnetostatic, and inductive field effects in the direction of the mean velocity of the species, is fully explicit and simpler than the full Darwin approximation. The results from a calculation of an ultrarelativistic beam interacting with a background of electrons, which uses the novel features, were contrasted to calculations using the quasistatic approximation and showed good agreement. As part of the analysis of the particle pusher, it was also demonstrated that under some provision it reproduces the correct gyroradius of particles moving in a constant magnetic field for any time step. Further work will analyze the algorithm in more detail and evaluate whether it might have properties that extend its range of usefulness to other areas of plasma modeling. Finally, the issues related to fully electromagnetic particle-incell simulations, like the numerical Cerenkov effect for example, will be analyzed in details and remediations will be explored.

![](images/4acda510e7443e04fa53cce7462c4c3294b4f9be6f58cb1427e4e2e026074618.jpg)  
FIG. 3. Color online- Fractional emittance growth in the vertical direction for a $5 0 0 \mathrm { G e V }$ proton beam interacting with a background of $1 0 ^ { 1 4 } \mathrm m ^ { - 3 }$ electrons.

# ACKNOWLEDGMENTS

The author would like to thank R. H. Cohen, A. Friedman, M. A. Furman, D. P. Grote, and I. Haber for useful discussions and comments. Additional thanks go to D. P. Grote for help with the implementation of the field solver into the WARP simulation code.

This work was supported under the auspices of the U.S. DOE by the University of California, LBNL under Contract No. DE-AC02-05CH11231, the U.S.-LHC Accelerator Research Program LARP-, and the U.S. Department of Energy, Office of Science grant of the SciDAC program, Community Petascale Project for Accelerator Science and Technology ComPASS-. This research used resources of the National Energy Research Scientific Computing Center, which is supported by the Office of Science of the U.S. Department of Energy under Contract No. DE-AC02-05CH11231.

# APPENDIX A: DETAILED CALCULATION OF THE EXPLICIT SOLUTION OF THE QUANTITIES $\pmb { u } ^ { j + 1 }$ AND $\gamma ^ { i + 1 }$ IN THE NEW PUSHER

Setting $\pmb { \tau } { } = ( q \Delta t / 2 m ) \mathbf { B } ^ { \mathbf { i } + 1 / 2 }$ , $\mathbf { t } { = } { \pmb { \tau } } / \gamma ^ { i { + } 1 }$ , and using the notation shortcuts $\mathbf { u } \equiv \mathbf { u } ^ { i + 1 }$ and $\mathbf { B } \equiv \mathbf { B } ^ { i + 1 / 2 }$ , Eq. 10- becomes

$$
\mathbf { u } = \mathbf { u } ^ { \prime } + \mathbf { u } \times \mathbf { t }
$$

or, equivalently

$$
\begin{array} { r l } & { u _ { x } = u _ { x } ^ { \prime } + u _ { y } t _ { z } - u _ { z } t _ { y } , } \\ & { } \\ & { u _ { y } = u _ { y } ^ { \prime } + u _ { z } t _ { x } - u _ { x } t _ { z } , } \\ & { } \\ & { u _ { z } = u _ { z } ^ { \prime } + u _ { x } t _ { y } - u _ { y } t _ { x } . } \end{array}
$$

Solving by substitution for $u _ { x }$ , eliminating $u _ { y }$ and $u _ { z }$ gives

$$
u _ { x } = \frac { u _ { x } ^ { \prime } + ( u _ { x } ^ { \prime } t _ { x } + u _ { y } ^ { \prime } t _ { y } + u _ { z } ^ { \prime } t _ { z } ) t _ { x } + u _ { y } ^ { \prime } t _ { z } - u _ { z } ^ { \prime } t _ { y } } { 1 + t _ { x } ^ { 2 } + t _ { y } ^ { 2 } + t _ { z } ^ { 2 } } .
$$

The expressions for $u _ { y }$ and $u _ { z }$ are obtained from Eq. A5- by circular permutation of the indices, and we get, in vector notation

$$
\mathbf { u } ^ { i + 1 } = \mathbf { u } = s [ \mathbf { u } ^ { \prime } + ( \mathbf { u } ^ { \prime } \cdot \mathbf { t } ) \mathbf { t } + \mathbf { u } ^ { \prime } \times \mathbf { t } ] ,
$$

where $s { = } 1 / \left( 1 { + } t ^ { 2 } \right)$ . Note that the expressions of each component of $\mathbf { u }$ depend on the other components only through the relativistic factor $\gamma ^ { i + 1 }$ which appears implicitly in the terms t and $s$ -.

We now seek the solution of $\gamma .$ . Taking the dot product of Eq. A1- and $\mathbf { u }$ , we get

$$
u ^ { 2 } = { \bf u } ^ { \prime } \cdot { \bf u } ,
$$

which, divided by the square of the speed of light and adding one, becomes

$$
\gamma ^ { 2 } = 1 + u ^ { 2 } / c ^ { 2 } = 1 + \mathbf { u } ^ { \prime } \cdot \mathbf { u } / c ^ { 2 } ,
$$

where we have used the notation shortcut $\gamma \equiv \gamma ^ { i + 1 }$ . Plugging Eq. A6- into Eq. A8- gives

$$
\gamma ^ { 2 } = 1 + s \big [ u ^ { \prime 2 } + ( { \mathbf { u } ^ { \prime } \cdot \mathbf { t } } ) ^ { 2 } \big ] / c ^ { 2 } ,
$$

which, written explicitly as a function of $\gamma$ , becomes

$$
\gamma ^ { 2 } = 1 + \frac { u ^ { \prime 2 } + ( \mathbf { u ^ { \prime } } \cdot \boldsymbol { \tau } / \gamma ) ^ { 2 } } { c ^ { 2 } ( 1 + \boldsymbol { \tau } ^ { 2 } / \gamma ^ { 2 } ) } .
$$

Factoring in powers of $\gamma$ finally leads to the equation

$$
\gamma ^ { 4 } + \big ( \tau ^ { 2 } - \gamma ^ { \prime 2 } \big ) \gamma ^ { 2 } - \tau ^ { 2 } - u ^ { * 2 } = 0 ,
$$

where $\gamma ^ { \prime } = \sqrt { 1 + { u ^ { \prime } } ^ { 2 } / c ^ { 2 } }$ and $u ^ { * } { = } { \bf { u } } ^ { \prime } \cdot { \pmb { \tau } } / c$ . Solving Eq. A11-, and discarding the negative or imaginary solutions, we get

$$
\gamma = \gamma ^ { i + 1 } = \sqrt { \frac { \sigma + \sqrt { \sigma ^ { 2 } + 4 ( \tau ^ { 2 } + u ^ { * 2 } ) } } { 2 } } ,
$$

where $\sigma = \gamma ^ { \prime 2 } - \tau ^ { 2 }$ .

# APPENDIX B: MOTION IN A CONSTANT MAGNETIC FIELD

Let us assume that the particle moves in a constant magnetic field $\mathbf { B }$ and no electric field. Equation 8- then becomes

$$
\frac { \gamma ^ { i + 1 } \mathbf { v } ^ { i + 1 } - \gamma ^ { i } \mathbf { v } ^ { i } } { \Delta t } = \frac { q } { m } \bigg ( \frac { \mathbf { v } ^ { i } + \mathbf { v } ^ { i + 1 } } { 2 } \times \mathbf { B } \bigg ) ,
$$

which is known5 to generate a rotation of angle

$$
{ \Delta \theta } = \omega { \Delta t } = 2 \arctan \biggl ( \frac { \omega _ { c } { \Delta t } } { 2 } \biggr ) ,
$$

where $\omega _ { c } { = } q B / \gamma m$ is the cyclotron frequency and $\omega$ is the numerical angular frequency of rotation of the particle, which is the same as the one obtained with the Boris scheme without the $\tan \left( \omega _ { c } \Delta t \right) / \omega _ { c } \Delta t$ correction.5 Solving Eq. 13- for ${ \bf E } { = } 0$ leads to

$$
\mathbf { v } ^ { i + 1 / 2 } = \left[ 1 + \left( \frac { \omega _ { c } \Delta t } { 2 } \right) ^ { 2 } \right] \frac { \mathbf { v } ^ { i } + \mathbf { v } ^ { i + 1 } } { 2 } .
$$

From Eq. 3-, we also get

$$
\frac { \mathbf { x } ^ { i + 3 / 2 } - \mathbf { x } ^ { i - 1 / 2 } } { \Delta t } = \mathbf { v } ^ { i } + \mathbf { v } ^ { i + 1 } .
$$

Since the particle moves on a circle of radius $R$ at the angular velocity $\omega$ , we also have

$$
\left\| { \bf x } ^ { i + 3 / 2 } - { \bf x } ^ { i - 1 / 2 } \right\| = 2 R \left| \sin ( \omega \Delta t ) \right| ,
$$

$$
\frac { \left\| \mathbf { v } ^ { i } + \mathbf { v } ^ { i + 1 } \right\| } { 2 } = \left\| \mathbf { v } ^ { i } \right\| \cdot \left| \cos \frac { \omega \Delta t } { 2 } \right| = \left\| \mathbf { v } ^ { i + 1 } \right\| \cdot \left| \cos \frac { \omega \Delta t } { 2 } \right| .
$$

Solving Eqs. B2-–B6-, we find

$$
R = \frac { \left\| { \bf v } ^ { i + 1 / 2 } \right\| } { \omega _ { c } } = \left[ 1 + \left( \frac { \omega _ { c } \Delta t } { 2 } \right) ^ { 2 } \right] ^ { 1 / 2 } \frac { \left\| { \bf v } ^ { i } \right\| } { \omega _ { c } } .
$$

Hence, if $\mathbf { v } ^ { i + 1 / 2 } = v _ { 0 }$ , then the new pusher recovers the physical gyroradius for any $\Delta t$ , while if $\mathbf { v } ^ { i } = v _ { 0 }$ , then the numerical gyroradius is larger than the physical gyroradius by the factor $[ 1 + ( \omega _ { c } \Delta t / 2 ) ^ { 2 } ] ^ { 1 / 2 }$ , similar to the Boris pusher, as shown in Ref. 10. This observation leads to a potentially interesting comparison of the new pusher with the interpolated pusher presented in Refs. 11 and 12, which obtains the physical gyroradius by setting an effective velocity which is used to push the particles positions and is an interpolation between the velocity obtained from the Boris push and the drift velocity obtained from gyrokinetic motion. For large $\Delta t$ , the magnitude of the effective velocity is much smaller than the velocity of the particles by the factor $1 / \big [ 1 + \big ( \omega _ { c } \Delta t / 2 \big ) ^ { 2 } \big ] .$ , ensuring that the numerical particle gyroradius equals the physical one. In the new pusher, we can identify the velocity that is computed at integer time steps $( i , i + 1 , \ldots )$ , which is the one that is used to update the positions, as the effective velocity in Refs. 11 and 12. Whether the numerical gyroradius that will be computed will be the same as the physical one depends on whether the velocity that is computed at the half time steps will match the physical instantaneous velocity of the particle  $\mathbf { v } ^ { i + 1 / 2 } = v _ { 0 }$ in our example- or not. This involves an analysis that goes beyond the scope of the present paper and will be treated elsewhere.

1 J.-L. Vay, Phys. Rev. Lett. 98, 130405 2007-.   
${ } ^ { 2 } \mathbf { J } .$ . P. Boris, “Relativistic plasma simulation-optimization of a hybrid code,” in Proceedings of the Fourth Conference on Numerical Simulation Plasmas Naval Research Laboratory, Washington, D.C., 1970-, pp. 3–67. $^ 3 \mathrm { C }$ . G. Darwin, Philos. Mag. 39, 537 1920-.   
${ ^ 4 } \mathrm { J }$ . D. Jackson, Classical Electrodynamics, 2nd ed. Wiley, New York, 1975-, pp. 593–595.   
${ } ^ { 5 } \mathrm { C }$ . K. Birdsall and A. B. Langdon, Plasma Physics via Computer Simulation McGraw-Hill, New York, 1985-.   
${ } ^ { 6 } \mathrm { D }$ . P. Grote, A. Friedman, J.-L. Vay, and I. Haber, AIP Conf. Proc. 749, 55 2005-.   
${ } ^ { 7 } \mathrm { P } .$ Sprangle, E. Esarey, and A. Ting, Phys. Rev. Lett. 64, 2011 1990-. $^ 8 \mathrm { G }$ . Rumolo and F. Zimmermann, Phys. Rev. ST Accel. Beams 5, 121002 2002-.   
${ } ^ { 9 } \mathrm { C }$ . Huang, V. K. Decyk, C. Ren, M. Zhou, W. Lu, W. B. Mori, J. H. Cooley, T. M. Antonsen, Jr., and T. Katsouleas, J. Comput. Phys. 217, 658 2006-.   
$^ { 1 0 } { \cal S } .$ E. Parker and C. K. Birdsall, J. Comput. Phys. 97, 91 1991-.   
$ { { ^ \mathrm { 1 1 } } } _ { \mathrm { R } }$ . H. Cohen, A. Friedman, D. P. Grote, and J.-L. Vay, Nucl. Instrum. Methods Phys. Res. A 577, 5257 2007-.   
${ } ^ { 1 2 } \mathbf { R } .$ H. Cohen, A. Friedman, M. Kireeff Covo, S. M. Lund, A. W. Molvik, F. M. Bieniosek, P. A. Seidl, J.-L. Vay, P. Stoltz, and S. Veitzer, Phys. Plasmas 12, 056708 2005-.