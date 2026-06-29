# Stable discrete representation of relativistically drifting plasmas

M. Kirchen,<sup>1,</sup> <sup>∗</sup> R. Lehe,<sup>2</sup> B. B. Godfrey,<sup>2,</sup> <sup>3</sup> I. Dornmair,<sup>1</sup> S. Jalas,<sup>1</sup> K. Peters,<sup>1</sup> J.-L. Vay,<sup>2</sup> and A. R. Maier<sup>1</sup>

<sup>1</sup>Center for Free-Electron Laser Science & Department of Physics,

University of Hamburg, 22761 Hamburg, Germany

<sup>2</sup>Lawrence Berkeley National Laboratory, Berkeley, CA 94720, USA

<sup>3</sup>University of Maryland, College Park, MD 20742, USA (Dated: October 20, 2018)

Representing the electrodynamics of relativistically drifting particle ensembles in discrete, copropagating Galilean coordinates enables the derivation of a Particle-in-Cell algorithm that is intrinsically free of the Numerical Cherenkov Instability for plasmas flowing at a uniform velocity. Application of the method is shown by modeling plasma accelerators in a Lorentz-transformed optimal frame of reference.

PACS numbers: 02.70.-c, 52.65.Rr, 52.27.Ny, 52.38.Kd

Describing complex physics beyond analytical theories requires numerical modeling of the underlying equations in discrete space. In plasma physics, astrophysics or accelerator physics, Particle-In-Cell (PIC) methods are commonly used to self-consistently solve the electromagnetic interaction of particle ensembles [1–4]. A PIC algorithm iteratively solves Maxwell’s equations on a discrete grid with particles following the equations of motion in a continuous space.

Some of the physical systems accessible with the PIC method feature plasmas drifting at relativistic velocities, for example when modeling plasma-based particle accelerators [5] in the optimal frame of reference [6] or astrophysical plasma interactions [7]. In those cases, the applicability of the to-date electromagnetic PIC algorithms is fundamentally limited by the Numerical Cherenkov Instability (NCI) [8–11], which either falsifies the numerical results or causes virulent growth of unphysical waves.

Here, we present a novel discrete formulation of the fundamental kinetic equations of plasmas, i.e. Maxwell’s and the Newton-Lorentz equations, that represents the physics in a moving Galilean frame of reference and thereby is intrinsically free of the NCI for plasmas drifting at uniform relativistic velocities.

The NCI originates from the coupling of distorted electromagnetic modes with spurious particle modes. Distortions of the electromagnetic field modes are caused by numerical inaccuracies of the discretized field-solving algorithm. Spurious spatial and temporal aliases of the physical particle modes result from the numerical mismatch of sampling the continuously distributed particle quantities to the discrete field grid. To first order, for example, Numerical Cherenkov Radiation (NCR) can occur, if the dispersion relation of the electromagnetic waves is numerically distorted. In this case, particles moving at relativistic velocities $v _ { p }$ ≈ c couple resonantly to electromagnetic waves of high frequency, which propagate at a spurious phase velocity $v _ { \Phi } < v _ { p } < c ,$ causing Cherenkovlike radiation to be emitted. Although many algorithms, such as pseudo-spectral solvers [12], do not sufer from

NCR, higher order NCI efects severely limit the stable modeling of relativistic plasmas.

So far, no electromagnetic, fully explicit PIC algorithm is intrinsically free of NCI, even for the simple case of a plasma drifting at a uniform relativistic velocity. Previously developed suppression strategies can limit the NCI growth rate, thereby retaining the physical meaningfulness of a simulation. For example, wide-band smoothing [13–15] or damping [16] of the currents or electromagnetic fields can hinder the development of the instability. Coupling of unphysical modes can be mitigated by slightly changing the ratio of the electric and magnetic fields as seen by the particles [17–19], by scaling the deposited currents with a frequency-dependent factor [20, 21], or by artificially modifying the physical electromagnetic dispersion relation [22–24]. Yet, all of these techniques rely on numerical methods that potentially alter the physics and could afect the results obtained with the algorithm.

