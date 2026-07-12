# Exact charge conservation scheme for Particle-in-Cell simulations for a big class of form-factors

T.Zh.Esirkepov

Forum for Theoretical Physics INFM, Pisa, Italy

Moscow Institute of Physics and Technology, Institutskij per.9, Dolgoprudnij,

Moscow region, 141700 Russia

tel. & fax.: +7 (095) 4086772

e-mail: timur@nonlin-gw.rphys.mipt.ru

Subject classifications: 65C20 Models, numerical methods; 65P20 Solution of discretized equations; 70F10 n-body problem; 77F05 Fluid-particle models.

Keywords: Particle-in-Cell, continuity equation, charge conservation.

Abstract. As an alternative to solving of Poisson equation in Particle-in-Cell methods, a new construction of current density exactly satisfying continuity equation in finite diferences is developed. This procedure called density decomposition is proved to be the only possible linear procedure for defining the current density associated with the motion of a particle. Density decomposition is valid at least for any n-dimensional form-factor which is the product of one-dimensional form-factors. The algorithm is demonstrated for parabolic spline form-factor.

## 1 Introduction

In the present paper we develope a new procedure called density decomposition for obtaining the current density automatically satisfying the continuity equation.

In the set of Maxwell equations along with hyperbolic equations of wave propagation we have an equation of elliptic type — Gauss’s law, that in terms of electric potential $\varphi$ can be expressed as Poisson equation. In practice Poisson equation is used for correction of “potential” part of electric field.

It is well known that Particle-in-Cell (PIC) method in plasma simulations can be implemented without solving Poisson equation for electric field correction. Instead, we need the continuity equation (or charge conservation law) in finite diferences to be satisfyed.

There are a few methods for satisfying the continuity equation locally — for charge and current density associated with each particle, Ref. [1, 2, 3]. For this purpose authors use special definition for the current density wich is naturally connected with the change of charge density due to particle motion. Unfortunately, these methods are implemented only for simple shapes of particles, for the zero- and the first-order form-factors. We present the generalization of these methods, valid for a big class of form-factors. Also we have proved that the density decomposition is the only possible linear procedure for defining the current density associated with the motion of a particle.

There are another methods for incorporating Gauss’s law into Maxwell solver

using usual definition of local current density, see [4, 5].

Very detailed study of PIC method can be found in $[ 6 , 7 , 8 ]$ . The new construction will be usefull firstly for overdensed plasma simulation with the paradigm of ’Clouds-in-Cell’ [9].

## 2 Continuity equation in finite diferences

Let us consider the local Maxwell solver, wich is equivalent to Finite Diference Time Domain (FDTD) method [10]

$$
\frac { { \bf { E } } ^ { n + 1 } - { \bf { E } } ^ { n } } { d t } = \nabla ^ { + } \times { \bf { B } } ^ { n + 1 / 2 } - \mathcal { T } ^ { n + 1 / 2 } ,\tag{1}
$$

$$
\frac { { \bf B } ^ { n + 1 / 2 } - { \bf B } ^ { n - 1 / 2 } } { d t } = - \nabla ^ { - } \times { \bf E } ^ { n } ,\tag{2}
$$

$$
\nabla ^ { - } \cdot \mathbf { E } ^ { n } = \rho ^ { n } ,\tag{3}
$$

$$
\nabla ^ { + } \cdot { \bf B } ^ { n + 1 / 2 } = 0 ,\tag{4}
$$

combined with the particle mover

$$
\frac { { \bf u } _ { \alpha } ^ { n + 1 / 2 } - { \bf u } _ { \alpha } ^ { n - 1 / 2 } } { d t } = 2 \pi \frac { q _ { \alpha } } { m _ { \alpha } } \frac { m _ { e } } { e } \left( { \bf E } ^ { n } ( { \bf x } _ { \alpha } ^ { n } , t ) + \frac { { \bf u } _ { \alpha } ^ { n } } { \gamma _ { \alpha } } \times { \bf B } ^ { n } ( { \bf x } _ { \alpha } ^ { n } , t ) \right) ,\tag{5}
$$

$$
\frac { \mathbf { x } _ { \alpha } ^ { n + 1 } - \mathbf { x } _ { \alpha } ^ { n } } { d t } = \frac { \mathbf { u } _ { \alpha } ^ { n + 1 / 2 } } { \gamma _ { \alpha } ^ { n + 1 / 2 } } ,\tag{6}
$$

