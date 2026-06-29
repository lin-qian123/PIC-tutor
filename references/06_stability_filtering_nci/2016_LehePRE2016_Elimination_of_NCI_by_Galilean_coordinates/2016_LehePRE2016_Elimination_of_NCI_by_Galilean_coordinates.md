# Elimination of Numerical Cherenkov Instability in flowing-plasma Particle-In-Cell simulations by using Galilean coordinates

Remi Lehe<sup>a</sup>,<sup>∗</sup> Manuel Kirchen<sup>b</sup>, Brendan B. Godfrey<sup>a,c</sup>, Andreas R. Maier<sup>b</sup>, and Jean-Luc Vay<sup>a</sup>

<sup>a</sup> Lawrence Berkeley National Laboratory, Berkeley, CA 94720, USA

<sup>b</sup> Center for Free-Electron Laser Science & Department of Physics,

University of Hamburg, 22761 Hamburg, Germany

<sup>c</sup> University of Maryland, College Park, MD 20742, USA

(Dated: August 28, 2018)

Particle-In-Cell (PIC) simulations of relativistic flowing plasmas are of key interest to several fields of physics (including e.g. laser-wakefield acceleration, when viewed in a Lorentz-boosted frame), but remain sometimes infeasible due to the well-known numerical Cherenkov instability (NCI). In this article, we show that, for a plasma drifting at a uniform relativistic velocity, the NCI can be eliminated by simply integrating the PIC equations in Galilean coordinates that follow the plasma (also sometimes known as comoving coordinates) within a spectral analytical framework. The elimination of the NCI is verified empirically and confirmed by a theoretical analysis of the instability. Moreover, it is shown that this method is applicable both to Cartesian geometry and to cylindrical geometry with azimuthal Fourier decomposition.

PACS numbers: 02.70.-c,52.35.-g,52.65.-y

## INTRODUCTION

Simulating relativistic flowing plasmas is of importance in several fields of physics, including relativistic astrophysics (e.g. [1, 2]) and laser-plasma acceleration [3]. More precisely, although in laser-plasma acceleration the plasma is typically at rest in the laboratory frame, it was shown [4] that simulating the interaction in a Lorentzboosted frame – where the plasma is flowing with relativistic speed – reduces computational demands by orders of magnitude.

However, despite the interest surrounding simulations of relativistic flowing plasmas, performing these simulations with Particle-In-Cell (PIC) algorithms [5, 6] remains a challenge. This is because a violent numerical instability, known as the numerical Cherenkov instability (NCI) [7–14], quickly develops for relativistic plasmas and disrupts the simulation.

Several solutions have been proposed to mitigate the NCI [15–22]. Although these solutions eficiently reduce the numerical instability, they typically introduce either strong smoothing of the currents and fields, or arbitrary numerical corrections, which are tuned specifically against the NCI and go beyond the natural discretization of the underlying physical equation. Therefore, it is sometimes unclear to what extent these added corrections could impact the physics at stake.

For instance, NCI-specific corrections include periodically smoothing the electromagnetic field components [7], using a special time step [8, 9] or applying a wide-band smoothing of the current components [8–10]. Another set of mitigation methods involve scaling the deposited currents by a carefully-designed wavenumber-dependent factor [15, 16] or slightly modifying the ratio of electric and magnetic fields (E/B) before gathering their value onto the macroparticles [17–19]. Yet another set of NCIspecific corrections [20–22] consists in combining a small timestep ∆t, a sharp low-pass spatial filter, and a spectral or high-order scheme that is tuned so as to create a small, artificial “bump” in the dispersion relation [20]. While most mitigation methods have only been applied to Cartesian geometry, this last set of methods ([20–22]) has the remarkable property that it can be applied [21] to both Cartesian geometry and quasi-cylindrical geometry (i.e. cylindrical geometry with azimuthal Fourier decomposition [23, 24]). However, the use of a small timestep proportionally slows down the progress of the simulation, and the artificial “bump” is again an arbitrary correction that departs from the underlying physics.

By contrast, in [25], we propose that the NCI can be eliminated – with no arbitrary correction – by simply integrating the PIC equations in Galilean coordinates (also known as comoving coordinates). More precisely, in our method, the Maxwell equations in Galilean coordinates are integrated analytically, using only natural hypotheses, within the PSATD framework (Pseudo-Spectral Analytical-Time-Domain [26, 27]). In the present article, we present the mathematical derivation and implementation of this Galilean PSATD scheme. Moreover, we conduct a detailed empirical and theoretical stability analysis for a uniform flowing plasma. On the other hand, the practical application of this algorithm to realistic, non-uniform plasmas (such as e.g. in laserwakefield acceleration) is presented in [25]. Overall, our method intrinsically supresses the NCI, does not require a small timestep, and applies to both Cartesian and quasicylindrical geometry.

The outline of the present article is the following. We give an intuitive explanation of the Galilean scheme in Section I, and then detail its exact implementation for

![](images/db5f19c9b7ef94a74869a30e5cfc04ae631406b77b836ac1448a3254499d6c0c.jpg)  
FIG. 1. Schematic representation of the Galilean scheme. As explained in the $_ \mathrm { t e x t , }$ the Galilean scheme is not equivalent to a moving window.

Cartesian geometry in Section II. We also show empirically, in Section II, that, for a plasma drifting at a uniform relativistic velocity, the Galilean scheme suppresses the NCI. This fact is then confirmed and explained by a theoretical stability analysis in Section III (again, for Cartesian geometry). Finally, Section IV shows that the Galilean scheme can also be applied to quasi-cylindrical geometry, and that it is then equally efective at suppressing the NCI.

## I. AN INTUITIVE EXPLANATION OF THE GALILEAN SCHEME

The idea of the proposed scheme is to perform a Galilean change of coordinates, and to carry out the simulation in the new coordinates:

$$
{ \pmb x } ^ { \prime } = { \pmb x } - { \pmb v } _ { g a l } t\tag{1}
$$

where $\pmb { x } = x \pmb { u } _ { x } + y \pmb { u } _ { y } + z \pmb { u } _ { z }$ and $\pmb { x } ^ { \prime } = x ^ { \prime } \pmb { u } _ { x } + y ^ { \prime } \pmb { u } _ { y } + z ^ { \prime } \pmb { u } _ { z }$ are the position vectors in the standard and Galilean coordinates respectively.

We typically choose ${ \pmb v } _ { g a l } = { \pmb v } _ { 0 }$ , where $\pmb { v } _ { \mathrm { 0 } }$ is the speed of the bulk of the relativistic plasma. In this case, in the Galilean coordinates $\mathbf { x } ^ { \prime } .$ , the plasma does not move with respect to the grid – or, equivalently, in the standard coordinates x, the grid moves along with the plasma (as represented in Fig. 1). The heuristic intuition behind this scheme is that these coordinates should prevent the discrepancy between the Lagrangian and Eulerian points of view, which gives rise to the NCI [12].

While in the standard coordinates x, the equations of particle motion and the Maxwell equations have the

familiar form

$$
{ \frac { d { \pmb x } } { d t } } = { \frac { \pmb p } { \gamma m } }\tag{2a}
$$

$$
{ \frac { d { \pmb p } } { d t } } = q \left( { \pmb E } + { \frac { \pmb p } { \gamma m } } \times { \pmb B } \right)\tag{2b}
$$

$$
{ \frac { \partial B } { \partial t } } = - \nabla \times { \bf E }\tag{2c}
$$

$$
\frac { 1 } { c ^ { 2 } } \frac { \partial \pmb { E } } { \partial t } = \nabla \times \pmb { B } - \mu _ { 0 } \pmb { j }\tag{2d}
$$

in the Galilean coordinates $\mathbf { x } ^ { \prime } .$ , these equations become

$$
\frac { d \pmb { x } ^ { \prime } } { d t } = \frac { \pmb { p } } { \gamma m } - \pmb { v } _ { g a l }\tag{3a}
$$

$$
{ \frac { d { \pmb p } } { d t } } = q \left( { \pmb E } + { \frac { \pmb p } { \gamma m } } \times { \pmb B } \right)\tag{3b}
$$

$$
\left( \frac { \partial } { \partial t } - { \pmb v } _ { g a l } \cdot { \pmb \nabla } ^ { \prime } \right) { \pmb B } = - { \pmb \nabla } ^ { \prime } \times { \pmb E }\tag{3c}
$$

$$
\frac { 1 } { c ^ { 2 } } \left( \frac { \partial } { \partial t } - { \pmb v } _ { g a l } \cdot { \pmb \nabla } ^ { \prime } \right) { \pmb E } = { \pmb \nabla } ^ { \prime } \times { \pmb B } - \mu _ { 0 } { \pmb j }\tag{3d}
$$

where $\mathbf { \nabla } \mathbf { \nabla } \mathbf { \nabla } \mathbf { V } ^ { \prime }$ denotes a spatial derivative with respect to the Galilean coordinates $\bar { \mathbf { \boldsymbol { x } } } ^ { \prime }$ . The idea of the Galilean scheme is to design a PIC code which integrates the equations Eqs. (3a) to (3d) instead of Eqs. (2a) to (2d). Of course, physically, these two sets of equations are equivalent, as they are simply connected by a change of variables. However, we show in this paper that, numerically, these sets of equations have diferent stability properties, when integrated with the PSATD scheme. Indeed, as shown in the next section, one of the unique feature of the PSATD scheme is that it takes into account the assumed time evolution of the current $j$ within one timestep. This allows us to push the idea of the coordinate change Eq. (1) further, by embedding it into the assumed time evolution of $j$ (see Eqs. (6) and (7) in the next section). As we will show in Section III, this turns out to be key for the elimination of the NCI.

Before going further, let us remark that the Galilean change of coordinates Eq. (1) is a simple translation. Thus, when used in the context of Lorentz-boosted simulations [4], it does of course preserve the relativistic dilatation of space and time which gives rise to the characteristic computational speedup of the boosted-frame technique.

Another important remark is that the Galilean scheme is not equivalent to a moving window (and in fact the Galilean scheme can be independently combined with a moving window). Whereas in a moving window, gridpoints are added and removed so as to efectively translate the boundaries, in the Galilean scheme the gridpoints themselves are translated (and, again, in this case the physical equations are modified accordingly). In addition, the assumed time evolution of j within one timestep (see Eqs. (6) and (7) in the next section) is diferent in a standard PSATD scheme with moving window and in a Galilean PSATD scheme.

## II. THE GALILEAN PSATD SCHEME IN CARTESIAN GEOMETRY

While the previous section gave an intuitive description of the Galilean scheme, in the present section we introduce the exact numerical scheme that corresponds to this intuitive description – in the case of Cartesian geometry.

We start by deriving the update equations for the fields (Section II A). The resulting PIC loop is then briefly described in Section II B. Finally, in section Section II C, we show empirically that this PIC scheme has better stability property than the standard PSATD in the case of a relativistic plasma.

## A. Derivation of the discretized Maxwell equations in the Galilean PSATD scheme

In the PSATD scheme, the Maxwell equations are advanced by tranforming the fields E and B into Fourier space, and then by integrating the Maxwell equations analytically over one timestep.

In the case of the Galilean PSATD scheme, in order to analytically integrate the Maxwell equations in Galilean coordinates Eqs. (3c) and (3d), we first decouple the equations for E and B by combining Eqs. (3c) and (3d) into second-order diferential equations:

$$
\left( { \frac { \partial } { \partial t } - { \pmb v } _ { g a l } \cdot { \pmb \nabla } ^ { \prime } } \right) ^ { 2 } { \pmb B } - c ^ { 2 } { \pmb \nabla ^ { \prime } } ^ { 2 } { \pmb B } = \frac { 1 } { \epsilon _ { 0 } } { \pmb \nabla } ^ { \prime } \times { \pmb j }\tag{4a}
$$

$$
\begin{array} { c } { \displaystyle \left( \frac { \partial } { \partial t } - \pmb { v } _ { g a l } \cdot \pmb { \nabla } ^ { \prime } \right) ^ { 2 } E \mathrm { - } c ^ { 2 } \pmb { \nabla } ^ { \prime } \mathrm { ^ 2 } \pmb { E } = - \frac { c ^ { 2 } } { \epsilon _ { 0 } } \pmb { \nabla } ^ { \prime } \rho } \\ { \displaystyle - \frac { 1 } { \epsilon _ { 0 } } \left( \frac { \partial } { \partial t } - \pmb { v } _ { g a l } \cdot \pmb { \nabla } ^ { \prime } \right) j } \end{array}\tag{4b}
$$

Note that we used the equations $\nabla ^ { \prime } \cdot \boldsymbol { E } = \rho / \epsilon _ { 0 } , \nabla ^ { \prime } \cdot \boldsymbol { B } = 0$ and $\epsilon _ { 0 } \mu _ { 0 } c ^ { 2 } = 1$ in order to obtain the above equations. In Fourier space, these equations become:

$$
\left( { \frac { \partial } { \partial t } - i { \pmb { k } } \cdot { \pmb { v } } _ { g a l } } \right) ^ { 2 } \hat { \pmb { \mathscr { B } } } + c ^ { 2 } { \pmb { k } } ^ { 2 } \hat { \pmb { \mathscr { B } } } = \frac { 1 } { \epsilon _ { 0 } } i { \pmb { k } } \times \hat { \pmb { \mathscr { I } } }\tag{5a}
$$

$$
\begin{array} { r } { \left( \displaystyle { \frac { \partial } { \partial t } - i \pmb { k } \cdot \pmb { v } _ { g a l } } \right) ^ { 2 } \hat { \pmb { \mathscr { E } } } + c ^ { 2 } \pmb { k } ^ { 2 } \hat { \pmb { \mathscr { E } } } = - \displaystyle { \frac { c ^ { 2 } } { \epsilon _ { 0 } } } \hat { \rho } i \pmb { k } } \\ { - \displaystyle { \frac { 1 } { \epsilon _ { 0 } } } \left( \displaystyle { \frac { \partial } { \partial t } - i \pmb { k } \cdot \pmb { v } _ { g a l } } \right) \hat { \pmb { \mathscr { I } } } } \end{array}\tag{5b}
$$

where the Fourier components are defined by $\hat { \mathcal { F } } ( \pmb { k } , t ) =$ $\textstyle \int d ^ { 3 } { \pmb x } ^ { \prime } F ( { \pmb x } ^ { \prime } , t ) e ^ { - i { \pmb k } \cdot { \pmb x } ^ { \prime } }$ , and F is either E, B, j or $\rho .$

Eqs. (5a) and (5b) are linear ordinary diferential equations in $t ,$ and they can be integrated analytically over one timestep (i.e. from $t = n \Delta t$ to $t = ( n + 1 ) \Delta t )$ provided that the time evolutions of the source terms $\hat { \mathcal { I } } ( k , t )$ and $\hat { \rho } ( \pmb { k } , t )$ are known over this timestep – or, equivalently, provided that the time evolutions of the corresponding real-space function $\boldsymbol { j } ( \boldsymbol { x } ^ { \prime } , t )$ and $\rho ( { \boldsymbol { \mathbf { \mathit { x } } } } ^ { \prime } , t )$ are known.

However, in a PIC code, $\boldsymbol { j } ( \boldsymbol { x } ^ { \prime } , t )$ and $\rho ( { \boldsymbol { \mathbf { \mathit { x } } } } ^ { \prime } , t )$ are obtained from the deposition of the macroparticles’ charge and current onto the grid. For this reason $\boldsymbol { j } ( \boldsymbol { x } ^ { \prime } , t )$ and $\rho ( { \boldsymbol { \mathbf { \mathit { x } } } } ^ { \prime } , t )$ are only known at a few discrete times between $n \Delta t$ and $( n + 1 ) \Delta t$ . For instance, in a typical PSATD PIC cycle, $j$ is only computed at time $( n + 1 / 2 ) \Delta t$ and $\rho$ at times $n \Delta t$ and $( n + 1 ) \Delta t$

Thus, in order to analytically integrate equations Eqs. (5a) and (5b), one needs to make explicit assumptions on the time evolution of $j$ and $\rho$ between these known times. In the standard PSATD scheme (i.e. when the Maxwell equations are integrated in the standard coordinates x), one typically assumes the current $j$ to be constant over one timestep:

$$
j ( x , t ) = j ( x , ( n + 1 / 2 ) \Delta t ) \qquad \forall t \in [ n \Delta t , ( n + 1 ) \Delta t ]\tag{6}
$$

However, when integrating the Maxwell equations in the Galilean variables $\bar { \mathbf { \ b { x } } ^ { \prime } }$ , it is more natural to assume

$$
j ( x ^ { \prime } , t ) = j ( x ^ { \prime } , ( n + 1 / 2 ) \Delta t ) \qquad \forall t \in [ n \Delta t , ( n + 1 ) \Delta t ]
$$

