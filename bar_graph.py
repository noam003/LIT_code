import pandas as pd
import numpy as np
import argparse
import os
import matplotlib.pyplot as plt

def graph(input_dir, filename, threshold):
    '''
        Computes the percentage of processed W.A.R. values >= threshold 
        against the original W.A.R. values.

        Parameters:
        input_dir (str): The directory where the input Excel file is located.
        filename (str): The name of the input Excel file.
        threshold (int): The threshold value for processed W.A.R. percentage.

        Returns:
        List[float]: A list of percentage values.
    '''
    if filename.startswith('~$'):
        print(f"Skipping temporary file: {filename}")
        return []
    
    input_file_path = os.path.join(input_dir, filename)
    df = pd.read_excel(input_file_path)

    # Drop unwanted column
    # df = df.drop(columns=['1'])
    
    war_mixed_list = []
    war_proc_list = []

    for index, row in df.iterrows():
        if index < len(df) - 1:  # Skip appending the last row
            war_mixed_list.append(row['Mixed W.A.R. (%)'])
            war_proc_list.append(row['Processed W.A.R. (%)'])

    # print(len(war_mixed_list))
    # for key, value in zip(war_mixed_list, war_proc_list):
    #     print(f"{key}: {value}")

    results = []
    expand_res = []

    for i in range(90, 9, -10):
        keys_over_i = [war_proc for war_mixed, war_proc in zip(war_mixed_list, war_proc_list) if (war_mixed >= i and war_mixed < (i+10)) ]
        count_ge_threshold = np.sum(np.array(keys_over_i) >= threshold)
        percentage_ge_threshold = (count_ge_threshold / len(keys_over_i)) * 100 
        results.append(percentage_ge_threshold)
        expand_res.append((count_ge_threshold, len(keys_over_i)))

    return results, expand_res

def read_excel_without_last_row(file_path):
    df = pd.read_excel(file_path)
    return df.iloc[:-1]  # Exclude the last row

def main():
    """
    Perform data processing on Excel files located in a specified directory (`input_dir`),
    generate a stacked bar graph showing the percentage of processed W.A.R. values for 
    different thresholds, and save an intermediate concatenated Excel file.

    Steps:
    1. Parses command-line arguments to get the directory (`input_dir`) containing Excel files.
    2. Reads each Excel file, excluding the last row, and concatenates them into a single DataFrame.
    3. Computes the percentage of processed W.A.R. values >= specified thresholds (90%, 80%, 70%).
    4. Generates a stacked bar graph using `matplotlib`, where each bar represents a threshold.
       The height of each bar corresponds to the percentage of values meeting or exceeding the threshold.
       Text annotations on each bar show the count of values meeting the threshold and the total count.
    5. Saves the concatenated DataFrame as `concatenated_data.xlsx` in the `input_dir`.
    6. Displays the graph using `plt.show()` and deletes the intermediate `concatenated_data.xlsx` file.

    Command-line Usage:
    python script_name.py /path/to/input_directory

    Requirements:
    - Requires `pandas`, `numpy`, and `matplotlib` Python libraries.
    - Excel files in `input_dir` must have columns 'Mixed W.A.R. (%)' and 'Processed W.A.R. (%)'.
    - Files starting with '~$' are skipped as temporary files.

    Returns:
    None
    """
    # Function code follows here
    
    parser = argparse.ArgumentParser(description='Process Excel files and generate a stacked bar graph.')
    parser.add_argument('input_dir', type=str, help='Directory where input Excel files are located')
    args = parser.parse_args()

    input_dir = args.input_dir
    # input_dir = '/Users/guzhaowen/Downloads/benchmarking_script/processed_excel/'
    # filename = 'Book1.xlsx'
    excel_files = [file for file in os.listdir(input_dir) if file.endswith('.xlsx') or file.endswith('.xls')]
    dfs = []
    for file in excel_files:
        file_path = os.path.join(input_dir, file)
        df = read_excel_without_last_row(file_path)
        dfs.append(df)
    
    concatenated_df = pd.concat(dfs, axis=0, ignore_index=True)
    output_file = input_dir+ 'concatenated_data.xlsx'
    concatenated_df.to_excel(output_file, index=False)
    
    thresholds = [90, 80, 70]
    colors = ['r', 'g', 'b']

    fig, ax = plt.subplots(figsize=(10, 6))

    width = 0.2  # width of the bars
    x = np.arange(9)  # the label locations
    x_labels = ['90%', '80%', '70%', '60%', '50%', '40%', '30%', '20%', '10%']

    for i, threshold in enumerate(thresholds):
        results, expand_res = graph(input_dir, output_file, threshold)
        bars = ax.bar(x + i * width, results, width, label=f'WAR >= {threshold}%', color=colors[i])
        for bar, result in zip(bars, expand_res):
            count_ge_i, total_keys_i = result
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f"{count_ge_i}/{total_keys_i}", ha='center', va='bottom')

    ax.set_ylabel('Processed W.A.R. %')
    ax.set_xlabel('W.A.R. on Original')
    ax.set_title('Bar Graph of Processed WAR% >= Thresholds vs. Original WAR%')
    ax.set_xticks(x + width)
    ax.set_xticklabels(x_labels)
    ax.legend()
    ax.set_ylim(0,140)

    plt.tight_layout()
    plt.show()
    
    os.remove(output_file)

if __name__ == "__main__":
    main()