import pandas as pd

class DataFrameIO:

    def __init__(self, column_names, data_upload_download_path):
        self.column_names = column_names
        self.DATA_UPLOAD_DOWNLOAD_PATH = data_upload_download_path\
        self.df = self.load_dataframe()

    def create_dataframe(self, agencies):
        df = pd.DataFrame(agencies, self.column_names)
        return df

    def save_dataframe(self, df):
        df.to_csv(self.DATA_UPLOAD_DOWNLOAD_PATH, index=False)


    def load_dataframe(self):
        try:
            df = pd.read_csv(self.DATA_UPLOAD_DOWNLOAD_PATH)
        except:
            print("No file exists. Creating blank dataframe.")
            agencies = []
            df = self.create_dataframe(agencies)

        return df


    def dataframe_to_list(self, df):
        agencies = []

        columns = list(df)

        for index, row in df.iterrows():
            entry = []

            for column in columns:
                entry.append(row[column])

            agencies.append(entry)

        return agencies


    def get_number_completed(self):
        number_completed = len(self.df['Zipcode'].unique())
        print("Number completed: " + str(number_completed))
        return number_completed



