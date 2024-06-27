import pandas as pd
import numpy as np
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

    for _, row in df.iterrows():
        war_mixed_list.append(row['Mixed W.A.R. (%)'])
        war_proc_list.append(row['Processed W.A.R. (%)'])

    print(len(war_mixed_list))
    for key, value in zip(war_mixed_list, war_proc_list):
        print(f"{key}: {value}")

    results = []
    expand_res = []

    for i in range(90, 9, -10):
        keys_over_i = [war_proc for war_mixed, war_proc in zip(war_mixed_list, war_proc_list) if (war_mixed >= i and war_mixed < (i+10)) ]
        count_ge_threshold = np.sum(np.array(keys_over_i) >= threshold)
        percentage_ge_threshold = (count_ge_threshold / len(keys_over_i)) * 100 
        results.append(percentage_ge_threshold)
        expand_res.append((count_ge_threshold, len(keys_over_i)))

    return results, expand_res

def main():
    """
    Main function to generate a single stacked bar graph showing 
    the percentage of processed W.A.R. values for different thresholds.
    """
    input_dir = '/home/sbir/Downloads/benchmarking_script/processed_excel/'
    filename = 'processed_3853-163249-0018_output.xlsx'
    thresholds = [90, 80, 70]
    colors = ['r', 'g', 'b']

    fig, ax = plt.subplots(figsize=(10, 6))

    width = 0.2  # width of the bars
    x = np.arange(9)  # the label locations
    x_labels = ['90%', '80%', '70%', '60%', '50%', '40%', '30%', '20%', '10%']

    for i, threshold in enumerate(thresholds):
        results, expand_res = graph(input_dir, filename, threshold)
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

if __name__ == "__main__":
    main()
