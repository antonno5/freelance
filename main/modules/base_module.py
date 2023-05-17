from abc import ABC, abstractmethod
from typing import Dict, List, Type

from django.http import HttpRequest


class Submodule:
    def __init__(self, submodule_class: Type['BaseModule'], args: List = None, kwargs: Dict = None,
                 enable_context_enclosure: bool = True):
        if args is None:
            args = list()
        if kwargs is None:
            kwargs = dict()
        self.submodule_class = submodule_class
        self.args = args
        self.kwargs = kwargs
        self.enable_context_enclosure = enable_context_enclosure


class BaseModule:
    required_submodules: Dict[str, Submodule] = {}

    def __init__(self, request: HttpRequest, order_id: int = 0, application_id: int = 0):
        self.request = request
        self.order_id = order_id
        self.application_id = application_id
        self.context: Dict = {}
        self.required_submodules_objects: Dict[str, BaseModule] = {}

        for submodule_name, submodule in self.required_submodules.items():
            submodule_object = submodule.submodule_class(self.request, *submodule.args, **submodule.kwargs)
            self.required_submodules_objects[submodule_name] = submodule_object
            submodule_object.process()

            if submodule.enable_context_enclosure:
                self.context.update(list(map(lambda tup: ('{}_{}'.format(submodule_name, tup[0]), tup[1]),
                                             submodule_object.context.items())))
            else:
                self.context.update(submodule_object.context.items())

    def process_logic(self):
        pass

    def process_context(self):
        pass

    def process(self):
        logic_return = self.process_logic()
        if logic_return is not None:
            return logic_return
        self.process_context()


class BaseViewModuleExtent(ABC):
    @abstractmethod
    def process_view(self):
        pass

    def view(self, request, *args, **kwargs):
        process_return = self.process()
        if process_return is not None:
            return process_return
        return self.process_view()

    @classmethod
    def as_view(cls, *init_args, **init_kwargs):
        def view(request, *args, **kwargs):
            module = cls(request, *args, **kwargs)
            return module.view(request, *args, **kwargs)

        return view


class BaseViewModule(BaseModule, BaseViewModuleExtent):
    @abstractmethod
    def process_view(self):
        pass