$$
\gamma _ { \alpha } = \left( 1 + ( \mathbf { u } _ { \alpha } ) ^ { 2 } \right) ^ { 1 / 2 } .\tag{7}
$$

Equations Eqs.(1-4) are discreetized Maxwell equations and Eqs.(5-6) are leapfrog scheme for solving of Newton-Lorentz equations. Here we use dimensionless variables defined by transformations $t  2 \pi \omega _ { 0 } ^ { - 1 } t , { \bf x }  \lambda _ { 0 } { \bf x } , ( { \bf E } , { \bf B } )  ( m _ { e } c \omega _ { 0 } / e ) ( { \bf E } , { \bf B } )$ where $m _ { e } , e$ — electron mass and charge, c — speed of light, $\omega _ { 0 }$ and $\lambda _ { 0 } \mathrm { ~ - ~ } \mathrm { s o m e }$ characteristic frequency and length (e.g. the frequency and wavelength of incident EM radiation). Index n denotes integer time step and α stands for the number of a particle; $d t , d x , d y , d z \_$ discreetization of time and space coordinates.

Diferent components of electromagnetic fields and charge density ρ and current density J are defined on diferent grids,

$$
\mathbf { E } = ( E _ { i , j + 1 / 2 , k + 1 / 2 } ^ { 1 } , E _ { i + 1 / 2 , j , k + 1 / 2 } ^ { 2 } , E _ { i + 1 / 2 , j + 1 / 2 , k } ^ { 3 } ) , \quad \mathbf { B } = ( B _ { i + 1 / 2 , j , k } ^ { 1 } , B _ { i , j + 1 / 2 , k } ^ { 2 } , B _ { i , j , k + 1 / 2 } ^ { 3 } ) ,
$$

$$
\rho = \rho _ { i + 1 / 2 , j + 1 / 2 , k + 1 / 2 } , \quad \mathcal { J } = ( \mathcal { I } _ { i , j + 1 / 2 , k + 1 / 2 } ^ { 1 } , \mathcal { I } _ { i + 1 / 2 , j , k + 1 / 2 } ^ { 2 } , \mathcal { I } _ { i + 1 / 2 , j + 1 / 2 , k } ^ { 3 } ) ,\tag{8}
$$

where $i , j , k$ are integers. Discreet operators $\nabla ^ { \pm }$ in Eqs.(1-4) are vectors,

$$
\begin{array} { l } { { \nabla ^ { + } f _ { i , j , k } = \left( \frac { f _ { i + 1 , j , k } - f _ { i , j , k } } { d x } , \frac { f _ { i , j + 1 , k } - f _ { i , j , k } } { d y } , \frac { f _ { i , j , k + 1 } - f _ { i , j , k } } { d z } \right) , } } \\ { { \nabla ^ { - } f _ { i , j , k } = \left( \frac { f _ { i , j , k } - f _ { i - 1 , j , k } } { d x } , \frac { f _ { i , j , k } - f _ { i , j - 1 , k } } { d y } , \frac { f _ { i , j , k } - f _ { i , j , k - 1 } } { d z } \right) . } } \end{array}\tag{9}
$$

These operators have the next convenient properties

$$
\nabla ^ { - } \times \nabla ^ { + } = \nabla ^ { + } \times \nabla ^ { - } = 0 , \quad \nabla ^ { - } \cdot \nabla ^ { + } = \nabla ^ { + } \cdot \nabla ^ { - } = \Delta ,\tag{10}
$$

where $\Delta$ is discreet Poisson operator in central diferences,

$$
\Delta f _ { i , j , k } = \frac { f _ { i - 1 , j , k } - 2 f _ { i , j , k } + f _ { i + 1 , j , k } } { d x ^ { 2 } } + \frac { f _ { i , j - 1 , k } - 2 f _ { i , j , k } + f _ { i , j + 1 , k } } { d y ^ { 2 } } + \frac { f _ { i , j , k - 1 } - 2 f _ { i , j , k } + f _ { i , j , k + 1 } } { d z ^ { 2 } } .\tag{11}
$$

Acting on the $\operatorname { E q . } ( 1 )$ by $( \nabla ^ { - } \times )$ and on the Eq.(2) by $( \nabla ^ { + } \times )$ , we obtain

$$
\frac { \rho ^ { n + 1 } - \rho ^ { n } } { d t } + \nabla ^ { - } \cdot \mathcal { T } ^ { n + 1 / 2 } = 0 ,\tag{12}
$$

