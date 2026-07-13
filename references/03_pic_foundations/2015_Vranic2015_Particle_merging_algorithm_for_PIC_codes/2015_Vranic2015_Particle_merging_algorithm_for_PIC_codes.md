# Particle Merging Algorithm for PIC Codes

M. Vranic<sup>a</sup>, T. Grismayer<sup>a</sup>, J. L. Martins<sup>a</sup>, R. A. Fonseca<sup>a,b</sup>, L. O. Silva<sup>a</sup>

<sup>a</sup>GoLP/Instituto de Plasmas e Fus˜ao Nuclear, Instituto Superior T´ecnico, Universidade de Lisboa, 1049-001 Lisbon, Portugal

<sup>b</sup>DCTI/ISCTE - Instituto Universit´ario de Lisboa, 1649-026 Lisboa, Portugal

## Abstract

Particle-in-cell merging algorithms aim to resample dynamically the sixdimensional phase space occupied by particles without distorting substantially the physical description of the system. Whereas various approaches have been proposed in previous works, none of them seemed to be able to conserve fully charge, momentum, energy and their associated distributions. We describe here an alternative algorithm based on the coalescence of N massive or massless particles, considered to be close enough in phase space, into two new macro-particles. The local conservation of charge, momentum and energy are ensured by the resolution of a system of scalar equations. Various simulation comparisons have been carried out with and without the merging algorithm, from classical plasma physics problems to extreme scenarios where quantum electrodynamics is taken into account, showing in addition to the conservation of local quantities, the good reproducibility of the particle distributions. In case where the number of particles ought to increase exponentially in the simulation box, the dynamical merging permits a considerable speedup, and significant memory savings that otherwise would make the simulations impossible to perform.

Keywords:

partice-in-cell, coalescence scheme, QED cascade

## 1. Introduction

Particle-in-cell (PIC) codes are a powerful tool of computational physics that allows to simulate non-linear evolution of electromagnetic systems. The standard electromagnetic PIC algorithm relies on solving the relativistic Maxwell equations for the evolution of the fields, coupled with the relativistic

Lorentz force to advance the charge density [1]. This is a fully self-consistent model that starts from first principles and conserves the energy and momenta throughout the simulations (in fact PIC codes are either momentum conserving or energy conserving and no algorithm conserves both exactly). The particles can explore the full 6D phase space, while the fields are confined on a grid. Maxwell equations are solved at grid points, from where the fields later can be interpolated to any particle locations. Plasma particles are represented by a distribution of macro particles, that may carry diferent statistical weights (one macro particle can represent several real particles). Extended PIC codes can include ionization [2, 3], binary collisions [4, 5] or quantum electrodynamics (QED) modules [6, 7, 8, 9, 10]. These codes have the capability to take full advantage of world’s leading high-performance parallel computing systems - for example, the OSIRIS framework [11] has been shown to run eficiently on systems with as many as $1 0 ^ { 5 } - 1 0 ^ { 6 }$ cores [12]. The scalability relies on carefully optimised parallelisation that divides the space in a way that minimises communications and maximises load balance.

While these codes have been successfully applied to a number of plasma physics scenarios, there are situations that are extremely dificult to model due to a significant accumulation of particles in a limited region of simulation space. For example, in QED cascades very localised regions of extremely strong field can easily produce vast numbers of electron-positron pairs even starting from just one seed electron, leading to an exponential growth of the number of particles being modelled, severely hindering simulation performance and eventually running out of memory. In principle, we could overcome this dificulty by resampling the 6D phase space with diferent macro-particles - many original macro-particles can be merged into fewer macro-particles with higher statistical weights. This is critical for simulating plasma in extreme conditions. However, one needs to ensure that merging does not alter the physics, so a special care should be taken to preserve not only fundamental properties of the system, but also the local particle phase space distribution.

Previous attempts to merge particles for QED cascades were focused on conservation of total quantities: Timokhin in ref.[6] presented a simple scheme where excess particles are deleted and their statistical weight is redistributed evenly among the rest of the simulation particles. This conserves the total charge, but does not conserve total energy and total momentum. None of the quantities are conserved locally, and this introduces diferences in the particle distribution. The authors in ref. [7] use a similar algorithm where the randomly selected particles are deleted while the charge, mass, and energy of the rest particles are increased by the charge, mass, and energy of the deleted particles, respectively. In refs. [13, 14] the authors present several coalescence and splitting schemes, but neither of them conserves the particle distribution function both locally and globally.

In this paper we present a diferent particle merging scheme that preserves the energy, momentum and charge locally and thereby minimises the potential influence to the relevant physics. The algorithm is applicable for massive particles (e.g. electrons, protons, positrons) or massless particles (photons). In addition, the algorithm naturally favourites faster merging in regions with many particles that have similar properties, and does not alter the tail of the distribution that is already sampled by only a small number of particles. All the particles that are merged together are close in 6D phase space. The main benefit of this scheme is that it allows for simulating scenarios that would otherwise be unaccessible, but it can also be used to accelerate simulations with high parallel load imbalance [12] that can occur by accumulation of a large number of particles in a small region of space.

The remainder of this paper is organised as follows: in section 2 we describe the merging algorithm that conserves particle phase space distribution. In section 3, the theoretical estimates for the merging rate in the simulations are presented. Section 4 focuses on the validation of the algorithm through examples of classical and QED plasma interactions: two-stream and filamentation instability, magnetic showers and QED cascades with a two-laser setup. Finally, we present our conclusions in section 5.

## 2. Algorithm

The goal of this algorithm is to map the coordinate and momentum phase space occupied by simulation particles, and resample it without changing the relevant properties of the particle distribution. This can be achieved by identifying the particles that are “close” to each other in 6D phase space (simultaneously close in coordinate and momentum space). The criteria on which particles are considered “close enough” will depend on the typical length/momentum scales that appear in a specific physical scenario. Here we consider the general problem and then, for each specific example, we address the criteria to determine some of the key parameters of the algorithm (merging rate, sampling of the phase space).

![](images/38db8956426f30f57e8e2c1b0b12529c99455bc63de5976f7e2cf3d448f53318.jpg)
Figure 1: Phase space mapping for the merging algorithm. a) An example of a merge cell in a 2D spatial grid. b) Momentum space within a single spatial merge cell. The small sub-cube represents a momentum cell, within which the particles are merged.

For now, we consider that a spatial merge cell contains an integer number of PIC cells in each direction, to be defined for each problem. Our division of space is shown in fig. 1 a) on an example of a 2D grid. Here, a merge cell is shaded and contains 9 PIC cells (3×3).

For the particles that lie within a given merge cell, we first identify what are the boundaries of the momentum space $( p _ { m i n }$ and $p _ { m a x }$ in each direction of the momentum space). The 3D momentum space for merging is represented in Fig. 1 b) where it spans between the minimal and maximal momenta in each direction. Then, we divide this momentum space in several sectors per direction, which yields $n _ { 1 } \times n _ { 2 } \times n _ { 3 }$ volume elements that we define as the momentum cells. Currently all the momentum cells are uniformly distributed but the algorithm can be easily generalised for heterogeneously sized momentum cells. The particles that are within the same momentum cell (they are already in the same spatial merge cell) are considered to be close to one another in 6D phase space and, therefore, candidates to be merged together.

