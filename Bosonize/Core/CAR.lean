import Mathlib.Algebra.Module.LinearMap.Basic
import Mathlib.LinearAlgebra.CliffordAlgebra.Basic

namespace Bosonize.Core.CAR

variable {ι V R : Type} [CommRing R] [AddCommGroup V] [Module R V]

/-- A representation of the CAR algebra. -/
structure CARRep (ι V R : Type) [CommRing R] [AddCommGroup V] [Module R V] where
  c : ι → Module.End R V
  cdag : ι → Module.End R V

end Bosonize.Core.CAR
