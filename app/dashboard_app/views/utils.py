def sort_assetlist_by(assets, sort_by_attribute, direction):
    """
    Simply handles the sorting of a 'Asset'-List.

    Keyword arguments:
        sort_by_attribute: The attribute to be sorted by.
        direction:         The sorting direction - Ascending 'asc' or Descending 'desc'.
    """

    if direction == 'asc':
        return sorted(assets, key=lambda item: item[sort_by_attribute])
    elif direction == 'desc':
        return sorted(assets, key=lambda item: item[sort_by_attribute])[::-1]
    else:
        return assets