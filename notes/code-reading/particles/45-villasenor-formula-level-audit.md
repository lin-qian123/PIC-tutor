# Villasenor-Buneman 1992 formula-level audit

## Scope

This note closes the first formula-level pass for the local current construction in the project-local full-text PDF and MinerU Markdown of Villasenor and Buneman (1992). It does not claim a new WarpX regression; it records the paper-to-source mapping used by Chapter 5.

## Four-boundary case

With the local origin at the nearest cell-boundary intersection, the paper writes the four boundary fluxes for a unit square charge as

$$
\begin{aligned}
J_{x1} &= \Delta x\left(\frac12-y-\frac12\Delta y\right), &
J_{x2} &= \Delta x\left(\frac12+y+\frac12\Delta y\right),\\
J_{y1} &= \Delta y\left(\frac12-x-\frac12\Delta x\right), &
J_{y2} &= \Delta y\left(\frac12+x+\frac12\Delta x\right).
\end{aligned}
$$

The formula is an average swept width multiplied by the displacement in the transport direction. The old and new transverse positions enter through the arithmetic mean. In current WarpX `XZ/RZ` code this structure appears as a directional displacement, a transverse old/new node average, and `seg_factor = dt_seg/dt`; the source is not a literal transcription because the modern kernel supports arbitrary shape order, geometry variants, and segment-local writeback.

## Seven- and ten-boundary cases

The paper does not introduce independent seven- or ten-boundary current formula families. A seven-boundary motion is split at the first complementary-mesh crossing into two four-boundary moves:

$$
\Delta x_1 = \frac12-x,\qquad
\Delta y_1 = \frac{\Delta y}{\Delta x}\Delta x_1,qquad
\Delta x_2=\Delta x-\Delta x_1,\qquad
\Delta y_2=\Delta y-\Delta y_1.
$$

A ten-boundary motion is split into three such moves, with each crossing producing a new local origin and a residual displacement. This is the paper-level origin of the modern algorithmic rule “find the earliest crossing, close one segment, repeat”. It is more accurate to map the paper cases to a repeated segment loop than to search WarpX for `seven-boundary` or `ten-boundary` branch labels.

## Three-dimensional cross term

For a 3D straight move, the paper gives the `x`-face contribution at one corner as

$$
\Phi_x = \Delta x\,\bar\eta\,\bar\zeta
       + \frac{\Delta x\,\Delta y\,\Delta z}{12},
$$

with the other three `x`-face contributions carrying the corresponding signs of the two transverse factors and of the cross term. Cyclic permutation gives the `y` and `z` faces. The paper explicitly identifies the `\Delta x\Delta y\Delta z/12` terms as new in 3D. Adding the three fluxes entering the upper corner produces the `1/4` cross contribution required by the difference of the two endpoint volume fractions.

The current WarpX 3D Villasenor kernel expresses the same coupling through four old/new transverse-weight products with `one_third` and `one_sixth`, rather than through one standalone `\Delta x\Delta y\Delta z/12` monomial. This is a representation change, not evidence that the cross coupling disappeared.

## Boundary of the claim

- The local PDF and MinerU Markdown support the formula-level paper claims above.
- The source mapping is grounded in `CurrentDeposition.H` Villasenor explicit/implicit kernels and the Chapter 5 line references.
- The audit does not prove bitwise equivalence between the 1992 unit-square construction and every modern WarpX geometry/order branch.
- Remaining publication work is figure-by-figure transcription and a full symbol/convention normalization pass.

## Executable bounded check

The paper-level identities are also exercised by:

```text
python scripts/verify_villasenor_formula_contract.py --samples 10000
```

With seed `1992`, the check reaches six crossings in one trajectory and obtains maximum 2D residuals of `4.440892098e-16` for the four-boundary flux sums, repeated-segment displacement closure, and segment flux closure. It also checks the Eq.(36) 3D face sums and volume-difference identity; their maximum residual is `1.7763568394002505e-15`. This is deliberately narrower than a WarpX regression: it checks the algebraic/geometric layer represented by the paper formulas, not the modern arbitrary-order kernel, boundary crop, RZ/3D branch, or bitwise output.
