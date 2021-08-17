import pandas as pd


def get_column_names(agencies):
    if len(agencies) == 0:
        column_names = ['Zipcode']

    elif len(agencies[0]) == 4:  # Check length of entry to determine whether or not to include email
        column_names = ["Name", "Address", "Number", "Zipcode"]

    elif len(agencies[0]) == 5:
        column_names = ["Name", "Address", "Number", "Email", "Zipcode"]

    else:
        raise ValueError('Problem with creating column names.')

    return column_names


def create_dataframe(agencies):
    column_names = get_column_names(agencies)
    df = pd.DataFrame(agencies, columns=column_names)
    return df


def save_dataframe(df, data_path):
    df.to_csv(data_path, index=False)


def load_dataframe(data_path):
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print("No file exists. Creating blank dataframe.")
        agencies = []
        df = create_dataframe(agencies)

    return df


def dataframe_to_list(df):
    agencies = []

    columns = list(df)

    for index, row in df.iterrows():
        entry = []

        for column in columns:
            entry.append(row[column])

        agencies.append(entry)

    return agencies


def get_number_completed(df):
    number_completed = len(df['Zipcode'].unique())
    print("Number completed: " + str(number_completed))
    return number_completed



