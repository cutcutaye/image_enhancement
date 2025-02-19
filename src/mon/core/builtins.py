#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module extends Python builtin data types."""

from __future__ import annotations

__all__ = [
    "concat_lists", "copy_attr", "get_module_vars", "intersect_dicts",
    "intersect_ordered_dicts", "iter_to_iter", "iter_to_list", "iter_to_tuple",
    "shuffle_dict", "split_list", "to_1list", "to_1tuple", "to_2list",
    "to_2tuple", "to_3list", "to_3tuple", "to_4list", "to_4tuple", "to_5list",
    "to_5tuple", "to_6list", "to_6tuple", "to_float", "to_int", "to_list",
    "to_nlist", "to_ntuple", "to_pair", "to_quadruple", "to_single",
    "to_triple", "to_tuple", "unique",
]

import copy
import itertools
import random
from collections import OrderedDict
from types import ModuleType
from typing import Any, Callable, Iterable

import multipledispatch


# region Object

def copy_attr(src: Any, dst: Any, include: list = [], exclude: list = []):
    """Copy all attributes from object :obj:`x` to object :obj:`y`, except
    for those that start with an underscore, or are in the :param:`exclude`
    :class:`list`.

    Args:
        src: An object to copy from.
        dst: An object to copy to.
        include: A :class:`list` of attributes to include. If given, only
            attributes whose names reside in this list are copied.
        exclude: A :class:`list` of attributes to exclude from copying.
    """
    for k, v in src.__dict__.items():
        if (len(include) and k not in include) \
            or k.startswith("_") \
            or k in exclude:
            continue
        else:
            setattr(dst, k, v)
    return dst


def get_module_vars(module: ModuleType) -> dict:
    """Return all public variables of a module in a :class:`dict`."""
    return {
        k: v for k, v in vars(module).items()
        if not (
            k == "__init__"
            or callable(k)
            or isinstance(v, ModuleType)
            or k.startswith(("_", "__", "annotations"))
        )
    }
    
# endregion


# region Numeric

def to_int(x: str | int | float) -> int:
    """Convert a value to :class:`int`."""
    if isinstance(x, str) and not x.isdigit():
        raise ValueError(f"x must be a digit string, but got {x}.")
    return int(x)


def to_float(x: str | int | float) -> float:
    """Convert a value to :class:`float`."""
    if isinstance(x, str) and not x.isdigit():
        raise ValueError(f"x must be a digit string, but got {x}.")
    return float(x)

# endregion


# region Collection

def intersect_dicts(x: dict, y: dict, exclude: list = []) -> dict:
    """Find the intersection between two :class:`dict`.
    
    Args:
        x: The first :class:`dict`.
        y: The second :class:`dict`.
        exclude: A :class:`list` of excluding keys.
    
    Returns:
        A :class:`dict` that contains only the keys that are in both :param:`x`
        and :param:`y`, and whose values are equal.
    """
    return {
        k: v for k, v in x.items()
        if k in y and not any(x in k for x in exclude) and v == y[k]
    }


def intersect_ordered_dicts(
    x      : OrderedDict,
    y      : OrderedDict,
    exclude: list = [],
) -> OrderedDict:
    """Find the intersection between two :class:`OrderedDict`.
    
    Args:
        x: The first ordered :class:`dict`.
        y: The second ordered :class:`dict`.
        exclude: A :class:`list` of excluding keys.
    
    Returns:
        An :class:`OrderedDict` that contains only the keys that are in both
        :param:`x` and :param:`y`, and whose values are equal.
    """
    return OrderedDict(
        (k, v) for k, v in x.items()
        if (k in y and not any(x in k for x in exclude) and v == y[k])
    )


def shuffle_dict(x: dict) -> dict:
    """Shuffle a :class:`dict` randomly."""
    keys = list(x.keys())
    random.shuffle(keys)
    shuffled = {}
    for key in keys:
        shuffled[key] = x[key]
    return shuffled
    
# endregion


# region Sequence

def concat_lists(x: list[list]) -> list:
    """Concatenate a :class:`list` of lists into a flattened :class:`list`."""
    x = list(itertools.chain(*x))
    return x


def iter_to_iter(x: Iterable, item_type: type, return_type: type | None = None):
    """Convert an :class:`Iterable` object to a desired sequence type specified
    by the :param:`return_type`. Also, cast each item into the desired
    :param:`item_type`.
    
    Args:
        x: An :class:`Iterable` object.
        item_type: The item type.
        return_type: The desired iterable type. Default: ``None``.
    
    Returns:
        An :class:`Iterable` object cast to the desired type.
    """
    if not isinstance(x, list | tuple | dict):
        raise TypeError(f"x must be a list, tuple, or dict, but got {type(x)}.")
    x = copy.deepcopy(x)
    x = map(item_type, x)
    if return_type is None:
        return x
    else:
        return return_type(x)


