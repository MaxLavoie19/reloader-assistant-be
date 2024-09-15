from typing import Dict

from server_io.service.SerializerService.JsonSerializerService import JsonSerializerService


class ComponentRepository:
    def __init__(self, serializer_service: JsonSerializerService):
        self.serializer_service = serializer_service

    def get_component_list(self, component_type_name: str):
        components = self.serializer_service.load_public_file(component_type_name)
        return components

    def get_or_create_component(self, component_type_name: str, component_dict: Dict, id_key='id'):
        components = self.get_component_list(component_type_name)
        filtered_components = list(filter(lambda x: x[id_key] == component_dict[id_key], components))
        if len(filtered_components):
            return filtered_components[0]
        components.append(component_dict)
        self.serializer_service.dump_public_file(component_type_name, components)
        return component_dict