$$
\frac { \nabla ^ { + } { \bf B } ^ { n + 1 / 2 } - \nabla ^ { + } { \bf B } ^ { n - 1 / 2 } } { d t } = 0 .\tag{13}
$$

It means that if the continuity equation Eq.(12) is fulfilled then the divergence of E is always equal to charge density (Gauss’s law), and if the initial discreet divergence of B is zero then it remains zero forever.

Thus, for solving Maxwell equations we need Eqs.(1-2) and Eq.(12) with initial conditions

$$
\nabla ^ { - } \cdot \mathbf { E } = \rho ~ \mathrm { a n d } ~ \nabla ^ { + } \cdot \mathbf { B } = 0 ~ \mathrm { a t } ~ t = 0 .\tag{14}
$$

Let us consider the continuity equation (or charge conservation law) in finite diferences

$$
\begin{array} { r } { \frac { \rho _ { i + 1 / 2 , j + 1 / 2 , k + 1 / 2 } ^ { n + 1 / 2 } - \rho _ { i + 1 / 2 , j + 1 / 2 , k + 1 / 2 } ^ { n } } { d t } + \frac { \mathcal { I } _ { i , j + 1 / 2 , k + 1 / 2 } ^ { 1 } - \mathcal { I } _ { i - 1 , j + 1 / 2 , k + 1 / 2 } ^ { 1 } } { d x } + } \\ { \frac { \mathcal { I } _ { i + 1 / 2 , j , k + 1 / 2 } ^ { 2 } - \mathcal { I } _ { i + 1 / 2 , j - 1 , k + 1 / 2 } ^ { 2 } } { d y } + \frac { \mathcal { I } _ { i + 1 / 2 , j + 1 / 2 , k } ^ { 3 } - \mathcal { I } _ { i + 1 / 2 , j + 1 / 2 , k - 1 } ^ { 3 } } { d z } = 0 . } \end{array}\tag{15}
$$

Further we will drop indices and modificators like $\pm 1 / 2$ , where it can not lead to an ambiguity. The charge density $\rho$ is constructed from form-factors of separate particles

$$
\rho _ { i , j , k } = \sum _ { \alpha } S _ { i , j , k } ( x _ { \alpha } , y _ { \alpha } , z _ { \alpha } ) ,\tag{16}
$$

where $S$ is the form-factor (or density) of a particle,

$$
S _ { i , j , k } ( x _ { \alpha } , y _ { \alpha } , z _ { \alpha } ) = S ( X _ { i } - x _ { \alpha } , Y _ { j } - y _ { \alpha } , Z _ { k } - z _ { \alpha } ) ,\tag{17}
$$

$X _ { i } , Y _ { j } , Z _ { k }$ denote coordinates of the grid, $\left( x _ { \alpha } , y _ { \alpha } , z _ { \alpha } \right)$ is the location of the particle with number $\alpha .$ Here form-factor can be interpreted as a charge density of a single particle. So the particle is considered as it would be a charged cloud. Form-factor must obey the rule of conservation of full charge which leads to

$$
\sum _ { i , j , k } S _ { i , j , k } ( x _ { \alpha } , y _ { \alpha } , z _ { \alpha } ) = 1 ,\tag{18}
$$

where the sum is taken over all grid nodes.

## 3 Density decomposition

Due to linearity of charge conservation law Eq.(15), it is suficient to construct current density associated with motion of a single particle.

Let us consider a single particle with form-factor Eq.(17) and coordinates $( x , y , z )$ We introduce vector W as finite diferences of the current density associated with particle motion:

$$
\begin{array} { r } { \mathcal { I } _ { i , j , k } ^ { 1 } - \mathcal { I } _ { i - 1 , j , k } ^ { 1 } = - \displaystyle \frac { d x } { d t } W _ { i , j , k } ^ { 1 } , } \\ { \mathcal { I } _ { i , j , k } ^ { 2 } - \mathcal { I } _ { i , j - 1 , k } ^ { 2 } = - \displaystyle \frac { d y } { d t } W _ { i , j , k } ^ { 2 } , } \\ { \mathcal { I } _ { i , j , k } ^ { 3 } - \mathcal { I } _ { i , j , k - 1 } ^ { 3 } = - \displaystyle \frac { d z } { d t } W _ { i , j , k } ^ { 3 } . } \end{array}\tag{19}
$$

Then according to charge conservation law, we can write dropping grid indices,