In contrast, the method presented in this paper inherently eliminates the NCI for a relativistically drifting plasma, as opposed to suppressing its growth by the measures described above. From a heuristic point of view, the main diference between modeling a plasma at rest, showing no NCI, and a relativistically drifting plasma, is that the particles move with respect to the static numerical grid. Thus, intuitively, by mathematically representing the underlying discrete equations such that this discrepancy in relative movement is eliminated, the NCI should be suppressed.

This is achieved by applying a Galilean coordinate transformation of the form

$$
{ \pmb x } ^ { \prime } = { \pmb x } - { \pmb v } _ { \mathrm { g a l } } t
$$

to the frame of reference in which a plasma is moving at a relativistic velocity. Consequently, the equations of motion and Maxwell’s equations transform to

$$
\begin{array} { c } { \displaystyle \frac { d { \boldsymbol x } ^ { \prime } } { d t } = \frac { \boldsymbol p } { \gamma m } - v _ { \mathrm { g a l } } , } \\ { \displaystyle \frac { d { \boldsymbol p } } { d t } = q \left( { \boldsymbol E } + \frac { \boldsymbol p } { \gamma m } \times { \boldsymbol B } \right) , } \\ { \displaystyle \left( \frac { \partial } { \partial t } - v _ { \mathrm { g a l } } \cdot \nabla ^ { \prime } \right) { \boldsymbol B } = - \nabla ^ { \prime } \times { \boldsymbol E } , } \\ { \displaystyle \frac { 1 } { c ^ { 2 } } \left( \frac { \partial } { \partial t } - v _ { \mathrm { g a l } } \cdot \nabla ^ { \prime } \right) { \boldsymbol E } = \nabla ^ { \prime } \times { \boldsymbol B } - \mu _ { 0 } { \boldsymbol j } , } \end{array}
$$

and the continuity equation becomes $\left( \partial _ { t } - \pmb { v } _ { \mathrm { g a l } } \cdot \pmb { \nabla } ^ { \prime } \right) \rho +$ $\nabla ^ { \prime } \cdot \boldsymbol { j } = 0$ . Here, $\mathbf { \nabla } \mathbf { \nabla } \mathbf { \nabla } \mathbf { V } ^ { \prime }$ denotes the spatial derivative with respect to the Galilean coordinates $\mathbf { x } ^ { \prime }$ . For ${ \pmb v } _ { \mathrm { g a l } } = { \pmb 0 } .$ these equations reduce to their well-known original form.

Using the Pseudo-Spectral Analytical Time Domain (PSATD) framework [12], the last two equations are transformed to Fourier space and can then be integrated analytically in time. As the quantities are only known at discrete times in a PIC algorithm, the time evolution of $\rho$ and $j$ needs to be explicitly taken into account during integration. Typically, the currents are assumed to be constant over one time step $\Delta t$ in the original coordinates x. A key diference of our new scheme is that we assume the currents to be co-moving with respect to the original coordinates x, hence constant over one time step in the Galilean coordinates $\mathbf { x } ^ { \prime }$ . The resulting Galilean-PSATD equations for the advance of the spectral field components, $\hat { \varepsilon }$ and B<sup>ˆ</sup>, from time step $n \Delta t$ to $( n + 1 ) \Delta t$ are then given by (see [25] for a derivation)

