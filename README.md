# Current Function
Currently, the 

# How to use
1. Create a "data" folder in the base directory
2. Run the following
```
pip install lcu-driver
pip install psutil
pip install asyncio
```
3. Open the league of legends client
4. Run the skinGetter.py file via `python skinGetter.py`. This will get all of the JSON files you need and store them in the data directory.
5. Run the skinChecker.py file to generate a csv file of all of the skins you have for champions you do not own. 
The league client does not need to be open for this step, since all the data is already stored in the JSON files.
If you want to refresh the data, rerun the skinGetter.py file.

That's pretty much it, feel free to mess around with it. If you want any features, DM me or open an issue. 