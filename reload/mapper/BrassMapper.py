from reload.mapper.ChamberingMapper import chambering_to_dict_mapper
from reload.model.BrassModel import BrassModel


def brass_to_dict_mapper(brass: BrassModel):
    brass_dict = {
        'id': brass.id,
        'chambering': chambering_to_dict_mapper(brass.chambering),
        'manufacturer': brass.manufacturer.__dict__,
    }
    if brass.barcode is not None:
        brass_dict['barcode'] = brass.barcode
    return brass_dict
