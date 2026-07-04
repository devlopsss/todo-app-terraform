import sys
import os

# Clean up any cached lambda_function modules before each test
def pytest_runtest_setup(item):
    mods_to_remove = [key for key in sys.modules.keys() 
                      if 'lambda_function' in key]
    for mod in mods_to_remove:
        del sys.modules[mod]
