""" This module provides a method to generate a random number between 0 and the specified number """
import random
import math


def random_num(max):
    """ 
    Generates a random number 

    Parameters: 
    max(int): the range upper limit

    Returns:
    int: the random number
    """
    return math.floor(random.random() * max)