$$
W ^ { 1 } + W ^ { 2 } + W ^ { 3 } = S ( x + \Delta x , y + \Delta y , z + \Delta z ) - S ( x , y , z ) .\tag{20}
$$

Here $( \Delta x , \Delta y , \Delta z )$ is 3-dimensional shift of the particle due to motion.

Shift of the particle generates eight functions

$$
\begin{array} { r } { S ( x , y , z ) , \quad S ( x + \Delta x , y , z ) , S ( x , y + \Delta y , z ) , S ( x , y , z + \Delta z ) , } \\ { S ( x + \Delta x , y + \Delta y , z ) , S ( x + \Delta x , y , z + \Delta z ) , S ( x , y + \Delta y , z + \Delta z ) , } \\ { S ( x + \Delta x , y + \Delta y , z + \Delta z ) . } \end{array}\tag{21}
$$

We will assume that vector W and corresponding current density linearly depends from these functions. The base for this assumption is the following. (1) We can consider the form-factor as charge density of the particle. If form-factor amplitude is increasing, the current density associated with a shift of the form-factor must increase proportionally. (2) We can decompose any three-dimensional shift of formfactor $S ( x , y , z )$ into three one-dimensional shifts:

$$
\begin{array} { r l r } & { } & { S ( x + \Delta x , y + \Delta y , z + \Delta z ) - S ( x , y , z ) = } \\ & { } & { S ( x + \Delta x , y , z ) - S ( x , y , z ) + } \\ & { } & { S ( x + \Delta x , y + \Delta y , z ) - S ( x + \Delta x , y , z ) + } \\ & { } & { S ( x + \Delta x , y + \Delta y , z + \Delta z ) - S ( x + \Delta x , y + \Delta y , z ) . } \end{array}\tag{22}
$$

Currents corresponding to each one-dimensional shift must be additive.

Let us formulate some conditions directly going form the nature of vector W .

1. Vector $W _ { i , j , k } ^ { 1 } , W _ { i , j , k } ^ { 2 } , W _ { i , j , k } ^ { 3 }$ is a decomposition of finite diference $S _ { i , j , k } ( x { + } \Delta x , y { + }$ $\Delta y , z + \Delta z ) - S _ { i , j , k } ( x , y , z )$ , Eq.(20).

2. If some of shifts $\Delta x , \Delta y , \Delta z$ iz zero, the corresponding component W is also zero:

$$
\Delta x = 0 \Rightarrow W ^ { 1 } = 0 , \Delta y = 0 \Rightarrow W ^ { 2 } = 0 , \Delta z = 0 \Rightarrow W ^ { 3 } = 0 .
$$

3. If $S ( x , y , z )$ is symmetrical with respect to permutation of $( x , y ) , S ( x , y , z ) =$ $S ( y , x , z )$ and $\Delta x = \Delta y$ , then $W ^ { 1 } = W ^ { 2 }$ . The same property is assumed for symmetries with respect to permutations of pairs $( x , z )$ and $( y , z )$

Suggestion. There is only one linear combination of eight functions $E q . ( { \mathcal { Q } } 1 )$ , each satisfying $E q . ( { \boldsymbol { 1 } } \delta )$ , that is consistent with properties 1-3:

$$
\begin{array} { r l r } { V _ { \perp } ^ { \perp } } & { \frac { 1 } { 8 } \xi _ { + } ( x + x ) _ { > } + ( 3 x + x ) _ { > } + ( 4 x ) _ { > } - \frac { 1 } { 8 } x ^ { 2 } x _ { \perp } x _ { \perp } x _ { \perp } + ( { \bf x } ) _ { \perp } x _ { \perp } x _ { \perp } + ( { \bf x } ) _ { \perp } x _ { \perp } x _ { \perp } + } \\ & { } & { + \frac { 1 } { 8 } x _ { \perp } x _ { \perp } x _ { \perp } + x _ { \perp } x _ { \perp } x _ { \perp } - x _ { \perp } x _ { \perp } x _ { \perp } - \frac { 1 } { 8 } x _ { \perp } ( x + x ) _ { \perp } x _ { \perp } x _ { \perp } + } \\ & { } & { + \frac { 1 } { 8 } x _ { \perp } x _ { \perp } x _ { \perp } - \frac { 1 } { 8 } x _ { \perp } x _ { \perp } x _ { \perp } + } \\ & { } & { + \frac { 1 } { 8 } x _ { \perp } x _ { \perp } x _ { \perp } + x _ { \perp } x _ { \perp } - x _ { \perp } x _ { \perp } x _ { \perp } } \\ { V _ { \perp } ^ { \perp } } & { \frac { 1 } { 8 } x _ { \perp } x _ { \perp } x _ { \perp } + } \\ & { } & { - \frac { 1 } { 8 } x _ { \perp } x _ { \perp } ( x _ { \perp } - x _ { \perp } ) _ { \perp } x _ { \perp } + } \\ & { } & { + \frac { 1 } { 8 } x _ { \perp } x _ { \perp } x _ { \perp } - x _ { \perp } x _ { \perp } x _ { \perp } + } \\ & { } & { - \frac { 1 } { 8 } x _ { \perp } x _ { \perp } x _ { \perp } - x _ { \perp } x _ { \perp } x _ { \perp } + } \\ & { } & { - \frac { 1 } { 8 } x _ { \perp } x _ { \perp } - x _ { \perp } x _ { \perp } x _ { \perp } + } \\ & { } &  - \frac   \end{array}\tag{23}
$$

