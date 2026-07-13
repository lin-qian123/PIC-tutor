# Laser-plasma interactions with a Fourier-Bessel Particle-in-Cell method

Igor A. Andriyash,<sup>1,</sup> <sup>2,</sup> <sup>a)</sup> Remi Lehe,<sup>3</sup> and Agustin Lifschitz<sup>2</sup>

<sup>1)</sup>Synchrotron Soleil, L’Orme des Merisiers, Saint Aubin, 91192 Gif-sur-Yvette,

<sup>2)</sup>LOA, ENSTA ParisTech, CNRS, Ecole polytechnique, Universit´e Paris-Saclay, 828 bd des Mar´echaux, 91762 Palaiseau cedex France

<sup>3)</sup>Lawrence Berkeley National Laboratory, Berkeley, CA 94720, USA

(Dated: 20 August 2019)

A new spectral particle-in-cell (PIC) method for plasma modeling is presented and discussed. In the proposed scheme, the Fourier-Bessel transform is used to translate the Maxwell equations to the quasi-cylindrical spectral domain. In this domain, the equations are solved analytically in time, and the spatial derivatives are approximated with high accuracy. In contrast to the finite-diference time domain (FDTD) methods that are commonly used in PIC, the developed method does not produce numerical dispersion, and does not involve grid staggering for the electric and magnetic fields. These features are especially valuable in modeling the wakefield acceleration of particles in plasmas. The proposed algorithm is implemented in the code PLARES-PIC, and the test simulations of laser plasma interactions are compared to the ones done with the quasi-cylindrical FDTD PIC code CALDER-CIRC.

## I. INTRODUCTION

In the last few decades, numerical simulation has become an indispensable tool for plasma physics in a wide range of problems from astro- and atmosphere physics, to laser plasma interactions. Often for such studies one needs to model plasma kinetics in presence of the strong electromagnetic fields, which produce relativistic motion of the charges in plasma. Such systems can be described by using the particle methods<sup>1</sup>, where plasma is presented by the macro-particles, which have the same charge-to-mass ratios as plasma particle species, but represent large quantities of the real ones. One example here is the particle-in-cell (PIC) method, which is widely used for the plasma modeling<sup>2</sup>. In PIC, the electromagnetic fields are calculated at the nodes of a spatial grid, and each macro-particle interacts with only a few such nodes in its vicinity.

The majority of the PIC codes advance the electromagnetic fields via the finite-diference time domain (FDTD) methods<sup>3</sup>. In this approach, the finite diferences approximate all derivatives in the Maxwell equations, and the discrete steps are used to advance the fields-particles system in time. The FDTD scheme stability is defined by the resolutions, ∆t and ∆r, which define the precisions of the temporal and spatial derivatives of the electric and magnetic fields. In practice, the velocities of the traveling waves in FDTD happen to depend on how well their propagation is resolved in space and time, and this phenomenon is known as the numerical dispersion. In the cases, where electromagnetic waves co-propagate with the relativistic particles, such dispersion may result to the unphysical wave-particle interactions, which should be treated explicitly<sup>4–6</sup>. On the other hand, the derivatives in the Maxwell equations are coupled, and for the better accuracy, the fields E and B in FDTD are usually staggered in space and in time. In this case, the terms $\mathbf { E } _ { p }$ and $\beta _ { p } \times { \bf B } _ { p }$ of the Lorentz force, with which wave acts on the particle, may compensate each other with a reminder $\mathbf { F } _ { p } \sim e \mathbf { E } _ { p } / \gamma _ { p } ^ { 2 } ,$ where $\gamma _ { p } = ( 1 - \beta _ { p } ^ { 2 } ) ^ { - 1 / 2 }$ is the particle’s Lorentz factor. For a relativistic particle, the force $\mathbf { F } _ { p }$ can be very small, and for the correct projection of the staggered fields a very fine temporal and spatial resolutions may be required<sup>7</sup>.

The mentioned issues become especially important in modeling the wakefield acceleration of particles (WFA). In WFA, the strong plasma waves transfer the energy from a high-power laser or particle driver beam, to the trailing particles, eventually injected into these waves<sup>8–10</sup>. These accelerators are being actively explored for the last two decades in pursuit for the compact sources of high intensity beams of energetic particles. The threedimensional FDTD PIC modeling is commonly used for the detailed theoretical studies of WFA physics, and to interpret the experiments. Besides the WFA modeling, such simulations are used to study the accompanying phenomena, e.g. generation of X-rays by the accelerated charges<sup>11</sup>, collimation of the particle beams<sup>7</sup> etc.

One alternative to the FDTD approach is the pseudo spectral time domain (PSTD) method<sup>12</sup>. In PSTD, at each time step the equations are translated from the real space to a spectral (e.g. Fourier) domain, where the derivatives are presented by the linear coeficients. This approach provides high precision in calculation of the spatial derivatives, and, in some cases, allows to run simulations with the much lower spatial resolutions, than the finite diferences methods<sup>13</sup>. Moreover, for a wide class of equations, their spectral counterparts can be integrated in time analytically, so that the accuracy of the fields dynamics modeling does not directly depend on the simulations temporal resolution<sup>12</sup>. This is known as the pseudo-spectral analytical time domain (PSATD) method, and it was shown to produce no numerical dispersion of electromagnetic fields associated with the temporal and spatial resolutions in $\mathrm { P I C ^ { 1 4 } }$

Here we develop the PSATD PIC considering that the model geometry has a certain level of cylindrical symmetry, which allows to replace the three-dimensional Cartesian geometry with a series of cylindrical models with different symmetries, e.g. Fourier series over the azimuthal angle. This is known as the quasi-cylindrical geometry, and previously it was proposed for the FDTD PIC simulations $\mathrm { i n } ^ { 1 5 }$ . Allowing to model the laser-plasma interactions with only few angular modes, the quasi-cylindrical FDTD approach has become popular for modeling WFAtype problems<sup>16</sup>, and the combinations of such method with the Fourier methods were considered<sup>17</sup>. For the fully spectral quasi-cylindrical PSATD, we consider the decomposition into the cylindrical harmonics, where the angular Fourier decomposition is naturally extended by the Fourier-Bessel transform of the azimuthal modes. Previously, the quasi-cylindrical spectral modeling was considered for a variety of problems<sup>18–20</sup>, and in this work we apply it for PIC simulations. One similar method was recently developed $\mathrm { i n ^ { 2 1 } }$ , in parallel with the present one. $\mathrm { { I n ^ { 2 1 } } }$ the diferent mathematical formulation is used, which has led to a diferent numerical scheme.

