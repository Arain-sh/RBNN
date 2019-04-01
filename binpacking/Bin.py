"""
Bin class.

Author: Arain, Linli
Date: March 29, 2019.
Bin data:
  Example for 2-D bin packing
      (x, y, u) tuples.
      x is the width, y is the height, u is 1 packed or 0 for unpacked.
"""


class Bin():
    """
    Bin class.

    (x, y, u) tuples.
    x is the width, y is the height, u is 1 packed or 0 for unpacked.
    """

    __dim = [2, 3]  # 2-D or 3-D
    x = 0
    y = 0
    u = 0

    def __init__(self, x, y, u):
        """Set up initial Bin configuration."""
        self.x = x
        self.y = y
        self.u = u