Proof. (Scenario). We can write all the properties 1-3 in the form of linear equations with unknown coeficients of eight functions. Remembering Eq.(18) we can obtain additional equations on coeficients taking sum over all grid points $( i , j , k )$ from each linear combination for $W$ . Solving 10 linear equations for all $S ,$ , we will find all the coeficients. Of course, not all eight values $\mathrm { E q . } ( 2 1 )$ are independent. We have six independend variables $x , y , z , \Delta x , \Delta y , \Delta z$ , so in the most general case only six values $S$ can be also independend, for example, excluding $S ( x , y , z )$ and $S ( x + \Delta x , y + \Delta y , z + \Delta z )$ . Among all possible solutions we must left only one, which doesn’t assume special numerical values for excluded functions. <sup>✷</sup>

Taking into account boundary conditions for the current of one particle (vanishing of the current density at nodes far from the form-factor domain), and using

Eq.(18) we obtain:

$$
\begin{array} { l } { { \displaystyle \sum _ { i } W _ { i , j , k } ^ { 1 } = 0 } , } \\ { { \displaystyle \sum _ { j } W _ { i , j , k } ^ { 2 } = 0 } , } \\ { { \displaystyle \sum _ { k } W _ { i , j , k } ^ { 3 } = 0 } . } \end{array}\tag{24}
$$

Two systems Eq.(23) and Eq.(24) define the density decomposition. Solving Eq.(19) with natural boundary condition we obtain the current density associated with a single particle motion.

The condition Eq.(24) can be easily satisfyed if form-factor have a property of inheritance in decreasing of the dimension, i.e. if sum of form-factor over any dimension is again form-factor but of lower dimension. Formally, it means

$$
S _ { i , j } ^ { ( 2 D ) } ( x , y ) = \sum _ { k } S _ { i , j , k } ^ { ( 3 D ) } ( x , y , z ) ,\tag{25}
$$

where $S _ { i , j } ^ { ( 2 D ) }$ doesn’t depend on z and obeys Eq.(18) automatically.

There is a big and widely used in PIC codes class of form-factors that have a property of inheritance: all form-factors that are the products of one-dimensional form-factors,

$$
S _ { i , j , k } ^ { 3 D } ( x , y , z ) = S _ { i } ^ { 1 D } ( x ) S _ { j } ^ { 1 D } ( y ) S _ { k } ^ { 1 D } ( z ) .\tag{26}
$$

Here we use the same symbol for (probably) diferent one-dimensional form-factors, each of them must satisfy conservation of full charge, Eq.(18).

It can be easily proved that density decomposition Eq.(23) along with Eq.(26) is the generalization of techniques proposed in [1, 2, 3].

## 4 Computing of the current with second-order polynomial form-factor

In this section we present an algorithm for density decomposition in the case of second-order piecewise-polynomial form-factor and discuss a problem of dimension reduction.

Let us consider well-known one-dimensional form-factor

$$
\begin{array} { r c l } { { S _ { i } ^ { ( 1 D ) } ( x ) = \displaystyle { \frac { 3 } { 4 } } - ( X _ { i } - x ) ^ { 2 } } } & { { , } } & { { } } \\ { { S _ { i \pm 1 } ^ { ( 1 D ) } ( x ) = \displaystyle { \frac { 1 } { 2 } } \left( \frac { 1 } { 2 } \mp ( X _ { i } - x ) \right) ^ { 2 } } } & { { , } } & { { | X _ { i } - x | < 1 / 2 , } } \end{array}\tag{27}
$$

