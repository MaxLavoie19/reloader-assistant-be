from reload.model.PrimerModel import PrimerModel


def primer_to_dict_mapper(primer: PrimerModel):
    primer_dict = {
        'id': primer.id,
        'name': primer.name,
        'size': primer.size,
        'manufacturer': primer.manufacturer.__dict__.copy(),
    }

    if primer.barcode is not None:
        primer_dict['barcode'] = primer.barcode

    return primer_dict
