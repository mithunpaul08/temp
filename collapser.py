
import sys



def get_new_name(prev, unique_new_ners, curr_ner, dict_tokenner_newner, curr_word, new_sent, ev_claim, full_name, unique_new_tokens):
    prev_ner_tag=prev[0]
    new_nertag_i=""
    full_name_c=" ".join(full_name)


    if(full_name_c in unique_new_tokens.keys()):

        new_nertag_i = unique_new_tokens[full_name_c]

    else:



        if(prev_ner_tag in unique_new_ners.keys()):
            old_index=unique_new_ners[prev_ner_tag]
            new_index=old_index+1
            unique_new_ners[prev_ner_tag]=new_index
            new_nertag_i=prev_ner_tag+"-"+ev_claim + str(new_index)
            unique_new_tokens[full_name_c] = new_nertag_i

        else:
            unique_new_ners[prev_ner_tag] = 1
            new_nertag_i = prev_ner_tag + "-" + ev_claim + "1"
            unique_new_tokens[full_name_c] = new_nertag_i


    if not ((full_name_c ,prev[0]) in dict_tokenner_newner):
        dict_tokenner_newner[full_name_c ,prev[0]]=new_nertag_i
    else:
        dict_tokenner_newner[full_name_c, prev[0]] = new_nertag_i

    new_sent.append(new_nertag_i)


    full_name = []
    prev=[]
    if(curr_ner!="O"):
        prev.append(curr_ner)





    return prev, dict_tokenner_newner, new_sent, full_name,unique_new_ners,unique_new_tokens

# def check_exists_in_claim(full_name,dict_tokenner_newner):
#     if (ev_claim == "e"):
#         new_name_evidence = check_exists_in_claim(full_name, dict_tokenner_newner)
#         #new_sent.append(new_name_evidence)
#
#
#     else:
#     name_evidence_split = set(full_name)
#     print(" value in name_evidence_split is")
#     print(name_evidence_split)
#
#     for tup in dict_tokenner_newner.keys():
#
#         name_cl=tup[0]
#         name_cl_split=name_cl.split(" ")
#         print("first value in tuples is")
#         print(name_cl_split)
#         if(name_evidence_split.intersection(name_cl_split)):
#             print("name exists")
#             val_claim=dict_tokenner_newner[tup]
#             return val_claim;



def collapse_both(claims_words_list,claims_ner_list,ev_claim):
    dict_tokenner_newner={}
    unique_new_tokens = {}
    unique_new_ners = {}
    prev = []
    new_sent = []


    full_name = []
    prev_counter = 0

    for index, (curr_ner, curr_word) in enumerate(zip(claims_ner_list, claims_words_list)):
        #print("unique_new_ners is:" + str(unique_new_ners))
        if (curr_ner == "O"):

            if (len(prev) == 0):
                new_sent.append(curr_word)
            else:
                prev, dict_tokenner_newner, new_sent, full_name,unique_new_ners,unique_new_tokens = get_new_name(prev, unique_new_ners, curr_ner,
                                                                               dict_tokenner_newner, curr_word,
                                                                               new_sent, ev_claim, full_name,unique_new_tokens)
                new_sent.append(curr_word)
        else:
            if (len(prev) == 0):
                prev.append(curr_ner)
                full_name.append(curr_word)
            else:
                if (prev[(len(prev) - 1)] == curr_ner):
                    prev.append(curr_ner)
                    full_name.append(curr_word)
                else:
                    prev, dict_tokenner_newner, new_sent, full_name,unique_new_ners,unique_new_tokens = get_new_name(prev, unique_new_ners, curr_ner,
                                                                                   dict_tokenner_newner, curr_word,
                                                                           new_sent, ev_claim, full_name)

    return new_sent, dict_tokenner_newner


if __name__=="__main__":
    claims_words_list = ["John", "Amsterdam", "worked", "with", "the", "Fox", "Broadcasting", "Company", "."]
    claims_ner_list = ["PERSON", "PERSON", "O", "O", "O", "ORGANIZATION", "ORGANIZATION", "ORGANIZATION", "O"]

    evidence_words_list =  ["He", "then", "played", "Detective", "John", "Amsterdam", "in", "the", "short-lived", "Fox",
                            "television", "series", "New", "Amsterdam", "-LRB-", "2008", "-RRB-", ",", "as", "well", "as", "appearing",
                            "as", "John", "Pike", "in", "the", "2009", "Fox", "television", "film", "Virtuality", ",", "originally", "intended", "as", "a", "pilot", "."]
    evidence_ner_list = ["O", "O", "O", "O", "PERSON", "PERSON", "O", "O", "O", "O", "O", "O", "O", "LOCATION", "O", "DATE", "O", "O", "O", "O", "O", "O", "O", "PERSON", "PERSON", "O", "O", "DATE", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"]


    ev_claim = "c"

    new_sent_after_collapse, dict_tokenner_newner_claims=collapse_both(claims_words_list,claims_ner_list,ev_claim )
    # print("new_sent_after_collapse="+str(new_sent))
    #print("dict_tokenner_newner is:" + str(dict_tokenner_newner))
    print(claims_words_list)
    print("new_sent_after_collapse")
    print(new_sent_after_collapse)


    ev_claim = "e"
    new_sent_after_collapse, dict_tokenner_newner_evidence = collapse_both(evidence_words_list, evidence_ner_list, ev_claim )
    print("dict_tokenner_newner is:" + str(dict_tokenner_newner_evidence))
    # print(evidence_words_list)
    print("new_sent_after_collapse")
    print(new_sent_after_collapse)
    sys.exit(1)
    print("done")