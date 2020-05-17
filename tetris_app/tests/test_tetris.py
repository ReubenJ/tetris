#!/usr/bin/env python3
from app import join_matrices


def test_join_matrixes():
    mat1 = [[0, 0, 0],
            [0, 0, 0]]
    mat2 = mat1[:]
    mat2_off = 0
    assert join_matrices(mat1, mat2, mat2_off) == mat1