It is now necessary to compute the total statistical weight $w _ { t } .$ momentum $\vec { p _ { t } }$ and energy $\epsilon _ { t }$ contained within one momentum cell:

$$
w _ { t } = \sum _ { i = 1 } ^ { N } w _ { i } \ , \quad \vec { p _ { t } } = \sum _ { i = 1 } ^ { N } w _ { i } \vec { p _ { i } } \ , \quad \epsilon _ { t } = \sum _ { i = 1 } ^ { N } w _ { i } \epsilon _ { i } \ .\tag{1}
$$

where N is the total number of particles of the species to be merged within the momentum cell, while $w _ { i } , \vec { p _ { i } }$ and $\epsilon _ { i }$ represent the statistical weight, the momentum and the energy of the i-th particle respectively. For further calculations we introduce a normalised system of units: $p \to p / m c , \epsilon \to \epsilon / ( m c ^ { 2 } )$ , $t  t \omega _ { N } , E  e E / ( m c \omega _ { N } ) , B  e B / ( m c \omega _ { N } )$ , where c is the speed of light, m is the electron mass, e elementary charge and $\omega _ { N }$ a normalising frequency (typically it is equal to the background plasma frequency or the laser frequency). All total quantities defined in Eq. (1) should be conserved after merging the particles. Ideally, one would conceive that the merging process would lead to one macro particle per momentum cell; however, this does not allow to conserve all the significant quantities. Let us assume that there exists a particle that would conserve $w _ { t } , \vec { p _ { t } }$ and $\epsilon _ { t } .$ . The weight $w _ { n } .$ , momentum $\vec { p _ { n } }$ and energy $\epsilon _ { n }$ of such new particle would then be:

$$
w _ { n } = w _ { t } \ , \vec { p _ { n } } = \frac { \vec { p _ { t } } } { w _ { t } } \ , \quad \epsilon _ { n } = \frac { \epsilon _ { t } } { w _ { t } }\tag{2}
$$

Such a particle would also need to satisfy an energy-momentum relation (in normalised units, for electrons it takes the form $\epsilon _ { n } ^ { 2 } = | | \vec { p _ { n } } | | ^ { 2 } + 1$ , and for photons $\epsilon _ { n } = | | \vec { p _ { n } } | | )$ . A simple example that illustrates a scenario where this is not satisfied is when initially we have only two particles in the momentum cell that have exactly the same weight w and energy $\epsilon ,$ but opposite nonzero momentum vectors $\vec { p }$ and $- { \vec { p . } }$ Here, $\vec { p _ { t } } = 0$ leading to also $\vec { p _ { n } } = 0$ $w _ { n } ~ = ~ w _ { t } ~ = ~ 2 w$ and $\epsilon _ { t } ~ = ~ 2 w \epsilon$ leading to $\epsilon _ { n } ~ = ~ \epsilon$ . If the particles to be merged are photons, the energy-momentum relation is not valid for the new particle because $\epsilon = | | \vec { p } | | > 0 \mathrm { ~ s o ~ } \epsilon _ { n } > | | \vec { p _ { n } } | | = 0$ . Similarly, for electrons $\epsilon = \sqrt { | | \vec { p } | | ^ { 2 } + 1 } > 1$ , hence $\epsilon _ { n } > \sqrt { | | \vec { p _ { n } } | | + 1 } = 1$

The previous example shows that merging into one macro particle would not always allow to locally conserve all the quantities we are interested in, as expected from the requirement to simultaneously conserve momentum and energy i.e. elastic merging. However, if the merging process results in two macro particles instead of one, all the relevant conservation laws can be satisfied. Let us consider two macro particles a and b with $w _ { a } , \vec { p _ { a } } , \epsilon _ { a }$ and $w _ { b }$ $\vec { p _ { b } } , \epsilon _ { b }$ . To conserve the weight, momentum and energy they have to satisfy the following relations:

$$
\begin{array} { c } { { w _ { t } = w _ { a } + w _ { b } \ , } } \\ { { { \vec { p _ { t } } } = w _ { a } { \vec { p _ { a } } } + w _ { b } { \vec { p _ { b } } } \ , } } \\ { { { \epsilon _ { t } } = w _ { a } \epsilon _ { a } + w _ { b } \epsilon _ { b } \ . } } \end{array}\tag{3}
$$

Besides eqs. (3), there are two more energy-momentum relations to be sat-

a)
![](images/e19df43bccd26b8fa7cd9cc737d17dc48b48402c48c10b5cf936728ba40241aa.jpg)
Figure 2: a) Planar view of the two new particles momentum vectors $\vec { p _ { a } }$ and $\vec { p _ { b } }$ that make $\vec { p _ { a } } + \vec { p _ { b } } = 2 \vec { p _ { t } } / w _ { t }$ . b) Diagonal vector of the momentum cell $\vec { d } = ( \pm \Delta p _ { 1 } , ~ \pm \Delta p _ { 2 } , ~ \pm \Delta p _ { 3 } )$

isfied

$$
\mathrm { f o r ~ p h o t o n s ~ ( m a s s l e s s ~ p a r t i c l e s ) : } \qquad \epsilon _ { a } = p _ { a } \ , \quad \epsilon _ { b } = p _ { b } \ ;\tag{4}
$$

$$
\mathrm { a n d ~ f o r ~ e l e c t r o n s ~ ( m a s s i v e ~ p a r t i c l e s ) : } \quad \epsilon _ { a } ^ { 2 } = p _ { a } ^ { 2 } + 1 \ , \quad \epsilon _ { b } ^ { 2 } = p _ { b } ^ { 2 } + 1\tag{5}
$$

From now on, we will consider, without loss of generality the massive particles to be electrons, but the algorithm is valid for other massive particles as well. Equations (3), (4) or (5) make for a system of 7 scalar equations to be satisfied by the proper choice of 10 scalar variables. For the sake of simplicity, we assume that the merged particles are identical i.e. $w _ { a } = w _ { b } = w _ { t } / 2$ and that $\epsilon _ { a } = \epsilon _ { b } = \epsilon _ { t } / w _ { t }$ . From (3) we then get

$$
\vec { p _ { a } } + \vec { p _ { b } } = \frac { 2 \vec { p _ { t } } } { w _ { t } } .\tag{6}
$$

From relations (4) and (5) we can express $p _ { a } = p _ { b } = f ( \epsilon _ { t } / w _ { t } )$ . We will not express it explicitly so that we can continue explaining the algorithm without making the choice if our particles are photons or electrons. For now, we assume that we can calculate the value of $p _ { a }$ and that $p _ { a } \ge p _ { t } / w _ { t }$ (the inequality follows from geometry and will be proven later).

