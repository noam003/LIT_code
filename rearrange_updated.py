import pandas as pd
# from openpyxl import load_workbook
# from openpyxl.styles import PatternFill
# import numpy as np
import os
# from openpyxl import Workbook

def edit_xlsx(input_dir,filename,output_dir):
    '''
        input_dir: the directory input file sits
        filename: takes an excel.xlsx file as input
        output_dir: output as processed_excel.xlsx in output directory, will create one if not exist
        this function:
        1. get rid of information except filenames and WAR
        2. rearrange them at mixed and proc with their WAR accordingly and calculate improvement from mixed to proc
        3. Add the average of each column to the bottom
        
        e.g.edit_xlsx('/Users/guzhaowen/Downloads/benchmarking_script_2/excel/','422-122949-0014_output.xlsx','/Users/guzhaowen/Downloads/benchmarking_script_2/processed_excel/')
    '''
    if filename.startswith('~$'):
        print(f"Skipping temporary file: {filename}")
        return
    
    input_file_path = input_dir+filename # Path to the input file
    # print(input_file_path)
    df = pd.read_excel(input_file_path)

    # Drop the 'Transcript' and '1' columns
    df = df.drop(columns=['Transcript', '0', 'Deletion error (%)','Insertion error (%)','Substitution error (%)','Reference Text','Duration'])
    
    df_sorted = df.sort_values(by='1')

    results = []
    new_results=[]
    names=[]
    for _, row in df_sorted.iterrows():
        results.append(row['W.A.R. (%)'])
        names.append(row['1'])

    rows = int(len(df)/2)
    for i in range(0,rows):
        new_results.append([names[i][-34:],round(results[i]*100),round(results[i+rows]*100),round((results[rows+10]-results[rows])*100)])

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_file_path = output_dir+'processed_'+filename  # Path for the output file

    results_df = pd.DataFrame(new_results, columns=['File index', 'Mixed W.A.R. (%)', 'Processed W.A.R. (%)', 'Improvement'])
    mixavg = results_df['Mixed W.A.R. (%)'].mean()
    # results_df.loc['Mixed W.A.R. (%)'] = mixavg
    procavg=results_df['Processed W.A.R. (%)'].mean()
    # results_df.loc['Processed W.A.R. (%)'] = procavg
    imp = results_df['Improvement'].mean()
    # results_df.loc['Improvement'] = imp
    new_results.append(['Average',mixavg,procavg,imp])
    results_df = pd.DataFrame(new_results, columns=['File index', 'Mixed W.A.R. (%)', 'Processed W.A.R. (%)', 'Improvement'])
    results_df.to_excel(output_file_path, index=False)

def rearrange_multiple(input_dir, output_dir):
    """
    input_dir: Directory where input Excel files are located.
    output_dir: Directory where processed Excel files will be saved.
    this function is going to organize and process every file in input_dir and output at output_dir
    """
    for file in os.listdir(input_dir):
        if file.endswith('xlsx'):
            edit_xlsx(input_dir, file, output_dir)
            
def summary(input_dir, output_file='Summary_Processed.xlsx'):
    """
    input_dir: Directory containing input Excel files (.xlsx).
    output_file: Path to the output Excel file where concatenated data will be saved.
    """
    all_data = pd.DataFrame()

    # Iterate over each file in the input directory
    for file in os.listdir(input_dir):
        if file.endswith('.xlsx'):
            file_path = os.path.join(input_dir, file)
            df = pd.read_excel(file_path)
            all_data = pd.concat([all_data, df], ignore_index=True)

    # Calculate the average of each numeric column across all_data
    avg_row = all_data.select_dtypes(include=[float, int]).mean()

    # Create a DataFrame for the average row with the same column names
    avg_row_df = pd.DataFrame([avg_row], columns=all_data.columns)

    # Fill the non-numeric columns in the average row with the label 'Average'
    avg_row_df[all_data.select_dtypes(exclude=[float, int]).columns] = 'Average'

    # Append avg_row_df as the last row to all_data
    all_data = pd.concat([all_data, avg_row_df], ignore_index=True)

    # Write all_data to a new Excel file
    all_data.to_excel(output_file, index=False)
    

def main():
    # edit_xlsx('/Users/guzhaowen/Downloads/benchmarking_script_2/excel/','422-122949-0014_output.xlsx','/Users/guzhaowen/Downloads/benchmarking_script_2/processed_excel/')
    rearrange_multiple('/Users/noamargolin/Desktop/benchmarking_script2/excel/',
    '/Users/noamargolin/Desktop/benchmarking_script2/processed_excel/')
    summary('/Users/noamargolin/Desktop/benchmarking_script2/processed_excel/')
if __name__ == "__main__":
    main()