$$
\begin{array} { r l } & { \bar { \mathcal { B } } ^ { n + 1 } = \theta ^ { 2 } C \bar { \mathcal { B } } ^ { n } - \frac { \theta ^ { 2 } S } { c k } \mathrm { i } k \times \bar { \mathcal { E } } ^ { n } + \frac { \theta _ { X 1 } } { \epsilon _ { 0 } c ^ { 2 } k ^ { 2 } } i k \times \bar { \mathcal { I } } ^ { n + 1 / 2 } , } \\ & { \bar { \mathcal { E } } ^ { n + 1 } = \theta ^ { 2 } C \bar { \mathcal { E } } ^ { n } + \frac { \theta ^ { 2 } S } { k } c i k \times \bar { \mathcal { B } } ^ { n } + \frac { i \omega \theta _ { X 1 } - \theta ^ { 2 } S } { \epsilon _ { 0 } c k } \bar { \mathcal { I } } ^ { n + 1 / 2 } } \\ & { \quad \quad - \frac { 1 } { \epsilon _ { 0 } k ^ { 2 } } \big ( \chi 2 \bar { \rho } ^ { n + 1 } - \theta ^ { 2 } \chi _ { 3 } \bar { \rho } ^ { n } \big ) i k , } \\ & { \quad \quad C = \cos ( c k \Delta t ) , \quad S = \sin ( c k \Delta t ) , \quad k = | k | , } \\ & { \quad \quad \nu = \frac { k \cdot \nu _ { \infty , 1 } } { c k } , \quad \theta = e ^ { i k \cdot \kappa _ { \infty , \mathrm { a b d } } \Delta t / 2 } , \quad \theta ^ { * } = e ^ { - i k \cdot \kappa _ { \infty , \mathrm { a b d } } \Delta t / 2 } , } \\ & { \quad \quad \times 1 = \frac { 1 } { 1 - \nu ^ { 2 } } \left( \theta ^ { * } - C \theta + i \nu \mathcal { B } \right) , } \\ & { \quad \quad \chi _ { 2 } = \frac { \chi _ { 1 } - \theta \big ( 1 - C \big ) } { \theta ^ { * } - \theta } , \quad \chi _ { 3 } = \frac { \chi _ { 1 } - \theta ^ { * } ( 1 - C ) } { \theta ^ { * } - \theta } , } \end{array}
$$

where k is the wavevector. The currents $\hat { \mathcal { I } }$ at time $( n +$ $1 / 2 ) \Delta t$ and the charge density $\hat { \rho }$ at time n∆t and $( n +$ 1)∆t are generated by the particles and deposited to the grid nodes before being transformed to Fourier space. Subsequently, the updated fields are transformed back to real space and interpolated to the particles, which are then advanced in time using the Galilean transformed equations of motion.

This algorithm allows to model a plasma moving at $\boldsymbol { v } _ { p }$ in a co-propagating set of coordinates $\mathbf { x } ^ { \prime }$ with $v _ { \mathrm { g a l } } =$ $v _ { p } .$ . As shown in fig. 1, the flowing plasma particles now remain static with respect to the numerical grid. Because of this and the co-moving current assumption, the NCI is completely eliminated for particles streaming at the velocity ${ \pmb v } _ { p } .$

![](images/042159cba04061f8f51b9680da49a7d5af065d53620fd772d5081f6740271ffd.jpg)  
FIG. 1. Schematic drawing illustrating the Galilean concept. Without applying a Galilean coordinate transformation to the Particle-In-Cell equations (Standard), a plasma flowing with velocity $v _ { \mathrm { p } }$ in z (represented by a single particle) would propagate a distance $v _ { \mathrm { p } } \Delta t$ with respect to the numerical grid (represented by a single cell) during one time step $\Delta t .$ However, in a Galilean transformed discrete space $\mathbf { x } ^ { \prime }$ with ${ v _ { \mathrm { g a l } } } = ( 0 , 0 , \upsilon _ { \mathrm { g a l } } = v _ { \mathrm { p } } )$ the plasma particles remain static with respect to the discrete grid nodes, which themselves propagate a distance $z + v _ { \mathrm { g a l } } \Delta t$ in the original coordinate system x.

The algorithm is implemented in the <sup>Warp</sup> code [26], for Cartesian coordinates, as well as in the recently developed quasi-cylindrical [27] code <sup>Fbpic</sup> [28]. In [25] we also present an analytical derivation of the dispersion relation and conduct a detailed empirical and theoretical stability analysis for uniform relativistically flowing plasmas. Here, we restrict ourselves to presenting the general concept and the practical demonstration of the stability and accuracy of our new method with a direct applica tion. In the following, Lorentz-boosted frame simulations of plasma acceleration with <sup>Fbpic</sup> are presented.