Figure 2 shows a plane that contains the direction of $\vec { p _ { t } }$ and illustrates how two particles can satisfy Eq. (6). It is enough that they have same momentum components parallel to the total momentum $( \vec { p _ { a } } ) _ { | | } = ( \vec { p _ { b } } ) _ { | | } = \vec { p _ { t } } / w _ { t }$ and the same magnitude of the antiparallel components perpendicular to the total momentum $( \vec { p _ { a } } ) _ { \perp } = - ( \vec { p _ { b } } ) _ { \perp }$ . The angle θ between $\vec { p _ { a } }$ and the direction of the total momentum $\vec { p _ { t } }$ is determined by

$$
\cos \theta = { \frac { p _ { t } } { w _ { t } p _ { a } } } \ ,\tag{7}
$$

and $( p _ { a } ) _ { \perp } = p _ { a }$ sin θ. If we choose a spherical coordinate system $( r , \ \theta , \ \phi )$ with the z-axis in direction of $\vec { p _ { t } }$ , it is clear that there is an infinite number of vectors that satisfy Eq. (6). In fact, from the previous considerations, there is still an arbitrary variable, and we could choose an arbitrary azimuthal angle $\phi$ for the vector $\vec { p _ { a } }$ as long as it makes angle θ with the z-axis, still satisfying Eq. (6). Once $\vec { p _ { a } }$ is chosen, this determines $\vec { p _ { b } }$ as well. Particle momenta chosen in this algorithm obey all the necessary constraints and conserve the weight, energy and momentum locally.

Even though $\phi$ and the plane in Fig. 2 a) can be chosen arbitrarily, while simultaneously guaranteeing the total momentum within the momentum cell is conserved, we note that this arbitrariness could distort the final distribution function. Let us assume a plasma that does not move in the $x _ { 3 }$ direction $( p _ { 3 } = 0 )$ , but has a very large momentum spread in other 2 directions. The $\vec { p _ { t } }$ of any momentum cell within any merging cell will be confined in the $p _ { 1 } { - } p _ { 2 }$ plane, but if we choose the plane of vectors $\vec { p _ { a } }$ and $\vec { p _ { b } }$ arbitrarily, this may result in a resulting merged particle having a nonzero component in the $x _ { 3 }$ direction. To avoid such efects, we should make the choice of a plane such that it naturally favours the momentum spreading of the merged particles $\vec { p _ { a } }$ and $\vec { p _ { b } }$ in the direction where the momentum spread already exists within the momentum cell.

To do so, we can use one of the space diagonal vectors joining the vertices of the momentum cell to form the plane with $\vec { p _ { t } }$ (see Fig. 2 b)). This immediately guarantees that if there is no motion in one of the directions, merging will not introduce any spreading along that direction (i.e. if both $\vec { p _ { t } }$ and $\vec { d }$ are in $x _ { 1 } { - } x _ { 2 }$ plane, the result will also be in $x _ { 1 } { - } x _ { 2 }$ plane). If the diagonal chosen is collinear with $\vec { p _ { t } }$ , we can specify another diagonal, provided that there are at least two directions where the momentum spread is non-zero. Special care should be taken when both momentum and momentum spread exist in one direction only - an example would be a particle beam with finite energy spread in $p _ { 1 }$ moving in $x _ { 1 }$ direction. We note that for photons, this is easily solved, because then $\epsilon _ { t } ~ = ~ p _ { t }$ and it is even possible to initialise one photon instead of two, while still conserving all the main quantities. For electrons, this can not be guaranteed and electrons in these conditions should not be merged.

After we have decided what are the momenta of the two new particles within the momentum cell, what is left is to decide where these particles will be initialised. It seems natural to arrange these two particles in the vicinity of the centre-of-mass of the group of particles they are replacing. But, here we will recall that a merge cell can contain several PIC cells, and the centre-ofmass of a sample of particles within a merge cell is more likely to be located in the central PIC cells. This is true for all the momentum cells within the merge cell, so we may put many particles created by merging in a small area of the merge cell. Therefore, if we pick the positions as centre-of-mass positions, we may be introducing local spikes in the density. To avoid this, we pick randomly two already existing particles within the momentum cell and put the new particles exactly at their positions. In this way, artificially induced spikes in the density will not appear provided that we have a large enough statistical sample, (which is automatically guaranteed because the merging is performed only when the number of particles in a merging cell becomes very large).

![](images/35be4020512945bbe00c4a48c5c954076f65159af66bb33438df63b76b9b2cc1.jpg)
Figure 3: Summarised loop of the merging algorithm.

## 2.1. Proof that $\begin{array} { r } { p _ { a } \geq \frac { p _ { t } } { w _ { t } } } \end{array}$

It is clear from Eq. (7) that for $p _ { a } < p _ { t } w _ { t }$ the above presented recipe would not give a sensible result (i. e. cos $\theta > 1 )$ , and, therefore, it is essential to show that the inequality $p _ { a } \ge p _ { t } / w _ { t }$ is always true. For photons, $p _ { a } =$ $\epsilon _ { a } = \epsilon _ { t } / w _ { t } ,$ so the inequality is equivalent to $\epsilon _ { t } \geq p _ { t }$ (the weights are always positive). In terms of a sum over the original photons this is written as

$$
\sum _ { i } w _ { i } \epsilon _ { i } \geq \left| \sum _ { i } w _ { i } \vec { p _ { i } } \right| ,\tag{8}
$$

where in the left-hand side we can use the relation $\epsilon _ { i } = p _ { i }$ and Eq. (8) can be re-written as

$$
\sum _ { i } w _ { i } p _ { i } \geq \left| \sum _ { i } w _ { i } \vec { p _ { i } } \right| .\tag{9}
$$

The inequality (9) is always satisfied for a set of vectors. This follows from the triangle inequality: the left-hand side is a fixed number and the right-hand side reaches the maximum when the vectors are all collinear and pointing in the same direction (then the sums are equal).

For electrons, $p _ { a } ^ { 2 } = \epsilon _ { a } ^ { 2 } - 1$ . In this case, the inequality becomes

$$
\frac { \epsilon _ { t } ^ { 2 } } { w _ { t } ^ { 2 } } - 1 \ge \frac { p _ { t } ^ { 2 } } { w _ { t } ^ { 2 } } , \quad \mathrm { o r } \quad \left( \sum _ { i } w _ { i } \epsilon _ { i } \right) ^ { 2 } \ge \left( \sum _ { i } w _ { i } p _ { i } \right) ^ { 2 } + \left( \sum _ { i } w _ { i } \right) ^ { 2 } .\tag{10}
$$

Here, we already used the inequality (9) valid for any set of vectors, to obtain a fully-scalar sum. This then yields

$$
\sum _ { i } w _ { i } ^ { 2 } \epsilon _ { i } ^ { 2 } + \sum _ { i , j , ~ i \neq j } w _ { i } w _ { j } \epsilon _ { i } \epsilon _ { j } \geq \sum _ { i } w _ { i } ^ { 2 } p _ { i } ^ { 2 } + \sum _ { i , j , ~ i \neq j } w _ { i } w _ { j } p _ { i } p _ { j } + \sum _ { i } w _ { i } ^ { 2 } + \sum _ { i , j , ~ i \neq j } w _ { i } w _ { j } \epsilon _ { i } .\tag{11}
$$