The physical and mathematical models are presented and discussed in section II. In section III, we briefly discuss the implementation of the scheme, and demonstrate a few examples of laser plasma simulations, which are compared to the ones provided by the quasi-cylindrical FDTD PIC. The conclusions are given in section IV, and are followed by a brief review of the spectral transforms (appendix A), and their properties (appendix B).

## II. PHYSICAL AND MATHEMATICAL MODELS

Two main ingredients of a numerical model of plasma electrodynamics are the integrator of the electromagnetic equations called Maxwell solver, and the particle pusher, which integrates the motion equations for the charged plasma particles. In our Maxwell solver, we employ the Fourier-Bessel transform for the spatial distributions of electromagnetic fields, and the charge densities and currents. The description of the transform is provided in appendix A, and in the following text we denote the spectral images with the hat-like accent, ${ \hat { f } } .$ The spatial dependencies are considered in the cylindrical coordinates $\mathbf { r } = ( x , r , \theta )$ , while the vectorial components are chosen to be Cartesian, $\mathbf { A } = ( A _ { x } , A _ { y } , A _ { z } )$ , so they are naturally well-defined on the axis, $r = 0$ (in contrast to the cylindrical components).

The components of the Fourier-Bessel series are the cylindrical harmonics, which are the eigenfunctions of the Laplace operator, $\widehat { \nabla ^ { 2 } f } = - \omega ^ { 2 } \widehat { f }$ . On the other hand, the first-order operators involve coupling of the azimuthal modes, and do not transform directly into the linear coeficients (see appendix B). Therefore, to take advantage of these properties, we derive the mathematical model, where the Laplace operator acts on the functions updated in time (i.e. are acted on by $\partial _ { t } )$ , and the operators ∇, ∇· and $\mathbf { v } \times$ act only on the terms, which are re-calculated at each iteration.

For convenience, in the following discussion we use the dimensionless units – the field components are normalized as $\pmb { \varepsilon } = e \mathbf { E } / ( m c ^ { 2 } k _ { 0 } )$ and $\mathbf { b } = \mathbf { \bar { \Pi } } ^ { } \mathbf { e B } / ( m _ { e } c ^ { 2 } k _ { 0 } )$ , where $m _ { e }$ and e are the mass of the electron and the elementary charge, $k _ { 0 } = 2 \pi / \lambda _ { 0 }$ and $\omega _ { 0 } = k _ { 0 } c$ are the wavenumber and the frequency, which correspond to a scale unity λ<sub>0</sub> $\left( \mathrm { e . g } \right.$ . laser or plasma wavelength). The mass, charge, velocity, coordinates of the particles are in the units of $m _ { e } , e , \mathrm { { } } c , k _ { 0 } ^ { - 1 }$ respectively, and time is normalized to $\omega _ { 0 } ^ { - 1 }$ The particles density $n _ { p }$ in this notations is normalized to the critical plasma density for the unity wavelength, $n _ { c } = m _ { e } \omega _ { 0 } ^ { 2 } / 4 \pi \bar { e } ^ { 2 }$

## A. Field equations in the spectral space

To construct the spectral Maxwell solver, we start from the standard equations for the electric and magnetic fields $\left( \mathrm { c f ^ { 2 2 } } \right)$ :

$$
\begin{array} { r } { \partial _ { t } \pmb { \varepsilon } = \pmb { \nabla } \times \mathbf { b } - \mathbf { j } , \quad \partial _ { t } \mathbf { b } = - \pmb { \nabla } \times \pmb { \varepsilon } , } \\ { \pmb { \nabla } \cdot \pmb { \varepsilon } = n , \quad \pmb { \nabla } \cdot \pmb { b } = 0 , } \end{array}\tag{1}
$$

where n and $\mathbf { j }$ are the normalized charge density and current.

As mentioned before, in the Fourier-Bessel space the first-order operators couple the angular Fourier modes, and are to be excluded from the integration. For this, we replace the magnetic field with its rotation vector, $\mathbf { g } = \mathbf { V } \times \mathbf { b }$ , which in contrast to the pseudo-vector b is a polar vector, and it behaves similarly to the currents (in magnetostatic problems $\mathbf { g } = \mathbf { j } )$ . Next, we take the curl of the Faraday’s law and combine it with the Poisson equation, which leads to:

$$
\begin{array} { r } { \partial _ { t } \boldsymbol { \varepsilon } = \mathbf { g } - \mathbf { j } , \quad \nabla ^ { 2 } \boldsymbol { \varepsilon } = \partial _ { t } \mathbf { g } + \nabla n , } \end{array}\tag{2a}
$$

and the equation for the magnetic field is:

$$
\nabla ^ { 2 } \mathbf { b } = - \nabla \times \mathbf { g } .\tag{2b}
$$

Equations (2) are now well adapted for the integration in the spectral space, and after the Fourier-Bessel transform the first pair reads:

$$
\partial _ { t } \widehat { \pmb { \varepsilon } } - \widehat { \mathbf { g } } = - \widehat { \mathbf { j } } , \quad \partial _ { t } \widehat { \mathbf { g } } + \omega ^ { 2 } \widehat { \pmb { \varepsilon } } = - \widehat { \nabla n } ,\tag{3a}
$$

where $\omega = \sqrt { k _ { x } ^ { 2 } + k _ { r } ^ { 2 } }$ , and $k _ { x }$ and $k _ { r }$ are the longitudinal and transverse wavenumbers (for details see appendices A and B). Equations (3a) can be used to advance ε and g in time, and the magnetic field, needed for the Lorentz force calculation, follows from the static equation,

$$
\widehat { { \bf b } } = \omega ^ { - 2 } \widehat { \nabla \times { \bf g } } .\tag{3b}
$$

It is easy to see, that, while ε and g can be advanced in time with $\mathrm { e q . }$ (3a), the first-order derivatives appear only to communicate fields with particles, so they are recalculated at each integration step.

## B. Integration cycle of the quasi-cylindrical spectral PIC

In the time-domain particle-in-cell methods, the system of fields and particles advances in time by the discrete steps. Let us consider one integration cycle on the time interval $( t _ { 0 } , t _ { 0 } + \Delta t )$ , and denote the variables at $t _ { 0 } .$ $t _ { 0 } + \Delta t / 2$ and $t _ { 0 } + \Delta t$ with the indices $^ { 6 6 } 0 ^ { 5 3 } , ^ { 6 6 } 1 / 2 ^ { 5 }$ and $^ { 6 6 } 1 ^ { 9 }$ respectively. During one cycle:

