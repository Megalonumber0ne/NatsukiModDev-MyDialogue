
default persistent.jn_natsuki_auto_outfit_change_enabled = True
default persistent.jn_outfit_list = {}
default persistent.jn_wearable_list = {}

init python in jn_outfits:
    import json
    import os
    import random
    import store
    import store.jn_affinity as jn_affinity
    import store.jn_utils as jn_utils

    # Tracks must be placed here for Natsuki to find them
    CUSTOM_OUTFITS_DIRECTORY = os.path.join(renpy.config.basedir, "custom_outfits/").replace("\\", "/")

    ALL_OUTFITS = {}
    ALL_WEARABLES = {}

    class JNWearable():
        """
        Describes a standalone object that Natsuki can wear.
        """
        def __init__(
            self,
            reference_name,
            display_name,
            unlocked,
        ):
            self.reference_name = reference_name
            self.display_name = display_name
            self.unlocked = unlocked

        @staticmethod
        def load_all():
            """
            Loads all persisted data for each wearable from the persistent.
            """
            global ALL_WEARABLES
            for wearable in ALL_WEARABLES.itervalues():
                wearable.__load()

        @staticmethod
        def save_all():
            """
            Saves all persistable data for each wearable to the persistent.
            """
            global ALL_WEARABLES
            for wearable in ALL_WEARABLES.itervalues():
                wearable.__save()

        def as_dict(self):
            """
            Exports a dict representation of this wearable.

            OUT:
                dictionary representation of the wearable object
            """
            return {
                "unlocked": self.unlocked
            }

        def __load(self):
            """
            Loads the persisted data for this wearable from the persistent.
            """
            if store.persistent.jn_wearable_list[self.reference_name]:
                self.unlocked = store.persistent.jn_wearable_list[self.reference_name]["unlocked"]

        def __save(self):
            """
            Saves the persistable data for this wearable to the persistent.
            """
            store.persistent.jn_wearable_list[self.reference_name] = self.as_dict()

    class JNHairstyle(JNWearable):
        """
        Describes a hairstyle for Natsuki; a wearable with additional functionality specific to hairstyles.
        """
        pass
    
    class JNEyewear(JNWearable):
        """
        Describes eyewear for Natsuki; a wearable with additional functionality specific to eyewear.
        """
        pass

    class JNAccessory(JNWearable):
        """
        Describes an accessory for Natsuki; a wearable with additional functionality specific to accessories.
        """
        pass

    class JNClothes(JNWearable):
        """
        Describes a set of clothes for Natsuki; a wearable with additional functionality specific to clothes.
        """
        pass

    class JNHeadgear(JNWearable):
        """
        Describes some headgear for Natsuki; a wearable with additional functionality specific to clothes.
        """
        pass

    class JNOutfit():
        """
        Describes a complete outfit for Natsuki to wear; including clothing, hairstyle, etc.
        At minimum, an outfit must consist of clothes and a hairstyle
        """
        def __init__(
            self,
            reference_name,
            display_name,
            unlocked,
            clothes,
            hairstyle,
            accessory=None,
            eyewear=None,
            headgear=None,
            necklace=None
        ):
            if clothes is None:
                raise TypeError("Outfit clothing cannot be None")
                return

            if hairstyle is None:
                raise TypeError("Outfit hairstyle cannot be None")
                return

            self.reference_name = reference_name
            self.display_name = display_name
            self.unlocked = unlocked
            self.clothes = clothes
            self.hairstyle = hairstyle
            self.accessory = accessory
            self.eyewear = eyewear
            self.headgear = headgear
            self.necklace = necklace

        @staticmethod
        def load_all():
            """
            Loads all persisted data for each outfit from the persistent.
            """
            global ALL_OUTFITS
            for outfit in ALL_OUTFITS.itervalues():
                outfit.__load()

        @staticmethod
        def save_all():
            """
            Saves all persistable data for each outfit to the persistent.
            """
            global ALL_OUTFITS
            for outfit in ALL_OUTFITS.itervalues():
                outfit.__save()

        @staticmethod
        def filter_outfits(
            outfit_list,
            not_reference_name=None,
            unlocked=None,
            has_accessory=None,
            has_eyewear=None,
            has_headgear=None,
            has_necklace=None
        ):
            """
            Returns a filtered list of outfits, given an outfit list and filter criteria.

            IN:
                - outfit_list - the list of JNOutfit outfits to query
                - not_reference_name - list of reference_names the outfit must not have 
                - unlocked - the boolean unlocked state to filter for
                - has_accessory - the boolean has_accessory state to filter for
                - has_eyewear - the boolean has_eyewear state to filter for
                - has_headgear - the boolean has_headgear state to filter for
                - has_necklace - the boolean has_necklace state to filter for

            OUT:
                - list of JNOutfit outfits matching the search criteria
            """
            return [
                _outfit
                for _outfit in outfit_list
                if _outfit.__filter_outfit(
                    unlocked,
                    not_reference_name,
                    has_accessory,
                    has_eyewear,
                    has_headgear,
                    has_necklace
                )
            ]
            pass

        def as_dict(self):
            """
            Exports a dict representation of this outfit.

            OUT:
                dictionary representation of the outfit object
            """
            return {
                "unlocked": self.unlocked
            }

        def __load(self):
            """
            Loads the persisted data for this outfit from the persistent.
            """
            if store.persistent.jn_outfit_list[self.reference_name]:
                self.unlocked = store.persistent.jn_outfit_list[self.reference_name]["unlocked"]

        def __save(self):
            """
            Saves the persistable data for this outfit to the persistent.
            """
            store.persistent.jn_outfit_list[self.reference_name] = self.as_dict()

        def __filter_outfit(
            self,
            unlocked=None,
            not_reference_name=None,
            has_accessory=None,
            has_eyewear=None,
            has_headgear=None,
            has_necklace=None
        ):
            """
            Returns True, if the outfit meets the filter criteria. Otherwise False.

            IN:
                - unlocked - the boolean unlocked state to filter for
                - not_reference_name - list of reference_names the outfit must not have 
                - has_accessory - the boolean has_accessory state to filter for
                - has_eyewear - the boolean has_eyewear state to filter for
                - has_headgear - the boolean has_headgear state to filter for
                - has_necklace - the boolean has_necklace state to filter for

            OUT:
                - True, if the outfit meets the filter criteria. Otherwise False
            """
            if unlocked is not None and self.unlocked != unlocked:
                return False

            if not_reference_name is not None and self.reference_name in not_reference_name:
                return False

            elif has_accessory is not None and bool(self.has_accessory) != has_accessory:
                return False

            elif has_eyewear is not None and bool(self.has_eyewear) != has_eyewear:
                return False

            elif has_headgear is not None and bool(self.has_headgear) != has_headgear:
                return False

            elif has_necklace is not None and bool(self.has_necklace) != has_necklace:
                return False

            return True

    def __register_outfit(outfit):
        """
        Registers a new outfit in the list of all outfits, allowing in-game access and persistency.
        If the outfit has no existing corresponding persistent entry, it is saved.

        IN:
            - outfit - the JNOutfit to register.
        """
        global ALL_OUTFITS
        if outfit.reference_name in ALL_OUTFITS:
            jn_utils.log("Cannot register outfit name: {0}, as an outfit with that name already exists.".format(outfit.reference_name))

        else:
            ALL_OUTFITS[outfit.reference_name] = outfit
            if outfit.reference_name not in store.persistent.jn_outfit_list:
                outfit.__save()

    def __register_wearable(wearable):
        """
        Registers a new wearable in the list of all wearables, allowing in-game access and persistency.
        """
        global ALL_WEARABLES
        if wearable.reference_name in ALL_WEARABLES:
            jn_utils.log("Cannot register wearable name: {0}, as a wearable with that name already exists.".format(outfit.reference_name))

        else:
            ALL_WEARABLES[wearable.reference_name] = wearable
            if wearable.reference_name not in store.persistent.jn_wearable_list:
                wearable.__save()

    def _load_wearable_from_json(json):
        """
        Attempts to load a wearable from a JSON object and register it.

        IN:
            - json - JSON object describing the wearable
        """
        # Sanity check the structure to make sure minimum attributes are specified
        if (
            "reference_name" not in json
            or "display_name" not in json
            or "unlocked" not in json
        ):
            jn_utils.log("Cannot load wearable as one or more key attributes do not exist.")
            return

        # Sanity check data types
        if (
            not isinstance(json["reference_name"], basestring)
            or not isinstance(json["display_name"], basestring)
            or not isinstance(json["unlocked"], bool)
        ):
            jn_utils.log("Cannot load wearable as one or more attributes are the wrong data type.")
            return

        else:
            wearable = JNWearable(
                reference_name=json["reference_name"],
                display_name=json["display_name"],
                unlocked=json["unlocked"]
            )

            __register_wearable(wearable)

    def _load_outfit_from_json(json):
        """
        Attempts to load an outfit from a JSON object and register it.

        IN:
            - json - JSON object describing the outfit
        """
        # Sanity check the structure to make sure minimum attributes are specified
        if (
            "reference_name" not in json
            or "display_name" not in json
            or "unlocked" not in json
            or "clothes" not in json
            or "hairstyle" not in json
        ):
            jn_utils.log("Cannot load outfit as one or more key attributes do not exist.")
            return

        # Sanity check data types
        if (
            not isinstance(json["reference_name"], basestring)
            or not isinstance(json["display_name"], basestring)
            or not isinstance(json["unlocked"], bool)
            or not isinstance(json["clothes"], basestring)
            or not isinstance(json["hairstyle"], basestring)
            or "eyewear" in json and not isinstance(json["eyewear"], basestring)
            or "headgear" in json and not isinstance(json["headgear"], basestring)
            or "necklace" in json and not isinstance(json["necklace"], basestring)
        ):
            jn_utils.log("Cannot load outfit as one or more attributes are the wrong data type.")
            return

        # Sanity check components to make sure they exist as registered wearables
        if not ALL_WEARABLES[json["clothes"]]:
            jn_utils.log("Cannot load outfit {0} as specified clothes do not exist.".format(json["reference_name"]))
            return

        elif not ALL_WEARABLES[json["hairstyle"]]:
            jn_utils.log("Cannot load outfit {0} as specified hairstyle does not exist.".format(json["reference_name"]))
            return

        elif "accessory" in json and not json["accessory"] in ALL_WEARABLES:
            jn_utils.log("Cannot load outfit {0} as specified accessory does not exist.".format(json["reference_name"]))
            return

        elif "eyewear" in json and not json["eyewear"] in ALL_WEARABLES:
            jn_utils.log("Cannot load outfit {0} as specified eyewear does not exist.".format(json["reference_name"]))
            return

        elif "headgear" in json and not json["headgear"] in ALL_WEARABLES:
            jn_utils.log("Cannot load outfit {0} as specified headgear does not exist.".format(json["reference_name"]))
            return

        elif "necklace" in json and not json["necklace"] in ALL_WEARABLES:
            jn_utils.log("Cannot load outfit {0} as specified necklace does not exist.".format(json["reference_name"]))
            return
        
        else:
            outfit = JNOutfit(
                reference_name=json["reference_name"],
                display_name=json["display_name"],
                unlocked=json["unlocked"],
                clothes=ALL_WEARABLES[json["clothes"]],
                hairstyle=ALL_WEARABLES[json["hairstyle"]],
                accessory=ALL_WEARABLES[json["accessory"]] if "accessory" in json else None,
                eyewear=ALL_WEARABLES[json["eyewear"]] if "eyewear" in json else None,
                headgear=ALL_WEARABLES[json["headgear"]] if "headgear" in json else None,
                necklace=ALL_WEARABLES[json["necklace"]]  if "necklace" in json else None
            )

            # Make sure locks aren't being bypassed with this outfit by locking the outfit if any components are locked
            if outfit.unlocked:
                if (
                    not outfit.clothes.unlocked
                    or not outfit.hairstyle.unlocked
                    or outfit.accessory and not outfit.accessory.unlocked
                    or outfit.eyewear and not outfit.eyewear.unlocked
                    or outfit.headgear and not outfit.headgear.unlocked
                    or outfit.necklace and not outfit.necklace.unlocked
                ):
                    jn_utils.log("Outfit {0} contains one or more locked components; locking outfit.".format(outfit.reference_name))
                    outfit.unlocked = False

            __register_outfit(outfit)

    def load_custom_wearables():
        """
        Loads the custom wearables from the game/wearables directory.
        """
        pass

    def load_custom_outfits():
        """
        Loads the custom wearables from the game/outfits directory.
        """
        if not jn_utils.get_directory_exists(CUSTOM_OUTFITS_DIRECTORY):
            jn_utils.log("Unable to load custom wearables as the directory does not exist, and was created.")
            return

        outfit_files = jn_utils.get_all_directory_files(CUSTOM_OUTFITS_DIRECTORY, [".json"])
        for file_name, file_path in outfit_files:
            try:
                with open(file_path) as outfit_data:
                    _load_outfit_from_json(json.loads(outfit_data.read()))

            except OSError:
                jn_utils.log("Unable to read file {0}; file could not be found.".format(file_name))

            except TypeError:
                jn_utils.log("Unable to read file {0}; corrupt file or invalid JSON.".format(file_name))

            except:
                raise

    # Default hairstyles
    __register_wearable(JNHairstyle(
        reference_name="jn_hair_bedhead",
        display_name="Bedhead",
        unlocked=True
    ))
    __register_wearable(JNHairstyle(
        reference_name="jn_hair_bun",
        display_name="Bun",
        unlocked=True
    ))
    __register_wearable(JNHairstyle(
        reference_name="jn_hair_twintails",
        display_name="Twintails",
        unlocked=True
    ))
    __register_wearable(JNHairstyle(
        reference_name="jn_hair_down",
        display_name="Down",
        unlocked=True
    ))
    __register_wearable(JNHairstyle(
        reference_name="jn_hair_messy_bun",
        display_name="Messy bun",
        unlocked=True
    ))
    __register_wearable(JNHairstyle(
        reference_name="jn_hair_ponytail",
        display_name="Ponytail",
        unlocked=True
    ))
    __register_wearable(JNHairstyle(
        reference_name="jn_hair_super_messy",
        display_name="Super messy",
        unlocked=True
    ))

    # Default eyewear
    __register_wearable(JNEyewear(
        reference_name="jn_eyewear_circles",
        display_name="Circle glasses",
        unlocked=True
    ))

    # Default accessories
    __register_wearable(JNAccessory(
        reference_name="jn_accessory_hairband_gray",
        display_name="Gray hairband",
        unlocked=True
    ))
    __register_wearable(JNAccessory(
        reference_name="jn_accessory_hairband_green",
        display_name="Green hairband",
        unlocked=True
    ))
    __register_wearable(JNAccessory(
        reference_name="jn_accessory_hairband_hot_pink",
        display_name="Hot pink hairband",
        unlocked=True
    ))
    __register_wearable(JNAccessory(
        reference_name="jn_accessory_hairband_purple",
        display_name="Purple hairband",
        unlocked=True
    ))
    __register_wearable(JNAccessory(
        reference_name="jn_accessory_hairband_red",
        display_name="Red hairband",
        unlocked=True
    ))
    __register_wearable(JNAccessory(
        reference_name="jn_accessory_hairband_white",
        display_name="White hairband",
        unlocked=True
    ))

    # Default clothes
    __register_wearable(JNClothes(
        reference_name="jn_clothes_school_uniform",
        display_name="School uniform",
        unlocked=True
    ))
    __register_wearable(JNClothes(
        reference_name="jn_clothes_casual",
        display_name="Casual clothes",
        unlocked=True
    ))
    __register_wearable(JNClothes(
        reference_name="jn_clothes_heart_sweater",
        display_name="Heart sweater",
        unlocked=False
    ))
    __register_wearable(JNClothes(
        reference_name="jn_clothes_low_cut_dress",
        display_name="Low-cut dress",
        unlocked=False
    ))
    __register_wearable(JNClothes(
        reference_name="jn_clothes_magical_girl",
        display_name="Magical girl cosplay",
        unlocked=False
    ))
    __register_wearable(JNClothes(
        reference_name="jn_clothes_red_rose_lace_dress",
        display_name="Valentine's dress",
        unlocked=False
    ))
    __register_wearable(JNClothes(
        reference_name="jn_clothes_rose_lace_dress",
        display_name="Rose lace dress",
        unlocked=False
    ))
    __register_wearable(JNClothes(
        reference_name="jn_clothes_sango_cosplay",
        display_name="Sango cosplay",
        unlocked=False
    ))
    __register_wearable(JNClothes(
        reference_name="jn_clothes_star_pajamas",
        display_name="Star pajamas",
        unlocked=False
    ))
    __register_wearable(JNClothes(
        reference_name="jn_clothes_trainer_cosplay",
        display_name="Trainer cosplay",
        unlocked=False
    ))

    # Default headgear
    __register_wearable(JNHeadgear(
        reference_name="jn_headgear_santa_hat",
        display_name="Santa hat",
        unlocked=False
    ))
    __register_wearable(JNHeadgear(
        reference_name="jn_headgear_trainer_hat",
        display_name="Trainer hat",
        unlocked=False
    ))

    # Default outfits
    __register_outfit(JNOutfit(
        reference_name="jn_school_uniform",
        display_name="School uniform",
        unlocked=True,
        clothes=ALL_WEARABLES["jn_clothes_school_uniform"],
        hairstyle=ALL_WEARABLES["jn_hair_twintails"],
        accessory=ALL_WEARABLES["jn_accessory_hairband_red"]
    ))
    __register_outfit(JNOutfit(
        reference_name="jn_casual_clothes",
        display_name="Casual clothes",
        unlocked=True,
        clothes=ALL_WEARABLES["jn_clothes_casual"],
        hairstyle=ALL_WEARABLES["jn_hair_bun"],
        accessory=ALL_WEARABLES["jn_accessory_hairband_white"]
    ))
    __register_outfit(JNOutfit(
        reference_name="jn_star_pajamas",
        display_name="Star pajamas",
        unlocked=True,
        clothes=ALL_WEARABLES["jn_clothes_star_pajamas"],
        hairstyle=ALL_WEARABLES["jn_hair_down"],
        accessory=ALL_WEARABLES["jn_accessory_hairband_hot_pink"]
    ))

