UPGRADES_FILE = "upgrades.txt"


def get_upgrades_data():
    """Читает данные улучшений из файла."""
    upgrades_data = {}
    try:
        with open(UPGRADES_FILE, "r", encoding="utf-8") as file:
            data = file.read().strip().split("\n")
            for entry in data:
                key, value = entry.split(":")
                upgrades_data[key] = int(value)
    except FileNotFoundError:
        upgrades_data = set_blank_upgrades()
    except ValueError:
        upgrades_data = set_blank_upgrades()
    return upgrades_data


def update_upgrades_data(upgrades_data):
    """Записывает данные улучшений в файл."""
    with open(UPGRADES_FILE, "w", encoding="utf-8") as file:
        for entry in upgrades_data:
            file.write(f"{entry}:{upgrades_data[entry]}\n")

def set_blank_upgrades():
    upgrades_data = {
        "scrap": 0,
        "healthrefillupgradelevel": 0,
        "scrapchanceupgradelevel": 0,
        "maxhpupgradelevel": 0,
        "xprequpgradelevel": 0
    }
    update_upgrades_data(upgrades_data)
    return upgrades_data