(i) particles velocities $\beta _ { 1 / 2 }$ are used to advance their positions from $\mathbf { r } _ { 0 }$ to r<sub>1</sub> (leapfrog),

(ii) densities $n _ { 1 }$ and currents $\mathbf { j } _ { 1 / 2 }$ are deposed onto the spatial grid for each angular mode,

(iii) spectral projections of $\hat { \bf j } _ { 1 / 2 }$ and $\widehat { \nabla n _ { 1 } }$ are calculated,

(iv) $\mathrm { e q . }$ (3a) is used to update $\widehat { \varepsilon } _ { 1 }$ and $\widehat { \bf g } _ { 1 }$ , and $\widehat { \mathbf { b } } _ { 1 }$ is calculated from eq. (3b)

(v) $\mathbf { b } _ { 1 }$ and $\varepsilon _ { 1 }$ are projected onto the spatial $\mathrm { g r i d }$

(vi) Lorentz force is calculated at the particles positions, and their velocities are advanced to $\beta _ { 3 / 2 }$

The steps $( \mathbf { i } , \mathbf { i } \mathbf { i } , \mathbf { v } \mathbf { i } )$ are common for the PIC methods, and their various implementations are widely discussed in the literature<sup>2</sup>. The steps (iii) and $\mathbf { \rho } ( \mathbf { v } )$ , are simply the translations between spectral and real domains, and these operations are discussed in appendix B.

The step (iv) corresponds to the spectral Maxwell solver, where eqs. (3a) are integrated in time for $\widehat { \varepsilon }$ and ${ \widehat { \mathbf { g } } } .$ Let us assume that, following the particles dynamics, <sup>b</sup>the current $\mathbf { j } _ { 1 / 2 }$ remains constant during one integration cycle, and the density evolves linearly from $n _ { 0 }$ to $n _ { 1 }$ . In this case, on the interval $( t _ { 0 } , t _ { 0 } + \Delta t )$ the electromagnetic equations can be written as:

$$
\begin{array} { l } { \displaystyle \partial _ { t } \widehat { \varepsilon } = \widehat { \mathbf { g } } - \widehat { \mathbf { j } } _ { 1 / 2 } , } \\ { \displaystyle \partial _ { t } \widehat { \mathbf { g } } = - \omega ^ { 2 } \widehat { \varepsilon } + \frac { t - \Delta t - t _ { 0 } } { \Delta t } \widehat { \nabla n } _ { 0 } - \frac { t - t _ { 0 } } { \Delta t } \widehat { \nabla n } _ { 1 } . } \end{array}\tag{4}
$$

Equation $( 4 )$ can be integrated in time analytically, which allows to obtain the fields at $t _ { 0 } + \Delta t$ as:

$$
\widehat { \pmb { \varepsilon } } _ { 1 } = \mathbf { C } _ { \varepsilon } \cdot \mathbf { S } , \quad \widehat { \pmb { \mathrm { g } } } _ { 1 } = \mathbf { C } _ { g } \cdot \mathbf { S } ,\tag{5}
$$

where vector ${ \bf S } = \left( \widehat { \varepsilon } _ { 0 } , \widehat { { \bf g } } _ { 0 } , \widehat { { \bf j } } _ { 1 / 2 } , \widehat { \nabla n } _ { 0 } , \widehat { \nabla n } _ { 1 } \right)$ contains the known variables, and the integration coeficients are:

$$
\begin{array} { r l } & { \mathbf { C } _ { \varepsilon } = \left( \cos \omega \Delta t , \frac { \sin \omega \Delta t } { \omega } , - \frac { \sin \omega \Delta t } { \omega } , \frac { \omega \Delta t \cos \omega \Delta t - \sin \omega \Delta t } { \omega ^ { 3 } \Delta t } , \frac { \sin \omega \Delta t - \omega \Delta t } { \omega ^ { 3 } \Delta t } \right) , } \\ & { \mathbf { C } _ { g } = \left( - \omega \sin \omega \Delta t , \cos \omega \Delta t , 1 - \cos \omega \Delta t , \frac { 1 - \cos \omega \Delta t - \omega \Delta t \sin \omega \Delta t } { \omega ^ { 2 } \Delta t } , - \frac { 1 - \cos \omega \Delta t } { \omega ^ { 2 } \Delta t } \right) . } \end{array}
$$

On any interval, when j and n can be assumed constant, eq. (5) is the exact solution of the Maxwell equations. The physical precision of such solution is independent of $\Delta t .$ , but is defined solely by the accuracies of the initial and boundary conditions. This is a principal advantage of the developed PSATD method along with the high accuracy of spatial derivatives achieved in spectral calculations.

a. Charge continuity. In the simulations, eq. (5) relies on the charge density and current, which are calculated via the weighted projections of macro-particles positions and velocities onto the grid. The numerical errors, produced in such projections, typically dominate the overall accuracy of the model, and should be considered with care. One issue related to the projection errors in PIC, is that the continuity equation,

$$
\partial _ { t } n + \nabla \cdot { \bf j } = 0 ,\tag{6}
$$

may be not satisfied with the suficient precision. Consequently, the violation of charge continuity leads to violation of the Poisson equation, $\mathbf { \nabla } \nabla \cdot \mathbf { E } = n .$ , and the magnetic monopoles absence condition, $\mathbf { \nabla } \nabla \cdot \mathbf { B } = 0$ . Considering the series of eq. (5), one may show that:

$$
\widehat { \nabla \cdot \varepsilon _ { 1 } } - \widehat { n _ { 1 } } \propto \widehat { \nabla \cdot g _ { 1 } } \propto \frac { \widehat { n _ { 1 } } - \widehat { n _ { 0 } } } { \Delta t } + \widehat { \nabla \cdot \mathbf { j } } _ { 1 / 2 } ,
$$

where the term in the rightmost side corresponds to the continuity equation eq. (6). The produced errors tend to accumulate, and the unphysical electric and magnetic fields may develop.

Commonly in the PIC methods, the charge continuity is assured by either correcting the deposed current<sup>23</sup>, or by using the charge-conserving deposition techniques<sup>24</sup>. The proper current correction may be introduced as, $\mathbf { j } ^ { \prime } = \mathbf { j } - \mathbf { \nabla } \mathbf { \bar { V } }$ , where Γ satisfies, $\nabla ^ { 2 } \bar { \Gamma } = \partial _ { t } n + \nabla \cdot \mathbf { j } .$ In the Fourier space, this correction becomes a simple algebraic operation, which makes this approach especially convenient in the spectral methods<sup>14</sup>. In the developed scheme, the current correction reads:

$$
\widehat { \mathbf { j } } _ { 1 / 2 } ^ { \prime } = \widehat { \mathbf { j } } _ { 1 / 2 } + \frac { 1 } { \omega ^ { 2 } } \left( \frac { \widehat { \nabla n } _ { 1 } - \widehat { \nabla n } _ { 0 } } { \Delta t } + \widehat { \nabla \nabla \cdot \mathbf { j } } _ { 1 / 2 } \right) ,\tag{7}
$$

and in contrast to the pure Fourier approach, diferential operations in eq. (7) are not linear in the Fourier-Bessel space, but involve matrix operations. In the simulations, this correction should applied at each PIC cycle after the step (iii).

b. Boundary conditions for the fields. In spectral methods, the boundary conditions of the simulation domain are determined by the basis functions, and providing the model-specific boundaries in the general case can be rather challenging. In our model, the vertical bound aries are periodic, as imposed by the Fourier transform, and the horizontal boundary, $r = R ,$ is chosen to be reflective (cf appendix A). In the situations, when these conditions do not correspond to the physical model, it is often possible to assume the unbounded media, i.e. sufficiently large simulation domain, so that the interaction does not reach the boundaries. In the cases, when such approximation cannot be provided, the absorbing boundaries can be produced by multiplying the concerned values by the evanescent envelopes (for an example, see<sup>25</sup>).

In beam-plasma interactions, the domain of interest may often be restricted to the area around a laser or particle beam, which travels through the plasma. In this case, we may apply the unbounded media model by considering the simulation domain, which covers the interaction region, and co-propagates with it. Obviously, such moving window technique requires the fields at the downstream boundary to be suppressed in order to prevent their upstream translation. In our scheme, when using the moving window, after each shift of the simulation domain we multiply ε and g with a profile function, which is equal to unity everywhere but in a narrow layer near the boundary, where it is evanescent. We have tested the profiles:

$$
f ( 0 < x < l _ { \mathrm { a b s } } ) = \frac { 1 } { 4 } \left( 1 - \cos \frac { \pi x } { l _ { \mathrm { a b s } } } \right) ^ { 2 } ,
$$

for suppression of ε, and

$$
\begin{array} { r } { f ( 0 < x < l _ { \mathrm { a b s } } ) = 1 - \mathrm { e } ^ { - 1 0 x ^ { 2 } / l _ { \mathrm { a b s } } ^ { 2 } } , } \end{array}
$$

for a less perturbing suppression of g. For this operation, the fields are projected to the real space along x-coordinate via the inverse Fourier transform, and returned to the spectral domain after the profiling. Plasma is also removed from this layer. The physical properties of such ”absorbing” layers are also afected by the fact, that they travel with the domain. In the performed tests, the described method has proven eficient, however, its more rigorous development remains a subject for the further studies.

## III. SIMULATIONS

The described algorithm was implemented as the separate module in the code PLARES<sup>20</sup>. The original code was designed to simulate physics of free electron lasers using the reduced Fourier and Fourier-Bessel Maxwell solvers acting directly on the particles. In PLARES-PIC we use the linear interpolation for the particle-grid projections, and the particles are advanced in the (r, p)- space via the standard Boris pusher<sup>26</sup>.

Code runtime is managed by the scripts written in Python, which provides very simple coding and takes benefit of the numerical and scientific computation modules, Numpy and Scipy<sup>27</sup>, and on-the-fly simulation visualization can be easily implemented using the Matplotlib module<sup>28</sup>. To provide the higher code performance, the computationally intense operations are written in Fortran 90, and are wrapped for Python calls via F2PY interface generator<sup>29</sup>. For the fast Fourier transforms we use the FFTW3 package<sup>30</sup>. The parallel computation is managed by MPI from the Python runtime via $\mathrm { M P I 4 P Y ^ { 3 1 } }$ . For simplicity in our code we use the radial decomposition, i.e. the spatial grid and the particles are divided into the slices along the radial direction.

## A. Linear laser-plasma interaction

Let us firstly check of the scheme dispersion properties, by modeling the propagation of laser pulse in vacuum and plasma. The classical dispersion relation of electromagnetic waves in plasma reads, $\omega ^ { 2 } = k ^ { 2 } c ^ { 2 } + \omega _ { p e } ^ { 2 } ,$ where $\omega _ { p e } ~ = ~ ( 4 \pi e ^ { 2 } n _ { e } / m _ { e } ) ^ { 1 / 2 }$ is the frequency of electron plasma with the density $n _ { e }$ (is cgs units). In the underdense plasmas, where $\omega _ { p e } ~ \ll ~ \omega _ { 0 } , \mathrm { ~ a ~ }$ simple estimate for the radiation group velocity can be derived, $\beta _ { G } = \partial _ { k c } \omega \simeq 1 - \omega _ { p e } ^ { 2 } / 2 k ^ { 2 } c ^ { 2 }$ . Moreover, even in vacuum the finite-size laser beam is slowed by the difraction<sup>32</sup>. As a result, the deviation of the Gaussian beams centroid velocity from the speed of light in vacuum estimates as:

$$
1 - \beta _ { G } = n _ { e } / 2 n _ { c } + ( \lambda _ { 0 } / 2 \pi w _ { 0 } ) ^ { 2 } ,\tag{8}
$$

where $n _ { e }$ is the plasma density, and $w _ { 0 }$ is the beam waist. In our test, we propagate the linearly polarized laser beam with the Gaussian profiles, $a = a _ { 0 } \exp ( - r ^ { 2 } / w _ { 0 } ^ { 2 } -$ $x ^ { 2 } / l _ { x } ^ { 2 } )$ , where the parameters are $a _ { 0 } = 1 0 ^ { - 2 } , w _ { 0 } = 1 2 \lambda _ { 0 }$ and $l _ { x } = 1 2 \lambda _ { 0 }$ . Firstly, laser travels $5 0 \lambda _ { 0 }$ distance in vacuum until its centroid enters the plasma. The plasma density increases linearly along first $5 0 \lambda _ { 0 }$ , and then reaches its maximal value of $n _ { e } = 1 0 ^ { - 3 } n _ { c } .$ , after which it remains constant. The longitudinal and transverse resolutions are $\Delta x = 0 . 0 4 8 \lambda _ { 0 }$ and $\Delta r = 0 . 3 2 \lambda _ { 0 }$ , and the timestep is $\Delta t = \Delta x / c$ . At each iteration we measure the laser beam centroid position as $\begin{array} { r } { x _ { c } = \sum x r E _ { z } ^ { 2 } / \sum r E _ { z } ^ { 2 } } \end{array}$ and then deduce its group velocity $\beta _ { G } = \Delta x _ { c } / \Delta t .$ , which is also averaged over the laser period.

