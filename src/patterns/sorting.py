import logging
import random
import time
from colorsys import hls_to_rgb

import numpy as np

from patterns.default import Default
from utils.modifier import Modifier

sorting_logger = logging.getLogger("sorting_logger")


class ToSort(list):
    """
    Custom list implementation for sorting algo
    sets color and sleep inside the setitem
    use call to get value
    """

    def __init__(self, color_set, rate):
        super(ToSort, self).__init__()
        self.color_set = color_set
        self.rate = rate

    def __getitem__(self, key):
        return super(ToSort, self).__getitem__(key)

    def __call__(self, key, *args, **kwargs):
        return super(ToSort, self).__getitem__(key)[0]

    def __setitem__(self, key, item):
        super(ToSort, self).__setitem__(key, item)
        self.color_set(key, item[1])
        time.sleep(self.rate())


class Sorting(Default):
    """
    Sorting
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pattern_name = "Sorting"

        rainbow = rainbow_color_stops(n=self.strip_length + 1, end=9 / 10)

        # define pixels as a list of (index, color) tuples
        self.pixels = [(idx, rainbow[idx]) for idx in range(self.strip_length + 1)]
        random.shuffle(self.pixels)

        # then cast to ToSort type
        srt = ToSort(self.color_set, self.rate)
        srt.extend(self.pixels)
        self.pixels = srt

        # define modifiers

        # dict used to set the visualizer effect
        self.sorting_dict = dict(
            bubble_sort=bubble_sort,
            insertion_sort=insertion_sort,
            shell_sort=shell_sort,
            selection_sort=selection_sort,
            heap_sort=heap_sort,
            quick_sort=quick_sort,

        )
        self.sorting_alg = bubble_sort
        self.sorting_modifier = Modifier("Sorting algorithm", "shell_sort", options=list(self.sorting_dict.keys()),
                                         on_change=self.on_sort_change)

        self.modifiers=dict(
            sorting_modifier=self.sorting_modifier
        )

    def color_set(self, index, rgb):
        """
        Set the color for the specified pixel
        :param index: int, indices of the pixel in range [0, strip_length]
        :param rgb: RGB class or tuple, the rgba values
        :return:
        """

        # scale rgb based on passed alpha
        r, g, b = np.multiply(rgb, self.alpha, casting='unsafe')

        # set with handler
        self.handler.set(index=index, r=int(r), g=int(g), b=int(b), a=self.alpha)
        self.show()

    def run(self):
        """
        Override run since we have an event based color change ( list value changed) rather than a time one
        :return:
        """

        for idx in range(self.strip_length + 1):
            self.color_set(idx, self.pixels[idx][1])

        self.show()

        sorting_logger.info(f"Started {self.pattern_name}  pattern with rate: {self.rate()}")
        try:
            while not self.stop:
                self.sorting_alg(self.pixels)
                time.sleep(2)
                random.shuffle(self.pixels)
        except KeyboardInterrupt:
            sorting_logger.info("Pattern has been interrupted")
        finally:
            self.close()

    def on_sort_change(self, value):
        """
        Set the effect to a certain value and change the visualization effect in the vis calss
        """
        try:
            alg = self.sorting_dict[value]
            self.sorting_alg = alg
        except KeyError as e:
            print(f"Error for key {value}\n{e}")


#################################################################
#################################################################
#       SORTING ALGORITHM
#################################################################
#################################################################


def bubble_sort(lst):
    # Swap the elements to arrange in order
    for iter_num in range(len(lst) - 1, 0, -1):
        for idx in range(iter_num):
            if lst(idx) > lst(idx + 1):
                temp = lst[idx]
                lst[idx] = lst[idx + 1]
                lst[idx + 1] = temp


def insertion_sort(lst):
    for i in range(1, len(lst)):
        j = i - 1
        nxt_element = lst[i]
        # Compare the current element with next one

        while (lst(j) > nxt_element[0]) and (j >= 0):
            lst[j + 1] = lst[j]
            j = j - 1
        lst[j + 1] = nxt_element


def shell_sort(lst):
    gap = len(lst) // 2
    while gap > 0:

        for i in range(gap, len(lst)):
            temp = lst[i]
            j = i
            # Sort the sub list for this gap

            while j >= gap and lst(j - gap) > temp[0]:
                lst[j] = lst[j - gap]
                j = j - gap
            lst[j] = temp

        # Reduce the gap for the next element

        gap = gap // 2


def selection_sort(lst):
    for idx in range(len(lst)):

        min_idx = idx
        for j in range(idx + 1, len(lst)):
            if lst(min_idx) > lst(j):
                min_idx = j
        # Swap the minimum value with the compared value

        lst[idx], lst[min_idx] = lst[min_idx], lst[idx]


def heapify(lst, heap_size, root_index):
    # Assume the index of the largest element is the root index
    largest = root_index
    left_child = (2 * root_index) + 1
    right_child = (2 * root_index) + 2

    # If the left child of the root is a valid index, and the element is greater
    # than the current largest element, then update the largest element
    if left_child < heap_size and lst(left_child) > lst(largest):
        largest = left_child

    # Do the same for the right child of the root
    if right_child < heap_size and lst(right_child) > lst(largest):
        largest = right_child

    # If the largest element is no longer the root element, swap them
    if largest != root_index:
        lst[root_index], lst[largest] = lst[largest], lst[root_index]
        # Heapify the new root element to ensure it's the largest
        heapify(lst, heap_size, largest)


def heap_sort(lst):
    n = len(lst)

    # Create a Max Heap from the list
    # The 2nd argument of range means we stop at the element before -1 i.e.
    # the first element of the list.
    # The 3rd argument of range means we iterate backwards, reducing the count
    # of i by 1
    for i in range(n, -1, -1):
        heapify(lst, n, i)

    # Move the root of the max heap to the end of
    for i in range(n - 1, 0, -1):
        lst[i], lst[0] = lst[0], lst[i]
        heapify(lst, i, 0)


# There are different ways to do a Quick Sort partition, this implements the
# Hoare partition scheme. Tony Hoare also created the Quick Sort algorithm.
def partition(lst, low, high):
    # We select the middle element to be the pivot. Some implementations select
    # the first element or the last element. Sometimes the median value becomes
    # the pivot, or a random one. There are many more strategies that can be
    # chosen or created.
    pivot = lst((low + high) // 2)
    i = low - 1
    j = high + 1
    while True:
        i += 1
        while lst(i) < pivot:
            i += 1

        j -= 1
        while lst(j) > pivot:
            j -= 1

        if i >= j:
            return j

        # If an element at i (on the left of the pivot) is larger than the
        # element at j (on right right of the pivot), then swap them
        lst[i], lst[j] = lst[j], lst[i]


def quick_sort(lst):
    # Create a helper function that will be called recursively
    def _quick_sort(items, low, high):
        if low < high:
            # This is the index after the pivot, where our lists are split
            split_index = partition(items, low, high)
            _quick_sort(items, low, split_index)
            _quick_sort(items, split_index + 1, high)

    _quick_sort(lst, 0, len(lst) - 1)


#################################################################
#################################################################
#       COLOR MAPS
#################################################################
#################################################################


def rainbow_color_stops(n=10, end=2 / 3):
    return [hls_to_rgb(end * i / (n - 1), 0.5, 1) for i in range(n)]