i.e. that the current is constant over one timestep in the Galilean coordinates. Because of the definition of $\mathbf { x } ^ { \prime }$ (see Eq. (1)), the assumptions Eq. (6) and Eq. (7) are not equivalent. In fact, assuming Eq. (7) instead of Eq. (6) is one of the key diference between the Galilean PSATD scheme described here, and the standard PSATD scheme.

Once we adopt the assumption Eq. (7), our numerical scheme is fully determined. Eq. (7) indeed results in:

$$
\hat { \mathcal { I } } ( k , t ) = \hat { \mathcal { I } } ( k , ( n + 1 / 2 ) \Delta t ) \qquad \forall t \in [ n \Delta t , ( n + 1 ) \Delta t ]\tag{8}
$$

This equation in turn allows us to infer the time evolution of $\hat { \rho } ( \boldsymbol { k } , t )$ between n∆t and $( n + 1 ) \Delta t$ . Indeed, in the Galilean coordinates, the equation of continuity reads $\left( \partial _ { t } - { \pmb v } _ { g a l } \cdot \pmb { \nabla } ^ { \prime } \right) \rho + \pmb { \nabla } ^ { \prime } \cdot \pmb { j } = \bar { \bf 0 } ,$ , which becomes in Fourier space $\left( \partial _ { t } - i \pmb { k } \cdot \pmb { v } _ { g a l } \right) \hat { \rho } + i \pmb { k } \cdot \hat { \pmb { \mathcal { I } } } = 0$ . The solution $\hat { \rho } ( \pmb { k } , t )$ of this equation for a constant $\hat { \mathcal { I } }$ is necessarily of the form:

$$
\begin{array} { r l } { \hat { \rho } ( \pmb { k } , t ) = \hat { \rho } ( \pmb { k } , ( n + 1 ) \Delta t ) \frac { 1 - e ^ { i \pmb { k } \cdot \pmb { v } _ { g a l } ( t - n \Delta t ) } } { 1 - e ^ { i \pmb { k } \cdot \pmb { v } _ { g a l } \Delta t } } } & { { } } \\ { - \hat { \rho } ( \pmb { k } , n \Delta t ) \frac { e ^ { i \pmb { k } \cdot \pmb { v } _ { g a l } \Delta t } - e ^ { i \pmb { k } \cdot \pmb { v } _ { g a l } ( t - n \Delta t ) } } { 1 - e ^ { i \pmb { k } \cdot \pmb { v } _ { g a l } \Delta t } } } & { { } } \end{array}\tag{9}
$$

where we explicitly ensured that this solution satisfies the known initial and final conditions $\hat { \rho } ( k , n \Delta t )$ and $\hat { \rho } ( k , ( n +$ $1 ) \Delta t )$ , which, again, are typically obtained from charge deposition during the PIC cycle. As a side note, notice that a necessary and suficient condition for Eq. (9) to be a solution of the continuity equation with $\operatorname { E q . } \ ( 8 )$ is that the following relation be satisfied:

$$
- i ( \boldsymbol { k } \cdot \boldsymbol { v } _ { g a l } ) \frac { \hat { \rho } ^ { n + 1 } - \hat { \rho } ^ { n } e ^ { i \boldsymbol { k } \cdot \boldsymbol { v } _ { g a l } \Delta t } } { 1 - e ^ { i \boldsymbol { k } \cdot \boldsymbol { v } _ { g a l } \Delta t } } + i \boldsymbol { k } \cdot \hat { \mathcal { I } } ^ { n + 1 / 2 } = 0\tag{10}
$$

where we introduced the short-hand notations $\hat { \rho } ^ { n } \equiv$ $\hat { \rho } ( \pmb { k } , n \Delta t ) , \hat { \rho } ^ { n + 1 } \equiv \hat { \rho } ( \pmb { k } , ( n + 1 ) \Delta t )$ and $\hat { \mathcal { I } } ^ { n + 1 / 2 } \equiv$ $\hat { \mathcal { I } } ( k , ( n + 1 / 2 ) \Delta t )$ . Thus Eq. (10) is the discrete equation that $\hat { \rho } ^ { n + 1 } , \hat { \rho } ^ { n } , \hat { \mathcal { T } } ^ { n + 1 / 2 }$ should satisfy in order to satisfy the continuity equation – and therefore to ensure charge conservation – in the Galilean coordinates. (Notice that in the limit ${ v _ { g a l } } = 0$ this equation reduces to $( \hat { \rho } ^ { n + 1 } - \hat { \rho } ^ { n } ) / \Delta t + i \pmb { k } \cdot \hat { \pmb { \mathcal { I } } } ^ { n + 1 / 2 } = 0 . )$ As such, it is also the equation that should be enforced during a PIC cycle, either through an Esirkepov-type deposition scheme or through a current correction scheme.

Finally, the time evolution of $\hat { \rho }$ and $\hat { \mathcal { T } } \mathrm { ~ \Omega ~ } ( \mathrm { E q s } $ (8) and (9)) is inserted into the right-hand side of the Maxwell equations Eqs. (5a) and (5b). Again, these equations are linear ordinary diferential equations, now with explicit expressions in their right-hand side, and they can be integrated analytically. Integrating these equations from $t = n \Delta t$ to $t = ( n + 1 ) \Delta t$ results in the following update equations (see appendix A for the details of the derivation):

$$
\hat { \pmb { \mathscr { B } } } ^ { n + 1 } = \theta ^ { 2 } C \hat { \pmb { \mathscr { B } } } ^ { n } - \frac { \theta ^ { 2 } S } { c k } i \pmb { k } \times \hat { \pmb { \mathscr { E } } } ^ { n } + \ \frac { \theta \chi _ { 1 } } { \epsilon _ { 0 } c ^ { 2 } k ^ { 2 } } \ i \pmb { k } \times \hat { \pmb { \mathscr { I } } } ^ { n + 1 / 2 }\tag{11a}
$$

$$
\begin{array} { r l r } {  { \hat { \pmb { \mathcal { E } } } ^ { n + 1 } = \theta ^ { 2 } C \hat { \pmb { \mathcal { E } } } ^ { n } + \frac { \theta ^ { 2 } S } { k } c i \pmb { k } \times \hat { \pmb { \mathcal { B } } } ^ { n } + \frac { i \nu \theta \chi _ { 1 } - \theta ^ { 2 } S } { \epsilon _ { 0 } c k } \hat { \pmb { \mathcal { I } } } ^ { n + 1 / 2 } } } \\ & { } & { - \frac { 1 } { \epsilon _ { 0 } k ^ { 2 } } ( \chi _ { 2 } \hat { \rho } ^ { n + 1 } - \theta ^ { 2 } \chi _ { 3 } \hat { \rho } ^ { n } ) i \pmb { k } \qquad \mathrm { ( 1 1 b ) } } \end{array}
$$

where we used the short-hand notations $\hat { \pmb { \mathscr { E } } } ^ { n } \equiv \hat { \pmb { \mathscr { E } } } ( { \pmb { k } } , n \Delta t )$ $\hat { \pmb { { \cal B } } } ^ { n } \equiv \hat { \pmb { { \cal B } } } ( k , n \Delta t )$ as well as:

$$
C = \cos ( c k \Delta t ) \quad S = \sin ( c k \Delta t ) \quad k = | \pmb { k } |\tag{12a}
$$

$$
\nu = { \frac { \pmb { k } \cdot \pmb { v _ { g a l } } } { c \pmb { k } } } \quad \theta = e ^ { i \pmb { k \cdot v _ { g a l } } \Delta t / 2 } \quad \theta ^ { * } = e ^ { - i \pmb { k \cdot v _ { g a l } } \Delta t / 2 }\tag{12b}
$$

$$
\chi _ { 1 } = \frac { 1 } { 1 - \nu ^ { 2 } } \left( \theta ^ { * } - C \theta + i \nu \theta S \right)\tag{12c}
$$

$$
\chi _ { 2 } = \frac { \chi _ { 1 } - \theta ( 1 - C ) } { \theta ^ { * } - \theta } \quad \chi _ { 3 } = \frac { \chi _ { 1 } - \theta ^ { * } ( 1 - C ) } { \theta ^ { * } - \theta }\tag{12d}
$$

Note that, in the limit ${ \pmb v } _ { g a l } = { \bf 0 }$ , Eqs. (11a) and (11b) reduce to the standard PSATD equations [26], as expected.

## B. Overview of the PIC cycle for the Galilean PSATD scheme

Eqs. (10), (11a) and (11b) are the fundamental field equations of our PIC cycle. While Section II A emphasized the logical reasoning that leads to these equations, it did not give a precise description of their role within the PIC cycle. Therefore, the present section gives a concise overview of the diferent steps of the PIC cycle, for the Galilean PSATD scheme.

Apart from the fact that the simulation is performed in Galilean coordinates, our PIC cycle is very close to the standard PSATD scheme [26]. In particular, the fields $E ,$ B and $\rho$ and the macroparticles’ positions $\mathbf { x } ^ { \prime }$ are defined at integer times, whereas the field J and the macroparticles’ momenta p are defined at half-integer times. All the fields are defined at the same points in space (i.e. the spatial grid is not staggered). The successive steps of the PIC cycle are represented in Fig. 2 and described below.

## 1. Particle push

The fields E and B are interpolated at time $t = n \Delta t$ from the spatial grid to the macroparticles’ positions (naturally using the Galilean coordinates $\mathbf { x } ^ { \prime }$ for the interpolation). The interpolated fields are then used to push the macroparticles’ momenta from $t = ( n - 1 / 2 ) \Delta t$ to $t = ( n + 1 / 2 ) \Delta t$ , using a discretized version of the equation of motion Eq. (3b). Note that Eq. (3b) is familiar, and can be discretized by using $\mathrm { e . g . }$ the Boris pusher [28] or, as we chose in this paper, the Vay pusher [29]. Then the macroparticles’ positions are pushed from $t = n \Delta t$ to $t = ( n + 1 ) \Delta t$ by using a trivial leap-frog discretization of Eq. (3a):

$$
\pmb { x } ^ { \prime n + 1 } = \pmb { x } ^ { \prime n } + \Delta t \left( \frac { \pmb { p } ^ { n + 1 / 2 } } { \gamma ^ { n + 1 / 2 } m } - \pmb { v } _ { g a l } \right)\tag{13}
$$

where γ<sup>n+1/2</sup> = <sup>p</sup>1 + (p<sup>n+1/2</sup>/mc)<sup>2</sup>.

## 2. Current and charge deposition

The charge density $\rho$ is then computed on the spatial grid at $\begin{array} { r } { t \ = \ n \Delta t } \end{array}$ and $t ~ = ~ ( n + 1 ) \Delta t$ from the macroparticles’ positions ${ \pmb x } ^ { \prime n }$ and $\pmb { x } ^ { m + 1 }$ respectively. In addition, by using the intermediate positions ${ \pmb x } ^ { \prime n + 1 / 2 } \equiv$ $( { \pmb x } ^ { \prime n } + { \pmb x } ^ { \prime n + 1 } ) / 2$ , the current $j _ { d }$ is calculated on the spatial grid at $t = ( n + 1 / 2 ) \Delta t$ . Here, the subscript d emphasizes the fact that we use a direct deposition scheme, rather than a charge-conserving deposition scheme. As a consequence, the Fourier transform $\hat { \mathcal { I } } _ { d } ^ { n + 1 / 2 }$ of the current $j _ { d } ^ { n + 1 / 2 }$ does not satisfy the discretized continuity equation Eq. (10) by default. For this reason, we use the Fourier transform of the charge density at $t = n \Delta t$ and $t = ( n + 1 ) \Delta t$ to compute a corrected current $\hat { \mathcal { I } } ^ { n + 1 / 2 }$ which does satisfy Eq. (10):

$$
\begin{array} { l } { { \displaystyle \hat { \mathcal { T } } ^ { n + 1 / 2 } = \hat { \mathcal { T } } _ { d } ^ { n + 1 / 2 } + \frac { i \pmb { k } } { k ^ { 2 } } \hat { \mathcal { G } } \ ~ ( 1 \pmb { \mathscr { s } } , 0 ) } } \\ { { \displaystyle \hat { \mathcal { G } } = - i ( \pmb { k } \cdot \pmb { v } _ { g a l } ) \frac { \hat { \rho } ^ { n + 1 } - \hat { \rho } ^ { n } e ^ { i \pmb { k } \cdot \pmb { v } _ { g a l } \Delta t } } { 1 - e ^ { i \pmb { k } \cdot \pmb { v } _ { g a l } \Delta t } } + i \pmb { k } \cdot \hat { \mathcal { T } } _ { d } ^ { n + 1 / 2 } } } \end{array}\tag{a}
$$

(14b)

Finally, a light amount of spatial smoothing is applied to $\hat { \rho } ^ { n } , \hat { \rho } ^ { n + 1 }$ and $\hat { \mathcal { I } } ^ { n + 1 / 2 }$ . More precisely, each of these fields is multiplied by a low-pass filter which is equivalent, in real-space, to a one-pass binomial smoother followed

![](images/89775dcf939cbb7d02799de9f4b0969109dce1f2169b4c02192d6fa83920cfec.jpg)  
FIG. 2. Schematic representation of the PIC cycle. The quantities that are known at the beginning of the PIC cycle are displayed in black, while the quantities that are computed during the PIC cycle are displayed in gray. The three successive steps of the PIC cycle – particle push (1), current deposition (2) and Maxwell solver (3) – are represented in purple, red and blue respectively.

by a compensator [6]:

$$
\begin{array} { r } { \hat { \mathcal { T } } ( \pmb { k } ) = \left( 1 - \sin ^ { 2 } ( k _ { x } \Delta x / 2 ) \right) \left( 1 + \sin ^ { 2 } ( k _ { x } \Delta x / 2 ) \right) } \\ { \times \left( 1 - \sin ^ { 2 } ( k _ { y } \Delta y / 2 ) \right) \left( 1 + \sin ^ { 2 } ( k _ { y } \Delta y / 2 ) \right) } \\ { \times \left( 1 - \sin ^ { 2 } ( k _ { z } \Delta z / 2 ) \right) \left( 1 + \sin ^ { 2 } ( k _ { z } \Delta z / 2 ) \right) } \end{array}\tag{15}
$$

where $\Delta x , \Delta y , \Delta z$ are the cell size of the spatial grid in each direction. (For 2D simulations in the x-z plane, this expression is applied with $k _ { y } = 0 . )$

## 3. Maxwell solver

In order to update the values of the fields E and B from $t = n \Delta t$ to $t = ( n + 1 ) \Delta t$ , we first transform them to Fourier space at $t = n \Delta t$ . We then use the deposited fields $\hat { \rho } ^ { n } , \hat { \rho } ^ { n + 1 }$ and $J ^ { n + 1 / 2 }$ as well as Eqs. (11a) and (11b) to obtain the updated values $\hat { \pmb { \mathcal { E } } } ^ { n + 1 }$ and $\hat { \pmb { B } } ^ { n + 1 }$ in spectral space. Finally, these fields are converted back to real space by using an inverse Fourier transform.

## C. Stability of a uniform, relativistic plasma

We implemented the Galilean PSATD scheme described in Section II B in the code Warp [30]. We then tested its stability for simulations of relativistic flowing plasmas, in a 2D Cartesian geometry.

In the test simulations, a uniform plasma of density $n _ { 0 }$ fills a periodic simulation box, and flows towards the positive z with a relativistic speed. The physical and numerical parameters of the simulation are summarized in Table I. We ran this simulation both with the standard

TABLE I. Parameters of the test simulations. The simulations are scaled by $k _ { p , r } \equiv k _ { p } / \gamma _ { 0 } ^ { 1 / 2 }$ , with $k _ { p } ^ { 2 } = n _ { 0 } e ^ { 2 } / m _ { e } \epsilon _ { 0 } c ^ { 2 } .$
<table><tr><td>Plasma density</td><td> $n _ { 0 }$  (scales the simulation)</td></tr><tr><td>Lorentz factor</td><td> $\gamma _ { 0 } = 1 3 0$ </td></tr><tr><td>Cell size along z</td><td> $\Delta z = 0 . 3 8 6 8 \ k _ { p , r } ^ { - 1 }$ </td></tr><tr><td>Cell size along x</td><td> $\Delta x = 0 . 3 8 6 8 \ k _ { p , r } ^ { - 1 }$ </td></tr><tr><td>Timestep</td><td> $\Delta t = \Delta z / c$ </td></tr><tr><td>Number of gridpoints</td><td> $N _ { x } = N _ { z } = 2 0 0$ </td></tr><tr><td>Order of the shape factor</td><td>3 (both in x and z)</td></tr></table>

