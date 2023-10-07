# qualities are static enough to have it here as a constant
# effects are not, use effects.json file instead (valve adds new effects yearly)
QUALITIES = {
    "Normal": 0,
    "Genuine": 1,
    "rarity2": 2,
    "Vintage": 3,
    "rarity3": 4,
    "Unusual": 5,
    "Unique": 6,
    "Community": 7,
    "Valve": 8,
    "Self-Made": 9,
    "Customized": 10,
    "Strange": 11,
    "Completed": 12,
    "Haunted": 13,
    "Collector's": 14,
    "Decorated Weapon": 15,
}

KILLSTREAKS = {
    "Basic": 1,
    "Specialized": 2,
    "Professional": 3,
}

EXTERIORS = {
    "Factory New": 1,
    "Minimal Wear": 2,
    "Field-Tested": 3,
    "Well-Worn": 4,
    "Battle Scarred": 5,
}


class Item:
    def __init__(self, item: dict) -> None:
        self.item = item
        self.name = item["market_hash_name"]
        self.descriptions = item.get("descriptions", [])
        self.tags = item.get("tags", [])

    def is_tf2(self) -> bool:
        return self.item["appid"] == 440

    def has_name(self, name: str) -> bool:
        return self.name == name

    def has_description(self, description: str) -> bool:
        for i in self.descriptions:
            if i["value"] == description:
                return True

        return False

    def has_tag(self, tag: str, exact: bool = True) -> bool:
        for i in self.tags:
            item_tag = i["localized_tag_name"]

            if (item_tag == tag) or (tag in item_tag.lower() and not exact):
                return True

        return False

    def has_quality(self, quality: str) -> bool:
        return self.get_quality() == quality

    def has_strange_in_name(self) -> bool:
        return "Strange" in self.name

    def has_vintage_in_name(self) -> bool:
        return "Vintage" in self.name

    def has_killstreak(self, killstreak: str) -> bool:
        return self.get_killstreak() == killstreak

    def get_killstreak(self) -> str:
        if not self.is_killstreak():
            return ""

        parts = self.name.split(" ")
        killstreak_index = parts.index("Killstreak")
        killstreak = parts[killstreak_index - 1]

        if killstreak not in ["Specialized", "Professional"]:
            killstreak = "Basic"

        return killstreak

    def get_quality(self) -> str:
        for tag in self.tags:
            if tag["localized_category_name"] != "Quality":
                continue

            return tag["localized_tag_name"]

        return ""  # could not find

    def get_quality_id(self) -> int:
        return QUALITIES[self.get_quality()]

    def get_defindex(self) -> int:
        for action in self.item["actions"]:
            if action["name"] != "Item Wiki Page...":
                continue

            wiki_link = action["link"]
            start = wiki_link.index("id=")
            end = wiki_link.index("lang=")
            # defindex = re.findall("\\d+", wiki_link[start:end])[0]

            # extract defindex from wiki link
            defindex = wiki_link[start + 3 : end - 1]
            return int(defindex)

        return -1  # could not find

    def get_effect(self) -> str:
        if not self.is_unusual():
            return ""

        string = "★ Unusual Effect: "

        for i in self.descriptions:
            if string in i["value"]:
                return i["value"].replace(string, "")

        return ""  # could not find

    def get_killstreak_id(self) -> int:
        if not self.is_killstreak():
            return -1

        return KILLSTREAKS[self.get_killstreak()]

    def get_exterior(self) -> str:
        for tag in self.tags:
            if tag["category"] != "Exterior":
                continue

            return tag["localized_tag_name"]

        return ""  # could not find

    def get_exterior_id(self) -> int:
        exterior = self.get_exterior()

        if not exterior:
            return -1

        return EXTERIORS[exterior]

    def is_genuine(self) -> bool:
        return self.has_quality("Genuine")

    def is_vintage(self) -> bool:
        return self.has_quality("Vintage")

    def is_unusual(self) -> bool:
        return self.has_quality("Unusual")

    def is_unique(self) -> bool:
        return self.has_quality("Unique")

    def is_strange(self) -> bool:
        return self.has_quality("Strange")

    def is_haunted(self) -> bool:
        return self.has_quality("Haunted")

    def is_collectors(self) -> bool:
        return self.has_quality("Collector's")

    def is_decorated_weapon(self) -> bool:
        return self.has_tag("Decorated Weapon")

    def is_craftable(self) -> bool:
        return not self.has_description("( Not Usable in Crafting )")

    def is_uncraftable(self) -> bool:
        return not self.is_craftable()

    def is_non_craftable(self) -> bool:
        return self.is_uncraftable()

    def is_festivized(self) -> bool:
        return "Festivized" in self.name

    def is_halloween(self) -> bool:
        return self.has_description("Holiday Restriction: Halloween / Full Moon")

    def is_craft_weapon(self) -> bool:
        return (
            self.is_unique() and self.is_craftable() and self.has_tag("weapon", False)
        )

    def is_cosmetic(self) -> bool:
        return self.has_tag("Cosmetic")

    def is_craft_hat(self) -> bool:
        return (
            self.is_unique()
            and self.is_craftable()
            and self.is_cosmetic()
            and not self.is_halloween()
        )

    def is_unusual_cosmetic(self) -> bool:
        return self.is_unusual() and self.is_cosmetic()

    def is_australium(self) -> bool:
        return "Australium" in self.name

    def is_key(self) -> bool:
        return (
            self.is_craftable()
            and self.is_unique()
            and self.has_name("Mann Co. Supply Crate Key")
        )

    def is_mann_co_key(self) -> bool:
        return self.is_key()

    def is_killstreak(self) -> bool:
        return "Killstreak" in self.name

    def is_basic_killstreak(self) -> bool:
        return self.has_killstreak("Basic")

    def is_specialized_killstreak(self) -> bool:
        return self.has_killstreak("Specialized")

    def is_professional_killstreak(self) -> bool:
        return self.has_killstreak("Professional")