Plasma-based accelerators [5] can sustain high field gradients, allowing for the acceleration of charged particles within distances shorter by orders of magnitude compared to conventional accelerators. In a plasma-wakefield accelerator, an intense driver beam (a high intensity laser pulse or particle bunch) propagates through an underdense plasma and induces a charge separation on the sub-mm scale. This leads to the excitation of a trailing density wave carrying large electric fields, suitable for the acceleration of electron bunches to high energies.

The natural frame of reference for PIC simulations of plasma accelerators is the laboratory frame. In this frame of reference the physical objects of small scale, i.e. the laser or particle beam, propagate at relativistic velocities in a single direction while interacting with a large scale object that is static, i.e. the plasma. A Lorentz transformation in the propagation direction of the driver beam then relaxes the requirements on the spatial resolution while contracting the required simulation distance [6]. In this Lorentz-boosted frame, the co-propagating quantities, e.g. the laser or the plasma wavelength, are elongated by $\gamma ( 1 + \beta )$ , whereas the previously static lengths, such as the plasma, are contracted by $\gamma$ and counterpropagate with a relativistic velocity $- \beta c .$ Thereby, a speed-up by orders of magnitude can be achieved that scales as $\propto \gamma _ { \mathrm { b o o s t } } ^ { 2 } .$ , with the maximum speed-up typically limited to ≈ $2 \gamma _ { \mathrm { w a k e } } ^ { 2 } .$ i.e. the phase velocity of the wake, in the case of laser-plasma acceleration.

In the following, we show simulations of a non-linear plasma wave driven by a laser pulse with wavelength $\lambda = 8 0 0 \mathrm { n m }$ , peak normalized vector potential $a _ { 0 } = 1 . 5$ pulse length $c \tau = 8$ µm and waist $w _ { 0 } = 3 0$ µm that propagates through a matched plasma guiding channel with an on-axis electron density $n _ { e } = 1 \cdot 1 0 ^ { 1 8 } \mathrm { { c m } ^ { - 3 } }$ . In the generated wakefields, a 1 $\mathrm { p C }$ electron bunch of size $\sigma _ { z } = 1 \mu \mathrm { m } .$ $\sigma _ { r } = 2 \mu \mathrm { m }$ , and normalized emittance $\epsilon _ { \mathrm { n } } = 0 . 5$ mm mrad, located at the back of the first wave bucket, is accelerated from 100 MeV to 687 MeV within a propagation distance of $\mathrm { z _ { p r o p } \approx 1 4 . 3 }$ mm. The resolution of the simulation is 40 cells per µm in the longitudinal and 2 cells per µm in the transverse direction. Third order particle shapes are used with 24 particles per cell. The time step is set to $\Delta t = \Delta z / c$

As described above, the occurrence of the NCI, caused by the counter-streaming relativistic plasma, can hinder the application of the Lorentz-boosted frame method for simulations of plasma-wakefield accelerators. With our new method, however, such a simulation is modeled in a Galilean transformed coordinate system that counterpropagates to the Lorentz-boosted frame with the velocity $v _ { \mathrm { g a l } } = - \beta c$ in the direction of the boosted plasma. With respect to the numerical grid, the background plasma is thus static, whereas the elongated quantities, such as the laser pulse and the electron bunch, propagate with a velocity increased by the same amount with respect to the grid.

![](images/41ce8f7051acf5ee5c1ab6a71acf36761ce64cc19c3d257c65fe4bb9923a1f0f.jpg)  
FIG. 2. Charge density $\rho$ obtained from a Lorentz-boosted frame simulation $( \gamma _ { \mathrm { b o o s t } } = 1 3 )$ of a non-linear laser-plasma wave. At the time step shown, a part of the laser pulse, propagating to the right, has already left the plasma, which is flowing to the left. The upper-half corresponds to a Galilean-PSATD simulation with $v _ { \mathrm { g a l } } = - \beta c$ , showing no instability. The lower half shows the same simulation, mirrored along the $x = 0$ axis, but conducted with the standard PSATD solver. Here, a fast growing, virulent NCI can be observed.