where we know that $\begin{array} { r } { \sum _ { i } w _ { i } ^ { 2 } \epsilon _ { i } ^ { 2 } = \sum _ { i } w _ { i } ^ { 2 } p _ { i } ^ { 2 } + \sum _ { i } w _ { i } ^ { 2 } } \end{array}$ because $\epsilon _ { i } ^ { 2 } = p _ { i } ^ { 2 } + 1$ for every particle (every i). What is now left to prove now is

$$
\sum _ { i , j , \ i \neq j } w _ { i } w _ { j } \epsilon _ { i } \epsilon _ { j } \geq \sum _ { i , j , \ i \neq j } w _ { i } w _ { j } p _ { i } p _ { j } + \sum _ { i , j , \ i \neq j } w _ { i } w _ { j } \ .\tag{12}
$$

If, for every two particles $( i \neq j )$ , we demonstrate that $\epsilon _ { i } \epsilon _ { j } \geq p _ { i } p _ { j } + 1$ , the inequality (12) will automatically be satisfied as well. Expressing the energy through the energy-momentum relation once again yields:

$$
\sqrt { p _ { i } ^ { 2 } + 1 } \sqrt { p _ { j } ^ { 2 } + 1 } \ge p _ { i } p _ { j } + 1 .\tag{13}
$$

Since both sides are positive, we can square the inequality and obtain

$$
p _ { i } ^ { 2 } p _ { j } ^ { 2 } + p _ { i } ^ { 2 } + p _ { j } ^ { 2 } + 1 \ge p _ { i } ^ { 2 } p _ { j } ^ { 2 } + 2 p _ { i } p _ { j } + 1\tag{14}
$$

![](images/4c1449f657692b442e6964d4217248e4d1674a00804aeb9d4b324c4a79cadf1b.jpg)

![](images/e96b3269b0f2ce3a8ea6e06f1568562a649b6587d7ba6e3b2401ded877aac250.jpg)
Figure 4: Number of particles as function of time for a 2D uniform thermal plasma. The initial velocity distribution is a waterbag distribution function in momentum space. The solid line shows the results of the PIC simulation, the dashed line represents the analytical prediction given by the numerical solution of Eq. (17) and the dotted line represents the asymptotic solution (18), for a) slow merging $\lambda = 0 . 1 4 4$ and b) fast merging $\lambda = 2 . 5 3$

which transforms to

$$
( p _ { i } - p _ { j } ) ^ { 2 } \geq 0 ,\tag{15}
$$

an inequality that is always satisfied. Therefore, for both photons and electrons $p _ { a } \geq p _ { t } / w _ { t }$

## 3. Merging rate

The algorithm allows to merge, in a single momentum cell associated with a spatial merging cell, N particles into two. Given all the momentum cells in the simulation, the number of particles $\Delta N _ { T }$ that are removed from the simulation in a time interval $\Delta t _ { m }$ (this time interval is problem dependent and corresponds to the inverse of the merging frequency, i.e., $\Delta t _ { m } = 1 / \omega _ { m } )$ defines the merging rate of the algorithm. Determining the merging rate allows us to assess the impact and the eficiency of the algorithm in the overall evolution of the number of particles in the simulation. In the general case, the total number of particles $\Delta N _ { T }$ being statistically deleted in a time $\Delta t _ { m }$ is

$$
\Delta N _ { T } = \sum _ { i = 1 } ^ { N _ { c } } \sum _ { j = 1 } ^ { N _ { m } } \sum _ { k = 3 } ^ { N _ { p , i } } P _ { i j } ( k ; N _ { p , i } , N _ { m } ) ( k - 2 )\tag{16}
$$

where $N _ { c }$ is the number of merging cells, $N _ { p , i }$ is the number of particles in the i-th merging cell, $N _ { m } = n _ { 1 } \times n _ { 2 } \times n _ { 3 }$ is the total number of momentum cells, and $P _ { i j } ( k )$ the probability of finding k particles in the j-th momentum cell of the i-th merging cell. A rigorous calculation of $\Delta N _ { T }$ is in general not possible since the distribution of particles in every merging cell is a priori unknown. However, we can choose a set-up such that Eq. (16) simplifies drastically; the case of a uniform density thermal plasma with an initial waterbag momentum distribution ofers the advantage of having an exact expression for the probability $P _ { i j } ( k )$ . The uniform density implies that all merging cells should have almost the same number of particles. The same reasoning applies for the momentum space where the waterbag distribution ensures that the number of particles in a merging cell will be evenly distributed in all momentum cells. These properties are exact if the distribution is continuous. In the case of a discrete distribution, fluctuations arise due to the thermal motion of the particles. Let us now assume that we can neglect the fluctuations in the density so that the number of particle in each merging cell is considered as constant. Nonetheless, the statistical fluctuations associated to the distribution of the particles in the binned momentum space are of high relevance to compute the number of particles being merged. For a discrete uniform distribution (such as the waterbag distribution function), the probability of finding k particles in a momentum cell (assuming that all momentum cells have here the same size) is the discrete Poisson probability: $P ( k ; \lambda ) = \lambda ^ { k } e ^ { - \lambda } / k !$ , where $\lambda = N _ { p } / N _ { m }$ . Therefore the merging rate for a uniform thermal plasma is

$$
\frac { d N _ { T } } { d t } = - \omega _ { m } N _ { c } N _ { m } \sum _ { k = 3 } ^ { N _ { p } } P ( k ; N _ { p } / N _ { m } ) ( k - 2 ) ,\tag{17}
$$

where $\omega _ { m } = 1 / \Delta t _ { m }$ is the merging frequency defined for each scenario. When the average number of particles per momentum cell is less than one, i.e., $N _ { p } \ll N _ { m } ,$ , the parameter λ is very small, the Poisson distribution reduces to $P ( k ; \lambda \ll 1 ) \simeq \lambda ^ { k } / k !$ and the result of the sum in Eq. (17) comes mainly from the contribution of the first term of the sum, $P ( k = 3 ; N _ { p } / N _ { m } )$ . The asymptotic formula, assuming λ constant, for the merging rate reads

$$
\frac { d N _ { T } } { d t } \simeq - \omega _ { m } \frac { N _ { c } N _ { p } ^ { 3 } } { 6 N _ { m } ^ { 2 } } .\tag{18}
$$

Surprisingly the merging persists for arbitrary small values of the ratio $N _ { p } / N _ { m } ,$ , thus leading to the conclusion that the number of particle decreases linearly with time in the limit $N _ { p } \ll N _ { m }$ . When the parameter λ is not small compared to one, there is no simple expression for the merging rate and the Eq. (17) should be evaluated numerically.