which is the second-order spline. The particle is bell-shaped. The correspondent 3-dimensional form-factor is Eq.(26).

Now we can formulate a scenario for computing the current density based on density decomposition Eq.(23). Suppose we consider a code that uses Finite Diference Time Domain (FDTD) technique [10], where electromagnetic fields and current density are defined on diferent regular grids. Here we do not pretend to show optimized or fastest algorithm.

1. Prepare 15-component array S0 containing one-dimensional form-factors corresponding to particle coordinates $( \mathsf { x 0 } , \mathsf { y 0 } , \mathsf { z 0 } )$ with respect to the grid of the charge density $\rho \colon$

$$
\begin{array} { r } { { \sf S 0 } ( i , 1 ) = { S } _ { i } ^ { ( 1 D ) } ( \sf x 0 ) , i = - 2 , 2 , } \\ { { \sf S 0 } ( j , 2 ) = { S } _ { j } ^ { ( 1 D ) } ( \sf y 0 ) , j = - 2 , 2 , } \\ { { \sf S 0 } ( k , 3 ) = { S } _ { k } ^ { ( 1 D ) } ( \sf z 0 ) , k = - 2 , 2 , } \end{array}\tag{28}
$$

Really, components $\mathsf { S } 0 ( - 2 , m )$ and ${ \mathsf { S } } 0 ( 2 , m )$ are zero, but we need these additional components for further calculations.

The actual 3-dimensional form-factor is 27-component array

$$
S ^ { ( 3 D ) } ( i , j , k ) = { 5 0 ( i , 1 ) } * { 5 0 ( j , 2 ) } * { 5 0 ( k , 3 ) } .\tag{29}
$$

2. Using S0 or precomputed $S ^ { ( 3 D ) }$ , compute the force acting on the particle. Here we can use fields spatially averaged to the grid of $\rho$ or compute additional form-factors for each type of grid. Advance particle and compute new particle coordinates $( \mathsf { x 1 } , \mathsf { y 1 } , \mathsf { z 1 } )$ . Note here that particle shift in any direction must be smaller or equal than grid step in this direction,

$$
\times 1 - \times 0 \leq d x , \quad \forall 1 - \forall 0 \leq d y , \quad \mathsf { z 1 } - \mathsf { z 0 } \leq d z .\tag{30}
$$

3. Using new particle coordinates compute a new array S1 containing new formfactors:

$$
\begin{array} { r } { { \sf S 1 } ( i , 1 ) = S _ { i } ^ { ( 1 D ) } ( { \sf x 1 } ) , i = - 2 , 2 , } \\ { { \sf S 1 } ( j , 2 ) = S _ { j } ^ { ( 1 D ) } ( { \sf y 1 } ) , j = - 2 , 2 , } \\ { { \sf S 1 } ( k , 3 ) = S _ { k } ^ { ( 1 D ) } ( { \sf z 1 } ) , k = - 2 , 2 . } \end{array}\tag{31}
$$

Components S1(−2, m) and S1(−2, m) are not zero in general, because of particle motion. If conditions Eq.(30) are satisfyed, the array S1(i, m) doesn’t have non-zero components out of i = −2, 2.

4. Compute auxiliary array of diferences of new and old form-factors:

$$
\begin{array} { r l } & { \mathsf { D S } ( i , 1 ) = 5 1 ( i , 1 ) - 5 0 ( i , 1 ) , i = - 2 , 2 , } \\ & { \mathsf { D S } ( j , 2 ) = 5 1 ( j , 2 ) - 5 0 ( j , 2 ) , j = - 2 , 2 , } \\ & { \mathsf { D S } ( k , 3 ) = 5 1 ( k , 3 ) - 5 0 ( k , 3 ) , k = - 2 , 2 . } \end{array}\tag{32}
$$

It is possible to use S1 for storage of diferences.

5. Compute $1 2 5 ^ { * } 3 .$ -component array containing density decomposition ${ \mathsf { W } } ( i , j , k , m )$ in accordance with Eq.(23). We need so many componets because we have current whose components are defined on diferent regular grids (in FDTD technique).