PSATD scheme and with the Galilean PSATD scheme, using ${ \pmb v } _ { g a l } = { \pmb v } _ { 0 }$ in the latter case, with ${ \pmb v } _ { 0 }$ the velocity of the plasma. (Thus in the standard PSATD simulation, the relativistic plasma cycles through the fixed periodic boundaries of the box, while in the Galilean PSATD sim ulation, the box moves along with the plasma.)

The results of this test are shown in Fig. 3. As shown in the top panel, in the case of the standard PSATD the fluctuations of the electric fields grow exponentially and saturate shortly after the beginning of the simulation. This a result of the well-known NCI. Conversely, with the Galilean PSATD the fluctuations of $E _ { x }$ remain at a low level, and can be explained by a simple accumulation of numerical noise. This interpretation is confirmed by the maps of the electric field in the middle and bottom panels. While the standard PSATD simulation exhibits a high-wavenumber pattern that is characteristic of the NCI, the Galilean PSATD simulation exhibits a random-looking pattern (with an amplitude that is lower by almost 10 orders of magnitude) that is consistent with numerical or thermal noise.

![](images/c67fea7025debced04e768d9667e9138e705bf5f7f3422907066471c21a73c5e.jpg)

Standard PSATD at $\omega _ { p , r } t = 3 2 9$  
![](images/46107bbc707ab12c5c323399ff7a595977e7ccd5e8c5e4486a8db22c6a31039d.jpg)

![](images/b07d344c93356711ccdba04261acbd2115536c6e0b2c4f9ad982f0eb39b3018c.jpg)  
FIG. 3. Results of a relativistic flowing plasma simulation in Warp, with the standard and Galilean PSATD scheme. Top panel: RMS amplitude of the electric field in the simulation box versus time. (By definition, $\omega _ { p , r } \equiv \omega _ { p } / \gamma _ { 0 } ^ { 1 / 2 }$ and $E _ { 0 } \equiv m _ { e } c \omega _ { p , r } / e . )$ Middle and bottom panels: Maps of the electric field in the simulation box, at a given time, for both the standard and Galilean PSATD scheme. $( k _ { p , r } \equiv k _ { p } / \gamma _ { 0 } ^ { 1 / 2 } )$

The Galilean PSATD scheme is thus empirically much more stable than the standard PSATD scheme. Again, a remarkable point is that we did not introduce any NCIspecific correction here. Instead, the Galilean scheme simply results from the natural analytical integration of the Maxwell equations in the Galilean coordinates, with no additional corrections.

## III. STABILITY ANALYSIS IN 2D CARTESIAN GEOMETRY

While the previous section showed empirically that the Galilean PSATD scheme is more stable, in the present section we confirm and explain these results by using the

theoretical dispersion relation that corresponds to this numerical scheme.

## A. Dispersion equation

More precisely, we start with a neutral, uniform plasma, flowing with a velocity $\pmb { v } _ { 0 } = v _ { 0 } \pmb { u } _ { z }$ (and Lorentz factor $\gamma _ { 0 } )$ through a 2D periodic grid, and we consider the evolution of a small perturbation to its fields, of the form:

$$
E , B \propto e ^ { i \mathbf { k } \cdot \mathbf { x } - i \omega t } = e ^ { i \mathbf { k } \cdot \mathbf { x } ^ { \prime } - ( \omega - \mathbf { k } \cdot \mathbf { v } _ { g a l } ) t }\tag{16}
$$

Notice that, with the above definition, the physical interpretation of ω and k is the natural one, and in particular this interpretation does not depend on the choice of ${ \pmb v } _ { g a l } .$

By combining the perturbed Vlasov equation and the Maxwell equations, we obtain a dispersion equation that relates $\omega$ and k. Importantly, the analysis – and the resulting dispersion equation – incorporate all the numerical efects that are introduced by the PIC cycle from Section II B (including finite timestep, finite spatial resolution, shape factors, current correction, etc.). Note however that the analysis has been restricted to the case where ${ { v } _ { g a l } }$ is along $z \left( \mathrm { i . e . } \ v _ { g a l } = v _ { g a l } { \pmb u } _ { z } \right)$ . The full derivation of the dispersion equation is given in appendix B. Although this derivation builds upon previous work [12–15], a number of important changes have been introduced in order to accomodate the specifics of the Galilean PSATD scheme.

The resulting dispersion relation is given in Eq. (19), along with the expression of the dimensionless coeficients ξ (Eqs. (20a) to (20c)), which represent the response of the plasma, and include the efects of spatial field smoothing $( { \hat { T } } ( k ) )$ , spatial aliases $\begin{array} { r } { ( K _ { m } = m _ { x } \frac { 2 \pi } { \Delta x } \pmb { u } _ { x } \ + } \end{array}$ $m _ { z } \frac { 2 \pi } { \Delta z } { \pmb u } _ { z } )$ and finite shape factor $( \hat { S } ( k ) )$ . The factor $\hat { S } ( k )$ indeed represents the Fourier transform of the macroparticle shape factor, so that e.g. for a shape factor of order $\ell _ { x }$ and $\ell _ { z }$ along x and z respectively, one has:

$$
\hat { S } ( k ) = \mathrm { s i n c } ^ { \ell _ { x } + 1 } \left( \frac { k _ { x } \Delta x } { 2 } \right) \mathrm { s i n c } ^ { \ell _ { z } + 1 } \left( \frac { k _ { z } \Delta z } { 2 } \right)\tag{17}
$$

with sin $\mathrm { c } ( x ) \ = \ \sin ( x ) / x .$ In addition, in Eqs. (19) and (21) we also used the short-hand notations

$$
s _ { x } = \sin \left( \frac { x \Delta t } { 2 } \right) \quad c _ { x } = \cos \left( \frac { x \Delta t } { 2 } \right) \quad t _ { x } = \tan \left( \frac { x \Delta t } { 2 } \right)\tag{18}
$$

and we introduced $\chi _ { 5 }$ and ${ \boldsymbol { \chi } } _ { 5 } ^ { \prime }$ , which are coeficients that depend only on $\omega ,$ k and $\nu = \pmb { k } \cdot \pmb { v } _ { g a l } / ( c k )$ , and whose mathematical expression results from the key hypothesis Eq. (7).

$$
\begin{array} { r l } & { ( s _ { \omega } ^ { 2 } - l _ { c k } ^ { 2 } c _ { \omega } ^ { 2 } ) \left[ 1 - \frac { 1 } { k } \left( k _ { x } \xi _ { 3 x } + \frac { k _ { z } \xi _ { 3 z } } { \gamma _ { 0 } ^ { 2 } } \right) \right] - \xi _ { 1 } \left[ \frac { \chi _ { 5 } } { k ^ { 2 } } \left( k _ { z } ^ { 2 } + \frac { k _ { x } ^ { 2 } } { \gamma _ { 0 } ^ { 2 } } \right) + \chi _ { 5 } ^ { \prime } \frac { k _ { z } v _ { 0 } } { c k } \right] } \\ & { + \frac { k _ { x } v _ { 0 } } { c k } \left[ \frac { \chi _ { 5 } } { k } \left( k _ { z } \xi _ { 2 x } - \frac { k _ { x } \xi _ { 2 z } } { \gamma _ { 0 } ^ { 2 } } \right) + \chi _ { 5 } ^ { \prime } \frac { \xi _ { 2 x } v _ { 0 } } { c } \right] + \frac { 1 } { \gamma _ { 0 } ^ { 2 } } \left( \chi _ { 5 } + \frac { k _ { z } v _ { 0 } } { c k } \chi _ { 5 } ^ { \prime } \right) \left[ \xi _ { 1 } \frac { k _ { x } \xi _ { 3 x } + k _ { z } \xi _ { 3 z } } { k } + \frac { k _ { x } v _ { 0 } } { c k } ( \xi _ { 3 x } \xi _ { 2 z } - \xi _ { 3 z } \xi _ { 2 x } ) \right] = 0 } \end{array}\tag{19}
$$

with

$$
\xi _ { 1 } = { \hat { T } } ( k ) { \frac { \omega _ { p } ^ { 2 } } { \gamma _ { 0 } c k } } \sum _ { m _ { x } , m _ { z } = - \infty } ^ { \infty } { \frac { 1 } { { \frac { 2 } { \Delta t } } \sin \left[ ( \omega - k _ { z } v _ { 0 } ) { \frac { \Delta t } { 2 } } + m _ { z } { \frac { \pi \Delta t } { \Delta z } } ( v _ { g a l } - v _ { 0 } ) \right] } } { \hat { S } } ^ { 2 } ( k + K _ { m } )\tag{20a}
$$

$$
\xi _ { 2 } = { \hat { \mathcal { T } } } ( k ) { \frac { \omega _ { p } ^ { 2 } } { \gamma _ { 0 } k } } \sum _ { m _ { x } , m _ { z } = - \infty } ^ { \infty } { \frac { \cos \left[ ( \omega - k _ { z } v _ { 0 } ) { \frac { \Delta t } { 2 } } + m _ { z } { \frac { \pi \Delta t } { \Delta z } } \left( v _ { g a l } - v _ { 0 } \right) \right] } { { \left( { \frac { 2 } { \Delta t } } \right) } ^ { 2 } \sin ^ { 2 } \left[ \left( \omega - k _ { z } v _ { 0 } \right) { \frac { \Delta t } { 2 } } + m _ { z } { \frac { \pi \Delta t } { \Delta z } } \left( v _ { g a l } - v _ { 0 } \right) \right] } } { \hat { \mathcal { S } } } ^ { 2 } ( k + K _ { m } ) ( k + K _ { m } )\tag{20b}
$$

$$
\xi _ { 3 } = { \hat { \mathcal { T } } } ( k ) { \frac { \omega _ { p } ^ { 2 } } { \gamma _ { 0 } k } } \sum _ { m _ { x } , m _ { z } = - \infty } ^ { \infty } { \frac { 1 } { \left( { \frac { 2 } { \Delta t } } \right) ^ { 2 } \sin ^ { 2 } \left[ \left( \omega - k _ { z } v _ { 0 } \right) { \frac { \Delta t } { 2 } } + m _ { z } { \frac { \pi \Delta t } { \Delta z } } \left( v _ { g a l } - v _ { 0 } \right) \right] } } { \hat { \mathcal { S } } } ^ { 2 } ( k + K _ { m } ) ( k + K _ { m } )\tag{20c}
$$

$$
\chi _ { 5 } = \frac { c _ { \omega } c _ { \nu e k } } { 1 - \nu ^ { 2 } } \left( t _ { \omega } ( t _ { c k } - \nu t _ { \nu c k } ) - t _ { c k } ( t _ { \nu c k } - \nu t _ { c k } ) \right) \qquad \chi _ { 5 } ^ { \prime } = \frac { c _ { \omega } c _ { \nu e k } } { 1 - \nu ^ { 2 } } \left( t _ { \omega } ( t _ { \nu c k } - \nu t _ { c k } ) - t _ { c k } ( t _ { c k } - \nu t _ { \nu c k } ) \right)\tag{21}
$$

Several remarks can be made on the dispersion equation Eq. (19). First of all, note that the set of equations Eqs. (19), (20a) to (20c) and (21) is valid for any value of $v _ { g a l }$ , including $v _ { g a l } = 0$ (standard PSATD) and $v _ { g a l } = v _ { 0 }$ (optimal Galilean PSATD).

Another important point is that it can be verified (although only after some algebra) that Eq. (19) reduces, for any value of $v _ { g a l }$ , to

$$
\frac { \Delta t ^ { 2 } } { 4 } \times \left( \omega ^ { 2 } - c ^ { 2 } k ^ { 2 } - \frac { \omega _ { p } ^ { 2 } } { \gamma _ { 0 } } \right) \times \left( 1 - \frac { \omega _ { p } ^ { 2 } } { \gamma _ { 0 } ^ { 3 } ( \omega - k _ { z } v _ { 0 } ) ^ { 2 } } \right) = 0\tag{22}
$$

in the limit of infinitely small timestep and cell size $( \omega \Delta t \ll 1 , \ k \Delta x \ll 1 , \ k \Delta z \ll 1 )$ Thus, as expected, in the limit of infinitely high resolution, the dispersion equation recovers the two independent physical modes of a relativistic plasma – the relativistic plasma mode $\omega = k _ { z } v _ { 0 } \pm \omega _ { p } \gamma _ { 0 } ^ { - 3 / 2 }$ and the relativistic electromagnetic mode $\omega ^ { 2 } = c ^ { 2 } k ^ { 2 } + \omega _ { p } ^ { 2 } / \gamma _ { 0 }$

Conversely, at finite resolution, Eq. (19) gives rise to distorted modes, which can potentially become unstable. This is particularly true near the numerical resonances of the plasma coeficients $\xi _ { 1 } , \xi _ { 2 } , \xi _ { 3 } .$ i.e. whenever

$$
\omega - k _ { z } v _ { 0 } + m _ { z } \frac { 2 \pi } { \Delta z } ( v _ { g a l } - v _ { 0 } ) = 0 \quad \left( \mathrm { m o d u l o } \ \frac { 2 \pi } { \Delta t } \right)\tag{23}
$$

so that the sine term in the denominators of Eqs. (20a) to (20c) goes to 0. Since the resonance condition Eq. (23) depends on the alias number $m _ { z } \in \mathbb { Z }$ , this equation expresses the well-known fact that resonances occur at a set of diferent frequencies (aliased resonances) [13–15].

In this regard, one consequence of the Galilean coordinates is clear: when choosing $v _ { g a l } = v _ { 0 }$ , the term proportional to $m _ { z }$ in the resonance condition Eq. (23) vanishes, and thus all the aliased resonances are relocated to the same frequency: $\omega - k _ { z } v _ { 0 } = 0$ (modulo $2 \pi / \Delta t )$ . Interestingly, when tracking the corresponding terms throughout appendix ${ \mathrm { B } } ,$ one realizes that this relocation of resonances is a direct consequence of the fact that the grid follows the plasma (as shown in Fig. 1), and that it does not depend on making the assumption Eq. (7) as opposed to $\operatorname { E q } .$ . (6).

Aside from this efect, the only other impact of $v _ { g a l }$ on the dispersion equation Eq. (19) is in the expression of the coeficients $\chi _ { 5 }$ and ${ \boldsymbol { \chi } } _ { 5 } ^ { \prime }$ (through $\nu = \pmb { k } \cdot \pmb { v } _ { g a l } / ( c k ) )$ ， which on the other hand does result from the assumption Eq. (7). This leads us to think that, in the case $v _ { g a l } = v _ { 0 }$ there are special relationships between $\chi _ { 5 }$ and $\chi _ { 5 } ^ { \prime } ,$ , which efectively cancel the relocated resonance. For instance, it can be shown that, in the case $v _ { g a l } = v _ { 0 }$ , the factor $( \chi _ { 5 } + ( k _ { z } v _ { 0 } / c k ) \chi _ { 5 } ^ { \prime } )$ in the last term of Eq. (19) cancels at the resonance, whereas this is not true for $v _ { g a l } = 0$

Beyond these first remarks, it is dificult to analytically extract more insights from Eq. (19), and thus this equation needs to be solved numerically in order to actually predict the stability of a given situation.

## B. Numerical solution and comparison with simulations

We solved the dispersion equation Eq. (19) numerically, with the physical and numerical parameters from Table I. In particular, when solving Eq. (19) for $\omega ,$ we allowed of course for a non-zero imaginary part – since Im(ω) corresponds the growth rate of the instability.

These predicted growth rates were calculated for $v _ { g a l } =$ 0 (standard PSATD) and $v _ { g a l } ~ = ~ v _ { 0 }$ (optimal Galilean PSATD), and they were compared with the corresponding Warp simulations from Section II C. The results of these comparisons are shown in Fig. 4. Note that in the Warp simulations, the growth rate was estimated by taking the Fourier transform of the fields at $\omega _ { p , r } t \simeq 1 2 0$ and $\omega _ { p , r } t \simeq 1 7 0$ (i.e. within the linear growth phase; see Fig. 3) and, for each Fourier mode, by calculating the diference in amplitude between those two times.

In the case of the standard PSATD (left panels in Fig. 4), one can see that the dispersion equation Eq. (19) correctly predicts that the simulation is unstable (existence of positive, non-zero Im(ω)). Moreover, the predicted growth rates from Eq. (19) are in excellent quantitative agreement with the growth rates observed in the Warp simulation. Notice also that, in the left panels of Fig. 4, the unstable modes cluster in two areas of k space: on a fine line at high k, which corresponds to the resonance $m _ { z } = 0$ from Eq. (23), and on a broader area at lower k. This second, broader area corresponds to a nonresonant instability, which has also been predicted and observed in previous work [15, 16, 19].

