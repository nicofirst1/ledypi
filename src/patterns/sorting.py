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

        # briefly set the color to white to highlight change
        self.color_set(key, (1, 1, 1))
        time.sleep(self.rate() // 10 + 0.001)

        # set the color to the correct one and sleep with rate
        self.color_set(key, item[1])
        time.sleep(self.rate())


class Sorting(Default):
    """
    Sorting patterns
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pattern_name = "Sorting"

        rainbow = rainbow_colormap(n=self.strip_length + 1, end=9 / 10)

        # define pixels as a list of (index, color) tuples
        self.pixels = [(idx, rainbow[idx]) for idx in range(self.strip_length + 1)]
        random.shuffle(self.pixels)

        # then cast to ToSort type
        srt = ToSort(self.color_set, self.rate)
        srt.extend(self.pixels)
        self.pixels = srt

        # dict used to set the sorting effect
        self.sorting_dict = dict(
            bubble_sort=bubble_sort,
            insertion_sort=insertion_sort,
            shell_sort=shell_sort,
            selection_sort=selection_sort,
            heap_sort=heap_sort,
            quick_sort=quick_sort,
            comb_sort=comb_sort,
            cycle_sort=cycle_sort,
            cocktail_sort=cocktail_sort,
            bitonic_sort=bitonic_sort,
            pancake_sort=pancake_sort,
            stooge_sort=stooge_sort,
            oddEven_sort=odd_even_sort,

        )
        self.sorting_alg = bubble_sort
        self.sorting_modifier = Modifier("Sorting algorithm", "quick_sort", options=list(self.sorting_dict.keys()),
                                         on_change=self.on_sort_change)

        self.modifiers = dict(
            sorting_modifier=self.sorting_modifier
        )

    def color_all(self, color):
        """
        Color all the pixels with the same color (useful to set all black)
        :param color: rgba values
        :return:
        """
        try:
            r, g, b = color
        except TypeError:
            return
        for idx in range(self.strip_length):
            # set with handler

            self.handler.set(index=idx, r=int(r), g=int(g), b=int(b), a=self.alpha)

        self.show()

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

        sorting_logger.info(f"Started {self.pattern_name}  pattern with rate: {self.rate()}")
        try:
            while not self.stop:
                for idx in range(self.strip_length + 1):
                    self.color_set(idx, self.pixels[idx][1])

                self.sorting_alg(self.pixels)
                time.sleep(2)
                self.color_all((0, 0, 0))
                time.sleep(1)
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


def heap_sort(lst):
    def heapify(l, heap_size, root_index):
        # Assume the index of the largest element is the root index
        largest = root_index
        left_child = (2 * root_index) + 1
        right_child = (2 * root_index) + 2

        # If the left child of the root is a valid index, and the element is greater
        # than the current largest element, then update the largest element
        if left_child < heap_size and l(left_child) > l(largest):
            largest = left_child

        # Do the same for the right child of the root
        if right_child < heap_size and l(right_child) > l(largest):
            largest = right_child

        # If the largest element is no longer the root element, swap them
        if largest != root_index:
            l[root_index], l[largest] = l[largest], l[root_index]
            # Heapify the new root element to ensure it's the largest
            heapify(l, heap_size, largest)

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


def quick_sort(lst):
    # There are different ways to do a Quick Sort partition, this implements the
    # Hoare partition scheme. Tony Hoare also created the Quick Sort algorithm.
    def partition(l, low, high):
        # We select the middle element to be the pivot. Some implementations select
        # the first element or the last element. Sometimes the median value becomes
        # the pivot, or a random one. There are many more strategies that can be
        # chosen or created.
        pivot = l((low + high) // 2)
        i = low - 1
        j = high + 1
        while True:
            i += 1
            while l(i) < pivot:
                i += 1

            j -= 1
            while l(j) > pivot:
                j -= 1

            if i >= j:
                return j

            # If an element at i (on the left of the pivot) is larger than the
            # element at j (on right right of the pivot), then swap them
            l[i], l[j] = l[j], l[i]

    # Create a helper function that will be called recursively
    def _quick_sort(items, low, high):
        if low < high:
            # This is the index after the pivot, where our lists are split
            split_index = partition(items, low, high)
            _quick_sort(items, low, split_index)
            _quick_sort(items, split_index + 1, high)

    _quick_sort(lst, 0, len(lst) - 1)


# Function to sort arr[] using Comb Sort
def comb_sort(arr):
    # To find next gap from current
    def get_next_gap(gap):
        # Shrink gap by Shrink factor
        gap = (gap * 10) // 13
        if gap < 1:
            return 1
        return gap

    n = len(arr)

    # Initialize gap
    gap = n

    # Initialize swapped as true to make sure that
    # loop runs
    swapped = True

    # Keep running while gap is more than 1 and last
    # iteration caused a swap
    while gap != 1 or swapped == 1:

        # Find next gap
        gap = get_next_gap(gap)

        # Initialize swapped as false so that we can
        # check if swap happened or not
        swapped = False

        # Compare all elements with current gap
        for i in range(0, n - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swapped = True


def cycle_sort(array):
    writes = 0

    # Loop through the array to find cycles to rotate.
    for cycle_start in range(0, len(array) - 1):
        item = array[cycle_start]

        # Find where to put the item.
        pos = cycle_start
        for i in range(cycle_start + 1, len(array)):
            if array[i] < item:
                pos += 1

        # If the item is already there, this is not a cycle.
        if pos == cycle_start:
            continue

        # Otherwise, put the item there or right after any duplicates.
        while item == array[pos]:
            pos += 1
        array[pos], item = item, array[pos]
        writes += 1

        # Rotate the rest of the cycle.
        while pos != cycle_start:

            # Find where to put the item.
            pos = cycle_start
            for i in range(cycle_start + 1, len(array)):
                if array[i] < item:
                    pos += 1

            # Put the item there or right after any duplicates.
            while item == array[pos]:
                pos += 1
            array[pos], item = item, array[pos]
            writes += 1

    return writes


def cocktail_sort(a):
    n = len(a)
    swapped = True
    start = 0
    end = n - 1
    while (swapped == True):

        # reset the swapped flag on entering the loop,
        # because it might be true from a previous
        # iteration.
        swapped = False

        # loop from left to right same as the bubble
        # sort
        for i in range(start, end):
            if (a[i] > a[i + 1]):
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True

        # if nothing moved, then array is sorted.
        if (swapped == False):
            break

        # otherwise, reset the swapped flag so that it
        # can be used in the next stage
        swapped = False

        # move the end point back by one, because
        # item at the end is in its rightful spot
        end = end - 1

        # from right to left, doing the same
        # comparison as in the previous stage
        for i in range(end - 1, start - 1, -1):
            if (a[i] > a[i + 1]):
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True

        # increase the starting point, because
        # the last stage would have moved the next
        # smallest number to its rightful spot.
        start = start + 1


# sorting its two halves in opposite sorting orders, and then
# calls bitonicMerge to make them in the same order
def bitonic_sort(a, low=0, cnt=None, dire=1):
    if cnt == None: cnt = len(a)

    # The parameter dir indicates the sorting direction, ASCENDING
    # or DESCENDING; if (a[i] > a[j]) agrees with the direction,
    # then a[i] and a[j] are interchanged.*/
    def comp_and_swap(a, i, j, dire):
        if (dire == 1 and a[i] > a[j]) or (dire == 0 and a[i] < a[j]):
            a[i], a[j] = a[j], a[i]

    # if dir = 1, and in descending order otherwise (means dir=0).
    # The sequence to be sorted starts at index position low,
    # the parameter cnt is the number of elements to be sorted.
    def bitonic_merge(a, low, cnt, dire):
        if cnt > 1:
            k = cnt // 2
            for i in range(low, low + k):
                comp_and_swap(a, i, i + k, dire)
            bitonic_merge(a, low, k, dire)
            bitonic_merge(a, low + k, k, dire)

    if cnt > 1:
        k = cnt // 2
        bitonic_sort(a, low, k, 1)
        bitonic_sort(a, low + k, k, 0)
        bitonic_merge(a, low, cnt, dire)


# The main function that
# sorts given array
# using flip operations
def pancake_sort(arr):
    # Start from the complete
    # array and one by one
    # reduce current size
    # by one

    # Returns index of the maximum
    # element in arr[0..n-1] */
    def find_max(arr, n):
        mi = 0
        for i in range(0, n):
            if arr[i] > arr[mi]:
                mi = i
        return mi

    # Reverses arr[0..i] */
    def flip(arr, i):
        start = 0
        while start < i:
            temp = arr[start]
            arr[start] = arr[i]
            arr[i] = temp
            start += 1
            i -= 1

    curr_size = len(arr)
    while curr_size > 1:
        # Find index of the maximum
        # element in
        # arr[0..curr_size-1]
        mi = find_max(arr, curr_size)

        # Move the maximum element
        # to end of current array
        # if it's not already at
        # the end
        if mi != curr_size - 1:
            # To move at the end,
            # first move maximum
            # number to beginning
            flip(arr, mi)

            # Now move the maximum
            # number to end by
            # reversing current array
            flip(arr, curr_size - 1)
        curr_size -= 1


def stooge_sort(arr, l=0, h=None):
    if h is None:
        h = len(arr) - 1

    if l >= h:
        return

    # If first element is smaller
    # than last, swap them
    if arr(l) > arr(h):
        t = arr[l]
        arr[l] = arr[h]
        arr[h] = t

        # If there are more than 2 elements in
    # the array
    if h - l + 1 > 2:
        t = int((h - l + 1) / 3)

        # Recursively sort first 2 / 3 elements
        stooge_sort(arr, l, (h - t))

        # Recursively sort last 2 / 3 elements
        stooge_sort(arr, l + t, h)

        # Recursively sort first 2 / 3 elements
        # again to confirm
        stooge_sort(arr, l, (h - t))


def odd_even_sort(arr):
    n = len(arr)
    # Initially array is unsorted
    is_sorted = 0
    while is_sorted == 0:
        is_sorted = 1
        for i in range(1, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                is_sorted = 0

        for i in range(0, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                is_sorted = 0


#       COLOR MAPS
#################################################################
#################################################################


def rainbow_colormap(n, end=2 / 3):
    return [hls_to_rgb(end * i / (n - 1), 0.5, 1) for i in range(n)]