$$
\begin{array} { r l } & { \mathbb { W } ( i , j , k , 1 ) = \mathsf { D S } ( i , 1 ) \ast ( \mathsf { S O } ( j , 2 ) \ast \mathsf { S O } ( k , 3 ) + \frac { 1 } { 2 } \ast \mathsf { D S } ( j , 2 ) \ast \mathsf { S O } ( k , 3 ) + } \\ & { + \frac { 1 } { 2 } \ast \mathsf { S O } ( j , 2 ) \ast \mathsf { D S } ( k , 3 ) + \frac { 1 } { 3 } \ast \mathsf { D S } ( j , 2 ) \ast \mathsf { D S } ( k , 3 ) ) , } \\ & { \mathbb { W } ( i , j , k , 2 ) = \mathsf { D S } ( j , 2 ) \ast ( \mathsf { S O } ( i , 1 ) \ast \mathsf { S O } ( k , 3 ) + \frac { 1 } { 2 } \ast \mathsf { D S } ( i , 1 ) \ast \mathsf { S O } ( k , 3 ) + } \\ & { + \frac { 1 } { 2 } \ast \mathsf { S O } ( i , 1 ) \ast \mathsf { D S } ( k , 3 ) + \frac { 1 } { 3 } \ast \mathsf { D S } ( i , 1 ) \ast \mathsf { D S } ( k , 3 ) ) , } \\ & { \mathbb { W } ( i , j , k , 3 ) = \mathsf { D S } ( k , 3 ) \ast ( \mathsf { S O } ( i , 1 ) \ast \mathsf { S O } ( j , 2 ) + \frac { 1 } { 2 } \ast \mathsf { D S } ( \bar { i } , 1 ) \ast \mathsf { S O } ( j , 2 ) + } \\ & { + \frac { 1 } { 2 } \ast \mathsf { S O } ( i , 1 ) \ast \mathsf { D S } ( j , 2 ) + \frac { 1 } { 3 } \ast \mathsf { D S } ( i , 1 ) \ast \mathsf { D S } ( j , 2 ) ) . } \end{array}\tag{3}
$$

Of course, this computation is easy to optimize.

6. Compute three components of the current density $\mathcal { I } ^ { 1 } , \mathcal { I } ^ { 2 } , \mathcal { I } ^ { 3 }$ associated with motion of the particle, using Eq.(19) and boundary condition (there is no current in nodes far from particle location),

$$
\begin{array} { l } { \displaystyle \mathcal { I } _ { i , j , k } ^ { 1 } - \mathcal { I } _ { i - 1 , j , k } ^ { 1 } = - \mathsf { Q } \frac { d x } { d t } \mathsf { W } ( i , j , k , 1 ) , } \\ { \displaystyle \mathcal { I } _ { i , j , k } ^ { 2 } - \mathcal { I } _ { i , j - 1 , k } ^ { 2 } = - \mathsf { Q } \frac { d y } { d t } \mathsf { W } ( i , j , k , 2 ) , } \\ { \displaystyle \mathcal { I } _ { i , j , k } ^ { 3 } - \mathcal { I } _ { i , j , k - 1 } ^ { 3 } = - \mathsf { Q } \frac { d z } { d t } \mathsf { W } ( i , j , k , 3 ) , } \end{array}\tag{34}
$$

where Q is the charge of the particle.

7. Add computed contribution from the single particle to array of the current density.

As this algorithm uses only simple polynomes, its accuracy is equivalent to the accuracy of the last digit of numerical representation $( \mathrm { e . g . ~ } 1 0 ^ { - 8 }$ in SINGLE PRECISION 4-BYTE data or $1 0 ^ { - 1 7 }$ in DOUBLE PRECISION 8-BYTE data).

Suppose we have two-dimensional problem, when all the variables depend on $( x , y )$ only. In this case density decomposition Eq.(23) provides only two first components of the current density. How to construct the third one, in consistency with the rest? The simplest idea is to derive the third component from 3-dimensional case by reducing the dimension. We can imagine chaines of infinite number of particles along z-axise. Being projected into $( x , y ) – \mathrm { p l a n e }$ these N chaines produces N 2-dimensional particles. Then we can do averaging over z-axise. As a result we will obtain first two components of the current density in accordance with Eq.(23), and the third component.

In the particular case of the above algorithm we must change formulae of items 5 and 6 in the following way:

$$
\begin{array} { l } { { { \displaystyle { \mathsf W } ( i , j , 1 ) = \mathsf { D } { \mathsf S } ( i , 1 ) * \left( \mathsf { S } 0 ( j , 2 ) + \frac 1 2 * \mathsf { D } { \mathsf S } ( j , 2 ) \right) } , } } \\ { { { \displaystyle { \mathsf W } ( i , j , 2 ) = \mathsf { D } { \mathsf S } ( j , 2 ) * \left( \mathsf { S } 0 ( i , 1 ) + \frac 1 2 * \mathsf { D } { \mathsf S } ( i , 1 ) \right) } , } } \\ { { { \displaystyle { \mathsf W } ( i , j , 3 ) = \mathsf { S } 0 ( i , 1 ) * \mathsf { S } 0 ( j , 2 ) + \frac 1 2 * \mathsf { D } { \mathsf S } ( i , 1 ) * \mathsf { S } 0 ( j , 2 ) + } } } \end{array}
$$

$$
+ \frac 1 2 * { \sf S O } ( i , 1 ) * { \sf D S } ( j , 2 ) + \frac 1 3 * { \sf D S } ( i , 1 ) * { \sf D S } ( j , 2 ) .\tag{35}
$$

$$
\begin{array} { r } { \mathcal { I } _ { i + 1 , j } ^ { 1 } - \mathcal { I } _ { i , j } ^ { 1 } = - \mathsf { Q } \displaystyle \frac { d x } { d t } \mathsf { W } ( i , j , 1 ) , } \\ { \mathcal { I } _ { i , j + 1 } ^ { 2 } - \mathcal { I } _ { i , j } ^ { 2 } = - \mathsf { Q } \displaystyle \frac { d y } { d t } \mathsf { W } ( i , j , 2 ) , } \\ { \mathcal { I } _ { i , j } ^ { 3 } = - \mathsf { Q } \mathsf { V } _ { \mathbf { z } } \mathsf { W } ( i , j , 3 ) , } \end{array}\tag{36}
$$

where $\mathsf { V } _ { z }$ is the third component of particle velocity.

As one can see these formulae have an obvious connection with 3D-case, Eqs.(33- 34).

## 5 Conclusion

In this paper we have developed a construction for a current density, which exactly satisfy the charge conservation law and is valid for a wide class of form-factors. It is shown that this construction is the only allowed by very natural conditions derived from the properties of the current density. An algorithm in the case of second-order polynomial form-factor is presented. One can see that this method is not restricted by special Maxwell solver, but uses only discreetized continuity equation. These teqnique was implemented by author and D.V.Sokolov in three-dimensional and two-dimensional PIC codes.

The author is glad to thank Dmitry Sokolov for collaboration, Prof. Vitaly A. Vshivkov and Dr. Hartmut Ruhl for useful discussion.

The author is pleased to thank Prof. Francesco Pegoraro and Prof. Giuseppe Bertin for support.

This work was prepared in Scuola Normale Superiore in Pisa and supported by Istituto Nazionale per la Fisica della Materia, Italy and by Russian Fond for Basic Research (No.98-02-16298).

## References

[1] R. L. Morse and C. W. Nielson, Numerical Simulation of the Weibel Instability in One and Two Dimensions, Phys. Fluids, 14 (1971).

[2] J. Villasenor and O. Buneman, Rigorous Charge Conservation for Local Electromagnetic Field Solvers, Comp. Phys. Comm., 69, 306 (1992).

[3] V. A. Vshivkov, M. A. Kraeva, V. E. Malyshkin, Parallel Implementation of the Particle-in-Cell Method, Programming and Computer Software, 23, N2, 87-97 (1997).

[4] A. B. Langdon, On enforcing Gauss’s law in electromagnetic particle-in-cell codes, Comput. Phys. Comm., 70, 447 (1992).

[5] B. Marder, A method for incorporating Gauss’s law into electromagnetic PIC codes, J. Comput. Phys., 68, 48 (1987).

[6] C. K. Birdsall and A. B. Langdon, Plasma Physics Via Computer Simulation (Adam-Hilger, 1991).

[7] R. W. Hockney, J. W. Eastwood, Computer Simulation Using Particles (McGraw-Hill Inc., 1981).

[8] Yu. A. Berezin and V. A. Vshivkov, Metod chastits v dinamike razrezhennoi plazmy (Novosibirsk: Izd-vo “Nauka”, 1980), Method of particles in underdense plasma dynamics, published in Russian.

[9] C. K. Birdsall, Dieter Fuss, Clouds-in-Clouds, Clouds-in-Cells Physics for Many-Body Plasma Simulations, J. Comput. Phys., 135, 141 (1997).

[10] K. S. Yee, Numerical Solution of Initial Boundary Value Problems Involving Maxwell’s Ewuations in Isotropic Media, IEEE Trans. Antennas Prop., 14 (1966).