<table><tr><td>Test</td><td>slow merging</td><td>fast merging</td></tr><tr><td>Dimension</td><td>2D</td><td>2D</td></tr><tr><td>Box size  $[ c / \omega _ { p } ]$ </td><td>5×5</td><td> $5 \times 5$ </td></tr><tr><td># cells</td><td> $5 0 \times 5 0$ </td><td> $5 0 \times 5 0$ </td></tr><tr><td> $\Delta t ~ [ 1 / \omega _ { p } ]$ </td><td> $0 . 0 6 7 2$ </td><td>0.0672</td></tr><tr><td>#  $\mathrm { P a r t } / \mathrm { c e l l }$ </td><td> $1 2 \times 1 2$ </td><td> $1 8 \times 1 8$ </td></tr><tr><td>Merge frequency</td><td> $5 0 ~ \Delta t$ </td><td> $5 0 ~ \Delta t$ </td></tr><tr><td>Merge cell size</td><td>1×1</td><td>2×2</td></tr><tr><td>Momentum cell</td><td> $1 0 \times 1 0 \times 1 0$ </td><td> $8 \times 8 \times 8$ </td></tr><tr><td>initial  $\lambda = N _ { p } / N _ { m }$ </td><td>0.144</td><td>2.53</td></tr><tr><td>Thermal velocity</td><td> $v _ { x } = v _ { y } = v _ { z } = 0 . 1 ~ c$ </td><td> $v _ { x } = v _ { y } = v _ { z } = 0 . 1 ~ c$ </td></tr></table>

Table 1: Simulation parameters for the merging rate.

To verify our predictions regarding the merging rate, we have performed simulations of thermal plasmas with initial waterbag distribution functions. Two simulations cases are presented here: a slow and a fast merging where the initial values of the parameter λ were respectively chosen to be $\lambda = 0 . 1 4 4$ and $\lambda = 2 . 5 3$ , corresponding to a finer (coarser) discretization of the momentum space begin resampled. The details of the two simulations can be found in the Table 1. The comparisons between the simulations and the Eqs.(17) and (18) are shown in Fig. 4. For both cases an excellent agreement is found between simulation and theory. We observe that Eq. (17) is only valid for uniform thermal plasmas with waterbag distribution function. Any deviations from this distribution would alter the predicted merging rate albeit keeping the same trend $( \mathrm { i f } \lambda \ll 1$ , one expects a constant merging rate). For instance, a classical Maxwellian distribution spreads the particles in momentum space from approximatively $- 5 p _ { t h }$ to $5 p _ { t h }$ (the particles out of this range represent a very small fraction of the total number, i.e., $1 - \operatorname { e r f } ( 5 / { \sqrt { ( 2 ) } } ) )$ whereas a waterbag distribution (corresponding to the same density and same amount of kinetic energy than the Maxwellian distribution) spreads exactly the particles from $- \sqrt { 3 } p _ { t h }$ to $\sqrt { 3 } p _ { t h }$ . Hence, for evenly spaced out momentum cells ranging from $p _ { m i n }$ to $p _ { m a x }$ in each direction, it is evident that a momentum cell for the Maxwellian will be bigger than for the waterbag distribution. Despite the diferent shapes of the two distributions, the merging rate corresponding to the Maxwellian distribution will be faster since the majority of the particles are actually contained into the bulk of the distribution. We have verified this in simulations with Maxwellian distribution functions.

<table><tr><td rowspan=1 colspan=1>Test</td><td rowspan=1 colspan=1>2-stream</td><td rowspan=1 colspan=1>Currentfilamentation</td><td rowspan=1 colspan=1>Magneticshower</td><td rowspan=1 colspan=1>QEDcascade</td></tr><tr><td rowspan=7 colspan=1>DimensionalityNorm freq [ωN]Box size [c/ωN]# cells $\Delta t \ [ 1 / \omega _ { N } ]$ # Part/cellMerge frequencyMerge cell sizeMomentum cell</td><td rowspan=1 colspan=1>quasi-1D</td><td rowspan=1 colspan=1>2D</td><td rowspan=2 colspan=1>2D $\omega _ { c } { = } 4 . 4 { \times } 1 0 ^ { 1 4 } / \mathrm { s }$ </td><td rowspan=4 colspan=1>2D $\omega _ { 0 } { = } 1 . 5 { \times } 1 0 ^ { 1 5 } / \mathrm { s }$  $3 0 0 \times 1 2 0$  $3 0 0 0 \times 1 2 0 0$ </td></tr><tr><td rowspan=3 colspan=1> $\omega _ { p }$  $1 0 . 0 { \times } 0 . 1$  $3 0 0 \times 5$ </td><td rowspan=1 colspan=1> $\omega _ { p }$ </td></tr><tr><td rowspan=1 colspan=1> $1 0 . 0 \times 1 0 . 0$ </td><td rowspan=1 colspan=1> $2 . 0 \times 2 . 0$ </td></tr><tr><td rowspan=1 colspan=1> $1 0 0 \times 1 0 0$ </td><td rowspan=1 colspan=1> $5 0 \times 5 0$ </td></tr><tr><td rowspan=3 colspan=1>0.0163 $6 \times 6$  $1 0 ~ \Delta t$  $1 \times 5$  $2 0 \times 2 0 \times 2 0$ </td><td rowspan=1 colspan=1>0.0672</td><td rowspan=1 colspan=1>0.001</td><td rowspan=1 colspan=1>0.0692</td></tr><tr><td rowspan=1 colspan=1> $6 \times 6$ </td><td rowspan=1 colspan=1> $5 \times 5$ </td><td rowspan=2 colspan=1>1 × 15 ∆t10×10 $1 0 \times 1 0 \times 1$ </td></tr><tr><td rowspan=1 colspan=1> $2 \times 2$  $2 0 \times 2 0 \times 2 0$ </td><td rowspan=1 colspan=1> $5 0 ~ \Delta t$  $1 \times 1$  $2 0 \times 2 0 \times 1$ </td></tr><tr><td rowspan=1 colspan=1>External fieldBackgroundFlowsFlow velocityThermal velocity</td><td rowspan=1 colspan=1> $e ^ { + }$  $e ^ { - } e ^ { - }$  $\pm 0 . 2 ~ c$ 0.001 c</td><td rowspan=1 colspan=1> $e ^ { + } e ^ { - }$  $e ^ { + } e ^ { - }$ 0.2 c0.001 c</td><td rowspan=1 colspan=1> $\overline { { \mathrm { B _ { 3 } } { = } 7 . 4 7 \times 1 0 ^ { 1 0 } \mathrm { ~ G } } }$ e $\gamma = 3 0 0 0$ </td><td rowspan=1 colspan=1> $a _ { 0 } { = } 1 0 0 0$ e1一</td></tr><tr><td rowspan=1 colspan=1>Run time womRun time wm</td><td rowspan=1 colspan=1>381 s289 s</td><td rowspan=1 colspan=1>139 s103 s</td><td rowspan=1 colspan=1>821 s340 s</td><td rowspan=1 colspan=1>29917 s1343 s</td></tr><tr><td rowspan=1 colspan=1># of Nodes</td><td rowspan=1 colspan=1> $2 \times 2$ </td><td rowspan=1 colspan=1> $2 \times 2$ </td><td rowspan=1 colspan=1> $2 \times 2$ </td><td rowspan=1 colspan=1>100 × 4</td></tr></table>

Table 2: Simulation parameters for benchmarks of the merging algorithm.

## 4. Numerical simulations

