from reload.model.BulletModel import BulletModel


def bullet_to_dict_mapper(bullet: BulletModel):
    bullet_dict = {
        'id': bullet.id,
        'caliber': bullet.caliber.__dict__,
        'manufacturer': bullet.manufacturer.__dict__,
        'model': bullet.model,
        'weight_in_grains': bullet.weight_in_grains,
        'g1_ballistic_coefficient': bullet.g1_ballistic_coefficient,
        'g7_ballistic_coefficient': bullet.g7_ballistic_coefficient,
        'sectional_density': bullet.sectional_density,
    }
    if bullet.barcode is not None:
        bullet_dict['barcode'] = bullet.barcode
    return bullet_dict