In the case of the Galilean PSATD $( v _ { g a l } = v _ { 0 } ;$ right panels in Fig. 4), the dispersion equation Eq. (19) predicts that all modes are stable $( \operatorname { I m } ( \omega ) = 0$ across all k space). This is again consistent with the observations from the Warp simulation, since the lower right panel in Fig. 4 displays only noise, with both positive and negative values of Im(ω). Again, in our understanding from the dispersion relation Eq. (19), this elimination of both the resonant and non-resonant NCI is due to mathematical expression of $\chi _ { 5 }$ and $\chi _ { 5 } ^ { \prime }$ , which result from the assumption on the time evolution of j Eq. (7).

On the whole, this section confirms that the Galilean PSATD scheme eliminates the NCI, since the absence of NCI was both predicted theoretically and observed in simulations. Remarkably, the Galilean scheme simultaneously supresses both the high-k resonant instability and low-k non-resonant instability. This contrasts with some of the previous mitigation techniques, which typically introduced two separate numerical corrections in order to handle the resonant and non-resonant instabilities respectively.

## C. Influence of $v _ { g a l }$ on the growth rate

An interesting question is whether $v _ { g a l } = v _ { 0 }$ is indeed the optimal value of the Galilean scheme. To answer this question, we solved the dispersion equation Eq. (19) for a range of value of $v _ { g a l } .$ , spanning from −c to +c (still with the parameters from Table I). In addition, in order to evaluate the robustness of our scheme with respect to the timestep $\Delta t .$ , we repeated this procedure for diferent values of ∆t. The corresponding growth rates are plotted in $\mathrm { F i g . 5 , }$ as a function of $v _ { g a l }$ . As shown on this figure, the growth of rate of the instability only goes to 0 for $v _ { g a l } \simeq c ,$ thereby confirming that the optimal Galilean scheme has $v _ { g a l } \simeq v _ { 0 }$ (in the case of an ultrarelativistic plasma). Remarkably, this behavior is observed for all the values of $\Delta t$ that were tested, thereby indicating that the Galilean scheme eliminates the NCI independently of the value of $\Delta t$

Another important feature of Fig. 5 is that the growth rate does not go to 0 for $v _ { g a l } = - c$ In other words, the NCI is not suppressed when the relativistic plasma and Galilean grid move with opposite velocities. While this fact is to be expected from the intuitive picture of Section I, it can potentially have important implications for practical simulations. For instance, in Lorentz boosted simulations of laser-wakefield acceleration, the optimal Galilean scheme would be that which follows the relativistically-flowing background plasma (in typical conventions, this plasma flows to the left). However, in this case, the accelerated electron beam (which typi cally moves to the right) would counter-propagate with respect to the Galilean grid – thereby potentially triggering the NCI. Nevertheless, in this particular case, we see no evidence of the NCI in practical simulations (see [25]), including when analyzing the emittance of the ac celerated beam. This absence of NCI is probably related to the lack of charge neutrality and limited spatial extent of the beam, and will be investigated further in the future. In this regard, one important efect is the fact that the NCI modes often have a group velocity that is lower than $c ,$ and thus they rapidly slip behind the beam and stop growing.

## IV. THE GALILEAN PSATD SCHEME IN QUASI-CYLINDRICAL GEOMETRY

In Section II and Section III, we discussed the Galilean scheme in the context of a spectral Cartesian PIC code. Recently, two spectral quasi-cylindrical PIC codes were developed [31, 32]. As shown in [23], simulations of physical systems with close-to-cylindrical symmetry can be made faster by orders of magnitude, when using a quasicylindrical grid instead of a 3D Cartesian grid. Therefore, in the present section, we extend the Galilean PSATD scheme to the spectral quasi-cylindrical framework of [31].

![](images/a94493bef63338cfdb72cc62765862b38b459467190dc1e7fa37b80fe9d9a230.jpg)  
Standard PSATD: Warp simulation

![](images/7be6805508e7ecdfffb6e7be22a421aa9102f47d893d2d81e76b01f79da4ae30.jpg)

![](images/c8a2e3906c71714c8b81df5c1be646fefcf2f1d2d0b5410d7618d122bc619c5a.jpg)

Galilean PSATD: Warp simulation  
![](images/47b1bae4767a79dc0923804f7b162840866c8f9d575e9182780758b4c765fa82.jpg)  
FIG. 4. Predicted and observed growth rates Im(ω) of the NCI, in k space (with $k _ { p , r } = k _ { p } / \gamma _ { 0 } ^ { 1 / 2 } )$ . The predicted growth rates (upper panels) are obtained from Eq. (19). All four panels use the parameters from Table I, and in addition the Galilean PSATD (right panels) uses ${ \pmb v } _ { g a l } = v _ { 0 } { \pmb u } _ { z }$

![](images/ddd3e477f727cf070b500a50903afdb16e7ccf73b1efbd28dc52180419fedd6e.jpg)  
FIG. 5. Maximum growth rate of the NCI across all spectral modes (i.e. across all k space), as a function of the velocity $v _ { g a l } ,$ and for diferent timesteps ∆t. The growth rates were calculated by solving Eq. (19) with the parameters from Table I.

## A. Numerical scheme in quasi-cylindrical geometry

It was shown in [31] that a PSATD algorithm could be derived in quasi-cylindrical geometry, by expressing any scalar field S(x) as a sum of Fourier-Bessel modes:

$$
S ( \pmb { x } ) = \sum _ { m = - \infty } ^ { \infty } \int _ { - \infty } ^ { \infty } \mathrm { d } k _ { z } \int _ { 0 } ^ { \infty } \frac { k _ { \bot } \mathrm { d } k _ { \bot } } { ( 2 \pi ) ^ { 2 } } \hat { S } _ { m } ( k _ { z } , k _ { \bot } ) J _ { m } ( k _ { \bot } r ) e ^ { i k _ { z } z - i m \theta }\tag{24}
$$

and similarly by expressing any vector field V (x) as

$$
\begin{array} { r } { V _ { r } ( \pmb { x } ) = \displaystyle \sum _ { m = - \infty } ^ { \infty } \int _ { - \infty } ^ { \infty } d k _ { z } \int _ { 0 } ^ { \infty } \frac { k _ { \bot } \mathrm { d } k _ { \bot } } { ( 2 \pi ) ^ { 2 } } \left( \hat { \mathcal { V } } _ { + , m } ( k _ { z } , k _ { \bot } ) J _ { m + 1 } ( k _ { \bot } r ) \right. } \\ { \left. + \hat { \mathcal { V } } _ { - , m } ( k _ { z } , k _ { \bot } ) J _ { m - 1 } ( k _ { \bot } r ) \right) e ^ { i k _ { z } z - i m \theta } \left. \left( 2 5 \mathrm { a } \right) \right. } \end{array}
$$

$$
\begin{array} { r } { V _ { \theta } ( \pmb { x } ) = \displaystyle \sum _ { m = - \infty } ^ { \infty } \int _ { - \infty } ^ { \infty } d k _ { z } \int _ { 0 } ^ { \infty } \frac { k _ { \perp } \mathrm { d } k _ { \perp } } { ( 2 \pi ) ^ { 2 } } i \left( \hat { \mathcal { V } } _ { + , m } ( k _ { z } , k _ { \perp } ) J _ { m + 1 } ( k _ { \perp } r ) \right. } \\ { \left. - \hat { \mathcal { V } } _ { - , m } ( k _ { z } , k _ { \perp } ) J _ { m - 1 } ( k _ { \perp } r ) \right) e ^ { i k _ { z } z - i m \theta } \left( 2 5 \mathrm { b } \right) } \end{array}
$$

$$
\begin{array} { r l r } {  { V _ { z } ( \pmb { x } ) = \sum _ { m = - \infty } ^ { \infty } \int _ { - \infty } ^ { \infty } d k _ { z } \int _ { 0 } ^ { \infty } \frac { k _ { \perp } \mathrm { d } k _ { \perp } } { ( 2 \pi ) ^ { 2 } } \times } } \\ & { } & { \hat { \mathcal { V } } _ { z , m } ( k _ { z } , k _ { \perp } ) J _ { m } ( k _ { \perp } r ) e ^ { i k _ { z } z - i m \theta } } \end{array}\tag{25c}
$$

where r is the radial coordinate, $J _ { m }$ is the Bessel function of order $m _ { \colon }$ , and where the sum over m is a sum over azimuthal modes. (In a practical PIC simulation, this sum is truncated to a low number of modes, depending on the degree of cylindrical symmetry of the physical problem.) The terms $\hat { \mathcal { V } } _ { + , m } , \hat { \mathcal { V } } _ { - , m } , \hat { \mathcal { V } } _ { z , m }$ and $\hat { S } _ { m }$ represent the spectral components of the fields $V ( x )$ and $S ( { \pmb x } )$

Within this formalism, the equations of the standard quasi-cylindrical PSATD are very similar to those of the standard Cartesian PSATD. In fact, although the quasicylindrical equations were derived from first principle in [31], they can alternatively be obtained by using a formal analogy (see Table II) between the representation of the diferential operators in a spectral Cartesian and spectral quasi-cylindrical framework. More precisely, starting from the equations of the standard Cartesian PSATD, one can obtain the standard quasi-cylindrical PSATD scheme by simply replacing the expressions in the second line of Table II by those in the third line.

Therefore here, using the same heuristic procedure, we obtain the equations of the Galilean quasi-cylindrical PSATD (see appendix C for their full expression) from the equations of the Galilean Cartesian PSATD Eqs. (10), (11a) and (11b), by simply replacing the expressions of the diferential operators. Note that, in this context, both ${ { v } _ { g a l } }$ and the velocity of the relativistic plasma v<sub>0</sub> are necessarily along z.

Apart from these modified equations, the structure of our PIC cycle in quasi-cylindrical geometry is identical to that presented in Section II B for Cartesian geometry.

## B. Stability of a uniform, relativistic plasma

The Galilean PSATD scheme described in the previous section was implemented in the spectral quasi-cylindrical code <sup>FBPIC</sup> [31]. We then performed test simulations featuring a uniform relativistic plasma. Apart from the shape factor (which was set to order 1), the numerical and physical parameters of the simulations are the same as in Table I (where $\Delta x$ and $N _ { x }$ are to be replaced with the corresponding radial parameters $\Delta r = \mathsf { 0 } . 3 8 6 8 k _ { p , r } ^ { - 1 }$ and $N _ { r } = 1 0 0 )$ . In addition, the spatial smoothing function $\hat { \tau }$ was set to $\begin{array} { r } { \hat { \mathcal { T } } ( k _ { z } , k _ { \perp } ) = \cos ^ { 2 } ( k _ { z } \Delta z / 2 ) \cos ^ { 2 } ( k _ { \perp } \Delta r / 2 ) } \end{array}$ as in [31].

The results of these simulations are represented in Fig. 6, using a similar layout as for the corresponding Cartesian simulation (see Fig. 3). These quasi-cylindrical simulations support the same conclusions as their Cartesian counterpart: the standard PSATD scheme is unstable due to the NCI (as evidenced by the solid line in the upper panel of Fig. 6 and by the high-frequency pattern in the corresponding field map, on the middle panel), while the Galilean PSATD scheme remains stable (see the dashed line in the upper panel, and the corresponding field map on the bottom panel, which are consistent with numerical and thermal noise).

![](images/f10631c10351263e5e36423df059f899753a4c231a318c2b1804b4584b7189f6.jpg)

Standard PSATD at $\underline { { \omega } } _ { p } ,$ <sub>; r</sub>t = 346  
![](images/6c5248a697b0755fabbbaec0954740b09a260807f07e504eb6ab86ebe624ecd1.jpg)

![](images/942b327cc9e71fff084c09745ce518d4f723f50c6bf952f7a4f6bf4e9650aead.jpg)  
FIG. 6. Results of a relativistic flowing plasma simulation in the quasi-cylindrical PIC code FBPIC – with both the standard and Galilean PSATD scheme. Top panel: evolution of the RMS amplitude of the electric field in the simulation box. Middle and bottom panels: Maps of the electric field in the simulation box, at a given time.

## CONCLUSION AND DISCUSSION

In this article, we showed that integrating the PIC equations in Galilean coordinates supresses the NCI, for a plasma drifting at a uniform relativistic velocity – both in Cartesian and quasi-cylindrical geometry. This new numerical scheme opens promising possibilities, especially for Lorentz-boosted simulations of laser-wakefield acceleration – as shown in [25].

Since the supression of the NCI is the aim of a number of previous schemes [15–22], it is worth discussing here the advantages and drawbacks of the Galilean PSATD scheme in relation to previous work, as well as areas of possible improvements.

As mentioned in the introduction, one advantage of the Galilean scheme is that it is built on the natural integration of the Maxwell equations, and does not introduce strong smoothing, or arbitrary or manually-tuned numerical corrections. This contrasts for instance with [15–18], but also with the methods from [20–22] in which both the timestep and “bump” in k space need to be tuned in relation with the plasma density [20] (making it potentially dificult to simulate plasmas with longitudinally or transversally varying density profiles). On the other hand, while the methods from [15–18, 20–22] can in some cases simulate relativistically crossing plasmas, in the present formulation of the Galilean scheme this could trigger the NCI for one of the two crossing plasmas (see Section III C). In future works, we will present an alternate formulation of the Galilean scheme, using multiple grids for the current J , which relaxes the restrictions on simulations of crossing plasmas.