We tested the merging algorithm in various scenarios to evaluate the efect of particle merging in the physics results. The problems tested ranged from classical plasma physics problems to more extreme scenarios that could be modeled without particle merging, showing excellent agreement between merged and non-merged simulations. We will focus here on 4 problems: i) 2 stream instability, ii) Current filamentation, iii) Magnetic shower and iv) QED cascade. Details for the simulation parameters can be found on table 2.

## 4.1. Input parameters

Merging and momentum cells: as we discussed in the algorithm description, the merging process needs to identify the particles that are close in the 6D phase space. The smallest possible merging cell, ensuring the closest proximity in real space, corresponds to a single simulation cell. However, we should keep in mind that an eficient merging is unlikely to occur in such scenario, given the small number of particles likely to be found in the merging cell. Larger merging cells should therefore be chosen, while ensuring that the merge cell size is still suficiently smaller than the smallest relevant physical scale in the simulation. In the algorithm it is also necessary to specify the number of bins each momentum space is divided into. The test runs we have carried out seem to indicate that is preferable to use at least 8 bins per dimension. This number may only be lowered in the dimensions where the momentum dispersion is absent.

Merging frequency: the simulations performed with and without the merging algorithm show that the merging frequency cannot be chosen arbitrarily. Merging every at time step will tend to wash out some of the details of the microphysics, so the choice of the merging frequency $\omega _ { m }$ should be such that the smallest characteristic time scale $\omega _ { c }$ of the system remains well described. The condition $\omega _ { m } \sim \omega _ { c }$ should therefore be suficient to ensure that all relevant physics is accurately modelled. However this condition is not always applicable because it generally leads to a slow merging rate, and as a rule of thumb we recommend a lower limit for the merging frequency such that $1 / \omega _ { m } > 5 \Delta t$ with $\Delta t$ being the PIC time step.

## 4.2. Streaming instabilities

The cold two-stream instabilities, both electrostatic and purely electromagnetic (sometimes referenced as Weibel or current filamentation [15]) have been studied by means of numerical simulations for decades [16, 17, 18, 19]. They represent simple setups that allow us to test validity of the merging algorithm that we have been describing in the previous sections. The simulations results for both instabilities are shown in Fig. 5. We observe an excellent agreement between the runs with and without merging, confirming that the algorithm does not alter the physics while merging the particles. As seen in Fig. 5 the algorithm leads to a decrease of approximatively 50 % of the total number of particles. We also see that both runs show a very similar trend: a slow merging rate during the linear phase of the instabilities (exponential growth of the field energy) followed by a fast merging during the early saturation and, finally, once again a slow merging after saturation. These three stages can be fully explained with our previous analysis of the merging rate. During the linear phase, $0 < \omega _ { p } t < 2 0$ , the number of particles decreases approximatively linearly with time. This is because the linear phase consists of small perturbations originating from thermal noise, (that can be neglected as long as they remain very small compared to the zeroth order quantities). The plasma is hence still close to its initial zero-order equilibrium state and according to the predictions of section 3, the number of particles should decrease in a linear manner since the initial merging parameter $\lambda \ll 1$ for both simulations $( \lambda = 6 ^ { 2 } \times 5 / 2 0 ^ { 3 } = 0 . 0 2 2 5$ for the two-stream and $\lambda = 6 ^ { 2 } \times 4 / 2 0 ^ { 3 } = 0 . 0 1 8$ for the current filamentation). The second stage is characterised by the saturation of the instabilities, corresponding to the time interval $2 0 < \omega _ { p } t < 3 0$ in Fig. 5. At saturation, the linear perturbed fluid quantities start to be on the order of the equilibrium parameters and, in the case of the two-stream instabilities, the density of the plasma exhibits strong modulations that can reach several times the initial density. The bunching in configuration space is accompanied by a bunching in momentum space that allows more particles to be merged. The parameter λ can reach values above one during this phase and one observes a fast merging with a curve that resembles the one obtained in section 3. Finally, the last stage is somehow similar to the first one. During the non-linear phase, the kinetic energy of the flow is converted into electromagnetic fields and thermal particles. The spikes of density are less pronounced as the time goes by and as a result the density tends to be more uniform. This is thus similar to the case of a thermal plasma with weakly modulated density which induces a slow merging, as seen in Fig. 5.

![](images/f51d2e321bf5bb1aaaf382671c5cb01652f235f1643bb72dca1a9fd9705f6c28.jpg)

![](images/519309ab31f63c82f3264071313e4fdcd3f3bf44ce269de44bc90a57d74d1880.jpg)
Figure 5: a) Two stream instability. b) Current filamentation instability. About 50% of particles are merged in both simulations. The left ordinate represent the electric/electromagnetic energy of the system while the right ordinate gives the total number of particle in the simulation. The blue and red lines depict respectively the total electromagnetic field energy of the system for the simulation with and without merging. The green lines show the total number of numerical particles in the simulation as a function of time.

![](images/9b28bdf9a3ad440b46565d3fd5e2fd7df4abb4e86a35449197385523d7737f6d.jpg)

![](images/38b1d413706ae16ea00851815cc2309a5eaa07ea90fa2df3ec7b1b7166d4b611.jpg)
Figure 6: Magnetic showers. a) Energy conservation. The energy transfers from electrons to photons and positrons, but the total energy remains unchanged. b) Number of particles in the simulation without merging, with merging and equivalent number of particles with merging.

## 4.3. Magnetic showers

In order to simulate the creation of electron-positron pairs, we have added a QED module which allows real photon emission from an electron or a positron and decay of the photons into pairs (Breit-Wheeler process). The implementation of such a module and the associated diferential probabilities used can be found in [20, 21, 22, 23, 24, 25]. The specific points of the implementation in OSIRIS are presented elsewhere. One of the challenges of QED-PIC simulations is the emergence of a vast number of particles (hard photons, electrons and positrons) that makes the simulations rather demanding. Among the QED scenarios where this is readily visible are magnetic showers.

Magnetic showers consist in an avalanche of electron-positron pairs produced by the decay of energetic photons in an ultra intense magnetic field [26, 27]. The setup we have chosen is a simple scenario identical as in ref. [8] where a monoenergetic relativistic electron beam propagates initially perpendicularly to a uniform magnetic field. In a purely classical case the beam would describe a circular orbit. However due to the extreme magnitude of the magnetic field (few percent of the Schwinger field), the electrons emit hard photons (through quantum synchrotron radiation) that eventually make the beam slow down and thus spiral down. The photons emitted in the plane perpendicular to the magnetic field decay into pairs which in turn radiate new photons. The process is repeated until the initial energy of the electron beam is fully converted into an electron-positron-photon plasma. The growth of such an avalanche is not exponential since at every step of the process the new pairs created cannot get further energy in the magnetic field and have thus a lower energy than the initial electron (or positron) they are originating from. The time evolution of the number of particles and their corresponding energy in a magnetic shower is depicted on Fig. 6. Figure 6 a) shows that the energy transfer that occurs between the species (the initial energy of the electron beam is converted into photons and positrons as well as lower energy electrons) is well reproduced when the simulation is carried out with the merging algorithm. The number of particles of every species as a function of time is shown in Fig. 6 b). In order to compare both simulations, we also show the equivalent number of particles for the merged simulation, represented by circles in Fig. 6 b), that we calculate by summing the weights of all the particles. The real number of simulation particles of every species with merging turned on is represented by the dashed lines. We observe that these weighted particles, created during the merging process, mimic well the physics of the magnetic showers since the number of equivalent particles agrees at any time with the number of particles obtained in the simulation performed without merging. In this example of magnetic shower, the merged particles represent on average three to five non-merged particles leading to a simulation speed-up of 2.5 (see Table 2).