Evolution of the laser group velocity in our simulation is shown in fig. 1 with a blue solid curve, and theoretical estimate eq. (8) is plotted with the black dot-dashed line. The blue dashed line corresponds to the FDTD PIC simulation, performed for the same grid resolutions with the quasi-cylindrical code CALDER-CIRC<sup>15</sup>. One can see that the numerical dispersion in FDTD PIC, significantly slows the laser free-space propagation and perturbs its propagation in plasma. To approach the correct laser velocity with the finite diferences method, we had to use much higher resolutions, $\Delta x = 0 . 0 1 6 \lambda _ { 0 } , \Delta r = 0 . 1 6 \lambda _ { 0 }$ (red dashed curve).

![](images/06c8f8fa6cea2ccf46a8b640200507a625159b2f21ddbe72877165ba400368b6.jpg)
FIG. 1. Group velocity of the laser beam in the PSATD PIC simulation with $\Delta x = 0 . 0 4 8 \lambda _ { 0 }$ (solid blue curve), and in FDTD PIC simulations with $\Delta x = 0 . 0 4 8 \lambda _ { 0 }$ (dashed blue curve), and $\Delta x = 0 . 0 1 6 \lambda _ { 0 }$ (dashed red curve). The black dotdashed line corresponds to the theoretical estimate eq. (8).

Propagating in plasma, the laser excites the plasma wave, often refereed as a wake. When $a _ { L } ^ { 2 } \ll 1$ , the produced wake is ”linear”, i.e. the density perturbations in electron plasma are very small, if compared to the plasma density. The laser-driven plasma waves have been extensively studied, and in the linear regime the generated electrostatic fields, aka wakefields, can be described analytically $\left( \mathrm { c f ^ { 3 3 } } \right)$ . From this linear theory, the longitudinal wakefield reads:

$$
\varepsilon _ { x } = \left( \frac { \omega _ { p e } } { 2 \omega _ { 0 } } \right) ^ { 2 } \int _ { x } ^ { \infty } \tilde { \varepsilon } _ { L } ^ { 2 } \cos [ k _ { p e } ( x - x ^ { \prime } ) ] \mathrm { d } x ^ { \prime } ,\tag{9}
$$

where the electron plasma wavenumber is $k _ { p e } = \omega _ { p e } / c .$

In fig. 2, we map with colors the distribution of electrostatic field $\varepsilon _ { x }$ , which clearly corresponds to the plasma wave. The solid blue curve shows the field at the axis $\varepsilon _ { x } ( x , r = 0 )$ , and it is compared to the estimate provided by eq. (9) shown by the dashed curve.

## B. Laser plasma acceleration of electrons

For a more complex test, we model the acceleration of electrons from the underdense plasma by a few-mJ-fewcycle laser pulse. The practical interest to this mechanism is related to the recent idea of using the high repetition rate (kHz) laser for the sources of low energy femtosecond electron beams<sup>34</sup>. Tightly focusing such a laser in a sub-millimeter short plasma, one produces a strong bubble-like wake along the laser Rayleigh length, which is only a few dozens of micrometers. To provide the electron injection into this wake, an abrupt change of the plasma density, so-called shock, is produced near the laser focus. Such interaction is rich with laser-plasma physics $\mathrm { e . g . }$ the laser-driven wakefield, which evolves from the linear to the bubble regime, laser self-focusing near the shock, and generation of the secondary wake by the accelerated beam.

![](images/dfe72677d850f09772d6e8adda3fc06015e50823da3a92fa6534e1ed40f33f4a.jpg)
FIG. 2. Map of the longitudinal electric field ε in plasma. Distribution of the on-axis field value $\varepsilon _ { x } ( r \ = \ 0 )$ extracted from the simulation (solid blue curve) and predicted by the theory (dashed red curve);

In our test, we consider the pre-ionized plasma with the density profile, which grows linearly along first $3 0 0 \lambda _ { 0 }$ to reach its maximal value of $n _ { m a x } ~ = ~ 0 . 0 0 5 n _ { c } ,$ then rapidly falls to $n _ { e } ~ = ~ 0 . 5 n _ { m a x }$ over $1 5 ~ \lambda _ { 0 }$ , and further remains constant. The Gaussian laser beam with $a _ { 0 } = 3$ $w _ { 0 } = 4 \lambda _ { 0 }$ , and $l _ { x } = 5 \lambda _ { 0 }$ is focused at the density peak at $x = 3 0 0 \lambda _ { 0 }$ . The interaction is visually demonstrated in section IV, where the animation is provided by the graphical output from the PLARES-PIC simulation.

For a more detailed analysis, we have compared this simulation with the same test performed with CALDER-CIRC code. Note, that the group velocity of such a tightly focused laser difers significantly from the speed of light in vacuum, hence, the simulation is rather sensitive to the numerical dispersion. In PSATD simulation we consider the grid with $\Delta x = 0 . 0 2 5 \lambda _ { 0 }$ and $\Delta r = 0 . 2 5 \lambda _ { 0 }$ and the time step is $\Delta t = \Delta x / c$ To resolve correctly the laser propagation, and hence the electron injection, the FDTD simulation requires higher resolution, and we used $\Delta x = 0 . 0 1 6 \lambda _ { 0 }$ and $\Delta r = 0 . 1 6 \lambda _ { 0 }$ , and the time step was $\Delta t = 0 . 9 8 \Delta x / c$

In both simulations the structures of the plasma wakes are almost identical, while the accelerated beams difer significantly. To study this we select the electrons with $\gamma _ { p } > 8$ (injected ones), and project their density onto the $( x , r )$ and $( \gamma , \beta _ { \perp } )$ planes for the time $3 8 5 \lambda _ { 0 } / c$ after laser enters the plasma. In the right of fig. 3 we plot the $( x , r )$ density profiles, and, while in PSATD beam has a clear structure with the injection signatures, in FDTD simulation the beam is blurred, and we see the small-scale density modulations near its front. These result from the artificial high-frequency electromagnetic waves, which in FDTD are significantly slowed by numerical difraction, and are generated by the relativistic particles, in a way similar to the physical Cherenkov radiation in the dispersive media. The numerical Cherenkov efect, along with the errors of Lorentz force projection, are known to also increase beams emittance in the wakefield acceleration simulations<sup>4,7</sup>. The particles transverse velocities FDTD is significantly afected by the numerical efects (see upper left of fig. 3), and for more of comparative analysis of the numerical efects in the quasi cylindrical FDTD and PSATD methods $\mathrm { s e e } ^ { 2 1 }$

