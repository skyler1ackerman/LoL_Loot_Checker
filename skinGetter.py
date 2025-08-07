import psutil
import asyncio
import platform
from lcu_driver import Connector

# Fix for Windows (Python 3.8+)
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

connector = Connector()

async def save_json(data, filename):
    import json
    with open(f"data/{filename}", 'w') as f:
        json.dump(data, f, indent=4)

@connector.ready
async def connect(connection):
    total_skin = 0
    total_champion = 0

    summoner_resp = await connection.request('get', '/lol-summoner/v1/current-summoner')
    if summoner_resp.status == 200:
        summoner_data = await summoner_resp.json()
        summoner_id = str(summoner_data['summonerId'])

        # Champions
        champions_resp = await connection.request(
            'get', f'/lol-champions/v1/inventories/{summoner_id}/champions'
        )
        champion_data = await champions_resp.json()
        
        total_champion = sum(1 for champ in champion_data if champ['ownership']['owned'])

        # Skins
        skins_resp = await connection.request(
            'get', f'/lol-champions/v1/inventories/{summoner_id}/skins-minimal'
        )
        skins_data = await skins_resp.json()
        total_skin = sum(1 for skin in skins_data if skin['ownership']['owned'])

        print(f"✅ Total Champions: {total_champion}")
        print(f"✅ Total Skins: {total_skin}")

        # Loot
        loot_resp = await connection.request(
            'get', f'/lol-loot/v1/player-loot'
        )
        loot_data = await loot_resp.json()

        # Save to JSON files
        await save_json(champion_data, 'champions.json')
        await save_json(skins_data, 'skins.json')
        await save_json(loot_data, 'loot.json')
        print("✅ Data saved to champions.json and skins.json")


def process_exists():
    for p in psutil.process_iter(attrs=['name']):
        try:
            if p.info['name'] == 'LeagueClient.exe':
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


if __name__ == '__main__':
    if process_exists():
        connector.start()
    else:
        print("⚠️ League Client not running!")
