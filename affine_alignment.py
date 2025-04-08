import sys
from typing import List, Dict, Iterable, Tuple

# Please do not remove package declarations because these are used by the autograder.
def graphConstruction(v: str, w:str, match_reward: int, mismatch_penalty: int, gap_opening_penalty: int, gap_extension_penalty: int):
    
    print()
    print("S: " + v)
    print("T: " + w)

    # S is the length of the substring such that v,w is the final length
    upper_score = []
    middle_score = []
    lower_score = []
    
    # Backtrack is the direction so to speak about the subseq
    upper_backtrack = []
    middle_backtrack = []
    lower_backtrack = []
    

    for i in range(len(v)+1):
        
        score = []
        emptyStr = []

        # Second for loop we're initializing the len(w) + 1 cols for the second for loop
        for j in range(len(w)+1):
            
            if (i == 0 and j == 0):
                score.append(0)
                
            else:
                score.append(-float('inf'))
            
            emptyStr.append("NONE")
        
        
        upper_backtrack.append(emptyStr[:])
        middle_backtrack.append(emptyStr[:])
        lower_backtrack.append(emptyStr[:])

        upper_score.append(score[:])
        middle_score.append(score[:])
        lower_score.append(score[:])
    
    for i in range(1, len(v)+1):
        if (i == 1):
            lower_score[i][0] = middle_score[i-1][0] - gap_opening_penalty
            lower_backtrack[i][0] = "down_beginning"
        
        else:
            lower_score[i][0] = middle_score[i-1][0] - gap_extension_penalty
            lower_backtrack[i][0] = "down_conti"

        middle_score[i][0] = lower_score[i][0]
        middle_backtrack[i][0] = "returned_lower"

    for i in range(1, len(w)+1):

        if (i == 1):
            upper_score[0][i] = middle_score[0][i-1] - gap_opening_penalty
            upper_backtrack[0][i] = "right_beginning"

        else:
            upper_score[0][i] = middle_score[0][i-1] - gap_extension_penalty
            upper_backtrack[0][i] = "right_conti"

        middle_score[0][i] = upper_score[0][i]
        middle_backtrack[0][i] = "returned_upper"

    for i in range(1, len(v) + 1):
        for j in range(1,len(w) + 1):
            
            case = 0

            if v[i - 1] == w[j -1]:
                case = match_reward

            elif v[i - 1] != w[j - 1]:
                case = -mismatch_penalty

            lower_score[i][j] = max(lower_score[i-1][j] - gap_extension_penalty, middle_score[i-1][j] - gap_opening_penalty)

            if lower_score[i][j] == lower_score[i-1][j] - gap_extension_penalty:

                lower_backtrack[i][j] = "down_conti"
            
            else:

                lower_backtrack[i][j] = "down_beginning"
    

            upper_score[i][j] = max(upper_score[i][j-1] - gap_extension_penalty, middle_score[i][j-1] - gap_opening_penalty)
            
            

            if upper_score[i][j] == upper_score[i][j-1] - gap_extension_penalty:
                upper_backtrack[i][j] = "right_conti"
            
            else:
                upper_backtrack[i][j] = "right_beginning"



            middle_score[i][j] = max(lower_score[i][j], middle_score[i-1][j-1] + case, upper_score[i][j])
            
            print()
            print("Lower Score: " + str(lower_score[i][j]))
            print("Middle Score: " + str(middle_score[i][j] + case))
            print("Upper Score: " + str(upper_score[i][j]))


            if middle_score[i][j] == lower_score[i][j] and lower_score[i][j] != upper_score[i][j]:
                middle_backtrack[i][j] = "returned_lower"

            elif middle_score[i][j] == upper_score[i][j]:
                middle_backtrack[i][j] = "returned_upper"
            
            elif middle_score[i][j] == middle_score[i-1][j-1] + case:
                middle_backtrack[i][j] = "diagonal"


    for i in range(len(upper_score)):
        print(upper_score[i])


    print()

    for i in range(len(upper_score)):
        print(middle_score[i])

    print()

    for i in range(len(upper_score)):
        print(lower_score[i])


    
    print("Upper")
    for i in range(len(upper_backtrack)):
        print(upper_backtrack[i])

    print()

    print("Middle")
    for i in range(len(middle_backtrack)):
        print(middle_backtrack[i])

    print()
    print("Lower")
    for i in range(len(middle_backtrack)):
        print(lower_backtrack[i])

                    
    return middle_backtrack, lower_backtrack, upper_backtrack, middle_score[len(v)][len(w)]


