from reload.model.ChamberingModel import ChamberingModel


def chambering_to_dict_mapper(chambering: ChamberingModel):
    chambering_dict = {
        'id': chambering.id,
        'name': chambering.name,
        'caliber': chambering.caliber.__dict__.copy(),
    }
    return chambering_dict
