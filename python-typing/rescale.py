# rescale.py
import numpy as np  # type: ignore


def rescale_from_to(array1d: np.ndarray,
                    from_: float = 0.0, to: float = 5.0) -> np.ndarray:
    min_ = np.min(array1d)
    max_ = np.max(array1d)
    rescaled = (array1d - min_) * (to - from_) / (max_ - min_) + from_
    return rescaled


my_array: np.array = np.array([1, 2, 3, 4])

rescaled_array = rescale_from_to(my_array)