![](images/000f9d2e7c267e2ca9943cb1b6cbd9f166ae7d45edc465eb85018129d445e456.jpg)

![](images/439cea85305f25514d78372097fc31f70e729288fc6f76c77327811f879e5e79.jpg)

![](images/2c193125b8089e715cf3970df28d22923828c9984a16fd8b3c0d5dfa70d24995.jpg)
FIG. 3. Maps of densities (left panel) and spectra (right panel) of accelerated electrons modeled with FDTD (upper figures) and PSATD (lower figures) methods.

The electrons energy in FDTD simulation is slightly bigger than one in PSATD, as well as the full charge, which is 33 $\mathrm { p C }$ and 28 $\mathrm { p C }$ in the FDTD and spectral models respectively (for $\lambda _ { 0 } = 0 . 8 \mu \mathrm { m } )$ . These diferences can be attributed to the electron injection modeling, which in this test is very fast and is therefore very sensitive to the laser velocity.

## IV. CONCLUSIONS

We have developed and discussed a spectral quasicylindrical particle-in-cell method designed for plasma modeling. The proposed scheme is based on the pseudospectral analytical time domain method, and, in contrast to the commonly used finite-diference PIC schemes, it does not produce grid-related numerical dispersion of electromagnetic fields. Moreover, the electric and magnetic fields are not staggered, which significantly reduces the errors of the Lorentz force projection. This makes the proposed approach advantageous in a wide class of problems, where co-propagation of relativistic particles and light is involved, e.g. simulations of the wakefield accelerators.

The developed model was implemented in the code PLARES-PIC, which was tested and benchmarked against the quasi-cylindrical FDTD PIC code CALDER-

CIRC. The new code has demonstrated capacity to accurately model the laser propagation in vacuum and in plasma, even with the spatial and temporal resolutions few times lower than in FDTD PIC. In the more complex test, we have simulated wakefield acceleration of electrons by a few-mJ-few-cycle laser in the configuration, where electrons are injected in the plasma density shock. The new spectral code has demonstrated a good agreement with the FDTD PIC, save for the numerical efects development in the latter.

The proposed method provides a principally new approach to three-dimensional modeling of plasma electrodynamics. Although the spectral transforms are computationally more demanding than conventional FDTD PIC, the natural accuracy of the spectral method and absence of the numerical dispersion, can often compensate the additional load by using lower temporal and spectral resolutions.

## ACKNOWLEDGMENTS

One of the authors (IAA) acknowledges the support of Victor Malka and Marie-Emmanuelle Couprie, and partial funding from their ERC programs X-Five (contract No. 339128) and COXINEL (contract No. 340015).

## SUPPLEMENTARY MATERIALS

$\mathrm { I n ^ { 3 5 } }$ , we use green colors to plot the electron density, and the colormap scales from the dark green at $n _ { e } = 0$ to the white at $n _ { e } = 0 . 0 1 n _ { c } .$ . The amplitude of the laser beam is mapped in semi-transparent red colors, and their colormap maximum is fixed at $\varepsilon _ { z } = 3$ . The video is based on 665 images, which the graphical module of PLARES-PIC outputs each 30 time-steps.

## Appendix A: Definition of Fourier-Bessel transform

The generalized Fourier-Bessel series consists of the cylindrical harmonics, $\mathcal { H } = \mathrm { e } ^ { i k _ { x } x + i m \theta } J _ { m } ( k _ { r } r )$ where $( x , r , \theta )$ are the coordinates, $J _ { m }$ is the m-th order Bessel function, and parameters $( k _ { x } , k _ { r } , m )$ are the coordinates in the spectral space. In the spectral transformation these harmonics are used to represent a function defined in a three-dimensional space as:

$$
f ( \mathbf { r } ) = \sum _ { \mathbf { k } \in \mathcal { K } } \mathcal { H } ( \mathbf { k } , \mathbf { r } ) \widehat { f } _ { \mathbf { k } } ,\tag{A1}
$$

where the discrete spectral domain K defines the possible wavenumbers ${ \boldsymbol { \mathsf { x } } } = ( k _ { x } , k _ { r } , m )$ . Practically, eq. (A1) corresponds to the three transforms of the initial function: Fourier transform over the angle θ, Fourier transform over x-axis, and Hankel transform in the radial direction.

In the quasi-cylindrical PIC methods, the angular Fourier decomposition is considered at the particles positions<sup>15</sup>. This means, that the weight of each macroparticle is presented as $\begin{array} { r } { w _ { p } = \sum _ { m } w _ { p } ^ { ( m ) } \mathrm { e } ^ { - i m \theta _ { p } } } \end{array}$ , and the components $w _ { p } ^ { ( m ) }$ are gathered on the grid separately, to obtain the azimuthal components of the charge density and current. When the angular components of the fields $\mathbf { E } _ { p } ^ { ( m ) }$ are calculated from electromagnetic equations, the total fields are projected onto the particles as, $\begin{array} { r } { \mathbf { E } _ { p } = \sum _ { m } \mathrm { e } ^ { i m \theta _ { p } } \mathbf { E } _ { p } ^ { ( m ) } } \end{array}$

The spectral decomposition in $( x , r )$ -space is done at the nodes of the grid via the consecutive discrete Fourier and Hankel transforms (DFT and DHT). For the DFT we use the fast Fourier transform (FFT), which operates on the uniform spatial and spectral grids, and involves only $\sim N _ { x }$ log $N _ { x }$ instead of the standard $N _ { x } ^ { 2 } { \mathrm { - f o l d } }$ DFT matrix product. Note, that FFT naturally provides the periodic boundaries at $x = 0$ and $x = N _ { x } \Delta x$

