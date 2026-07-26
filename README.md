<p align="center">
<img src="assets/ap-ootmm.png" alt="[ap-ootmm logo]" width="25%"/>
</p>

# AP-OOTMM

An Archipelago implementation of OOTMM.

Configuration files are generated from OOTMM, then processed at runtime for the Archipelago apworld.  
Once the game is generated; [Unknown how yet] the OOTMM rom is patched, and it is set up for the AP multiworld.  

## Terms you should know to make it less confusing

- **OOTMM** - The OOTMM combo rando developed by the OOTMM Dev team.
  - [OOTMM Github Link](https://github.com/OoTMM/OoTMM)
- **AP-OOTMM / OOTxMM** - The Archipelago implementation of OOTMM
  - [AP-OOTMM Github Link](https://github.com/Quasky/AP-OOTMM)  
  - AP-OOTMM is the '*public*' name of the project (everything but code)
  - OOTxMM is the internal code-name of the project (code only)

# Development
Right now:  
- Regions and Locations are generated and processed at runtime.  
- Items are static.
- Logic is unfinished.
- Options are unfinished.

Step 1 is just getting a viable product developed where the multiworld can generate and be playable as a v0.1.  

### GenerateMetadata.py
- `GenerateMetadata.py` should be the central source/process for converting OOTMM logic/data into formats used by AP-OOTMM.
    - Any data that must be compiled from OOTMM to AP-OOTMM should be processed through this script as the 'single source of conversion'  
    - All data will be output as yaml (as that's native to OOTMM and more human-readable), then converted into JSON for use by AP-OOTMM 
    - These files are collectively called the AP world's `metadata`

- To generate/update the json/yamls for the AP world:  
    1) Download the source of OOTMM into `/raw/ootmm`
    2) `cd` into the `raw` directory.
      - Make sure you're in `raw`! The script is pretty picky about the locations of these files and their output.
    4) Running `GenerateMetadata.py` will generate the files that are processed by the APworld

### Items
Items are "staticly" defined in `items.py` in like-item-lists.  
AP's World API require items to have a unique associated ID. To make sure there is room to insert new items if need be. Each item will have a one digit 'game identifier' (`GID`), a one digit catagory 'catagory identifier' (`CID`), and a three digit 'item id' (`IID`).  
  > As an example; OOT_FISH is `11069`  
  > `1` - OOT  
  > `1` - Item  
  > `069` - IID for the fish  
  > Thus the final AP ItemID would be `11069`

  > Another example; MM_SOUL_NPC_DAMPE is `22520`  
  > `2` - MM  
  > `2` - Soul  
  > `520` - IID for Dampe's Soul  
  > Thus the final AP ItemID would be `22520`

|Game|GID|
|-----|-----|
|OOT|1|
|MM|2|
|Shared|3|

|Catagory|CID|
|-----|-----|
|Item|1|
|Soul|2|

### These lists are currently broken up as:
|Catagory|Name|GIDs|CIDs|Finished ID Ranges|
|-----|-----|-----|-----|-----|
|Items|OOT Items              |1|1|11001 - 11999|
|Items|MM Items               |2|1|21001 - 21999|
|Items|Shared Items           |3|1|31001 - 31999|
|Souls|OOT Enemy Soul List    |1|2|12001 - 12499|
|Souls|OOT NPC Soul List      |1|2|12501 - 12999|
|Souls|MM Enemy Soul List     |2|2|22001 - 22499|
|Souls|MM NPC Soul List       |2|2|22501 - 22999|
|Souls|Shared Enemy Soul List |3|2|32001 - 32499|
|Souls|Shared NPC Soul List   |3|2|32501 - 32999|
- Possible TODO item lists:
  - Silver ruppee list (?)
  - Songs (?)

And are combined into a single itemlist upon generation depending on options.
> At this moment, there are no options, so all into one big list it is! :)

You'll notice that some ID Ranges are split, that's to further devide the pool without requiring a new catagory. This is useful where items are still "similar" but you don't really want them mixed together, and don't want them in seperate catagories.

## TODO
|Task|Static?|Dynamic?|Done?|
|-----|-----|-----|-----|
|AP - World|x|x||
|AP - Items|x|||
|AP - Locations|x|x||
|AP - Regions|x|x||
|AP - Rules||||
|AP - Options||||
|Game - Generator/Patch||||
|AP - Setup page|x|x||
|AP - Game page|x|x||

- Misc Tasks:
  - Get license permissions for OOTMM properly (ask them how they'd like to deal with it really)
  - Make a proper logo for github/discord.


# Special Thanks
Thank you to [Fletch64](https://github.com/Fletch64) and [alphaONE2](https://github.com/alphaONE2) for their work on the first pass at an OOTMM AP world/generator.  

Thank you to the [OOTMM Dev Team](https://github.com/OoTMM/OoTMM) for creating OOTMM in the first place.

Thank you to the Archipelago contribution community for continuing to make something awesome.  