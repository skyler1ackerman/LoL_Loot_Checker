# Current Function
Currently, the 

## How to use
1. Run the following
```
pip install lcu-driver
pip install psutil
pip install asyncio
pip install pillow
pip install tk
```
2. Open the league of legends client
3. Run the skinGetter.py file via `python skinGetter.py`. This will get all of the JSON files you need and store them in the data directory.
4. Run the skinChecker.py file with `python skinChecker.py` to generate a csv file of all of the skins you have for champions you do not own. 
The league client does not need to be open for this step, since all the data is already stored in the JSON files.
If you want to refresh the data, rerun the skinGetter.py file.
5. Alternatively, just run `python skinUI.py` instead of step 4 to get a basic UI with all the information.
Note that LUX is a placeholder for all the icons I don't have, because the champions are too new.

That's pretty much it, feel free to mess around with it. If you want any features, DM me or open an issue. 