label outfits_wear_outfit:
    n 1unmaj "Huh?{w=0.2} You want me to put on another outfit?"
    n 1fchbg "Sure thing!{w=0.5}{nw}"
    extend 1unmbg " What do you want me to wear?{w=1.5}{nw}"
    show natsuki idle at jn_left

    python:
        # Get unlocked outfits available for selection
        available_outfits = []
        for outfit in jn_outfits.ALL_OUTFITS.itervalues():
            if outfit.unlocked:
                available_outfits.append([outfit.display_name, outfit])

        available_outfits.sort(key = lambda option: option[0])
        available_outfits.insert(0, ("You pick!", "random"))

    call screen scrollable_choice_menu(available_outfits, ("Nevermind.", None))
    show natsuki at jn_center

    if isinstance(_return, jn_outfits.JNOutfit):
        # Wear the chosen outfit
        $ outfit_name = _return.display_name.lower()
        n 1unmaj "Oh?{w=0.2} You want me to wear my [outfit_name]?{w=0.5}{nw}"
        extend 1uchbg " Gotcha!"
        n 1nchsm "Just give me a second...{w=2}{nw}"

        play audio clothing_ruffle
        $ JN_NATSUKI.set_outfit(_return)
        with Fade(out_time=0.1, hold_time=1, in_time=0.5, color="#181212")

        n 1nchbg "Okaaay!"
        n 1tnmsm "How do I look,{w=0.1} [player]?{w=0.5}{nw}"
        extend 1flldvl " Ehehe."

    elif _return == "random":
        # Wear a random unlocked outfit
        n 1fchbg "You got it!{w=1.5}{nw}"
        extend 1fslss " Now what have we got here...{w=1.5}{nw}"
        n 1ncssr "...{w=1.5}{nw}"
        n 1fnmbg "Aha!{w=1.5}{nw}"
        extend 1fchbg " This'll do.{w=1.5}{nw}"
        extend 1uchsm " One second!"

        play audio clothing_ruffle
        $ JN_NATSUKI.set_outfit(
            random.choice(
                jn_outfits.JNOutfit.filter_outfits(
                    outfit_list=jn_outfits.ALL_OUTFITS.itervalues(),
                    unlocked=True,
                    not_reference_name=JN_NATSUKI._outfit_name)
            )
        )
        with Fade(out_time=0.1, hold_time=1, in_time=0.5, color="#181212")

        n 1nchbg "All done!"

    else:
        # Nevermind
        n 1nnmbo "Oh.{w=1.5}{nw}"
        extend 1nllaj " Well, that's fine."
        n 1nsrpol "I didn't wanna change anyway."

    return

label outfits_load_from_json:
    n 1fwlts "This isn't done yet."
    return

label outfits_suggest_outfit:
    n 1fwlts "This isn't done yet."
    return

label outfits_remove_outfit:
    n 1fwlts "This isn't done yet."
    return