Fig. 2 shows the charge density obtained in a Lorentz boosted frame $( \gamma _ { \mathrm { b o o s t } } = 1 3 )$ with boosted longitudinal coordinate $z _ { \mathrm { b o o s t } } ~ = ~ \gamma ( z \mathrm { ~ - ~ } v t )$ The upper-half of the plot shows the results of a simulation with the Galilean-PSATD solver, whereas the lower-half shows the corresponding results of a standard PSATD simulation. Here, a fast growing NCI can be observed. In contrast, the same simulation remains completely stable when mod eled in the Galilean transformed discrete space. We emphasize that all numerical parameters are the same in these simulations, except for the diference in using $v _ { \mathrm { g a l } } = - \beta c$ instead of $v _ { \mathrm { g a l } } = 0$ for the Galilean-PSATD equations. Thus, the absence of the instability results solely from the Galilean transformation of the underlying discrete equations. Even though the electron bunch and the grid move in opposite directions, we do not observe any NCI around the bunch. This can be explained by the fact that the electron bunch has a density that is much lower than the plasma, as it is elongated in the Lorentz boosted frame. Moreover, due to its non-zero charge, it is probably much less afected by higher order Numerical Cherenkov efects. Likewise, in a laboratory frame simulation, a relativistic electron bunch does typically not lead to an instability, as long as NCR is suppressed [29].

![](images/e0798a80743d30d2fc70166f36ef9d3e3e3dee52c22cff791e9e8ab89602ee93.jpg)

![](images/23f9bb2b848601e7a5c97db0d15497073480b82b271c3d3f25d384c1f80a31b6.jpg)  
FIG. 3. Comparison of the accelerating fields $( E _ { z }$ fields and on-axis lineout) and the focusing fields $( E _ { y }$ fields and ofaxis, $y \ = \ 1 1 . 2 5 \mu \mathrm { m } .$ , lineout). The upper-half of the plots shows the results of a laboratory frame simulation (solid line) with $\gamma _ { \mathrm { b o o s t } } = 1$ . The lower-half shows the back-transformed results of a Lorentz-boosted frame simulation (dashed line) with $\gamma _ { \mathrm { b o o s t } } = 1 3$ , mirrored along the $x , y = 0 ~ \mathrm { a x i s }$

In order to validate the accuracy of our new method, results from the stable Lorentz-boosted frame simulation are compared to a laboratory frame simulation. Fig. 3 shows the electric fields at the end of the acceleration distance. The upper-half of the plots shows the results of the reference simulation $( \gamma _ { \mathrm { b o o s t } } = 1 )$ , whereas the lower-half shows the corresponding back-transformed results of the Lorentz-boosted frame simulation $( \gamma _ { \mathrm { b o o s t } } = 1 3 )$ . Both the longitudinal fields $E _ { z }$ and the transverse fields $E _ { y }$ show no diferences. Note that the results in the Lorentzboosted frame are obtained within only a few thousand time steps, whereas the lab frame simulation takes more than half a million time steps to complete. We achieve a speed-up of ≈ 287 (≈ 92% of the optimal speed-up) with <sup>Fbpic</sup>, where the only overhead is the on-the-fly backtransformation of data to the laboratory frame.

![](images/b7014d667d9a802821f5556f1da159c624d366aec8cb174da0a01850cb6700de.jpg)  
FIG. 4. Comparison of the laser and electron bunch evolution between the laboratory frame (solid line) and the Lorentzboosted frame (dashed line) simulation. The upper plot shows the pulse duration τ (blue) and the laser waist w<sub>0</sub> (red) and the lower plot shows the kinetic Energy $\mathrm { E } _ { \mathrm { k i n } }$ (red), the rms energy spread $\sigma _ { \mathrm { E } }$ (gray area) and the normalized emittance $\epsilon _ { \mathrm { n } }$ (blue) over the complete acceleration distance of $z _ { \mathrm { p r o p } }$ ≈ 14.3 mm.

