from glob import glob

from comp_utils import *

def main():
    quiz_submissions = glob('C:/Users/Bharg/OneDrive/Desktop/Bhargavi/Spring-2024/PPL/AIV_checker/submissions_DS/*.c')

    #print(quiz_submissions)

    for index1 in range(len(quiz_submissions) - 1):
        filename1 = quiz_submissions[index1]
        student1 = filename1.split('\\')[1].split('_')[0]
        with open(filename1, 'r',encoding='latin-1') as file1:
            code1 = file1.read()

        for index2 in range(index1 + 1, len(quiz_submissions)):
            filename2 = quiz_submissions[index2]
            student2 = filename2.split('\\')[1].split('_')[0]
            with open(filename2, 'r',encoding='latin-1') as file2:
                code2 = file2.read()

            similarity = simple_compare_code(code1, code2)
            #print(similarity)

            if similarity > 0.7:
                print(f"{student1} and {student2}: {similarity}")
           
        
    


main()
