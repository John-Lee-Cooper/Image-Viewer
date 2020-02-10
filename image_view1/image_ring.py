#!/usr/bin/env python

"""
Display all images in paths
"""

import ui
from pathlib import Path
from type_ext import Tuple, List, FilePath, Image
from image_paths import images_in_paths, imread
from ring_buffer import RingBuffer


class ImageRing:
    def __init__(self, paths: List[FilePath]):

        first_image = None
        image_paths_ = images_in_paths(paths)
        if len(image_paths_) == 1:
            first_image = image_paths_[0]
            image_paths_ = images_in_paths([first_image.parent])
        self._ring = RingBuffer(image_paths_, first_image)
        self._image_path = None
        self._image = None
        self.fetch()

    def __call__(self) -> Tuple[FilePath, Image]:
        return self._image_path, self._image.copy()

    def fetch(self) -> None:
        self._image_path = self._ring.value()
        self._image = imread(self._image_path)

    def next(self) -> None:
        self._ring.next()
        self.fetch()

    def prev(self) -> None:
        self._ring.prev()
        self.fetch()

    def pop(self) -> None:
        self._ring.pop()
        self.fetch()
