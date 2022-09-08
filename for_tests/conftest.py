"""
Pytest fixtures.
"""
import pytest

@pytest.fixture
def _function1():
  print('ici _function1')
  return 3


@pytest.fixture  
def _function2(i_val: int = 10) -> int:
  print('_function2')
  return i_val+2

