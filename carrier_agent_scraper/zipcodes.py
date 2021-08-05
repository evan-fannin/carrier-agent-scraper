import zipcodes as zp


def get_zipcodes_in_state(state):
    state_zips = zp.filter_by(state=state)  # list of dictionaries, one for each zip code
    zips = []
    for z in state_zips:
        zipcode = z['zip_code']
        zips.append(zipcode)
    return zips

