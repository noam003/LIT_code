import pandas as pd
import os
# This version of rearrange corrects the file naming bug and can take the average for different db levels
def transform_file_name(file_name):
    if isinstance(file_name, str) and file_name != "nan":
        parts = file_name.split('_')
        return '_'.join(parts[2:])
    return file_name

def db_count(transformed_names):
    count = 0
    db_set = set()
    for file_name in transformed_names:
        if isinstance(file_name, str) and file_name != "nan":
            #print(file_name.split('_')[4])
            db_level = file_name.split('_')[4]
            db_set.add(db_level)
    return len(db_set)
    


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
    file_names=[]
    for _, row in df_sorted.iterrows():
        results.append(row['W.A.R. (%)'])
        file_names.append(row['1'])
        
    transformed_names = [transform_file_name(name) for name in file_names]
    
    db_levels = db_count(transformed_names)
    #print(f'db levels: {db_levels}')
    rows = len(df)//2
    db_section_size = rows//db_levels
    
    print(f'db_section_size: {db_section_size}')
    # for loop gets mixed and proc values by going through i+rows
    
    for i in range(0,rows):
        file_name = transformed_names[i]
        mixed_res = round(results[i] * 100)
        proc_res = round(results[i + rows] * 100)
        imp_res = proc_res - mixed_res
        new_results.append([file_name,mixed_res,proc_res,imp_res])

            
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_file_path = output_dir+'processed_'+filename  # Path for the output file

    results_df = pd.DataFrame(new_results, columns=['File index', 'Mixed W.A.R. (%)', 'Processed W.A.R. (%)', 'Improvement'])
    #mixavg = results_df['Mixed W.A.R. (%)'].mean()
    # results_df.loc['Mixed W.A.R. (%)'] = mixavg
    #procavg=results_df['Processed W.A.R. (%)'].mean()
    # results_df.loc['Processed W.A.R. (%)'] = procavg
    #imp = results_df['Improvement'].mean()
    # results_df.loc['Improvement'] = imp
    
    final_results = []

    for i in range(db_levels):
        start_index = i * db_section_size
        end_index = (i + 1) * db_section_size if i != db_levels - 1 else len(results_df)
        section = results_df.iloc[start_index:end_index]
        
        # Append the current section to final results
        final_results.append(section)
        
        #if i < db_levels - 1:  # Add the new row except after the last section
        avg_mixed = section['Mixed W.A.R. (%)'].mean()
        avg_processed = section['Processed W.A.R. (%)'].mean()
        avg_improvement = section['Improvement'].mean()
        
        avg_row = pd.DataFrame({
            'File index': ['Average'],
            'Mixed W.A.R. (%)': [avg_mixed],
            'Processed W.A.R. (%)': [avg_processed],
            'Improvement': [avg_improvement]
        })
        
        # Append the average row to final results
        final_results.append(avg_row)
    
    # Concatenate all sections and average rows into the final DataFrame
    result_df = pd.concat(final_results).reset_index(drop=True)
    
    # Save the final DataFrame to Excel
    result_df.to_excel(output_file_path, index=False)
    print(f"Saved output to {output_file_path}")
    
    #mixavg = results_df['Mixed W.A.R. (%)'].mean(skipna=True)
    #procavg = results_df['Processed W.A.R. (%)'].mean(skipna=True)
    #impavg = results_df['Improvement'].mean(skipna=True)
    

    '''
    for i in range(0, len(results_df), db_iters + 1):
        if i < len(results_df) and results_df.iloc[i].isnull().all():
            segment = results_df.iloc[i + 1:i + db_iters + 1]
            avg_result_1 = segment['Mixed W.A.R. (%)'].mean(skipna=True)
            avg_result_2 = segment['Processed W.A.R. (%)'].mean(skipna=True)
            avg_difference = segment['Improvement'].mean(skipna=True)
            results_df.iloc[i] = ["Average", avg_result_1, avg_result_2, avg_difference]
    '''
    #new_results.append(['Average',mixavg,procavg,imp])
    
    #results_df = pd.DataFrame(new_results, columns=['File index', 'Mixed W.A.R. (%)', 'Processed W.A.R. (%)', 'Improvement'])
    

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
    #summary('/Users/noamargolin/Desktop/benchmarking_script2/processed_excel/')
if __name__ == "__main__":
    main()
