from dataclasses import dataclass

from reload.model.RecipeModel import RecipeModel


@dataclass
class BatchModel:
    batch_id: str
    recipe: RecipeModel
