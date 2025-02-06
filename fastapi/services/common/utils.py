import fnmatch
import importlib
import os
from typing import Optional


def autodiscover(package: str, pattern: str, max_depth: Optional[int] = None):
    package_spec = importlib.util.find_spec(package)
    if not package_spec or not package_spec.submodule_search_locations:
        raise ImportError(f"Package '{package}' not found or cannot be searched.")

    package_path = package_spec.submodule_search_locations[0]
    base_depth = package_path.count(os.sep)

    for root, _, files in os.walk(package_path):
        current_depth = root.count(os.sep) - base_depth

        if max_depth is not None and current_depth > max_depth:
            continue

        for filename in fnmatch.filter(files, pattern):
            module_name = os.path.splitext(
                os.path.relpath(os.path.join(root, filename), package_path)
            )[0]
            module_name = module_name.replace(os.sep, ".")

            try:
                importlib.import_module(f"{package}.{module_name}")
            except ModuleNotFoundError as e:
                print(f"Warning: Could not import module {package}.{module_name}: {e}")
