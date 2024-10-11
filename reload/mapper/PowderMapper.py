from reload.model.PowderModel import PowderModel


def powder_to_dict_mapper(powder: PowderModel):
    powder_dict = {
        'id': powder.id,
        'name': powder.name,
        'manufacturer': powder.manufacturer.__dict__.copy(),
    }

    if powder.barcode is not None:
        powder_dict['barcode'] = powder.barcode

    return powder_dict