## 4.4. QED cascades

The QED cascades are characterised by the creation of a pair plasma in a strong laser field [7, 28, 29]. They difer from the usual pair avalanches in the fact that the newly created electrons and positrons are accelerated in the laser field and produce a new generation of photons and pairs similar to their ancestors. The process is then self-similar at every stage and one can expect an exponential growth of the number of pairs. We have a set-up similar to the one proposed by [28] and that has been first simulated by [7]. The cascade is seeded by a few immobile electrons that are located in the central position between two counter-propagating laser pulses. The two laser pulses have temporal Gaussian envelopes with a duration of 60 fs each and the focal spot size is about 10 µm at the location of the electron cloud initially placed at the centre of the simulation box. The additional parameters of the simulation can be found in Table 2. The noticeable diference, in comparison with the magnetic showers, is the exponential growth rate of the number of pairs in the laser field zone. The time evolution of the number and the energy of the produced pairs and photons are identical with and without merging as we can see in Fig. 7. There is also no noticeable diference in energy conservation between the two cases.

![](images/64b81545838e1ef23244af1fcfb7a6bc7c613956330f8ff82523ea947ffc2911.jpg)

![](images/672b42eb348d6e508e93ba3aa7629704cd77a900d2bb4ff59e195f639ccfe0fa.jpg)
Figure 7: Cascade - a) Energy conservation. The energy transfers from the lasers to the electrons and positrons as they get accelerated; later, some of this energy is converted to photons through radiation emission. The inset shows a small level of laser absorption. b) Number of particles with and without merging, and equivalent number of particles with merging.

Even if the main point of this study is not to dwell on the physics of QED cascades, it is also worth mentioning that the self-consistent created pair plasma reaches the relativistic critical density which in turn depletes, due to laser absorption (converted into thermal energy), a fraction of the initial electromagnetic energy. The inset of Fig. 7 a) shows a laser depletion of 3%. The simulation parameters were chosen to keep this value low in order to allow a direct comparison between simulations with and without merging, since the exponentially growing number of particles that results from this scenario would eventually cause the non-merged simulation to run out of memory. Whereas the examples we have discussed previously also showed us the good reproducibility of usual setups with merging, it is truly in scenarios such as QED cascades that the advantage of the algorithm becomes apparent as one notices that the number of pairs/photons is kept low (a factor of 1000 lower in the simulation with merging) in comparison with the standard run, see Fig. 7 b). This considerable reduction of the number of PIC-particles does more than compensate the overhead time due to the merging process and leads to a simulation speed-up of 22 in this particular run. If one envisages to perform QED-PIC simulations that aimed to augment by several orders of magnitude the number of pairs/photons created, it is clear that a standard

![](images/8b067403ef44ce02fe3f4238f91e14a0174ad3c18e81ecc8d8bcb9ed33316b43.jpg)
Figure 8: Cascade (top to bottom) - particle distributions in longitudinal momenta, transverse momenta and energy; weight distribution as compared with the initial weight

QED-PIC code would be unable to accomplish such a task and that the only way to perform these simulations is to rely on a merging algorithm.

The nine top insets of Fig. 8 compare the distribution functions for the merged and non-merged simulations, showing the space averaged momentum $\langle \partial f / \partial p \rangle$ and energy $\langle \partial f / \partial \gamma \rangle$ distributions of the electrons, positrons and photons at time $\omega _ { 0 } t = 1 0 0$ corresponding to the end of the cascade. Despite some small fluctuations in the tail of the distributions, the merged pairs/photons follow the same distributions as the non-merged ones. We have additionally plotted in Fig. 8 the total weight distributions $\langle \partial N / \partial w \rangle$ of each species (electrons, positrons and photons). The pioneering works of [20, 21, 22, 23, 24, 25] tell us that photon emission is a more probable process than pair creation. It results in a higher number of photons merged than pairs and consequently the photon population is distributed over higher weights. In this simulation, the distributions of pairs spread up to $w \sim 5 0 0 w _ { 0 }$ (initially the electrons seeding the cascade had the weight $w _ { 0 } )$ whereas the weight of photons can reach $w \sim 1 0 ^ { 4 } ~ w _ { 0 }$ . We observe that, if required, it is also conceivable to establish an upper bound for the weight of the merged particles. Notwithstanding, all of the weight distributions display similar shapes: a bulk localised at small weights and a lower number of particles in an exponential tail at high weights. It is an additional indication that the dynamical merging does not jeopardise the PIC statistics, as the particles outside of the vastly occupied regions of 6D phasespace retain their original weights.

## 5. Conclusions

In summary, the particle merging algorithm for PIC simulations that has been implemented and tested conserves locally energy, momentum and charge by a detailed resampling of the 6D phase space. This particle merging algorithm naturally favors resampling the bulk of the particle distribution, and leaving the areas with a small statistical sample intact. When using this scheme, one should be aware of the typical length scales associated with the physics of the simulation and choose the size of the merging cells accordingly.

We have studied the influence of merging on the simulation results in classical and QED scenarios, by comparing the full-PIC simulations with and without merging of particles. The presented scheme is found to be very successful in reproducing results both for linear and nonlinear plasma processes. We have also provided an estimate of the expected merging rate, that could help in the design and planning of the simulations.

This algorithm will allow for significant speedups whenever the number of numerical particles in the simulation grows significantly (e.g. due to ionisation or pair-creation mechanisms). For instance, a huge speedup of QED cascading simulations has been verified and has enabled us to simulate problems in timescales otherwise impossible due to the exponential growth rate of the number of particles. Local conservation of energy, momentum and charge minimises the efect of resampling on the underlying physics, so it can be used also to improve the load balance of many other PIC simulations that encounter strong particle grouping both in real and in momentum space. More importantly, with marcroparticle merging algorithm it is now possible to explore problems that would otherwise not be accessible due to memory limitations.

## Acknowledgement

M. Vranic and T. Grismayer contributed equally to this work. This work was partially supported by the European Research Council (ERC-2010-AdG Grant 267841) and FCT (Portugal) grants FCT/IF/01780/2013, SFRH/BD/62137/2009. We would like to acknowledge the assistance of high performance computing resources (Tier-0) provided by PRACE on JuQUEEN and SuperMUC based in Germany. Simulations were performed at the IST cluster (Lisbon, Portugal), JuQUEEN and SuperMUC (Germany).

## References

[1] C. K. Birdsall, A. B. Langdon, Plasma Physics via Computer Simulation, Taylor & Francis, 2004.

