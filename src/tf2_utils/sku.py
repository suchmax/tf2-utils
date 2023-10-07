from .item import Item

from .schema import EFFECTS

from tf2_sku import to_sku


def get_sku_properties(item_description: dict) -> dict:
    item = Item(item_description)

    quality = item.get_quality_id()
    effect = item.get_effect()

    # TODO: add rest
    sku_properties = {
        "defindex": item.get_defindex(),
        "quality": quality,
        "australium": item.is_australium(),
        "craftable": item.is_craftable(),
        "wear": item.get_exterior_id(),
        "killstreak_tier": item.get_killstreak_id(),
        "festivized": item.is_festivized(),
        #
        # "effect": "u{}",
        # "australium": "australium",
        # "craftable": "uncraftable",
        # "wear": "w{}",
        # "skin": "pk{}",
        # "strange": "strange",
        # "killstreak_tier": "kt-{}",
        # "target_defindex": "td-{}",
        # "festivized": "festive",
        # "craft_number": "n{}",
        # "crate_number": "c{}",
        # "output_defindex": "od-{}",
        # "output_quality": "oq-{}",
    }

    if effect:
        sku_properties["effect"] = EFFECTS[effect]

    # e.g. strange unusual
    if quality != 11:
        sku_properties["strange"] = item.has_strange_in_name()

    return sku_properties


def get_sku(item: dict) -> str:
    properties = get_sku_properties(item)
    return to_sku(properties)
