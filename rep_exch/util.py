import matplotlib.pyplot as plt
import numpy as np
import openmm as mm
import openmm.app.element as elem
from openmm import *
from openmm import unit
from openmm.app import *
from scipy.optimize import curve_fit


def distance(positions_1, positions_2):
    """
    Calculate the distance between two particles, given their positions.

    :param positions_1: Positions for the first particle
    :type positions_1: `Quantity() <http://docs.openmm.org/development/api-python/generated/simtk.unit.quantity.Quantity.html>`_ ( np.array( [3] ), simtk.unit )

    :param positions_2: Positions for the first particle
    :type positions_2: `Quantity() <http://docs.openmm.org/development/api-python/generated/simtk.unit.quantity.Quantity.html>`_ ( np.array( [3] ), simtk.unit )

    :returns:
        - distance ( `Quantity() <http://docs.openmm.org/development/api-python/generated/simtk.unit.quantity.Quantity.html>`_) - Distance between two particles

    :Example:

    >>> from foldamers.cg_model.cgmodel import CGModel
    >>> cgmodel = CGModel()
    >>> particle_1_coordinates = cgmodel.positions[0]
    >>> particle_2_coordinates = cgmodel.positions[1]
    >>> particle_distance = distance(particle_1_coordinates,particle_2_coordinates)

    """

    # Ensure that the output keeps the original units:
    positions_unit = positions_1.unit
    p1 = positions_1.value_in_unit(positions_unit)
    p2 = positions_2.value_in_unit(positions_unit)
    
    distance = np.sqrt(np.sum(np.power((p1-p2),2)))
    distance *= positions_unit
    
    return distance


def get_box_vectors(box_size):
    """
    Given a simulation box length, construct a vector.

    :param box_size: Length of individual sides of a simulation box
    :type box_size: `Quantity() <http://docs.openmm.org/development/api-python/generated/simtk.unit.quantity.Quantity.html>`_ ( float, simtk.unit )

    :returns:
         - box_vectors ( List( `Quantity() <http://docs.openmm.org/development/api-python/generated/simtk.unit.quantity.Quantity.html>`_ ) ) - Vectors to use when defining an OpenMM simulation box.

    """

    units = box_size.unit
    a = unit.Quantity(np.zeros([3]), units)
    a[0] = box_size
    b = unit.Quantity(np.zeros([3]), units)
    b[1] = box_size
    c = unit.Quantity(np.zeros([3]), units)
    c[2] = box_size
    box_vectors = [a, b, c]
    return box_vectors


def set_box_vectors(system, box_size):
    """
    Impose a set of simulation box vectors on an OpenMM simulation object.

    :param system: OpenMM System()
    :type system: `System() <https://simtk.org/api_docs/openmm/api4_1/python/classsimtk_1_1openmm_1_1openmm_1_1System.html>`_

    :param box_size: Length of individual sides of a simulation box
    :type box_size: `Quantity() <http://docs.openmm.org/development/api-python/generated/simtk.unit.quantity.Quantity.html>`_ ( float, simtk.unit )

    :returns:
        - system (`System() <https://simtk.org/api_docs/openmm/api4_1/python/classsimtk_1_1openmm_1_1openmm_1_1System.html>`_) - OpenMM system object

    """

    a, b, c = get_box_vectors(box_size)
    system.setDefaultPeriodicBoxVectors(a, b, c)
    return system


def get_temperature_list(min_temp, max_temp, num_replicas):
    """
        Given the parameters to define a temperature range as input, this function uses logarithmic spacing to generate a list of intermediate temperatures.

        :param min_temp: The minimum temperature in the temperature list.
        :type min_temp: `Quantity() <http://docs.openmm.org/development/api-python/generated/simtk.unit.quantity.Quantity.html>`_

        :param max_temp: The maximum temperature in the temperature list.
        :type max_temp: `Quantity() <http://docs.openmm.org/development/api-python/generated/simtk.unit.quantity.Quantity.html>`_

        :param num_replicas: The number of temperatures in the list.
        :type num_replicas: int

        :returns:
           - temperature_list ( 1D numpy array ( float * simtk.unit.temperature ) ) - List of temperatures

    """

    T_unit = min_temp.unit

    temperature_list = np.logspace(
        np.log10(min_temp.value_in_unit(T_unit)),
        np.log10(max_temp.value_in_unit(T_unit)),
        num=num_replicas
        )

    # Reassign units:
    temperature_list *= T_unit

    return temperature_list

