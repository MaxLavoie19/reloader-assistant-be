from plistlib import Dict

from server_io.service.SerializerService.JsonSerializerService import JsonSerializerService


class ComponentRepository:
    def __init__(self, json_serializer_service: JsonSerializerService):
        self.json_serializer_service = json_serializer_service

    def get_component_list(self, component_type_name: str):
        components = self.json_serializer_service.load_public_file(component_type_name)
        return components

    def get_or_create_component(self, component_type_name: str, component_dict: Dict):
        components = self.get_component_list(component_type_name)
        filtered_components = list(filter(lambda x: x["id"] == component_dict["id"], components))
        if len(filtered_components):
            return filtered_components[0]
        components.append(component_dict)
        self.json_serializer_service.dump_public_file(component_type_name, components)
        return component_dict
