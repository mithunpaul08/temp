
import sys



def get_new_name(prev, unique_new_ners, curr_ner, dict_tokenner_newner, curr_word, new_sent, ev_claim, full_name, unique_new_tokens,dict_newner_token):
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

    dict_newner_token[new_nertag_i]=full_name_c

    new_sent.append(new_nertag_i)


    full_name = []
    prev=[]
    if(curr_ner!="O"):
        prev.append(curr_ner)





    return prev, dict_tokenner_newner, new_sent, full_name,unique_new_ners,unique_new_tokens,dict_newner_token

def check_exists_in_claim(new_ev_sent_after_collapse, dict_tokenner_newner_evidence, dict_newner_token_ev, dict_tokenner_newner_claims):

    combined_sent=[]


    for ev_new_ner_value in new_ev_sent_after_collapse:
        #while parsig through the new evidence sentence you might encounter a new NER tag (eg: PER-E1). find its corresponding string value Eg: "tolkein"
        if ev_new_ner_value in dict_newner_token_ev.keys():

            #find its corresponding string value Eg: "tolkein"
            token=dict_newner_token_ev[ev_new_ner_value]

            token_split=set(token.split(" "))
            #print(token_split)

            found_intersection=False
            for tup in dict_tokenner_newner_claims.keys():
                name_cl = tup[0]
                ner_cl=tup[1]
                name_cl_split = set(name_cl.split(" "))
                # print("first value in tuples is")
                # print(type(token_split))
                # print(type(name_cl_split))
                #

                #if (token_split.intersection(name_cl_split)):
                if (token_split.issubset(name_cl_split) or name_cl_split.issubset(token_split)):
                    #print("name exists")


                    # also confirm that NER value also matches. This is to avoid john amsterdam PER overlapping with AMSTERDAM LOC
                    actual_ner_tag=""
                    for k, v in dict_tokenner_newner_evidence.items():

                        if (ev_new_ner_value == v):

                            # print(new_ner_value)
                            # print(k, v)
                            actual_ner_tag=k[1]
                            #print("the value of actual_ner_tag is:"+str(actual_ner_tag))

                            break

                    #now check if this NER tag in evidence also matches with that in claims
                    if(actual_ner_tag==ner_cl):

                        val_claim = dict_tokenner_newner_claims[tup]
                        combined_sent.append(val_claim)
                        found_intersection=True

            if not (found_intersection):
                combined_sent.append(ev_new_ner_value)
                new_ner=""
                #get the evidence's PER-E1 like value
                for k,v in dict_tokenner_newner_evidence.items():
                    #print(k,v)
                    if(ev_new_ner_value==v):
                        new_ner=k[1]

                dict_tokenner_newner_claims[token, new_ner] = ev_new_ner_value



        else:
            combined_sent.append(ev_new_ner_value)


    print(combined_sent)
    sys.exit(1)






def collapse_both(claims_words_list,claims_ner_list,ev_claim):
    dict_newner_token={}
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

                prev, dict_tokenner_newner, new_sent, full_name,unique_new_ners,unique_new_tokens,dict_newner_token = get_new_name(prev, unique_new_ners, curr_ner,
                                                                               dict_tokenner_newner, curr_word,
                                                                               new_sent, ev_claim, full_name,unique_new_tokens,dict_newner_token)
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
                    prev, dict_tokenner_newner, new_sent, full_name,unique_new_ners,unique_new_tokens,dict_newner_token = get_new_name(
                        prev, unique_new_ners, curr_ner,
                                                                                   dict_tokenner_newner, curr_word,
                                                                           new_sent, ev_claim, full_name,unique_new_tokens,dict_newner_token)

    return new_sent, dict_tokenner_newner,dict_newner_token


if __name__=="__main__":


    claims_ner_list = ['ORGANIZATION', 'ORGANIZATION', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
    claims_words_list = ['Fox', '2000', 'Pictures', 'released', 'the', 'film', 'Soul', 'Food', '.']

    evidence_words_list = ['Soul', 'Food', 'is', 'a', '1997', 'American', 'comedy-drama', 'film', 'produced', 'by', 'Kenneth', '``', 'Babyface', "''", 'Edmonds', ',', 'Tracey', 'Edmonds', 'and', 'Robert', 'Teitel', 'and', 'released', 'by', 'Fox', '2000', '.']
    evidence_ner_list = ['O', 'O', 'O', 'O', 'DATE', 'MISC', 'O', 'O', 'O', 'O', 'PERSON', 'O', 'O', 'O', 'PERSON', 'O', 'PERSON', 'PERSON', 'O', 'PERSON', 'PERSON', 'O', 'O', 'O', 'ORGANIZATION', 'ORGANIZATION', 'O']

    # claims_words_list = ["Roman", "Atwood", "is", "a", "content", "creator", "."]
    # claims_ner_list = ["O", "PERSON", "O", "O", "O", "O", "O"]
    # evidence_words_list = ["He", "also", "has", "another", "YouTube", "channel", "called", "``", "RomanAtwood", "''", ",", "where", "he", "posts", "pranks", "."]
    # evidence_ner_list = ["O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O"]

    # claims_words_list =     ["The", "Boston", "Celtics", "play", "their", "home", "games", "at", "TD", "Garden", "."]
    # claims_ner_list = ["O", "ORGANIZATION", "ORGANIZATION", "O", "O", "O", "O", "O", "LOCATION", "LOCATION", "O"]
    # evidence_words_list = ["The", "Celtics", "play", "their", "home", "games", "at", "the", "TD", "Garden", ",", "which", "they", "share", "with", "the", "National", "Hockey", "League", "-LRB-", "NHL", "-RRB-", "'s", "Boston", "Bruins", "."]
    # evidence_ner_list = ["O", "ORGANIZATION", "O", "O", "O", "O", "O", "O", "LOCATION", "LOCATION", "O", "O", "O", "O", "O", "O", "ORGANIZATION", "ORGANIZATION", "ORGANIZATION", "O", "ORGANIZATION", "O", "O", "ORGANIZATION", "ORGANIZATION", "O"]



    ev_claim = "c"

    new_sent_after_collapse, dict_tokenner_newner_claims,dict_newner_token=collapse_both(claims_words_list,claims_ner_list,ev_claim )
    # print("new_sent_after_collapse="+str(new_sent))
    #print("dict_newner_token is:" + str(dict_newner_token))

    print(claims_words_list)
    #print("new_sent_after_collapse")
    #print(new_sent_after_collapse)


    ev_claim = "e"
    new_sent_after_collapse, dict_tokenner_newner_evidence ,dict_newner_token_ev= collapse_both(evidence_words_list, evidence_ner_list, ev_claim )
    #print("dict_newner_token is:" + str(dict_newner_token))


    #print("new_sent_after_collapse")
    #print(new_sent_after_collapse)
    print(evidence_words_list)
    check_exists_in_claim(new_sent_after_collapse, dict_tokenner_newner_evidence, dict_newner_token_ev,dict_tokenner_newner_claims)


    print("done")