For the radial transforms, we define the matrices of the inverse Hankel transforms as, IDH $\Gamma = J _ { m } ( k _ { r } ^ { ( m ) } r _ { j } )$ ， and consider the uniform spatial grid $r _ { j } = j R / N _ { r }$ , where $j = 1 , . . , N _ { \ i }$ are integers, and R is a radial boundary of the simulation domain. Note, that the radial grid is common for all modes, and the point $r = 0$ is excluded, so that the matrices for m $> 0$ will not be degenerate. In this case, the DHT matrix can be computed via the numerical inversion $\mathrm { D H T } = \mathrm { I D H T ^ { - 1 } }$

The choice of the spectral grids $k _ { r } ^ { ( m ) }$ defines the properties of the radial boundaries for each azimuthal mode. We choose the radial boundary $r = R ,$ , to satisfy the Dirichlet condition, $f ( R ) \equiv 0$ , for which $k _ { r } ^ { ( m ) } = u _ { j } ^ { ( m ) } / R$ , where $u _ { j } ^ { ( m ) }$ are the zeros of $J _ { m }$ . In the continuous space, such choice provides the orthogonality of the Bessel terms, and assures the transforms reversibility.

## Appendix B: Useful diferential properties of Fourier-Bessel transform

Mathematical properties of the Fourier-Bessel series are well known, and here we briefly revise their main features used in our study. The diferential properties of eq. (A1) are defined by the basis functions $ { \mathrm { e } } ^ { i \hat { k } _ { x } x } , \  { \mathrm { e } } ^ { i m \theta }$ and $J _ { m } ( k _ { r } r )$ . It is easy to see that, cylindrical harmonics are the eigenfunctions of the Laplace operator, i.e. $\widehat { \nabla ^ { 2 } f } = - \omega ^ { 2 } \widehat { f }$ , where $\omega = \sqrt { k _ { x } ^ { 2 } + k _ { r } ^ { 2 } }$

Let us, construct the first-order diferential operators for the Cartesian vector components. For this, we note that the derivative over the longitudinal coordinate is $\partial _ { x } = i k _ { x }$ , and the transverse derivatives can be presented as,

$$
\partial _ { y } = \cos \theta \partial _ { r } - \frac { \sin \theta } { r } \partial _ { \theta } , \quad \partial _ { z } = \sin \theta \partial _ { r } - \frac { \cos \theta } { r } \partial _ { \theta } .
$$

Using the properties of the Bessel functions, we calculate

the components of the scalar function gradient as:

$$
\begin{array} { r l } & { \partial _ { x } f ^ { ( m ) } = \mathrm { I D F T } _ { x k _ { x } } * \mathrm { I D H T } _ { r k _ { r } } ^ { ( m ) } * i k _ { x } \widehat f _ { k _ { x } k _ { r } } ^ { ( m ) } , } \\ & { \partial _ { y } f ^ { ( m ) } = \mathrm { I D F T } _ { x k _ { x } } * \left( \partial _ { \bot } \mathrm { I D H T } _ { r k _ { r } } ^ { ( m + 1 ) } * \widehat f _ { k _ { x } k _ { r } } ^ { ( m + 1 ) } - \right. } \\ & { \qquad \left. - \partial _ { \bot } \mathrm { I D H T } _ { r k _ { r } } ^ { ( m - 1 ) } * \widehat f _ { k _ { x } k _ { r } } ^ { ( m - 1 ) } \right) , } \\ & { \partial _ { z } f ^ { ( m ) } = \mathrm { I D F T } _ { x k _ { x } } * \left( \partial _ { \bot } \mathrm { I D H T } _ { r k _ { r } } ^ { ( m + 1 ) } * i \widehat { f } _ { k _ { x } k _ { r } } ^ { ( m + 1 ) } + \right. } \\ & { \qquad \left. + \partial _ { \bot } \mathrm { I D H T } _ { r k _ { r } } ^ { ( m - 1 ) } * i \widehat { f } _ { k _ { x } k _ { r } } ^ { ( m - 1 ) } \right) , } \end{array}\tag{B1}
$$

where ”∗” means matrix product, and the transformation matrices for the transverse derivatives are:

$$
{ \partial _ { \perp } } \mathrm { I D H T } _ { r k _ { r } } ^ { ( m \pm 1 ) } = \frac { k _ { r } ^ { ( m \pm 1 ) } } { 2 } J _ { m } \left( k _ { r } ^ { ( m \pm 1 ) } r \right) .
$$

In contrast to the ordinary Fourier series, the transverse derivatives in eq. (B1) couple the azimuthal modes m with $m + 1$ and $m - 1$

Linearly combining the transformation matrices, one can construct any necessary diferential operatior. For example, for the spectral-spectral and real-spectral derivative projectors one should use the operators,

$$
\mathrm { D H T } _ { k _ { r } r } ^ { ( m ) } * \partial _ { \perp } \mathrm { I D H T } _ { r k _ { r } } ^ { ( m \pm 1 ) } ,
$$

and,

$$
\mathrm { D H T } _ { k _ { r } r } ^ { ( m ) } * \partial _ { \perp } \mathrm { I D H T } _ { r k _ { r } } ^ { ( m \pm 1 ) } * \mathrm { D H T } _ { k _ { r } r } ^ { ( m \pm 1 ) } ,
$$

respectively.

In our study, we use eq. (B1) for spectral-real projection of the magnetic field, and another diferential operator is constructed for the real-spectral projection of charge density n directly to its gradient $\widehat { \nabla n }$ The spectral-spectral rot, div and grad operations are used for the current correction operations in eq. (7) and for magnetic field calculation eq. (3b).

<sup>1</sup>R.W. Hockney and J.W. Eastwood. Computer Simulation Using Particles. CRC Press, 1988.

<sup>2</sup>C.K. Birdsall and A.B. Langdon. Plasma physics via computer simulation. Series in plasma physics. Taylor & Francis, 2004.

<sup>3</sup>A. Taflove and S.C. Hagness. Computational Electrodynamics: The Finite-Diference Time-Domain Method. Norwood, MA: Artech House, 3rd edition, 2005.

<sup>4</sup>R. Lehe, A. Lifschitz, C. Thaury, V. Malka, and X. Davoine. Numerical growth of emittance in simulations of laser-wakefield acceleration. Phys. Rev. ST Accel. Beams, 16:021301, Feb 2013.

<sup>5</sup>R. Nuter, M. Grech, P. Gonzalez de Alaiza Martinez, G. Bonnaud, and E. d’Humieres. Maxwell solvers for the simulations of the laser-matter interaction. The European Physical Journal D, 68(6), 2014.

<sup>6</sup>B.B. Godfrey and Vay J.-L. Suppressing the numerical cherenkov instability in {FDTD} {PIC} codes. Journal of Computational Physics, 267:1 – 6, 2014.

