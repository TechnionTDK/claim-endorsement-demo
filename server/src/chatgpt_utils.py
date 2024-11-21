from utils import get_chatgpt_key
import openai
import pandas as pd
from utils import *


def chatgpt_chat_request(request_string,max_tokens=2):
    key=get_chatgpt_key()
    openai.api_key = key
    message_string=request_string
    message = [

        {"role": "user", "content": message_string}]
    chat=openai.ChatCompletion.create(model=CHATGPT_MODEL_STRING,messages=message,temperature=0)
    reply=chat.choices[0].message.content
    print(f"""
    Request={message_string}
    ChatGPT: {reply}
    """)
    return reply
    #messages.append({"role": "assistant", "content": reply})


def create_group_string(attr,value,grp1,grp2,aggregate_list,target,translation_dict):
    _, agg_func_desc, _ = aggregate_list
    return f"Among people with {translation_dict[attr]}={value}, people with {grp2} had a higher {agg_func_desc} {target} than people with {grp1}."


def create_education_string(attr,value,grp1,grp2,aggregate_list,target,translation_dict):
    _, agg_func_desc, _ = aggregate_list
    return f"Among people with {translation_dict[attr]}={value}, people with {grp2} education had a higher {agg_func_desc} {target} than people with {grp1} education"


def create_ethnicity_string(attr,value,grp1,grp2,aggregate_list,target,translation_dict):
    _, agg_func_desc, _ = aggregate_list
    return f"Among people with {translation_dict[attr]}={value}, {grp2} people had a higher {agg_func_desc} {target}  {grp1} people"


def create_sex_string(attr,value,grp1,grp2,aggregate_list,target,translation_dict):
    _, agg_func_desc, _ = aggregate_list
    return f"Among people with {translation_dict[attr]}={value},  {grp2} had a higher {agg_func_desc} {target} than {grp1}."


def create_chatgpt_request_naturalnesss_comparison_string(string_list):
    str="\n"
    for i in range(len(string_list)):
        str += f"{i+1}. {string_list[i]}\n"
    return f"""
                Which of the following statements sounds less cherry picked?
                {str}
                Please return a number, or 0 if the statements sound equally cherry picked
            """

def create_chatgpt_ranking_request(string_list):
    str="\n"
    for i in range(len(string_list)):
        str+=f"{i+1}. {string_list[i]}\n"

    return f"""
                Please order the following sentences from least cherry picked to most cherry picked:
                {str}
                Please respond with only numbers
            """


def fullsplit_with_chatgpt(result_df, translation_dict, chatgpt_string_template_func):
    print(f"Before: {len(result_df)}")
    result_df = result_df.assign(Chatgpt_Ranking="")
    filtered_df = result_df[result_df["pvalue"] < 0.05].sort_values(by="Cosine Similarity", ascending=False)

    result_df = result_df[~result_df.isin(filtered_df)].dropna(how='all')  #We are doing set subtraction of the form: df-result_df
    print(f"After Subtraction: {len(result_df)}")
    #print(result_df)
    df_lists = filtered_df.head(10).apply(lambda row: [
        row["Original_Attr"], row["Value"], row["Group1"], row["Group2"], median_list, "salary", translation_dict, ]
        if row["Original_Attr"] == row["Split_Attr"]
        else [row["Original_Attr"], row["Split_Attr"], row["Group1"], row["Group2"], median_list, "salary", translation_dict, ], axis=1)
    df_strings = [chatgpt_string_template_func(*l) for l in df_lists]
    chatgpt_reply_str = chatgpt_chat_request(request_string=create_chatgpt_ranking_request(df_strings))
    ranking_str_list = chatgpt_reply_str.split("\n")
    #print(ranking_str_list)
    for ranking_str in ranking_str_list:
        split_string = ranking_str.split('.')
        ranking = int(split_string[0])
        df_index = int(split_string[1]) - 1
        # sorted_df.iloc[df_index]["Chatgpt Ranking"]=ranking
        # result_df["Chatgpt_Ranking"][df_index]=ranking
        row_tuple = list(filtered_df.iloc[df_index])
        row_tuple[-1] = ranking
        filtered_df.iloc[df_index] = tuple(row_tuple)
        # print(f"({ranking},{df_index})")
    # print(result_df)
    result_df = pd.concat([result_df,filtered_df])#there should be no duplicates here
    print(f"Result: {len(result_df)}")
    result_df.to_csv(FULL_SPLIT_DEFAULT_OUTPUT_PATH)