TABLE II. Representation of common diferential operators in a spectral Cartesian framework and spectral quasi-cylindrical framework (Eqs. (24) and (25a) to (25c)). The expression of the spectral quasi-cylindrical representation can be derived by performing the same type of calculation as in appendix B of [31].
<table><tr><td>Operator</td><td colspan="2">Gradient:  ${ \pmb F } = \pmb { \nabla } S$ </td><td> ${ \mathrm { C u r l } } \colon F = \nabla \times V$ </td><td>Divergence:  $F = \nabla \cdot V$ </td></tr><tr><td>Spectral Cartesian representation</td><td>i.e.</td><td> $\mathbf { \mathcal { \hat { F } } } = i \mathbf { k } \mathbf { \mathcal { \hat { S } } }$   $\left( \begin{array} { l } { \hat { \mathcal { F } } _ { x } = i k _ { x } \hat { S } } \end{array} \right.$   $\begin{array} { r } { \left( \begin{array} { l } { \hat { \mathcal { F } } _ { y } = i k _ { y } \hat { \mathcal { S } } } \end{array} \right) } \end{array}$   $\begin{array} { r } { \bigl ( \hat { \mathcal { F } } _ { z } = i k _ { z } \hat { S } } \end{array}$ </td><td> $\mathcal { \hat { F } } = i \pmb { k } \times \mathcal { \hat { V } }$   $\left( \begin{array} { c } { \hat { \mathcal F } _ { x } = i k _ { y } \hat { \mathcal V } _ { z } - i k _ { z } \hat { \mathcal V } _ { y } } \end{array} \right)$   $\left. \begin{array} { r } { \hat { \mathcal { F } } _ { y } = i k _ { z } \hat { \mathcal { V } } _ { x } - i k _ { x } \hat { \mathcal { V } } _ { z } } \end{array} \right.$   $\begin{array} { r } { \left. \begin{array} { c } { \hat { \mathcal F } _ { z } = i k _ { x } \hat { \mathcal { V } } _ { y } - i k _ { y } \hat { \mathcal { V } } _ { x } } \end{array} \right. } \end{array}$ </td><td> $\hat { \mathcal { F } } = i \pmb { k } \cdot \hat { \mathcal { V } }$   $i . e . \hat { \mathcal { F } } = i k _ { x } \hat { \mathcal { V } } _ { x } + i k _ { y } \hat { \mathcal { V } } _ { y } + i k _ { z } \hat { \mathcal { V } } _ { z }$ </td></tr><tr><td>Spectral cylindrical representation</td><td colspan="2"> $\hat { \mathcal { F } } _ { + , m } = - k _ { \perp } \hat { S } _ { m } / 2$   $\hat { \ F } _ { - , m } = k _ { \perp } \hat { S } _ { m } / 2$   $\hat { \mathcal { F } } _ { z , m } = i k _ { z } \hat { S } _ { m }$ </td><td> $\sqrt { \hat { \mathcal { F } } _ { + , m } = k _ { z } \hat { \mathcal { V } } _ { + , m } - i k _ { \perp } \hat { \mathcal { V } } _ { z , m } / 2 }$   $\mathsf { \Pi } _ { \hat { \mathcal { F } } _ { - , m } } ^ { ' { } } = - k _ { z } \hat { \mathcal { V } } _ { - , m } - i k _ { \perp } \hat { \mathcal { V } } _ { z , m } / 2$   $\mid \hat { \mathcal { F } } _ { z , m } = i k _ { \perp } \hat { \mathcal { V } } _ { + , m } + i k _ { \perp } \hat { \mathcal { V } } _ { - , m }$ </td><td> $\hat { \mathcal { F } } _ { m } = k _ { \perp } ( \hat { \mathcal { V } } _ { + , m } - \hat { \mathcal { V } } _ { - , m } ) + i k _ { z } \hat { \mathcal { V } } _ { z , m }$ </td></tr></table>

Another important point is that the usual advantages of the standard PSATD scheme naturally carry over to the Galilean PSATD scheme, including dispersion-free wave propagation (in all directions) and suppression of staggered interpolation artifacts (see e.g. [31]). This is not the case for methods based on Finite-Diference Time-Domain (FDTD), Pseudo-Spectral Time-Domain (PSTD) or hybrid schemes (PSTD longitudinally and FDTD transversally), as in [17–22]. On the other hand, the methods based on FDTD or hybrid schemes can be more easily scaled to multiple computing nodes (see esp. [22]). In order to mitigate this limitation, the Galilean scheme is using domain decomposition, as proposed in [27] in both Warp and FBPIC. To remove the limitation further, this was extended in Warp (and will be extended in FBPIC in the future) to incorporate a spectral representation of finite-diference high-order operators (as discussed e.g. in [22, 33–35]), which have better scalability than purely-spectral operators.

## ACKNOWLEDGMENTS

The simulation results were stored and visualized using the new open-source format openPMD [36]. The authors wish to thank the openPMD contributors, and in particular its creator Axel Huebl (HZDR, Germany). The authors also thank Patrick Lee (U. Paris-Sud, France) for interesting discussions and for performing additional tests of the Galilean PSATD scheme (not presented here).

This work was partly supported by the Director, Ofice of Science, Ofice of High Energy Physics, U.S. Dept. of Energy under Contract No. DE-AC02-05CH11231, including from the Laboratory Directed Research and Development (LDRD) funding from Berkeley Lab.

This document was prepared as an account of work sponsored in part by the United States Government. While this document is believed to contain correct information, neither the United States Government nor any agency thereof, nor The Regents of the University of California, nor any of their employees, nor the authors makes any warranty, express or implied, or assumes any legal responsibility for the accuracy, completeness, or usefulness of any information, apparatus, product, or process disclosed, or represents that its use would not infringe privately owned rights. Reference herein to any specific commercial product, process, or service by its trade name, trademark, manufacturer, or otherwise, does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States Government or any agency thereof, or The Regents of the University of California. The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States Government or any agency thereof or The Regents of the University of California.

Appendix A: Analytical integration of the Maxwell equations from $t = n \Delta t$ to $t = ( n + 1 ) \Delta t$

After inserting Eqs. (8) and (9) into Eqs. (5a) and (5b), we obtain the following equations:

$$
\left( \frac { \partial } { \partial t } - i \mathbf { k } \cdot v _ { g a l } \right) ^ { 2 } \hat { \pmb { \mathscr { B } } } + c ^ { 2 } \pmb { k } ^ { 2 } \hat { \pmb { \mathscr { B } } } = \frac { 1 } { \epsilon _ { 0 } } i \pmb { k } \times \hat { \pmb { \mathscr { I } } } ^ { n + 1 / 2 }\tag{A1a}
$$

$$
\begin{array} { r l r } {  { ( \frac { \partial } { \partial t } - i \pmb { k } \cdot \pmb { v } _ { g a l } ) ^ { 2 } \hat { \pmb { \mathscr { E } } } + c ^ { 2 } \pmb { k } ^ { 2 } \hat { \pmb { \mathscr { E } } } = \frac { 1 } { \epsilon _ { 0 } } i ( \pmb { k } \cdot \pmb { v } _ { g a l } ) \hat { \pmb { \mathscr { I } } } ^ { n + 1 / 2 } } } \\ & { } & { - \frac { c ^ { 2 } } { \epsilon _ { 0 } } \hat { \rho } ^ { n + 1 } \frac { 1 - e ^ { i \pmb { k } \cdot \pmb { v } _ { g a l } ( t - n \Delta t ) } } { 1 - e ^ { i \pmb { k } \cdot \pmb { v } _ { g a l } \Delta t } } i \pmb { k } } \\ & { } & { + \frac { c ^ { 2 } } { \epsilon _ { 0 } } \hat { \rho } ^ { n } \frac { e ^ { i \pmb { k } \cdot \pmb { v } _ { g a l } \Delta t } - e ^ { i \pmb { k } \cdot \pmb { v } _ { g a l } ( t - n \Delta t ) } } { 1 - e ^ { i \pmb { k } \cdot \pmb { v } _ { g a l } \Delta t } } i \pmb { k } } \end{array}\tag{A1b}
$$

where $\hat { \rho } ^ { n + 1 } , \hat { \rho } ^ { n }$ and $\hat { \mathcal { I } } ^ { n + 1 / 2 }$ are constant. Notice in particular that the time derivative of $\hat { \mathcal { I } }$ from Eq. (5b) vanishes in Eq. (A1b) due to Eq. (8).

For the purpose of time integration, both equations can be cast into the following general form:

$$
\left( { \frac { \partial } { \partial t } } - i \nu c k \right) ^ { 2 } f + c ^ { 2 } k ^ { 2 } f = \alpha + \beta e ^ { i \nu c k ( t - n \Delta t ) }\tag{A2}
$$

where $\nu \equiv \pmb { k } \cdot \pmb { v } _ { g a l } / c k$ as in Eq. (12b), and where α and $\beta$ are constants. For instance, in the case of Eq. (A1a),

one has:

$$
\alpha = \frac { 1 } { \epsilon _ { 0 } } i \pmb { k } \times \hat { \pmb { \mathcal { I } } } ^ { n + 1 / 2 } \qquad \beta = 0 \qquad f = \pmb { \hat { B } }\tag{A3}
$$

while in the case of Eq. (A1b):

$$
\begin{array} { l } { \displaystyle \alpha = \frac { i \nu c k } { \epsilon _ { 0 } } \hat { \mathcal { I } } ^ { n + 1 / 2 } - \frac { c ^ { 2 } } { \epsilon _ { 0 } } \frac { \hat { \rho } ^ { n + 1 } - \hat { \rho } ^ { n } e ^ { i \nu c k \Delta t } } { 1 - e ^ { i \nu c k \Delta t } } i k } \\ { \displaystyle \beta = \frac { c ^ { 2 } } { \epsilon _ { 0 } } \frac { \hat { \rho } ^ { n + 1 } - \hat { \rho } ^ { n } } { 1 - e ^ { i \nu c k \Delta t } } i k \quad \quad f = \hat { \pmb { \varepsilon } } } \end{array}\tag{A4}
$$

The general solution of Eq. (A2) is:

$$
\begin{array} { r l } & { f ( t ) = \kappa _ { 1 } \cos ( c k ( t - n \Delta t ) ) e ^ { i \nu c k ( t - n \Delta t ) } } \\ & { \qquad + \kappa _ { 2 } \sin ( c k ( t - n \Delta t ) ) e ^ { i \nu c k ( t - n \Delta t ) } } \\ & { \qquad + \frac { \alpha } { c ^ { 2 } k ^ { 2 } ( 1 - \nu ^ { 2 } ) } + \frac { \beta } { c ^ { 2 } k ^ { 2 } } e ^ { i \nu c k ( t - n \Delta t ) } } \end{array}\tag{A5}
$$

where $\kappa _ { 1 }$ and $\kappa _ { 2 }$ are integration constants. These integration constants can be determined from the initial condition $f ( n \Delta t )$ and $\partial _ { t } f ( n \Delta t )$ , in which case Eq. (A5) becomes:

$$
\begin{array} { l } { { \displaystyle f ( t ) = [ f ( n \Delta t ) - \frac { \alpha } { c ^ { 2 } k ^ { 2 } ( 1 - \nu ^ { 2 } ) } - \frac { \beta } { c ^ { 2 } k ^ { 2 } } ] \cos ( c k ( t - n \Delta t ) ) e ^ { i \nu c k ( t - n \Delta t ) } + \frac { \alpha } { c ^ { 2 } k ^ { 2 } ( 1 - \nu ^ { 2 } ) } + \frac { \beta } { c ^ { 2 } k ^ { 2 } } e ^ { i \nu c k ( t - n \Delta t ) } } } \\ { { \displaystyle \qquad +  \frac { 1 } { c k } [ \partial _ { t } f ( n \Delta t ) - i \nu c k f ( n \Delta t ) + i \nu c k \frac { \alpha } { c ^ { 2 } k ^ { 2 } ( 1 - \nu ^ { 2 } ) } ] \sin ( c k ( t - n \Delta t ) ) e ^ { i \nu c k ( t - n \Delta t ) } } } \end{array}\tag{A6}
$$

Finally, since our purpose is to integrate Eqs. (A1a) and (A1b) from $t = n \Delta t$ to $t = ( n + 1 ) \Delta t$ , let us evaluate the above equation at $t = ( n + 1 ) \Delta t \mathrm { : }$

$$
\begin{array} { r l r } { f ( ( n + 1 ) \Delta t ) } & { { } = } & { \displaystyle C \theta ^ { 2 } f ( n \Delta t ) + \frac { \theta \chi _ { 1 } } { c ^ { 2 } k ^ { 2 } } \alpha + \frac { \theta ^ { 2 } ( 1 - C ) } { c ^ { 2 } k ^ { 2 } } \beta } \\ { \displaystyle + \frac { S \theta ^ { 2 } } { c k } [ \partial _ { t } f ( n \Delta t ) - i \nu c k f ( n \Delta t ) ] } & { { } ~ \mathrm { ( A } } \end{array}\tag{7}
$$

where C, S, θ and $\chi _ { 1 }$ have the same definition as in Eqs. (12a) to (12c). The integrated Maxwell equations Eqs. (11a) and (11b) are then obtained by combining Eq. (A7) with Eqs. (A3) and (A4) respectively. In particular, in order to evaluate the last term in Eq. (A7), we used the equations:

$$
\left( { \frac { \partial } { \partial t } } - i \nu c k \right) { \hat { \pmb { \beta } } } = - i { \pmb { k } } \times { \hat { \pmb { \varepsilon } } }\tag{A8a}
$$

$$
\left( \frac { \partial } { \partial t } - i \nu c k \right) \hat { \pmb { \varepsilon } } = c ^ { 2 } i \pmb { k } \times \pmb { \hat { \pmb { \beta } } } - \frac { 1 } { \epsilon _ { 0 } } \hat { \pmb { \mathcal { I } } }\tag{A8b}
$$

which are the spectral representations of the Maxwell equations Eqs. (3c) and (3d).

## Appendix B: Derivation of the dispersion relation, for the Galilean PSATD scheme

The dispersion relation typically results from combining the Vlasov equation and Maxwell equations. Here, we use a discretized version of the Vlasov equation and Maxwell equation that take into account all the numerical efects described in section Section II B (interpolation to grid; current correction, etc.).

We consider a periodic box, and a uniform plasma having a density $n _ { 0 }$ and a relativistic factor $\gamma _ { 0 }$ . We will treat perturbations $\delta f$ to the distribution function, as well as the fields E and B, as small quantities.

## 1. Notations and definitions

Let us consider a 2D Cartesian grid with $N _ { x } \times N _ { z }$ gridpoints and periodic boundaries. We will denote the position of the gridpoints $\pmb { x } _ { j } ^ { \prime }$ , i.e.

$$
\begin{array} { r } { \pmb { x } _ { j } ^ { \prime } = j _ { x } \Delta x \pmb { u } _ { x } + j _ { z } \Delta z \pmb { u } _ { z } \quad j _ { x } \in [ 0 , N _ { x } - 1 ] } \\ { j _ { z } \in [ 0 , N _ { z } - 1 ] } \end{array}\tag{B1}
$$

where $j _ { x }$ and $j _ { z }$ are integers. In addition, we will denote $X _ { \ell }$ the vectors of periodicity of the grid, i.e.

$$
{ X _ { \ell } } = \ell _ { x } { N _ { x } } \Delta x { { \mathbf { u } } _ { x } } + \ell _ { z } { N _ { z } } \Delta z { { \mathbf { u } } _ { z } } \qquad \ell _ { x } \in \mathbb { Z } , \ell _ { z } \in \mathbb { Z }\tag{B2}
$$

With these notations, any vector of the reciprocal lattice can be written as $\pmb { k _ { m } } = \pmb { k _ { \bot } } + \pmb { K _ { m } }$ where k is a vector of the first Brillouin zone, and $K _ { m }$ is a vector of periodicity of the reciprocal lattice i.e. k and $K _ { m }$ are of the form:

$$
K _ { m } = m _ { x } \frac { 2 \pi } { \Delta x } { \pmb u } _ { x } + m _ { z } \frac { 2 \pi } { \Delta z } { \pmb u } _ { z } \qquad m _ { x } \in \mathbb { Z } , m _ { z } \in \mathbb { Z }\tag{B3}
$$

$$
k = j _ { x } \frac { 2 \pi } { N _ { x } \Delta x } { \pmb u } _ { x } + j _ { z } \frac { 2 \pi } { N _ { z } \Delta z } { \pmb u } _ { z } \quad \pmb j _ { x } \in [ - N _ { x } / 2 , N _ { x } / 2 - 1 ]\tag{B4}
$$

where $j _ { x }$ and $j _ { z }$ are integers.

With these definitions, the expressions of the discrete Fourier transforms of the grid fields E and B (which are defined exclusively on the gridpoints $ { \boldsymbol { { x } } } _ { j } ^ { \prime } )$ are:

$$
\hat { \pmb { \mathscr { E } } } ( \pmb { k } ) = \frac { \sum _ { j } e ^ { - i \pmb { k } \cdot \pmb { x } _ { j } ^ { \prime } } E ( \pmb { x } _ { j } ^ { \prime } ) } { N _ { x } N _ { z } } \qquad \hat { \pmb { \mathscr { B } } } ( \pmb { k } ) = \frac { \sum _ { j } e ^ { - i \pmb { k } \cdot \pmb { x } _ { j } ^ { \prime } } B ( \pmb { x } _ { j } ^ { \prime } ) } { N _ { x } N _ { z } }\tag{B5}
$$

By contrast, the expression of the Fourier transform for the distribution function $f ( { \pmb x } ^ { \prime } , { \pmb p } )$ (which is defined also inbetween gridpoints, and is periodic) is:

$$
\hat { f } ( k + K _ { m } , p ) = \frac { 1 } { N _ { x } N _ { z } \Delta x \Delta z } \int _ { b o x } ^ { d x ^ { \prime } } e ^ { - i ( k + K _ { m } ) \cdot x ^ { \prime } } f ( x ^ { \prime } , p )\tag{B6}
$$

where the integration is performed over the (finite) extent of the box.

Finally, the Fourier transform of the particle shape factor S (which is defined over $\mathbb { R } ^ { 2 }$ and is not periodic – since for instance $S ( { \pmb x } ) = ( 1 - | { \pmb x } | / \Delta x ) \Theta ( \Delta x - | { \pmb x } | ) \times ( 1 -$ $| z | / \Delta z ) \Theta ( \Delta z - | z | )$ for order 1 shape factor) is:

$$
\hat { S } ( \pmb { k } + \pmb { K _ { m } } ) = \frac { 1 } { \Delta x \Delta z } \int _ { \mathbb { R } ^ { 2 } } d \pmb { x } ^ { \prime } e ^ { - i \pmb { k } + \pmb { K _ { m } } \cdot \pmb { x } ^ { \prime } } S ( \pmb { x } ^ { \prime } )\tag{B7}
$$

These distinctions regarding the Fourier transform are important in order to correctly derive the space aliases.

## 2. Discretized Vlasov equation

Let us define $f ^ { n + 1 / 2 } ( { \pmb x } ^ { \prime } , { \pmb p } )$ as the distribution function of positions and momenta at half-integer step (n + $1 / 2 ) \Delta t .$ , and let us derive the evolution of the f from one half-integer step to the next.

From the equations of motion of the particles Eqs. (3b) and (13), the evolution of position and momenta of one given particle from one half-integer timestep to the next

is:

$$
\frac { \ b { x } ^ { \prime n + 1 / 2 } - \ b { x } ^ { \prime n - 1 / 2 } } { \Delta t } = \frac { \ b { p } ^ { n + 1 / 2 } } { 2 m \gamma ^ { n + 1 / 2 } } + \frac { \ b { p } ^ { n - 1 / 2 } } { 2 m \gamma ^ { n - 1 / 2 } } - \ b { v } _ { g a l }\tag{B8a}
$$

$$
\begin{array} { r l r } {  { \frac { p ^ { n + 1 / 2 } - p ^ { n - 1 / 2 } } { \Delta t } = q { \bf { { E } } } _ { i n t e r p } ^ { n } + } } \\ & { } & { q ( \frac { p ^ { n + 1 / 2 } } { 2 m \gamma ^ { n + 1 / 2 } } + \frac { p ^ { n - 1 / 2 } } { 2 m \gamma ^ { n - 1 / 2 } } ) \times B _ { i n t e r p } ^ { n } } \end{array}\tag{B8b}
$$

where by definition ${ \pmb x } ^ { \prime n + 1 / 2 } \equiv ( { \pmb x } ^ { \prime n + 1 } + { \pmb x } ^ { \prime n } ) / 2$ , and where $\pmb { { E } } _ { i n t e r p } ^ { n }$ and $\boldsymbol { B } _ { i n t e r p } ^ { n }$ are the interpolated fields at the particle’s position, at time $n \Delta t$

Since the fields E and B are treated as small quantities, the modifications of p over one timestep is small, and thus these equations can be approximated to:

$$
\frac { { \pmb x } ^ { \prime } { } ^ { n + 1 / 2 } - { \pmb x } ^ { \prime } { } ^ { n - 1 / 2 } } { \Delta t } = \frac { { \pmb p } ^ { n - 1 / 2 } } { m \gamma ^ { n - 1 / 2 } } - { \pmb v } _ { g a l }\tag{B9a}
$$

$$
\frac { { { p } ^ { n + 1 / 2 } } - { { p } ^ { n - 1 / 2 } } } { \Delta t } = q \pmb { { E } } _ { i n t e r p } ^ { n } + q \frac { { { p } ^ { n - 1 / 2 } } } { m \gamma ^ { n - 1 / 2 } } \times { { B } _ { i n t e r p } ^ { n } }\tag{B9b}
$$

Because the volume in phase space is conserved during this evolution, the corresponding evolution of the distribution function f is:

$$
\begin{array} { l } { { f ^ { n + 1 / 2 } \displaystyle \left[ { \pmb x } ^ { \prime } + \left( \frac { { \pmb p } } { m \gamma } - { \pmb v } _ { g a l } \right) \Delta t , \right. } } \\ { { \displaystyle \left. { \pmb \ p } + q \Delta t \left( { \pmb E } _ { i n t e r p } ^ { n } + \frac { { \pmb p } } { m \gamma } \times { \pmb B } _ { i n t e r p } ^ { n } \right) \right] = f ^ { n - 1 / 2 } ( { \pmb x } ^ { \prime } , { \pmb p } ) } } \end{array}\tag{B10}
$$

Now $f ^ { n + 1 / 2 } ( { \pmb x } ^ { \prime } , { \pmb p } )$ is of the form $f _ { 0 } ( \pmb { p } ) + \delta f ^ { n + 1 / 2 } ( \pmb { x } ^ { \prime } , \pmb { p } )$ where $f _ { 0 }$ is the distribution function of a uniform, stationary plasma and $\delta f$ is a perturbation. Since $\delta f$ , E and B are treated as small perturbations, the above equation can be Taylor-expanded to first order:

$$
\begin{array} { r l } & { \delta f ^ { n + 1 / 2 } ( { \pmb x } ^ { \prime } + { \pmb v } \Delta t - { \pmb v } _ { g a l } \Delta t , \pmb p ) - \delta f ^ { n - 1 / 2 } ( { \pmb x } ^ { \prime } , { \pmb p } ) } \\ & { ~ + q \Delta t \big ( { \pmb E } _ { i n t e r p } ^ { n } + { \pmb v } \times { \pmb B } _ { i n t e r p } ^ { n } \big ) \cdot \frac { \partial f _ { 0 } } { \partial { \pmb p } } = 0 } \end{array}\tag{B11}
$$

where we used the short-hand notation ${ \pmb v } \equiv { \pmb p } / ( \gamma m )$

Now since $\pmb { { E } } _ { i n t e r p } ^ { n }$ is interpolated to the macroparticles at time $n \Delta t$ , its expression for a given macroparticle at position ${ \pmb x } ^ { \prime n }$ is:

$$
\begin{array} { l } { { \displaystyle { \pmb E } _ { i n t e r p } ^ { n } = \sum _ { j , \ell } S ( { \pmb x } ^ { \prime n } - { \pmb x } _ { j } ^ { \prime } - X _ { \ell } ) { \pmb E } ^ { n } ( { \pmb x } _ { j } ^ { \prime } + X _ { \ell } ) } } \\ { ~ } \\ { { \displaystyle ~ = \sum _ { j , \ell } S ( { \pmb x } ^ { \prime n } - { \pmb x } _ { j } ^ { \prime } - X _ { \ell } ) { \pmb E } ^ { n } ( { \pmb x } _ { j } ^ { \prime } ) } } \end{array} (\tag{B12}
$$

where $X _ { \ell }$ are vectors of periodicity of the grid and $\pmb { x } _ { j } ^ { \prime }$ denote gridpoints (see Eqs. (B1) and (B2)) and where the sum over $j$ corresponds to a sum over the whole (finite) grid. S is the shape factor of the macroparticle. Finally $E ^ { n } ( \pmb { x } _ { i } ^ { \prime } )$ is the expression of E on the grid. Since B is defined on the same grid and at the same time as E (i.e. the grid is not staggered here), the equation for $\boldsymbol { B } _ { i n t e r p } ^ { n }$ is similar to Eq. (B12). By combining Eq. (B12) with Eq. (B11) and the equation $\pmb { x } ^ { \prime n } = \pmb { x } ^ { \prime n - 1 / 2 } + [ \hat { \pmb { p } } ^ { n - 1 / 2 } / ( \gamma ^ { \hat { n } - 1 / 2 } m ) - \pmb { v } _ { g a l } ] \Delta \hat { t } / 2$ , we obtain:

$$
\begin{array} { r l r } {  { \delta f ^ { n + 1 / 2 } ( { \pmb x } ^ { \prime } + { \pmb v } \Delta t - { \pmb v } _ { g a l } \Delta t , { \pmb p } ) - \delta f ^ { n - 1 / 2 } ( { \pmb x } ^ { \prime } , { \pmb p } ) + } } \\ & { } & { + q \Delta t \sum _ { j , \ell } S ( { \pmb x } ^ { \prime } + \frac { ( { \pmb v } - { \pmb v } _ { g a l } ) \Delta t } { 2 } - { \pmb x } _ { j } ^ { \prime } - { \pmb X } _ { \ell } ) } \\ & { } & { \times ( E ^ { n } ( { \pmb x } _ { j } ^ { \prime } ) + { \pmb v } \times { \pmb B } ^ { n } ( { \pmb x } _ { j } ^ { \prime } ) ) \cdot \frac { \partial f _ { 0 } } { \partial { \pmb p } } = 0 \quad \mathrm { ( I } } \end{array}\tag{13}
$$

Let us evaluate the Fourier transform of the above equation, at a vector of the reciprocal lattice $\boldsymbol { k } _ { m } ~ =$ $\boldsymbol { k } + \boldsymbol { K } _ { m }$ (see Eqs. (B3) and (B4)). By using the definition Eq. (B6), we have:

$$
\begin{array}{c} \begin{array} { l } { { \delta \hat { f } ^ { n + 1 / 2 } ( k _ { m } , p ) e ^ { i k _ { m } \cdot ( v - v _ { g a l } ) \Delta t } - \delta \hat { f } ^ { n - 1 / 2 } ( k _ { m } , p ) } } \\ { { + \displaystyle \frac { q \Delta t } { \Delta x \Delta z } \sum _ { j } \left[ \int _ { \mathbb { R } ^ { 2 } } d x ^ { \prime } e ^ { - i k _ { m } \cdot x ^ { \prime } } S \left( x ^ { \prime } + \frac { ( v - v _ { g a l } ) \Delta t } { 2 } - x _ { j } ^ { \prime } \right) \right] } } \\ { { \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \left[ { } \frac { 1 } { \mathrm { } } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \times \right.} { B } ^ { n } ( x _ { j } ^ { \prime } ) \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \mathrm { } \frac { \partial { } f _ { 0 } } { \mathrm { } p } = 0 \mathrm { } } \mathrm { }  \end{array}    \end{array}\tag{B14}
$$

And finally, by using Eqs. (B5) and (B7):

$$
\begin{array} { r l } & { \delta \hat { f } ^ { n + 1 / 2 } ( k _ { m } , p ) e ^ { i \pmb { k } _ { m } \cdot ( \pmb { v } - \pmb { v } _ { g a l } ) \Delta t / 2 } } \\ & { \quad - \delta \hat { f } ^ { n - 1 / 2 } ( \pmb { k } _ { m } , \pmb { p } ) e ^ { - i \pmb { k } _ { m } \cdot ( \pmb { v } - \pmb { v } _ { g a l } ) \Delta t / 2 } } \\ & { \quad + q \Delta t \hat { S } ( \pmb { k } _ { m } ) \left( \hat { \pmb { \mathcal { E } } } ^ { n } ( \pmb { k } ) + \pmb { v } \times \hat { \pmb { \mathcal { B } } } ^ { n } ( \pmb { k } ) \right) \cdot \frac { \partial f _ { 0 } } { \partial \pmb { p } } = 0 } \end{array}\tag{B15}
$$

## 3. Discretized Maxwell equation

Let us now derive an expression of the discretized Maxwell equations, where the source terms are expressed as a function of $\delta f .$ . Let us first remark that, in Eqs. (11a) and (11b), the terms $\hat { \rho } ^ { n } , \hat { \rho } ^ { n + 1 }$ and $\hat { \mathcal { I } } ^ { n + 1 / 2 }$ are the charge and current obtained after current correction and smoothing, as described in Section II B. After inserting the explicit expression for current correction and smoothing Eqs. (14a) and (15), the discretized Maxwell equations become:

$$
\pmb { \hat { \mathcal { B } } } ^ { n + 1 } = \theta ^ { 2 } C \pmb { \hat { \mathcal { B } } } ^ { n } - \frac { \theta ^ { 2 } S } { c k } i \pmb { k } \times \pmb { \hat { \mathcal { E } } } ^ { n } + \ \frac { \theta \chi _ { 1 } \hat { T } } { \epsilon _ { 0 } c ^ { 2 } k ^ { 2 } } \ i \pmb { k } \times \pmb { \hat { \mathcal { I } } } _ { d } ^ { n + 1 / 2 }\tag{B16a}
$$

$$
\begin{array} { r l r } {  { \hat { \pmb { \mathcal { E } } } ^ { n + 1 } = \theta ^ { 2 } C \hat { \pmb { \mathcal { E } } } ^ { n } + \frac { \theta ^ { 2 } S } { k } c i \pmb { k } \times \hat { \pmb { \mathcal { B } } } ^ { n } - \frac { \hat { T } i \pmb { k } } { \epsilon _ { 0 } k ^ { 2 } } ( \hat { \rho } ^ { n + 1 } - \theta ^ { 2 } C \hat { \rho } ^ { n } ) } } \\ & { } & { + \frac { i \nu \theta \chi _ { 1 } - \theta ^ { 2 } S } { \epsilon _ { 0 } c k } \hat { T } ( \hat { \pmb { \mathcal { I } } } _ { d } ^ { n + 1 / 2 } - \frac { ( \pmb { k } \cdot \hat { \pmb { \mathcal { I } } } _ { d } ^ { n + 1 / 2 } ) \pmb { k } } { k ^ { 2 } } ) } \end{array}\tag{B16b}
$$

where $\hat { \rho } ^ { n } , \hat { \rho } ^ { n + 1 }$ and $\hat { \mathcal { I } } _ { d } ^ { n + 1 / 2 }$ are the charge and current obtained just after deposition and before current correction and smoothing, and where $\hat { \tau }$ is the smoothing factor defined in Eq. (15) (with $k _ { y } = 0$ in the 2D Cartesian case).

In addition, the above equations can be rewritten in a time-symmetrical form, which is more convenient for the analysis in the rest of this appendix. It can indeed be verified that, if $\hat { \varepsilon }$ and $\hat { B }$ satisfy Eqs. (B16a) and (B16b), as well as the associated conservation equations $i k \cdot { \hat { \pmb { \beta } } } ^ { n } =$ 0 and $\boldsymbol { k } \cdot \hat { \pmb { \mathcal { E } } } ^ { n } = \hat { T } \hat { \rho } ^ { n } / \epsilon _ { 0 }$ , then they also satisfy

$$
\begin{array} { l }  { \displaystyle { \theta ^ { * } c \hat { \pmb { \mathcal { B } } } ^ { n + 1 } - \theta c \hat { \pmb { \mathcal { B } } } ^ { n } = - t _ { c k } \frac { i { \pmb { k } } \times ( { \theta ^ { * } \hat { \pmb { \mathcal { E } } } ^ { n + 1 } } + { \theta \hat { \pmb { \mathcal { E } } } } ^ { n } ) } { k } } } \\ { { \displaystyle ~ + 2 \chi _ { 4 } ^ { \prime } \frac { \hat { T } } { \epsilon _ { 0 } c k } \frac { { \pmb { k } } \times \hat { \pmb { \mathcal { I } } _ { d } } ^ { n + 1 / 2 } } { k } } } \end{array}\tag{B17}
$$

$$
\begin{array} { l } { { \theta ^ { * } \mathring { \pmb { \mathcal { E } } } ^ { n + 1 } - \theta \hat { \pmb { \mathcal { E } } } ^ { n } = t _ { c k } \frac { i \boldsymbol { k } \times ( \theta ^ { * } c \hat { \pmb { \mathcal { B } } } ^ { n + 1 } + \theta c \hat { \pmb { \mathcal { B } } } ^ { n } ) } { k } } } \\ { { - \frac { \hat { T } i \boldsymbol { k } } { \epsilon _ { 0 } k ^ { 2 } } ( \theta ^ { * } \hat { \rho } ^ { n + 1 } - \theta \hat { \rho } ^ { n } ) } } \\ { { - 2 \chi _ { 4 } \frac { \hat { T } } { \epsilon _ { 0 } c k } \left( \hat { \pmb { \mathcal { I } } } _ { d } ^ { n + 1 / 2 } - \frac { ( \boldsymbol { k } \cdot \hat { \pmb { \mathcal { I } } } _ { d } ^ { n + 1 / 2 } ) \boldsymbol { k } } { k ^ { 2 } } \right) } } \end{array}\tag{B18}
$$

where <sup>∗</sup> denotes the complex conjugate, and where

$$
\chi _ { 4 } = \frac { c _ { \nu c k } ( t _ { c k } - \nu t _ { \nu c k } ) } { ( 1 - \nu ^ { 2 } ) } \qquad \chi _ { 4 } ^ { \prime } = \frac { c _ { \nu c k } ( t _ { \nu c k } - \nu t _ { c k } ) } { ( 1 - \nu ^ { 2 } ) }
$$

$$
t _ { c k } \equiv \tan \left( \frac { c k \Delta t } { 2 } \right) \qquad c _ { c k } \equiv \cos \left( \frac { c k \Delta t } { 2 } \right)\tag{B19}
$$

(B20)

$$
t _ { \nu c k } \equiv \tan \left( \frac { \nu c k \Delta t } { 2 } \right) \qquad c _ { \nu c k } \equiv \cos \left( \frac { \nu c k \Delta t } { 2 } \right)\tag{B21}
$$

Let us now express the deposited charge and currents as a function of $\delta f$ . The current density, which is deposited at half-integer time, is given within one given cell by

$$
J _ { d } ^ { n + \frac { 1 } { 2 } } ( { \pmb x } _ { j } ^ { \prime } ) = \frac { 1 } { \Delta x \Delta z } \int d p \int _ { \mathbb { R } ^ { 2 } } d { \pmb x } ^ { \prime } q v S ( { \pmb x } _ { j } ^ { \prime } - { \pmb x } ^ { \prime } ) \delta f ^ { n + 1 / 2 } ( { \pmb x } ^ { \prime } , p )\tag{B22}
$$

In the above expression, the integration is carried out over all space $( \mathbb { R } ^ { \hat { 2 } } )$ because the shape factor S may extend beyond the finite grid. Let us now expand the periodic function $\delta f$ in Fourier series:

$$
\begin{array} { r } { J _ { d } ^ { n + \frac { 1 } { 2 } } ( x _ { j } ^ { \prime } ) = \cfrac { 1 } { \Delta x \Delta z } \displaystyle \int d p \int _ { \mathbb { R } ^ { 2 } } d x ^ { \prime } q v S ( x _ { j } ^ { \prime } - x ^ { \prime } ) } \\ { \times \sum _ { k _ { m } } \delta \hat { f } ^ { n + 1 / 2 } ( k _ { m } , p ) e ^ { i k _ { m } \cdot x ^ { \prime } } } \end{array}\tag{B23}
$$

where the sum is over all vectors $\pmb { k _ { m } } = \pmb { k _ { \bot } } + \pmb { K _ { m } }$ of the reciprocal lattice (see Eqs. (B3) and (B4)). With some

algebra, this can be rewritten as:

$$
J _ { d } ^ { n + \frac { 1 } { 2 } } ( x _ { j } ^ { \prime } ) = \sum _ { k } e ^ { i k \cdot x _ { j } ^ { \prime } } \sum _ { m } \hat { S } ( k _ { m } ) \int d p q v \delta \hat { f } ^ { n + 1 / 2 } ( k _ { m } , p )\tag{B24}
$$

where we used the relation $e ^ { i K _ { m } \cdot x _ { j } ^ { \prime } } = 1$ , which comes from Eqs. (B1) and (B4). By identification, we have

$$
\hat { \mathcal { T } } _ { d } ^ { n + \frac { 1 } { 2 } } ( k ) = \sum _ { m } \hat { S } ( k _ { m } ) \int d p q v \delta \hat { f } ^ { n + 1 / 2 } ( k _ { m } , p )\tag{B25}
$$

Similarly, since the charge density $\rho ^ { n }$ is deposited from the particle position ${ { \pmb x } ^ { \prime } } ^ { n } = { { \pmb x } ^ { \prime } } ^ { n + 1 / 2 } - ( { { \pmb v } ^ { n + 1 / 2 } } - { { \pmb v } _ { g a l } } ) \Delta t / 2 ,$ its expression is:

$$
\rho ^ { n } ( x _ { j } ^ { \prime } ) = { \frac { 1 } { \Delta x \Delta z } } { \int } d p { \int } _ { \mathbb { R } ^ { 2 } } q _ { \normalfont \ S } \left( x _ { j } ^ { \prime } - x ^ { \prime } + { \frac { ( v - v _ { g a l } ) \Delta t } { 2 } } \right)
$$

$$
\times \delta f ^ { n + 1 / 2 } ( { \pmb x } ^ { \prime } , { \pmb p } )\tag{B26}
$$

And thus the expression of $\hat { \rho } ^ { n }$ is:

$$
\hat { \rho } ^ { n } ( k ) = \sum _ { m } \hat { S } ( k _ { m } ) \int d p q \delta \hat { f } ^ { n + 1 / 2 } ( k _ { m } , p ) e ^ { \frac { i k _ { m } \cdot ( v - v _ { g a l } ) \Delta t } { 2 } }\tag{B27}
$$

And similarly the expression of $\hat { \rho } ^ { n + 1 }$ is:

$$
\hat { \rho } ^ { n + 1 } ( \pmb { k } ) = \sum _ { m } \hat { S } ( \pmb { k _ { m } } ) \int d \pmb { p } q \delta \hat { f } ^ { n + 1 / 2 } ( \pmb { k _ { m } } , \pmb { p } ) e ^ { - \frac { i \pmb { k _ { m } } \cdot ( \pmb { v } - \pmb { v _ { g a l } } ) \Delta t } { 2 } }\tag{B28}
$$

## 4. Eigenmodes and eigensystem

The discretized Vlasov equation $\operatorname { E q . }$ (B15), the discretized Maxwell equations Eqs. (B17) and (B18) and the expression of the source terms Eqs. (B25), (B27) and (B28) form a set of coupled equations of evolution. Let us look for eigenmodes of this set of equations, where we assume all perturbations to be of the form $e ^ { i { \bf k } \cdot { \bf x } - i \omega t } = e ^ { i { \bf k } \cdot { \bf x } ^ { \prime } - i ( \omega - { \bf k } \cdot { \bf \dot { v } } _ { g a l } ) t }$ , so that the definition of ω is independent of $v _ { g a l }$ , and corresponds to physical intuition. This results in the following expressions

$$
\pmb { \hat { \mathcal { E } } } ^ { n } ( \pmb { k } ) = \pmb { \hat { \mathcal { E } } } ( \pmb { k } ) e ^ { - i ( \omega - \pmb { k } \cdot \pmb { v } _ { g a l } ) n \Delta t }\tag{B29a}
$$

$$
\hat { \pmb { \beta } } ^ { n } ( \pmb { k } ) = \hat { \pmb { \beta } } ( \pmb { k } ) e ^ { - i ( \omega - \pmb { k } \cdot \pmb { v } _ { g a l } ) n \Delta t }\tag{B29b}
$$

$$
\delta \hat { f } ^ { n + \frac { 1 } { 2 } } ( \pmb { k } _ { m } , \pmb { p } ) = \delta \hat { f } ( \pmb { k } _ { m } , \pmb { p } ) e ^ { - i ( \omega - \pmb { k \cdot v } _ { g a l } ) ( n + 1 / 2 ) \Delta t }\tag{B29c}
$$

Notice that we used k instead of $\pmb { k } _ { m } \equiv \pmb { k } + \pmb { K } _ { m }$ in the expression of the time evolution of $\delta \hat { f } ^ { n + \frac { 1 } { 2 } } ( k _ { m } , p )$ . This is because, by definition of an eigenmode, all quantities (in this case $\hat { \pmb { \mathscr { E } } } , \hat { \pmb { \mathscr { B } } }$ and $\delta \hat { f } )$ should have the same time evolution.

With these expressions, the discretized Vlasov equation Eq. (B15) yields:

$$
\delta { \hat { f } } ( { \pmb k } _ { m } , { \pmb p } ) = - i \frac { q \Delta t } { 2 } { \hat { S } } ( { \pmb k } _ { m } ) \frac { ( { \hat { \pmb \varepsilon } } ( { \pmb k } ) + { \pmb v } \times { \hat { \pmb { \beta } } } ( { \pmb k } ) ) \cdot \frac { \partial f _ { 0 } } { \partial { \pmb p } } } { \sin \left( \frac { \left( \omega - { \pmb k } \cdot { \pmb v } - { \pmb K } _ { m } \cdot ( { \pmb v } - { \pmb v } _ { g a l } ) \right) \Delta t } { 2 } \right) }\tag{B30}
$$

And, after some algebra, inserting the above expression into Eqs. (B25), (B27) and (B28) results in:

$$
\begin{array} { l } { \displaystyle \hat { \mathcal { T } } _ { d } ^ { n + \frac { 1 } { 2 } } = i \frac { \epsilon _ { 0 } \omega _ { p } ^ { 2 } } { \gamma _ { 0 } } e ^ { - i ( \omega - \pmb { k \cdot v } _ { g a l } ) ( n + 1 / 2 ) \Delta t } } \\ { \displaystyle \qquad \times \sum _ { m } \hat { \mathcal { S } } ^ { 2 } ( \pmb { k } _ { m } ) \left( \frac { \hat { \mathcal { F } } } { \frac { 2 } { \Delta t } s _ { \omega ^ { \prime } } } + \frac { c _ { \omega ^ { \prime } } ( \pmb { k } _ { m } \cdot \hat { \pmb { \mathcal { F } } } ) \pmb { v } _ { 0 } } { \left[ \frac { 2 } { \Delta t } s _ { \omega ^ { \prime } } \right] ^ { 2 } } \right) } \end{array}\tag{B31}
$$

$$
\theta ^ { * } \hat { \rho } ^ { n + 1 } - \theta \hat { \rho } ^ { n } = \frac { 2 \epsilon _ { 0 } \omega _ { p } ^ { 2 } } { \gamma _ { 0 } } s _ { \omega } e ^ { - i ( \omega - \pmb { k \cdot v } _ { g a l } ) ( n + 1 / 2 ) \Delta t }
$$

$$
\times \sum _ { m } \hat { S } ^ { 2 } ( k _ { m } ) \frac { ( \hat { \mathcal { F } } \cdot k _ { m } ) } { \left[ \frac { 2 } { \Delta t } s _ { \omega ^ { \prime } } \right] ^ { 2 } }\tag{B32}
$$

where

$$
\mathcal { \hat { F } } \equiv \mathcal { \hat { E } } ( k ) + v _ { 0 } \times \hat { \pmb { \mathcal { B } } } ( k ) - \frac { ( \pmb { v } _ { 0 } \cdot \pmb { \hat { \mathcal { E } } } ( k ) ) \pmb { v } _ { 0 } } { c ^ { 2 } }\tag{B33}
$$

$$
\omega _ { p } ^ { 2 } = \frac { n _ { 0 } q ^ { 2 } } { m \epsilon _ { 0 } } \qquad s _ { \omega } = \sin \left( \frac { \omega \Delta t } { 2 } \right)\tag{B34}
$$

$$
s _ { \omega ^ { \prime } } = \sin { \left( \frac { ( \omega - \boldsymbol { k } \cdot \boldsymbol { v } _ { 0 } - K _ { m } \cdot ( \boldsymbol { v } _ { 0 } - \boldsymbol { v } _ { g a l } ) ) \Delta t } { 2 } \right) }\tag{B35}
$$

$$
c _ { \omega ^ { \prime } } = \cos { \left( \frac { ( \omega - \boldsymbol { k } \cdot \boldsymbol { v _ { 0 } } - K _ { m } \cdot ( \boldsymbol { v _ { 0 } } - \boldsymbol { v _ { g a l } } ) ) \Delta t } { 2 } \right) }\tag{B36}
$$

In the derivation of Eqs. (B31) and (B32), we used integration by parts and the fact that the distribution function of the unperturbed background plasma, is $f _ { 0 } ( \pmb { p } ) =$ $n _ { 0 } \delta ( { \pmb p } - \gamma _ { 0 } m { \pmb v } _ { 0 } )$ , and we also made use of the relation $\partial _ { p } \cdot ( { \pmb v } \times { \pmb \hat { \mathcal B } } ) = 0$ when ${ \pmb v } = { \pmb p } ( 1 + ( { \pmb p } / m c ) ^ { 2 } ) ^ { - 1 / 2 } / m$

Finally, inserting Eqs. (B31), (B32), (B29a) and (B29b) into the time-symmetrical discrete Maxwell equations Eqs. (B17) and (B18) results in the eigensystem:

$$
\mathscr { s } _ { \omega } c \pmb { \hat { B } } - t _ { c k } c _ { \omega } \frac { \pmb { k } \times \hat { \pmb { \varepsilon } } } { k } = - \chi _ { 4 } ^ { \prime } \xi _ { 1 } \frac { \pmb { k } \times \hat { \pmb { \mathcal { F } } } } { k } - \chi _ { 4 } ^ { \prime } ( \pmb { \xi } _ { 2 } \cdot \pmb { \hat { \mathcal { F } } } ) \frac { \pmb { k } \times \pmb { v } _ { 0 } } { c k }\tag{B37a}
$$

$$
s _ { \omega } \hat { \mathcal { E } } + t _ { c k } c _ { \omega } \frac { \boldsymbol { k } \times { c } \hat { \mathcal { B } } } { k } = s _ { \omega } ( \boldsymbol { \xi } _ { 3 } \cdot \hat { \mathcal { F } } ) \frac { \boldsymbol { k } } { k } + \chi _ { 4 } \xi _ { 1 } \frac { \boldsymbol { k } \times \hat { \mathcal { F } } } { k } \times \frac { \boldsymbol { k } } { k }
$$

$$
+ \chi _ { 4 } ( \pmb { \xi } _ { 2 } \cdot \hat { \pmb { \mathcal { F } } } ) \frac { \pmb { k } \times \pmb { v } _ { 0 } } { c k } \times \frac { \pmb { k } } { k }\tag{B37b}
$$

where the $\xi$ coeficients represent the response of the plasma

$$
\xi _ { 1 } = \frac { \hat { \mathcal { T } } \omega _ { p } ^ { 2 } } { \gamma _ { 0 } c k } \left( \sum _ { m } \frac { \hat { S } ^ { 2 } ( k _ { m } ) } { \frac { 2 } { \Delta t } s _ { \omega ^ { \prime } } } \right)\tag{B38a}
$$

$$
\pmb { \xi } _ { 2 } = \frac { \hat { \mathcal { T } } \omega _ { p } ^ { 2 } } { \gamma _ { 0 } k } \left( \sum _ { m } \frac { c _ { \omega ^ { \prime } } \hat { S } ^ { 2 } ( k _ { m } ) } { \left[ \frac { 2 } { \Delta t } { } ^ { S } \omega ^ { \prime } \right] ^ { 2 } } k _ { m } \right)\tag{B38b}
$$

$$
\pmb { \xi } _ { 3 } = \frac { \hat { \mathcal { T } } \omega _ { p } ^ { 2 } } { \gamma _ { 0 } k } \left( \sum _ { m } \frac { \hat { \mathcal { S } } ^ { 2 } ( \pmb { k } _ { m } ) } { \left[ \frac { 2 } { \Delta t } \mathcal { s } _ { \omega ^ { \prime } } \right] ^ { 2 } } k _ { m } \right)\tag{B38c}
$$

## 5. Dispersion relation

Finally, let us simplify the above eigensystem in the case where both $v _ { g a l }$ and the velocity of the unperturbed plasma ${ \pmb v } _ { 0 }$ are along $\mathbf { \Delta } \pmb { u } _ { z }$ (i.e. ${ \pmb v } _ { g a l } = v _ { g a l } { \pmb u } _ { z }$ and ${ \boldsymbol { v } } _ { 0 } =$ $v _ { 0 } \mathbf { } u _ { z } )$ . In this case, projecting Eq. (B37a) along y and Eq. (B37b) along x and z (as well as using the expression of $\hat { \mathcal { F } }$ from $\operatorname { E q }$ . (B33)) results in the eigensystem:

$$
M \left( \begin{array} { c } { { c \hat { \mathcal { B } } _ { y } } } \\ { { \hat { \mathcal { E } } _ { z } } } \\ { { \hat { \mathcal { E } } _ { x } } } \end{array} \right) = \left( \begin{array} { c } { { 0 } } \\ { { 0 } } \\ { { 0 } } \end{array} \right)\tag{B39}
$$

where the matrix M can be expressed as

$$
M = M _ { v a c u u m } + U _ { 1 } ( V _ { 1 } ^ { T } + V _ { 2 } ^ { T } ) + s _ { \omega } U _ { 3 } V _ { 3 } ^ { T }\tag{B40}
$$

where <sup>T</sup> denotes the tranpose operation and where

$$
{ \cal M } _ { v a c u u m } = \left( \begin{array} { c c c } { { s _ { \omega } } } & { { t _ { c k } c _ { \omega } k _ { x } / k ~ - t _ { c k } c _ { \omega } k _ { z } / k } } \\ { { t _ { c k } c _ { \omega } k _ { x } / k ~ } } & { { s _ { \omega } } } & { { 0 } } \\ { { - t _ { c k } c _ { \omega } k _ { z } / k ~ } } & { { 0 } } & { { s _ { \omega } } } \end{array} \right)\tag{B41}
$$

$$
U _ { 1 } = \left( \begin{array} { c } { { \chi _ { 4 } ^ { \prime } } } \\ { { \chi _ { 4 } k _ { x } / k } } \\ { { - \chi _ { 4 } k _ { z } / k } } \end{array} \right) \quad V _ { 1 } = \xi _ { 1 } \left( \begin{array} { c } { { - k _ { z } v _ { 0 } / ( c k ) } } \\ { { - k _ { x } / ( k \gamma _ { 0 } ^ { 2 } ) } } \\ { { k _ { z } / k } } \end{array} \right)\tag{B42}
$$

$$
U _ { 2 } = \left( \begin{array} { c } { { \chi _ { 4 } } } \\ { { \chi _ { 4 } ^ { \prime } k _ { x } / k } } \\ { { - \chi _ { 4 } ^ { \prime } k _ { z } / k } } \end{array} \right) \quad V _ { 2 } = \frac { k _ { x } v _ { 0 } } { c k } \left( \begin{array} { c } { { \xi _ { 2 x } v _ { 0 } / c } } \\ { { - \xi _ { 2 z } / \gamma _ { 0 } ^ { 2 } } } \\ { { - \xi _ { 2 x } } } \end{array} \right)\tag{B43}
$$

$$
U _ { 3 } = \left( \begin{array} { c } { { 0 } } \\ { { k _ { z } / k } } \\ { { k _ { x } / k } } \end{array} \right) \quad V _ { 3 } = \left( \begin{array} { c } { { \xi _ { 3 x } v _ { 0 } / c } } \\ { { - \xi _ { 3 z } / \gamma _ { 0 } ^ { 2 } } } \\ { { - \xi _ { 3 x } } } \end{array} \right)\tag{B44}
$$

where we also introduced an additional vector $U _ { 2 }$ which is not used in Eq. (B40) but will be useful below.

The final dispersion relation is obtained by solving the equation $d e t ( M ) = 0 $ However, calculating the analytical expression of the determinant $d e t ( M )$ using e.g. Sarrus’ rule can be a daunting task. Instead, the calculation of $d e t ( M )$ can be faciltated by expressing the matrix M in the basis $( U _ { 1 } , U _ { 2 } , U _ { 3 } )$ (an operation which does not change its determinant). In other words, one has $d e t ( M ) = d e t ( M ^ { \prime } )$ where $M ^ { \prime }$ is the expression of the matrix M in the basis $( U _ { 1 } , U _ { 2 } , U _ { 3 } )$ :

$$
M ^ { \prime } = \left( \begin{array} { c c c } { { s _ { \omega } + ( V _ { 1 } ^ { T } + V _ { 2 } ^ { T } ) U _ { 1 } } } & { { t _ { c k } c _ { \omega } } } & { { s _ { \omega } V _ { 3 } ^ { T } U _ { 1 } } } \\ { { t _ { c k } c _ { \omega } + ( V _ { 1 } ^ { T } + V _ { 2 } ^ { T } ) U _ { 2 } } } & { { s _ { \omega } } } & { { s _ { \omega } V _ { 3 } ^ { T } U _ { 2 } } } \\ { { ( V _ { 1 } ^ { T } + V _ { 2 } ^ { T } ) U _ { 3 } } } & { { 0 } } & { { s _ { \omega } ( 1 + V _ { 3 } ^ { T } U _ { 3 } ) } } \end{array} \right)\tag{B45}
$$

Using this property, the equation det(M) = 0 becomes

$$
\begin{array} { r l } & { ( s _ { \omega } ^ { 2 } - t _ { c k } ^ { 2 } c _ { \omega } ^ { 2 } ) ( 1 + V _ { 3 } ^ { T } U _ { 3 } ) + ( V _ { 1 } ^ { T } + V _ { 2 } ^ { T } ) U } \\ & { + ( V _ { 3 } ^ { T } U _ { 3 } ) ( V _ { 1 } ^ { T } U ) - ( V _ { 1 } ^ { T } U _ { 3 } ) ( V _ { 3 } ^ { T } U ) } \\ & { + ( V _ { 3 } ^ { T } U _ { 3 } ) ( V _ { 2 } ^ { T } U ) - ( V _ { 2 } ^ { T } U _ { 3 } ) ( V _ { 3 } ^ { T } U ) = 0 } \end{array}\tag{B46}
$$

where the trivial solution $s _ { \omega } = 0$ has be discarded, and where $U = s _ { \omega } U _ { 1 } - t _ { c k } c _ { \omega } U _ { 2 }$ After some algebra, this equation reduces to Eq. (19).

## Appendix C: Expression of the PSATD equations in quasi-cylindrical geometry

As mentioned in the text, the PSATD equations in quasi-cylindrical geometry are obtained from the equations in Cartesian geometry Eqs. (10), (11a) and (11b), using the correspondance table Table II. Thus, with this method, the discretized continuity equation Eq. (10) becomes

$$
\begin{array} { r l } {  { - i k _ { z } v _ { g a l } \frac { \hat { \rho } _ { m } ^ { n + 1 } - \hat { \rho } _ { m } ^ { n } e ^ { i k _ { z } v _ { g a l } \Delta t } } { 1 - e ^ { i k _ { z } v _ { g a l } \Delta t } } } \quad } & { { } } \\ & { + k _ { \perp } ( \hat { \mathcal { I } } _ { + , m } ^ { n + 1 / 2 } - \hat { \mathcal { I } } _ { - , m } ^ { n + 1 / 2 } ) + i k _ { z } \hat { \mathcal { I } } _ { z , m } ^ { n + 1 / 2 } = 0 } \end{array}\tag{C1}
$$

and the corresponding current correction (Eq. (14a) in Cartesian geometry) becomes

$$
\hat { \mathcal { I } } _ { + , m } ^ { n + 1 / 2 } = \hat { \mathcal { I } } _ { d + , m } ^ { n + 1 / 2 } - k _ { \perp } \hat { \mathcal { G } } _ { m } / ( 2 k ^ { 2 } )\tag{C2a}
$$

$$
\hat { \mathcal { I } } _ { - , m } ^ { n + 1 / 2 } = \hat { \mathcal { I } } _ { d \mathrm { ~ } - , m } ^ { n + 1 / 2 } + k _ { \perp } \hat { \mathcal { G } } _ { m } / ( 2 k ^ { 2 } )\tag{C2b}
$$

$$
\hat { \mathcal { I } } _ { z , m } ^ { n + 1 / 2 } = \hat { \mathcal { I } } _ { d z , m } ^ { n + 1 / 2 } + i k _ { z } \hat { \mathcal { G } } _ { m } / k ^ { 2 }\tag{C2c}
$$

where $k ^ { 2 } = k _ { \perp } ^ { 2 } + k _ { z } ^ { 2 }$ by definition. In the above equations, $\hat { \mathcal { I } } _ { d }$ and $\hat { \mathcal { I } }$ are the deposited current and corrected current respectively, and the expression of $\hat { \mathcal { G } } _ { m }$ is obtained by replacing $\hat { \mathcal { I } }$ by $\hat { \mathcal { I } } _ { d }$ in the left-hand side of Eq. (C1).

Similarly, the update equations for the $\hat { \pmb { { B } } }$ and $\hat { \varepsilon }$ field (Eqs. (11a) and (11b)) become:

$$
\hat { \mathcal { B } } _ { + , m } ^ { n + 1 } = \theta ^ { 2 } C \hat { \mathcal { B } } _ { + , m } ^ { n } - \frac { \theta ^ { 2 } S } { c k } \left( k _ { z } \hat { \mathcal { E } } _ { + , m } ^ { n } - \frac { i k _ { \perp } } { 2 } \hat { \mathcal { E } } _ { z , m } ^ { n } \right) + \frac { \theta \chi _ { 1 } } { \epsilon _ { 0 } c ^ { 2 } k ^ { 2 } } \left( k _ { z } \hat { \mathcal { I } } _ { + , m } ^ { n + 1 / 2 } - \frac { i k _ { \perp } } { 2 } \hat { \mathcal { I } } _ { z , m } ^ { n + 1 / 2 } \right)\tag{C3a}
$$

$$
\small \hat { \mathcal { B } } _ { - , m } ^ { n + 1 } = \theta ^ { 2 } C \hat { \mathcal { B } } _ { - , m } ^ { n } - \frac { \theta ^ { 2 } S } { c k } \left( - k _ { z } \hat { \mathcal { E } } _ { - , m } ^ { n } - \frac { i k _ { \perp } } { 2 } \hat { \mathcal { E } } _ { z , m } ^ { n } \right) + \frac { \theta \chi _ { 1 } } { \epsilon _ { 0 } c ^ { 2 } k ^ { 2 } } \left( - k _ { z } \hat { \mathcal { T } } _ { - , m } ^ { n + 1 / 2 } - \frac { i k _ { \perp } } { 2 } \hat { \mathcal { T } } _ { z , m } ^ { n + 1 / 2 } \right)\tag{C3b}
$$

$$
\hat { \mathcal { B } } _ { z , m } ^ { n + 1 } = \theta ^ { 2 } C \hat { \mathcal { B } } _ { z , m } ^ { n } - \frac { \theta ^ { 2 } S } { c k } \left( i k _ { \perp } \hat { \mathcal { E } } _ { + , m } ^ { n } + i k _ { \perp } \hat { \mathcal { E } } _ { - , m } ^ { n } \right) + ~ \frac { \theta \chi _ { 1 } } { \epsilon _ { 0 } c ^ { 2 } k ^ { 2 } } \left( i k _ { \perp } \hat { \mathcal { I } } _ { + , m } ^ { n + 1 / 2 } + i k _ { \perp } \hat { \mathcal { I } } _ { - , m } ^ { n + 1 / 2 } \right)\tag{C3c}
$$

$$
\mathcal { \hat { E } } _ { + , m } ^ { n + 1 } = \theta ^ { 2 } C \mathcal { \hat { E } } _ { + , m } ^ { n } + \frac { \theta ^ { 2 } S c } { k } \left( k _ { z } \mathcal { \hat { B } } _ { + , m } ^ { n } - \frac { i k _ { \perp } } { 2 } \hat { { B } } _ { z , m } ^ { n } \right) + \frac { i \nu \theta \chi _ { 1 } - \theta ^ { 2 } S } { \epsilon _ { 0 } c k } \ \hat { \mathcal { I } } _ { + , m } ^ { n + 1 / 2 } + \frac { 1 } { \epsilon _ { 0 } k ^ { 2 } } \left( \chi _ { 2 } \hat { \rho } _ { m } ^ { n + 1 } - \theta ^ { 2 } \chi _ { 3 } \hat { \rho } _ { m } ^ { n } \right) \frac { k _ { \perp } } { 2 }\tag{C4a}
$$

$$
\hat { \mathcal { E } } _ { - , m } ^ { n + 1 } = \theta ^ { 2 } C \hat { \mathcal { E } } _ { - , m } ^ { n } + \frac { \theta ^ { 2 } S c } { k } \left( - k _ { z } \hat { \mathcal { B } } _ { - , m } ^ { n } - \frac { i k _ { \perp } } { 2 } \hat { \mathcal { B } } _ { z , m } ^ { n } \right) + \frac { i \nu \theta \chi _ { 1 } - \theta ^ { 2 } S } { \epsilon _ { 0 } c k } \hat { \mathcal { T } } _ { - , m } ^ { n + 1 / 2 } - \frac { 1 } { \epsilon _ { 0 } k ^ { 2 } } \left( \chi _ { 2 } \hat { \rho } _ { m } ^ { n + 1 } - \theta ^ { 2 } \chi _ { 3 } \hat { \rho } _ { m } ^ { n } \right) \frac { k _ { \perp } } { 2 }\tag{C4b}
$$

$$
\hat { \mathcal { E } } _ { z , m } ^ { n + 1 } = \theta ^ { 2 } C \hat { \mathcal { E } } _ { z , m } ^ { n } + \frac { \theta ^ { 2 } S c } { k } \left( i k _ { \perp } \hat { \mathcal { B } } _ { + , m } ^ { n } + i k _ { \perp } \hat { \mathcal { B } } _ { - , m } ^ { n } \right) + \frac { i \nu \theta \chi _ { 1 } - \theta ^ { 2 } S } { \epsilon _ { 0 } c k } \hat { \mathcal { T } } _ { z , m } ^ { n + 1 / 2 } - \frac { 1 } { \epsilon _ { 0 } k ^ { 2 } } \left( \chi _ { 2 } \hat { \rho } _ { m } ^ { n + 1 } - \theta ^ { 2 } \chi _ { 3 } \hat { \rho } _ { m } ^ { n } \right) i k _ { z }\tag{C4c}
$$

In the above equations, the coeficients $\theta , C , S , \nu , \chi _ { 1 } , \chi _ { 2 }$ and $\chi _ { 3 }$ have the same expression as in Eqs. (12a) to (12d) (bearing in my mind, in quasi-cylindrical geometry, that

[1] A. Spitkovsky, The Astrophysical Journal Letters 682, L5 (2008), 0802.3216.

[2] U. Keshet, B. Katz, A. Spitkovsky, and E. Waxman, The Astrophysical Journal Letters 693, L127 (2009).

[3] T. Tajima and J. M. Dawson, Phys. Rev. Lett. 43, 267 (1979).

[4] J.-L. Vay, Phys. Rev. Lett. 98, 130405 (2007).

[5] R. Hockney and J. Eastwood, Computer Simulation Using Particles (Taylor & Francis, 1988).

[6] C. Birdsall and A. Langdon, Plasma Physics via Computer Simulation, Appendix E , Series in Plasma Physics (Taylor & Francis, 2004).

[7] S. F. Martins, R. A. Fonseca, L. O. Silva, W. Lu, and W. B. Mori, Computer Physics Communications 181, 869 (2010).

[8] J. Vay, C. G. R. Geddes, C. Benedetti, D. L. Bruhwiler, E. CormierMichel, B. M. Cowan, J. R. Cary, and D. P. Grote, AIP Conference Proceedings 1299, 244 (2010).

[9] J.-L. Vay, C. Geddes, E. Cormier-Michel, and D. Grote, Journal of Computational Physics 230, 5908 (2011).

[10] J.-L. Vay, C. G. R. Geddes, E. Cormier-Michel, and D. P. Grote, Physics of Plasmas 18, 030701 (2011), http://dx.doi.org/10.1063/1.3559483.

[11] B. B. Godfrey, Journal of Computational Physics 15, 504 (1974).

[12] B. B. Godfrey, Journal of Computational Physics 19, 58 (1975).

[13] B. B. Godfrey and J.-L. Vay, Journal of Computational Physics 248, 33 (2013).

[14] X. Xu, P. Yu, S. F. Martins, F. S. Tsung, V. K. Decyk, J. Vieira, R. A. Fonseca, W. Lu, L. O. Silva, and W. B. Mori, Computer Physics Communications 184, 2503 (2013).

[15] B. B. Godfrey, J.-L. Vay, and I. Haber, Journal of Computational Physics 258, 689 (2014).

[16] B. Godfrey, J.-L. Vay, and I. Haber, Plasma Science, IEEE Transactions on 42, 1339 (2014).

[17] B. B. Godfrey and J.-L. Vay, Journal of Computational Physics 267, 1 (2014).

[18] B. B. Godfrey, ArXiv e-prints (2014), arXiv:1408.1146 [physics.plasm-ph].

[19] B. B. Godfrey and J.-L. Vay, Computer Physics Communications , (2015).

[20] P. Yu, X. Xu, V. K. Decyk, F. Fiuza, J. Vieira, F. S.

$v _ { g a l }$ is necessarily along $\mathbf { \Delta } \mathbf { u } _ { z }$ and that the expression of k is $\sqrt { k _ { \perp } ^ { 2 } + k _ { z } ^ { 2 } } )$

Tsung, R. A. Fonseca, W. Lu, L. O. Silva, and W. B. Mori, Computer Physics Communications 192, 32 (2015).

[21] P. Yu, X. Xu, A. Tableman, V. K. Decyk, F. S. Tsung, F. Fiuza, A. Davidson, J. Vieira, R. A. Fonseca, W. Lu, L. O. Silva, and W. B. Mori, Computer Physics Communications 197, 144 (2015).

[22] F. Li, P. Yu, X. Xu, F. Fiuza, V. K. Decyk, T. Dalichaouch, A. Davidson, A. Tableman, W. An, F. S. Tsung, R. A. Fonseca, W. Lu, and W. B. Mori, ArXiv e-prints (2016), arXiv:1605.01496 [physics.comp-ph].

[23] A. F. Lifschitz, X. Davoine, E. Lefebvre, J. Faure, C. Rechatin, and V. Malka, J. Comput. Phys. 228, 1803 (2009).

[24] A. Davidson, A. Tableman, W. An, F. S. Tsung, W. Lu, J. Vieira, R. A. Fonseca, L. O. Silva, and W. B. Mori, Journal of Computational Physics 281, 1063 (2015), arXiv:1403.6890 [physics.comp-ph].

[25] M. Kirchen, R. Lehe, B. B. Godfrey, J.-L. Vay, and A. R. Maier, to be submitted (2016).

[26] I. Haber, R. Lee, H. Klein, and J. Boris, Proc. Sixth Conf. on Num. Sim. Plasmas, Berkeley, CA (1973).

[27] J.-L. Vay, I. Haber, and B. B. Godfrey, Journal of Computational Physics 243, 260 (2013).

[28] J. Boris, in Proceeding of the Fourth Conference on Numerical Simulations of Plasmas (Naval Research Laboratory, 1970).

[29] J.-L. Vay, Physics of Plasmas (1994-present) 15, 056701 (2008).

[30] J.-L. Vay, D. P. Grote, R. H. Cohen, and A. Friedman, Computational Science & Discovery 5, 014019 (2012).

[31] R. Lehe, M. Kirchen, I. A. Andriyash, B. B. Godfrey, and J.-L. Vay, Computer Physics Communications 203, 66 (2016).

[32] I. A. Andriyash, R. Lehe, and A. Lifschitz, Physics of Plasmas 23, 033110 (2016), http://dx.doi.org/10.1063/1.4943281.

[33] C. Birdsall and A. Langdon, Plasma Physics via Computer Simulation, Appendix E , Series in Plasma Physics (Taylor & Francis, 2004).

[34] J. Vay and A. Arefiev, AIP Conference Proceedings in press (2014).

[35] H. Vincenti and J.-L. Vay, Computer Physics Communications 200, 147 (2016).

[36] A. Huebl, R. Lehe, J.-L. Vay, D. P. Grote, I. Sbalzarini,

S. Kuschel, M. Bussmann, and A. Huebl, “openpmd 1.0.0: Initial release,” (2015).