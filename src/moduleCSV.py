import moduleOS
import os

def create_csv_files(df, csv_directory, file_name, first_rows, sample_rows, last_rows, nrows_value):
    import moduleOS
    moduleOS.create_directory(csv_directory)

    if first_rows > 0:
        csv_file_path_explore = os.path.join(csv_directory, f'{file_name}_explore.csv')
        df.head(nrows_value).to_csv(csv_file_path_explore, index=False, encoding='UTF-8')
        print(f"Exporté en CSV : {csv_file_path_explore}")
    if first_rows > 0:
        csv_file_path_head = os.path.join(csv_directory, f'{file_name}_head.csv')
        df.head(first_rows).to_csv(csv_file_path_head, index=False, encoding='UTF-8')
        print(f"Exporté en CSV : {csv_file_path_head}")
    if sample_rows > 0:
        csv_file_path_sample = os.path.join(csv_directory, f'{file_name}_sample.csv')
        df.sample(frac=0.50).to_csv(csv_file_path_sample, index=False, encoding='UTF-8')
        print(f"Exporté en CSV : {csv_file_path_sample}")
    if sample_rows > 0:
        csv_file_path_big_sample = os.path.join(csv_directory, f'{file_name}_big_sample.csv')
        df.sample(frac=0.10).to_csv(csv_file_path_big_sample, index=False, encoding='UTF-8')
        print(f"Exporté en CSV : {csv_file_path_big_sample}")
    if last_rows > 0:
        csv_file_path_tail = os.path.join(csv_directory, f'{file_name}_tail.csv')
        df.tail(last_rows).to_csv(csv_file_path_tail, index=False, encoding='UTF-8')
        print(f"Exporté en CSV : {csv_file_path_tail}")