def backtrack(upper:[], middle:[], lower:[], emptyback:[], where: str, v:str, w:str, i:int, j:int):

    #print(v)
    #print()
    #print("Running: I: " + str(i) + " J: " + str(j))
    #print("Where: " + where)
    if i == 0 and j == 0:

        return "", emptyback
    
    # CHECK ALL CONDITIONALS TO MAKE SURE IT IS CORRECT
    if where == "lower":
        #print("Curr Lower: " + lower[i][j])
        if lower[i][j] == "down_conti":

            emptyback.append("down_conti")

            return backtrack(upper, middle, lower, emptyback, "lower", v,w, i-1, j)[0] + "-", emptyback

        elif lower[i][j] == "down_beginning":
            emptyback.append("down_beginning")
            return backtrack(upper, middle, lower, emptyback, "middle", v,w, i-1, j)[0] + "-", emptyback

    elif where == "upper":
        #print("Curr Upper: " + upper[i][j])
        if upper[i][j] == "right_conti":
            emptyback.append("right_conti")
            return backtrack(upper, middle, lower, emptyback, "upper", v,w, i, j-1)[0]+ w[j-1], emptyback

        elif upper[i][j] == "right_beginning":
            emptyback.append("right_beginning")
            return backtrack(upper, middle, lower, emptyback, "middle", v,w, i, j-1)[0]+ w[j-1], emptyback

    else:
        #print("Curr Middle: " + middle[i][j])
        if middle[i][j] == "diagonal":
            emptyback.append("diagonal")
            return backtrack(upper, middle, lower, emptyback, "middle", v,w, i-1, j-1)[0]+ w[j-1], emptyback

        elif middle[i][j] == "returned_upper":
            emptyback.append("returned_upper")
            return backtrack(upper, middle, lower, emptyback, "upper", v,w, i, j)[0]+ "", emptyback
        
        elif middle[i][j] == "returned_lower":
            emptyback.append("returned_lower")
            return backtrack(upper, middle, lower, emptyback, "lower", v,w, i, j)[0]+ "", emptyback
        

# Insert your affine_alignment function here, along with any subroutines you need
def affine_alignment(match_reward: int, mismatch_penalty: int,
                     gap_opening_penalty: int, gap_extension_penalty: int,
                     s: str, t: str) -> Tuple[int, str, str]:
    """
    Compute the affine alignment of two strings based on match reward, mismatch penalty, 
    gap opening penalty, and gap extension penalty.
    """
    middle, lower, upper, score = graphConstruction(t,s, match_reward, mismatch_penalty, gap_opening_penalty, gap_extension_penalty)
    emptyback = []
    
    alignedV, backtracking = backtrack(upper, middle, lower, emptyback, "middle", t,s, len(t), len(s))


    backtracking = backtracking[::-1]
    print()
    print(backtracking)
    aligned2 = ""
    pos = 0

    for path in backtracking:
        print(aligned2)
        if path == "diagonal":
            
            aligned2 = aligned2 + t[pos]
            pos += 1
        
        elif path == "right_beginning" or path == "right_conti":
            aligned2 = aligned2 + "-"

        elif path == "down_beginning" or path == "down_conti":
            aligned2 = aligned2 + t[pos]
            pos +=1

        else:
            next
    
    if len(s) < len(t):
        return score, alignedV, aligned2


    return score, alignedV, aligned2


    pass  # Implement the function logic here

v = "GTTCCAGGTA"
w = "CAGTAGTCGT"

match = 2
mismatch = 3
opening = 3
extension = 2

score, aligned1, aligned2 = affine_alignment(match, mismatch, opening, extension, v, w)
print()
print("Score: " + str(score))
print("Aligned1: "  + aligned1)
print("Aligned2: " + aligned2)