<sup>7</sup>R. Lehe, C. Thaury, E. Guillaume, A. Lifschitz, and V. Malka. Laser-plasma lens for laser-wakefield accelerators. Phys. Rev. ST Accel. Beams, 17:121301, Dec 2014.

<sup>8</sup>E. Esarey, C. B. Schroeder, and W. P. Leemans. Physics of laser-driven plasma-based electron accelerators. Rev. Mod. Phys., 81:1229–1285, Aug 2009.

<sup>9</sup>M. Litos and et. al. High-eficiency acceleration of an electron beam in a plasma wakefield accelerator. Nature, 515:92–95, 2014.

<sup>10</sup>S. Corde and et. al. Multi-gigaelectronvolt acceleration of positrons in a self-loaded plasma wakefield. Nature, 524:442–445, 2015.

<sup>11</sup>S. Corde, K. Ta Phuoc, G. Lambert, R. Fitour, V. Malka, A. Rousse, A. Beck, and E. Lefebvre. Femtosecond x rays from laser-plasma accelerators. Rev. Mod. Phys., 85:1–48, Jan 2013.

<sup>12</sup>I Haber, R. Lee, H. Klein, and Boris J. Advances in electromagnetic simulation techniques. In Proc. Sixth Conf. on Num. Sim. Plasmas, Berkeley, CA, pages 46–48, 1973.

<sup>13</sup>Q. H. Liu. The pstd algorithm: A time-domain method requiring only two cells per wavelength. Microwave and Optical Technology Letters, 15(3):158–165, 1997.

<sup>14</sup>J.-L. Vay, I. Haber, and B.B. Godfrey. A domain decomposition method for pseudo-spectral electromagnetic simulations of plasmas. Journal of Computational Physics, 243:260 – 268, 2013.

<sup>15</sup>A.F. Lifschitz, X. Davoine, E. Lefebvre, J. Faure, C. Rechatin, and V. Malka. Particle-in-cell modelling of laser–plasma interaction using fourier decomposition. Journal of Computational Physics, 228(5):1803 – 1814, 2009.

<sup>16</sup>A. Davidson, A. Tableman, W. An, F.S. Tsung, W. Lu, J. Vieira, R.A. Fonseca, L.O. Silva, and W.B. Mori. Implementation of a hybrid particle code with a {PIC} description in r–z and a gridless description in φ into {OSIRIS}. Journal of Computational Physics, 281:1063 – 1077, 2015.

<sup>17</sup>P. Yu, X. Xu, A. Tableman, V. K. Decyk, F. S. Tsung, F. Fiuza, A. Davidson, J. Vieira, R. A. Fonseca, W. Lu, L. O. Silva, and W. B. Mori. Mitigation of numerical cerenkov radiation and instability using a hybrid finite diference-ft maxwell solver and a local charge conserving current deposit. ArXiv e-prints, February 2015.

<sup>18</sup>M. Guizar-Sicairos and J.C. Gutierrez-Vega. Computation of quasi-discrete hankel transforms of integer order for propagating optical wave fields. J. Opt. Soc. Am. A, 21(1):53, 2004.

<sup>19</sup>M. Veysman, B. Cros, N. E. Andreev, and G. Maynard. Theory and simulation of short intense laser pulse propagation in capillary tubes with wall ablation. Physics of Plasmas, 13(5):053114, 2006.

<sup>20</sup>I.A. Andriyash, R. Lehe, and V. Malka. A spectral unaveraged algorithm for free electron laser simulations. Journal of Computational Physics, 282(0):397 – 409, 2015.

<sup>21</sup>R. Lehe, M. Kirchen, I.A. Andriyash, B.B. Godfrey, and J.-L. Vay. A spectral, quasi-cylindrical and dispersion-free particle-incell algorithm. arXiv.1507.04790, 2015.

<sup>22</sup>L.D. Landau and Lifshitz E.M. The Classical Theory of Fields, volume 2 of Course of Theoretical Physics. Pergamon Press, fourth edition, 1975.

<sup>23</sup>R. L. Morse and C. W. Nielson. Numerical simulation of the weibel instability in one and two dimensions. Physics of Fluids, 14(4):830–840, 1971.

<sup>24</sup>T.Zh. Esirkepov. Exact charge conservation scheme for particlein-cell simulation with an arbitrary form-factor. Computer Physics Communications, 135(2):144 – 153, 2001.

<sup>25</sup>R. Koslof and D. Koslof. Absorbing boundaries for wave propagation problems. Journal of Computational Physics, 63(2):363 – 376, 1986.

<sup>26</sup>J.P. Boris. Relativistic plasma simulation - optimization of a hybrid code. Proceedings, Fourth Conference on the Numerical Simulation of Plasma, 1970.

<sup>27</sup>S. van der Walt, S.C. Colbert, and G. Varoquaux. The numpy array: A structure for eficient numerical computation. Computing in Science Engineering, 13(2):22–30, 2011.

<sup>28</sup>J.D. Hunter. Matplotlib: A 2d graphics environment. Computing in Science Engineering, 9(3):90–95, 2007.

<sup>29</sup>Pearu Peterson. F2py: a tool for connecting fortran and python programs. Int. J. of Computational Science and Engineering, 4(4):296–305, 2009.

<sup>30</sup>Matteo Frigo, Steven, and G. Johnson. The design and implementation of ftw3. In Proceedings of the IEEE, pages 216–231,

2005.

<sup>31</sup>Lisandro D. Dalcin, Rodrigo R. Paz, Pablo A. Kler, and Alejandro Cosimo. Parallel distributed computing using python. Advances in Water Resources, 34(9):1124 – 1139, 2011. New Computational Methods and Software Tools.

<sup>32</sup>E. Esarey, P. Sprangle, M. Pillof, and J. Krall. Theory and group velocity of ultrashort, tightly focused laser pulses. J. Opt. Soc. Am. B, 12(9):1695–1703, Sep 1995.

<sup>33</sup>L.M. Gorbunov and V.I. Kirsanov. Excitation of plasma waves by an electromagnetic wave packet. Sov. Phys. JETP, 66:290–294, 1987.

<sup>34</sup>B. Beaurepaire, Lifschitz A., and Faure J. Electron acceleration in sub-relativistic wakefields driven by few-cycle laser pulses. New Journal of Physics, 16(2):023023, 2014.

<sup>35</sup>https://www.dropbox.com/s/hoqtlas8ut914o0/plares\_movie. avi.
