import moduleOS
import os

def create_csv_files(df, csv_directory, file_name, first_rows, sample_rows, last_rows, nrows_value):
    import moduleOS
    moduleOS.create_directory(csv_directory)

    if first_rows > 0:
        df.head(nrows_value).to_csv(os.path.join(csv_directory, f'{file_name}_explore.csv'), index=False, encoding='UTF-8')
    if first_rows > 0:
        df.head(first_rows).to_csv(os.path.join(csv_directory, f'{file_name}_head.csv'), index=False, encoding='UTF-8')
    if sample_rows > 0:
        df.sample(sample_rows).to_csv(os.path.join(csv_directory, f'{file_name}_sample.csv'), index=False, encoding='UTF-8')
    if sample_rows > 0:
        df.sample(nrows_value).to_csv(os.path.join(csv_directory, f'{file_name}_big_sample.csv'), index=False, encoding='UTF-8')
    if last_rows > 0:
        df.tail(last_rows).to_csv(os.path.join(csv_directory, f'{file_name}_tail.csv'), index=False, encoding='UTF-8')