Furthermore, we compare characteristic bunch and laser parameters to demonstrate that the physics is preserved in the Lorentz-boosted frame. Fig. 4 shows the evolution of the laser waist $w _ { 0 }$ and the pulse duration $\tau ,$ as well as the kinetic energy $\operatorname { E } _ { \mathrm { k i n } } .$ , the rms energy spread $\sigma _ { \mathrm { E } }$ and the normalized emittance $\epsilon _ { \mathrm { n } }$ of the accelerated electron bunch. During the propagation through the plasma guiding channel, the laser pulse self-focuses transversely and the pulse duration shortens due to the relativistic interaction with the plasma. The electron bunch is initially situated at the minimum of the accelerating field and slips towards the laser pulse during the propagation. It is accelerated to 687 MeV, while accumulating an rms energy spread of ≈ 11.5 %, due to the slope of the accelerating field. As the bunch enters the plasma, strong transverse fields act on it abruptly, causing transverse oscillations of the bunch size and growth of the emittance $\epsilon _ { \mathrm { n } }$ to around 1.4 mm mrad. In direct comparison with the laboratory simulation, all the quantities shown difer only on the sub-percent level at the end of the propagation distance, which resembles a remarkable precision.

In conclusion, we have proposed a novel discrete formulation of the fundamental kinetic equations of plasmas in Galilean transformed coordinates. To the best of our knowledge, we thereby derived the first electromagnetic, fully explicit PIC representation that is intrinsically free of the NCI for plasmas flowing at a uniform velocity. Our concept is not reliant on otherwise inevitable numerical corrections and, unlike most of the previous NCI suppression strategies, it is independent of the specific geometry. This allows to combine the accuracy and eficiency of a spectral, quasi-3D PIC algorithm with the superior stability properties of the presented method. Applying the Galilean scheme to simulations of plasma accelerators in the Lorentz-boosted frame yields excellent agreement, while achieving a close-to-optimal speed-up of more than two orders of magnitude in practice.

Future research will cover the applicability of the Galilean scheme to other solvers, the parallelization based on domain decomposition [30] with arbitrary-order spectral methods [4, 24, 31] and the potential generalization to support arbitrary relativistic plasma flows. For example, the new method could directly be extended to model collisionless astrophysical shocks [7] involving two plasmas, by employing separate numerical grids for each plasma using diferent Galilean transformed coordinates. Taking advantage of the superposition principle, only the electromagnetic fields would be shared between those individual grids.

We gratefully acknowledge the computing time provided on the supercomputer JURECA under project HHH20 and on the PHYSnet cluster of the University of Hamburg. Work at LBNL was funded by the Director, Ofice of Science, Ofice of High Energy Physics, U.S. Dept. of Energy under Contract No. DE-AC02- 05CH11231, including from the Laboratory Directed Research and Development (LDRD) funding from Berkeley Lab.

∗ manuel.kirchen@desy.de

[1] O. Buneman, C. Barnes, J. Green, and D. Nielsen, Journal of Computational Physics 38, 1 (1980).

[2] J. M. Dawson, Rev. Mod. Phys. 55, 403 (1983).

[3] R. Hockney and J. Eastwood, Computer Simulation Using Particles (Taylor & Francis, 1988).

[4] C. Birdsall and A. Langdon, Plasma Physics via Computer Simulation, Series in Plasma Physics (Taylor & Francis, 2004).

[5] E. Esarey, C. B. Schroeder, and W. P. Leemans, Rev.

Mod. Phys. 81, 1229 (2009).

[6] J.-L. Vay, Phys. Rev. Lett. 98, 130405 (2007).

[7] L. Sironi, A. Spitkovsky, and J. Arons, The Astrophysical Journal 771, 54 (2013).

