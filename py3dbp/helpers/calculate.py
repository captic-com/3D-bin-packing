from py3dbp import Packer, Bin, Item
import random


def has_item_on_top(item, all_items):
    x1, y1, z1 = item.position
    w1, h1, d1 = item.width, item.height, item.depth
    top_z = z1 + d1  # top surface in Z

    x1_end = x1 + w1
    y1_end = y1 + h1

    for other in all_items:
        if other == item:
            continue
        x2, y2, z2 = other.position
        w2, h2, d2 = other.width, other.height, other.depth

        # Check if other item sits exactly above this one's top face
        if z2 == top_z:
            x2_end = x2 + w2
            y2_end = y2 + h2

            # Check XY overlap
            if not (x1_end <= x2 or x2_end <= x1 or y1_end <= y2 or y2_end <= y1):
                return True  # there's overlap
    return False


def get_top_items(all_items):

    items_without_top = []
    items_without_top_idx = []

    for i, item in enumerate(all_items):
        if not has_item_on_top(item, all_items):
            items_without_top.append(item)
            items_without_top_idx.append(i)
    return items_without_top, items_without_top_idx


def optimize_rotation_around_z(width, height, depth):

    # init packing function
    packer = Packer()

    # Pallet
    # Unit cm/kg
    box = Bin(
        partno="example0", WHD=(120, 80, 160), max_weight=500, corner=0, put_type=0
    )
    packer.addBin(box)

    item = Item(
        partno="test",
        name="test",
        typeof="cube",
        WHD=(width, height, depth),
        weight=10,
        level=1,
        loadbear=100,
        updown=True,
        color="#{:06x}".format(random.randint(0, 0xFFFFFF)),
    )

    for i in range(int(box.getVolume() / item.getVolume()) + 1):

        packer.addItem(item)

    # Pack
    packer.pack(
        bigger_first=True,
        distribute_items=False,
        fix_point=True,  # Try switching fix_point=True/False to compare the results
        check_stable=True,
        support_surface_ratio=0.75,
        number_of_decimals=0,
    )

    # Calculate score
    normal_score = (
        float(
            sum([x.getVolume() for x in packer.bins[0].items])
            / packer.bins[0].getVolume()
        )
        * 100
    )

    # init packing function
    packer = Packer()

    # Pallet
    # Unit cm/kg
    box = Bin(
        partno="example0", WHD=(120, 80, 160), max_weight=500, corner=0, put_type=0
    )
    packer.addBin(box)

    item = Item(
        partno="test",
        name="test",
        typeof="cube",
        WHD=(height, width, depth),
        weight=10,
        level=1,
        loadbear=100,
        updown=True,
        color="#{:06x}".format(random.randint(0, 0xFFFFFF)),
    )

    for i in range(int(box.getVolume() / item.getVolume()) + 1):

        packer.addItem(item)

    # Pack
    packer.pack(
        bigger_first=True,
        distribute_items=False,
        fix_point=True,  # Try switching fix_point=True/False to compare the results
        check_stable=True,
        support_surface_ratio=0.6,
        number_of_decimals=0,
    )

    # Calculate score
    rotated_score = (
        float(
            sum([x.getVolume() for x in packer.bins[0].items])
            / packer.bins[0].getVolume()
        )
        * 100
    )

    if normal_score > rotated_score:
        # print(f"normal score wins with: {normal_score} - ({width}, {height}, {depth})")
        return width, height, depth
    else:
        # print(f"rotated score wins with: {rotated_score} - ({height}, {width}, {depth})")
        return height, width, depth
