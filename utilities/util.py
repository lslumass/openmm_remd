from openmm import unit


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