[2] M. Chen, E. Cormier-Michel, C. Geddes, D. Bruhwiler, L. Yu, E. Esarey, C. Schroeder, W. Leemans, Numerical modeling of laser tunneling ionization in explicit particle-in-cell codes, Journal of Computational Physics 236 (0) (2013) 220 – 228. doi:http://dx.doi.org/10.1016/ j.jcp.2012.11.029.

[3] D. L. Bruhwiler, D. A. Dimitrov, J. R. Cary, E. Esarey, W. Leemans, R. E. Giacone, Particle-in-cell simulations of tunneling ionization efects

in plasma-based accelerators, Physics of Plasmas 10 (5) (2003) 2022– 2030. doi:http://dx.doi.org/10.1063/1.1566027.

[4] F. Peano, M. Marti, L. O. Silva, G. Coppa, Statistical kinetic treatment of relativistic binary collisions, Phys. Rev. E 79 (2009) 025701. doi: 10.1103/PhysRevE.79.025701.

[5] T. Takizuka, H. Abe, A binary collision model for plasma simulation with a particle code, Journal of Computational Physics 25 (3) (1977) 205 – 219. doi:http://dx.doi.org/10.1016/0021-9991(77)90099-7.

[6] A. N. Timokhin, Time-dependent pair cascades in magnetospheres of neutron stars i. dynamics of the polar cap cascade with no particle supply from the neutron star surface, Mon. Not. R. Astron. Soc. 408 (2010) 20922114. doi:10.1111/j.1365-2966.2010.17286.x.

[7] E. N. Nerush, I. Y. Kostyukov, A. M. Fedotov, N. B. Narozhny, N. V. Elkina, H. Ruhl, Laser field absorption in self-generated electronpositron pair plasma, Phys. Rev. Lett. 106 (2011) 035001. doi:10. 1103/PhysRevLett.106.035001.

[8] M. Lobet, E. dHumieres, M. Grech, C. Ruyer, X. Davoine, L. Gremillet, Modeling of radiative and quantum electrodynamics efects in pic simulations of ultra-relativistic laser-plasma interaction, ArXiv 1311.1107v2.

[9] C. P. Ridgers, C. S. Brady, R. Duclous, J. G. Kirk, K. Bennett, T. D. Arber, A. P. L. Robinson, A. R. Bell, Dense electron-positron plasmas and ultraintense γ rays from laser-irradiated solids, Phys. Rev. Lett. 108 (2012) 165006. doi:10.1103/PhysRevLett.108.165006.

[10] T. Grismayer, to be submitted (2014).

[11] R. A. Fonseca, L. O. Silva, F. S. Tsung, V. K. Decyk, W. Lu, C. Ren, W. B. Mori, S. Deng, S. Lee, T. Katsouleas, J. C. Adam, OSIRIS: A three-dimensional, fully relativistic particle in cell code for modeling plasma based accelerators, Vol. 2331, Springer Berlin / Heidelberg, 2002.

[12] R. A. Fonseca, J. Vieira, F. Fiuza, A. Davidson, F. S. Tsung, W. B. Mori, L. O. Silva, Exploiting multi-scale parallelism for large scale numerical modelling of laser wakefield accelerators, Plasma Physics and Controlled Fusion 55 (12) (2013) 124011.

[13] G. Lapenta, J. U. Brackbill, Dynamic and selective control of the number of particles in kinetic plasma simulations, Journal of Computational Physics 115 (1) (1994) 213 – 227. doi:http://dx.doi.org/10.1006/ jcph.1994.1188.

[14] G. Lapenta, Particle rezoning for multidimensional kinetic particle-incell simulations, Journal of Computational Physics 181 (1) (2002) 317 – 337. doi:http://dx.doi.org/10.1006/jcph.2002.7126.

[15] M. V. Medvedev, A. Loeb, Generation of magnetic fields in the relativistic shock of gamma-ray burst sources, The Astrophysical Journal 526 (2) (1999) 697.

[16] L. O. Silva, R. A. Fonseca, J. W. Tonge, J. M. Dawson, W. B. Mori, M. V. Medvedev, Interpenetrating plasma shells: Near-equipartition magnetic field generation and nonthermal particle acceleration, The Astrophysical Journal Letters 596 (1) (2003) L121.

[17] W. E. Drummond, J. H. Malmberg, T. M. ONeil, J. R. Thompson, Nonlinear development of the beam-plasma instability, Physics of Fluids (1958-1988) 13 (9) (1970) 2422–2425. doi:http://dx.doi.org/10. 1063/1.1693255.

[18] A. Bret, M.-C. Firpo, C. Deutsch, Collective electromagnetic modes for beam-plasma interaction in the whole k space, Phys. Rev. E 70 (2004) 046401. doi:10.1103/PhysRevE.70.046401.

[19] L. E. Thode, R. N. Sudan, Two-stream instability heating of plasmas by relativistic electron beams, Phys. Rev. Lett. 30 (1973) 732–735. doi: 10.1103/PhysRevLett.30.732.

[20] A. I. Nikishov, V. I. Ritus, Quantum processes in the field of a plane electromagnetic wave and in a constant field, Sov. Phys. JETP 19 (1964) 529–541.

[21] A. I. Nikishov, V. I. Ritus, Pair production by a photon and photon emission by an electron in the field of ultra intense electromagnetic wave and in a constant field, Sov. Phys. JETP 25 (6).

[22] V. Ritus, Quantum efects of the interaction of elementary particles with an intense electromagnetic field, Journal of Soviet Laser Research 6 (5) (1985) 497–617. doi:10.1007/BF01120220.

[23] V. Baier, V. Katkov, Quantum efects in magnetic bremsstrahlung, Physics Letters A 25 (7) (1967) 492 – 493. doi:http://dx.doi.org/ 10.1016/0375-9601(67)90003-5.

[24] N. P. Klepikov, Emission of photons or electron-positron pairs in magnetic fields, Zhur. Esptl. i Teoret. Fiz. 26.

[25] T. ERBER, High-energy electromagnetic conversion processes in intense magnetic fields, Rev. Mod. Phys. 38 (1966) 626–659. doi:10.1103/ RevModPhys.38.626.

[26] A. I. Akhiezer, N. P. Merenkov, A. P. Rekalo, On a kinetic theory of electromagnetic showers in strong magnetic fields, Journal of Physics G: Nuclear and Particle Physics 20 (9) (1994) 1499.

[27] V. Anguelov, H. Vankov, Electromagnetic showers in a strong magnetic field, Journal of Physics G: Nuclear and Particle Physics 25 (8) (1999) 1755.

[28] A. R. Bell, J. G. Kirk, Possibility of prolific pair production with highpower lasers, Phys. Rev. Lett. 101 (20) (2008) 200403. doi:10.1103/ PhysRevLett.101.200403.

[29] A. M. Fedotov, N. B. Narozhny, G. Mourou, G. Korn, Limitations on the attainable intensity of high power lasers, Phys. Rev. Lett. 105 (2010) 080402. doi:10.1103/PhysRevLett.105.080402.