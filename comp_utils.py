import difflib
import pandas as pd
from python_minifier import minify


def compare_all_robust(code_df, min_similarity = 0.8, diagnostic = False, code_dump = False, code_filename_base = ''):
    '''Compare all code strings in Solution Code column. 
    Returns a dictionary of IDs and similarities when min similarity exceeded.  
    
    Keyword argument:
    min_similarity -- the minimum similarity required to identify a match (default 0.8)
    '''
    if diagnostic:
        print(f"Comparing {len(code_df)} submissions... ", end = '')

    sim_results = dict()
    for row1 in range(len(code_df)-1):
        for row2 in range(row1 + 1, len(code_df)):
            user1 = str(code_df.iloc[row1]["Username"])
            user2 = str(code_df.iloc[row2]["Username"])
            #if diagnostic:
            #    print(f"Comparing {user1} to {user2}... ", end='')
            similarity = robust_compare_code(code_df.iloc[row1]["Solution Code"], code_df.iloc[row2]["Solution Code"])
            #if diagnostic:
            #    print("Done.")
            if similarity >= min_similarity:
                # Code dump if requested
                if code_dump:
                    code_comp_filename = code_filename_base + '_' + user1 + '_' + user2
                    write_code_comp(user1, code_df.iloc[row1]["Solution Code"], user2, code_df.iloc[row2]["Solution Code"], code_comp_filename)
                
                # Record match found
                if user1 not in sim_results:
                    sim_results[user1] = {user2 : similarity}
                else:
                    sim_results[user1][user2] = similarity
    if diagnostic:
        print(f"Done.")
        
    return sim_results

def compare_all_simple(code_df, min_similarity = 0.8, diagnostic = False, code_dump = False, code_filename_base = ''):
    '''Compare all code strings in Solution Code column. 
    Returns a dictionary of IDs and similarities when min similarity exceeded.  
    
    Keyword argument:
    min_similarity -- the minimum similarity required to identify a match (default 0.8)
    '''
    if diagnostic:
        print(f"Comparing {len(code_df)} submissions... ", end = '')

    sim_results = dict()
    for row1 in range(len(code_df)-1):
        for row2 in range(row1 + 1, len(code_df)):
            user1 = str(code_df.iloc[row1]["Username"])
            user2 = str(code_df.iloc[row2]["Username"])
            # if diagnostic:
            #     print(f"Comparing {user1} to {user2}... ", end='')
            similarity = simple_compare_code(code_df.iloc[row1]["Solution Code"], code_df.iloc[row2]["Solution Code"])
            #if diagnostic:
            #    print("Done.")
            if similarity >= min_similarity:
                # Code dump if requested
                if code_dump:
                    code_comp_filename = code_filename_base + '_' + user1 + '_' + user2
                    write_code_comp(user1, code_df.iloc[row1]["Solution Code"], user2, code_df.iloc[row2]["Solution Code"], code_comp_filename)
                # Record match found
                if user1 not in sim_results:
                    sim_results[user1] = {user2 : similarity}
                else:
                    sim_results[user1][user2] = similarity
    if diagnostic:
        print(f"Done.")

    return sim_results

def robust_compare_code(code1, code2):
    '''Compare similarity between two code submissions after removing
    comments and identifiers.'''
    # Minify code to remove variable naming and commenting
    
    code1 = minify(code1)
    code2 = minify(code2)

    # Tokenize the code chunks
    tokens1 = code1.split()
    tokens2 = code2.split()

    # Calculate the similarity score using the SequenceMatcher
    similarity = difflib.SequenceMatcher(None, tokens1, tokens2).ratio()

    return similarity

def simple_compare_code(code1, code2):
    '''Compare similarity between two code submissions.'''
    # Tokenize the code chunks
    tokens1 = code1.split()
    tokens2 = code2.split()

    # Calculate the similarity score using the SequenceMatcher
    similarity = difflib.SequenceMatcher(None, tokens1, tokens2).ratio()

    return similarity

def write_sim_report(filename, sim_results):
    '''Write similarity results to a CSV file.'''
    with open(filename, 'w') as out_file:
        out_file.write("User_1,User_2,similarity\n")
        for user1 in sim_results:
            for user2 in sim_results[user1]:
                out_file.write(f"{user1},{user2},{sim_results[user1][user2]}\n")

def write_code_comp(user1, code_str1, user2, code_str2, code_comp_filename):
    '''Write the similar code to file for easier reference.'''
    with open(code_comp_filename, 'w') as comp_file:
        comp_file.write(f'{user1} submission:\n')
        comp_file.write('--------------------------------------------------\n')
        comp_file.write(code_str1)
        comp_file.write(f'{user2} submission:\n')
        comp_file.write('--------------------------------------------------\n')
        comp_file.write(code_str2)

    return True