[8] B. B. Godfrey, Journal of Computational Physics 15, 504 (1974).

[9] B. B. Godfrey, Journal of Computational Physics 19, 58 (1975).

[10] B. B. Godfrey and J.-L. Vay, Journal of Computational Physics 248, 33 (2013).

[11] X. Xu, P. Yu, S. F. Martins, F. S. Tsung, V. K. Decyk, J. Vieira, R. A. Fonseca, W. Lu, L. O. Silva, and W. B. Mori, Computer Physics Communications 184, 2503 (2013).

[12] I. Haber, R. Lee, H. Klein, and J. Boris, Proc. Sixth Conf. on Num. Sim. Plasmas, Berkeley, CA (1973).

[13] J. Vay, C. G. R. Geddes, C. Benedetti, D. L. Bruhwiler, E. CormierMichel, B. M. Cowan, J. R. Cary, and D. P. Grote, AIP Conference Proceedings 1299, 244 (2010).

[14] J.-L. Vay, C. Geddes, E. Cormier-Michel, and D. Grote, Journal of Computational Physics 230, 5908 (2011).

[15] J.-L. Vay, C. G. R. Geddes, E. Cormier-Michel, and D. P. Grote, Physics of Plasmas 18, 030701 (2011), http://dx.doi.org/10.1063/1.3559483.

[16] S. F. Martins, R. A. Fonseca, L. O. Silva, W. Lu, and W. B. Mori, Computer Physics Communications 181, 869 (2010).

[17] B. B. Godfrey and J.-L. Vay, Journal of Computational Physics 267, 1 (2014).

[18] B. B. Godfrey, ArXiv e-prints (2014), arXiv:1408.1146 [physics.plasm-ph].

[19] B. B. Godfrey and J.-L. Vay, Computer Physics Communications , (2015).

[20] B. B. Godfrey, J.-L. Vay, and I. Haber, Journal of Com-

putational Physics 258, 689 (2014).

[21] B. Godfrey, J.-L. Vay, and I. Haber, Plasma Science, IEEE Transactions on 42, 1339 (2014).

[22] P. Yu, X. Xu, V. K. Decyk, F. Fiuza, J. Vieira, F. S. Tsung, R. A. Fonseca, W. Lu, L. O. Silva, and W. B. Mori, Computer Physics Communications 192, 32 (2015).

[23] P. Yu, X. Xu, A. Tableman, V. K. Decyk, F. S. Tsung, F. Fiuza, A. Davidson, J. Vieira, R. A. Fonseca, W. Lu, L. O. Silva, and W. B. Mori, Computer Physics Communications 197, 144 (2015).

[24] F. Li, P. Yu, X. Xu, F. Fiuza, V. K. Decyk, T. Dalichaouch, A. Davidson, A. Tableman, W. An, F. S. Tsung, R. A. Fonseca, W. Lu, and W. B. Mori, ArXiv e-prints (2016), arXiv:1605.01496 [physics.comp-ph].

[25] R. Lehe, M. Kirchen, B. B. Godfrey, A. R. Maier, and J.-L. Vay, to be submitted (2016).

[26] J.-L. Vay, D. P. Grote, R. H. Cohen, and A. Friedman, Computational Science & Discovery 5, 014019 (2012).

[27] A. F. Lifschitz, X. Davoine, E. Lefebvre, J. Faure, C. Rechatin, and V. Malka, J. Comput. Phys. 228, 1803 (2009).

[28] R. Lehe, M. Kirchen, I. A. Andriyash, B. B. Godfrey, and J.-L. Vay, Computer Physics Communications 203, 66 (2016).

[29] R. Lehe, A. Lifschitz, C. Thaury, V. Malka, and X. Davoine, Phys. Rev. ST Accel. Beams 16, 021301 (2013).

[30] J.-L. Vay, I. Haber, and B. B. Godfrey, Journal of Computational Physics 243, 260 (2013).

[31] H. Vincenti and J.-L. Vay, Computer Physics Communications 200, 147 (2016).