def iter_to_list(x: Iterable, item_type: type) -> list:
    """Convert an arbitrary :class:`Iterable` object to a :class:`list`."""
    return iter_to_iter(x=x, item_type=item_type, return_type=list)


def iter_to_tuple(x: Iterable, item_type: type) -> tuple:
    """Convert an arbitrary :class:`Iterable` object to a :class:`tuple`."""
    return iter_to_iter(x=x, item_type=item_type, return_type=tuple)


def split_list(x: list, n: int | list[int]) -> list[list]:
    """Slice a single :class:`list` into a list of lists.
    
    Args:
        x: A :class:`list` object.
        n: A number of sub-lists, or a :class:`list` of integers to specify the
            length of each sub-list.
        
    Returns:
        A :class:`list` of lists.
    
    Examples:
        >>> x = [1, 2, 3, 4, 5, 6]
        >>> y = split_list(x, n=2)          # [1, 2, 3], [4, 5, 6]
        >>> z = split_list(x, n=[1, 3, 2])  # [1], [2, 3, 4], [5, 6]
    """
    if isinstance(n, int):
        if len(x) % n == 0:
            raise ValueError(
                f"x cannot be evenly split into {n} sub-list, got length of x "
                f"is {len(x)}."
            )
        n = [n] * int(len(x) / n)
    
    if sum(n) != len(x):
        raise ValueError(
            f"The total length of new sub-lists must match the length of x, "
            f"but got: {sum(n) != len(x)}."
        )
    
    y = []
    idx = 0
    for i in range(len(n)):
        y.append(x[idx: idx + n[i]])
        idx += n[i]
    return y


def to_list(x: Any) -> list:
    """Convert an arbitrary value into a :class:`list`."""
    if isinstance(x, list):
        pass
    elif isinstance(x, tuple):
        x = list(x)
    elif isinstance(x, dict):
        x = list(x.values())
    else:
        x = [x]
    return x


def to_nlist(n: int) -> Callable[[Any], list]:
    """Take an integer :param:`n` and return a function that takes an
    :class:`Iterable` object and returns a :class:`list` of length :param:`n`.
    
    Args:
        n: The number of elements in the :class:`list`.
    
    Returns:
        A function that takes an integer and returns :class:`list` of that
        integer :param:`n` repeated n times.
    """
    def parse(x) -> list:
        if isinstance(x, Iterable):
            x = list(x)
            if len(x) == 1:
                x = list(itertools.repeat(x[0], n))
        else:
            x = list(itertools.repeat(x, n))
        return x
    
    return parse


to_1list = to_nlist(1)
to_2list = to_nlist(2)
to_3list = to_nlist(3)
to_4list = to_nlist(4)
to_5list = to_nlist(5)
to_6list = to_nlist(6)


def to_tuple(x: Any) -> tuple:
    """Convert an arbitrary value into a :class:`tuple`."""
    if isinstance(x, list):
        x = tuple(x)
    elif isinstance(x, tuple):
        pass
    elif isinstance(x, dict):
        x = tuple(x.values())
    else:
        x = tuple(x)
    return x


def to_ntuple(n: int) -> Callable[[Any], tuple]:
    """Take an integer :param:`n` and return a function that takes an
    :class:`Iterable` object and returns a :class:`tuple` of length :param:`n`.
    
    Args:
        n: The number of elements in the :class:`tuple`.
    
    Returns:
        A function that takes an integer :param:`n`n and returns a
        :class:`tuple` of that integer repeated n times.
    """
    def parse(x) -> tuple:
        if isinstance(x, Iterable):
            x = tuple(x)
            if len(x) == 1:
                x = tuple(itertools.repeat(x[0], n))
        else:
            x = tuple(itertools.repeat(x, n))
        return x
    
    return parse


to_1tuple    = to_ntuple(1)
to_2tuple    = to_ntuple(2)
to_3tuple    = to_ntuple(3)
to_4tuple    = to_ntuple(4)
to_5tuple    = to_ntuple(5)
to_6tuple    = to_ntuple(6)
to_single    = to_ntuple(1)
to_pair      = to_ntuple(2)
to_triple    = to_ntuple(3)
to_quadruple = to_ntuple(4)


@multipledispatch.dispatch(list)
def unique(x: list) -> list:
    """Get unique items from a :class:`list`."""
    return list(set(x))


@multipledispatch.dispatch(tuple)
def unique(x: tuple) -> tuple:
    """Get unique items from a :class:`tuple`."""
    return tuple(set(x))

# endregion
