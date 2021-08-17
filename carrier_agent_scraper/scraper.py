from carrier_agent_scraper import carriers

# carrier_class = getattr(carriers, 'Dairyland')()
# carrier_class.test()


def scrape_and_parse(carrier, zipcode):
    carrier_class_name = format_to_class_name(carrier)
    carrier_class = getattr(carriers, carrier_class_name)()
    source_code = carrier_class.get_source_code(zipcode)
    # source_code = globals()[scraper_function_name](zipcode) # Call method of same module by string name.
    data = carrier_class.parse_data(source_code, zipcode)
    return data


def format_to_class_name(carrier_name):
    words = carrier_name.split('_')

    for i, word in enumerate(words):
        words[i] = word.capitalize()

    class_name = "".join(words)

    return class_name

