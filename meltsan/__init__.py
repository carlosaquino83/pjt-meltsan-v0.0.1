#No space after comments (Meltsan convention)

import os
import inspect
import keyword
import importlib

#Absolute path of meltsan package
MLTS_ROOT_PATH = os.path.dirname(__file__)

#Internal registries
MLTS_MODULES = {}
MLTS_CLASSES = {}

#Used for validations
__mlts_file_registry = {}
__mlts_class_registry = {}

#First pass
#Validate filenames

#Walking Meltsan root path
for root, dirs, files in os.walk(MLTS_ROOT_PATH):
    #On each files found
    for file_name in files:
        #If is not a python file
        if not file_name.endswith(".py"):
            continue
        #Or an init file
        if file_name == "__init__.py":
            continue
        #Getting the name normalized
        base_name = file_name[:-3]
        normalized_name = base_name.lower()
        #Python reserved words check
        if keyword.iskeyword(base_name):
            #Ups, reserved word found
            raise Exception(
                f"Reserved Python keyword detected:\n"
                f"{file_name}\n"
                f"Location:\n"
                f"{os.path.join(root, file_name)}"
            )
        #Duplicate filenames?
        if normalized_name in __mlts_file_registry:
            #Ups, duplicated class found
            raise Exception(
                f"Duplicate filename detected:\n"
                f"{file_name}\n\n"
                f"First location:\n"
                f"{__mlts_file_registry[normalized_name]}\n\n"
                f"Second location:\n"
                f"{os.path.join(root, file_name)}"
            )
        #Ok, valid normalized name to local register container var
        __mlts_file_registry[normalized_name] = os.path.join(
            root,
            file_name
        )

#Second pass
#Import every module and register classes

#Walking Meltsan root path, again
for root, dirs, files in os.walk(MLTS_ROOT_PATH):
    #On each files found
    for file_name in files:
        #If is not a python file
        if not file_name.endswith(".py"):
            continue
        #Or an init file
        if file_name == "__init__.py":
            continue
        #Getting Absolute file
        absolute_file = os.path.join(
            root,
            file_name
        )
        #Getting Relative file
        relative_file = os.path.relpath(
            absolute_file,
            MLTS_ROOT_PATH
        )
        #Getting Module name
        module_name = relative_file[:-3].replace(
            os.sep,
            "."
        )
        #Getting Full module name
        full_module_name = f"{__name__}.{module_name}"
        #Import library
        module = importlib.import_module(full_module_name)
        #To append into Meltsan modules
        MLTS_MODULES[full_module_name] = module
        #And walking all inspected module
        for class_name, obj in inspect.getmembers(module):
            #Not a class obj
            if not inspect.isclass(obj):
                continue
            #Only classes defined inside the module
            if obj.__module__ != module.__name__:
                continue
            #Normalizing the class name
            normalized_class_name = class_name.lower()
            #Duplicated class?
            if normalized_class_name in __mlts_class_registry:
                #Adding actual class to previous collection
                previous_module = __mlts_class_registry[
                    normalized_class_name
                ]
                #Ups, this class is duplicated
                raise Exception(
                    f"Duplicate class detected:\n"
                    f"{class_name}\n\n"
                    f"First module:\n"
                    f"{previous_module}\n\n"
                    f"Second module:\n"
                    f"{module.__name__}"
                )
            #Valid class register
            __mlts_class_registry[normalized_class_name] = module.__name__
            #Valid object to add in the collection
            MLTS_CLASSES[class_name] = obj
            #Expose globally
            globals()[class_name] = obj

#Public API
__all__ = sorted(MLTS_CLASSES.keys())
