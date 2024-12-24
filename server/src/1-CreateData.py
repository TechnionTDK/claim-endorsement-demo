import json
import pandas as pd
import sys
import os

def create_data_file_from_csv(index,pathIndex):
    custom_headers = ['Attr1', 'Value1', 'Attr2', 'Value2', 'mean1', 'N1', 'mean2',
                      'N2', 'statistical_significance_stat', 'pvalue', 'Time', 'MI', 
                      'Normalized_MI', 'Anova_F_Stat', 'Anova_Pvalue', 
                      'Normalized Anova F Stat', 'Attr1_str', 'Value1_str',
                      'Attr2_str', 'Value2_str', 'Cosine Similarity', 
                      'Inverted pvalue', 'Coverage','AggDiff', 'Metrics Average']

    file_path = f'data/{pathIndex}/results/demo_test.csv'
    if not os.path.exists(file_path):
        return "-1"
    if os.path.getsize(file_path) == 0:
        return "-1"
    if(index==0):
        index=1
    file2 = pd.read_csv(file_path, )
    csv_headers = file2.columns.tolist()
    
    # Print or return the headers

    file = pd.read_csv(file_path, skiprows=index, header=None,names=csv_headers)
    ##file=pd.read_csv('data/SO/results/demo_test.csv')
        # Step 2 & 3: Extract the first row and convert to dictionary
    data_list = file.to_dict('records')


    # Return the list of dictionaries
    json_output = json.dumps(data_list)

    # Return the JSON string
    return json_output




def create_data_file_from_csv_for_test():
    file_path = '../data/SO/results/claim_endorsement_user_study_with_generality_filter_version_1.csv'
    if os.path.getsize(file_path) == 0:
        return "-1"
    custom_headers = [ 'predicate', 'BSc avg salary', 'MSC avg salary', 'BSc count', 'MSc count', 'sentence']
    file = pd.read_csv(file_path, nrows=19, skiprows=2, header=None,names=custom_headers)
    ##file=pd.read_csv('data/SO/results/demo_test.csv')
        # Step 2 & 3: Extract the first row and convert to dictionary
    data_list = file.to_dict('records')

    # Return the list of dictionaries
    json_output = json.dumps(data_list)
    with open('output-StackOverflow.json', 'w') as json_file:
        json_file.write(json_output)
        
        
        
        
        
    custom_headers = [ 'predicate', 'Men avg salary', 'Women avg salary', 'Men count', 'Women count', 'sentence']
    file = pd.read_csv(file_path, nrows=19, skiprows=24, header=None,names=custom_headers)

    data_list = file.to_dict('records')

    # Return the list of dictionaries
    json_output = json.dumps(data_list)
    with open('output-ACS.json', 'w') as json_file:
        json_file.write(json_output)
        
        
        
        
         
        
        
        
        
    custom_headers = [ 'saturday delays','sentence','predicate', 'monday delays',   ]
    
    
    file = pd.read_csv(file_path, nrows=10, skiprows=47, header=None,names=custom_headers)
    ##file=pd.read_csv('data/SO/results/demo_test.csv')
        # Step 2 & 3: Extract the first row and convert to dictionary
    data_list = file.to_dict('records')

    # Return the list of dictionaries
    json_output = json.dumps(data_list)
    with open('output-Flights.json', 'w') as json_file:
        json_file.write(json_output)
if __name__ == '__main__':
   index = int(sys.argv[1])
   pathIndex = str(sys.argv[2])
#create_data_file_from_csv_for_test()
   value= create_data_file_from_csv(index,pathIndex)
   print(value)