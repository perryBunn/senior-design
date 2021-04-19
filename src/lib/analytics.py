def stats(pallets, container):
    print("================================")
    print("Packing Eff: ")
    index = 1
    for pallet in pallets:
        volume = 0
        print("--------------------------------")
        print(f"Pallet {index}")
        for item in pallet:
            if item.item == None:
                continue
            volume = volume + item.item.get_volume()

        print((volume/container.volume)*100, "occupied/available")
        index+=1

    print("================================")

