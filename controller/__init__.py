import os
import glob

controller_path = os.path.dirname(__file__)
module_names = [os.path.splitext(os.path.basename(file))[0] for file in glob.glob(os.path.join(controller_path, '*.py'))]
__all__ = module_names
