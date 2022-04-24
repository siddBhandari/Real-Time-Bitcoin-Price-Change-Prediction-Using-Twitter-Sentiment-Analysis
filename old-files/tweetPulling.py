import requests
import os
import json
import re
import numpy as np
from csv import DictWriter
import pandas
# to clean the tweets and remove links hashtags etc from text

bearer_token = "AAAAAAAAAAAAAAAAAAAAAH%2F2YgEAAAAA88cF6Vnz0h%2FofudQiZMYaC0kq%2BE%3DhXg1vaTm1vT95nTFmsMzAazWilrQ9KV3yHh8FXjWGekJSdF70F"

def bearer_oauth(r):
    # Method for authentication by bearer token
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r

def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()

def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))

def set_rules(delete):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "Bitcoin", "tag": "bitcoin OR btc"},
        {"value": "Ethereum", "tag": "ethereum OR eth"},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))

# def get_stream(set):
#     response = requests.get(
#         "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
#     )
#     print(response.status_code)
#     if response.status_code != 200:
#         raise Exception(
#             "Cannot get stream (HTTP {}): {}".format(
#                 response.status_code, response.text
#             )
#         )
# #     data = ''
#     print("Working or wot?")
#     print("response is type of ",type(response))
#     # lines = response.text.splitlines()
    
#     # reader = csv.reader(lines)
#     for response_line in response.iter_lines():
#         if response_line:
#             json_response = json.loads(response_line)
#             print(json.dumps(json_response, indent=4, sort_keys=True))

#             json = pd.DataFrame({"data": file})
#             json.to_csv("response.csv")
# #               tweet = clean_tweet(json_response["data"]["text"])
#             #   print(response_line)
# #               data = data + response_line
# #     return data

def get_stream(set):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )

    # dic = response.json()
    # df.to_csv('respons.csv', index=False, sep="\t")
    # df = pandas.DataFrame(dic)
    index = 1
    field_names = ['ID','TEXT','MATCHING_RULES']
    with open('event.csv', 'a') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=field_names)
        dict={'ID':"ID",'TEXT':'TEXT','MATCHING_RULES':'MATCHING_RULES'}
        dictwriter_object.writerow(dict)
        for response_line in response.iter_lines():
            if response_line:
                json_response = json.loads(response_line)
                # print("type of json_resp", type(json_response))
                print(json_response["data"]["text"])
                print(json_response["matching_rules"][0]["tag"])
                # print("this is printed")
                # List = [index,json_response["data"]["text"],json_response["matching_rules"]["tag"]]
                dict={'ID':index,'TEXT':json_response["data"]["text"],'MATCHING_RULES':json_response["matching_rules"][0]["tag"]}

                    # Pass this file object to csv.writer()
                    # and get a writer object
                # writer_object = writer(f_object)
            
                # Pass the list as an argument into
                # the writerow()
                # writer_object.writerow(List)
            
                # Pass the file object and a list 
                # of column names to DictWriter()
                # You will get a object of DictWriter
                
            
                #Pass the dictionary as an argument to the Writerow()
                dictwriter_object.writerow(dict)

                index = index + 1
                

                # print(json.dumps(json_response, indent=4, sort_keys=True))
        f_object.close()

def clean_tweet(tweet):
    if type(tweet) == np.float:
        return ""
    temp = tweet.lower()
    temp = re.sub("'", "", temp) # to avoid removing contractions in english
    temp = re.sub("@[A-Za-z0-9_]+","", temp)
    temp = re.sub("#[A-Za-z0-9_]+","", temp)
    temp = re.sub(r'http\S+', '', temp)
    temp = re.sub('[()!?]', ' ', temp)
    temp = re.sub('\[.*?\]',' ', temp)
    temp = re.sub("[^a-z0-9]"," ", temp)
   
  # print(json.dumps(json_response, indent=4, sort_keys=True))
#             tweet = clean_tweet(json_response["data"]["text"])
#             tweetData.append(tweet)  #tweetData can be a list, not defined yet 

def main():
    rules = get_rules()
    delete = delete_all_rules(rules)
    set = set_rules(delete)
    data = get_stream(set)
    print(":::::::::::::::Here is the data:::::::::::::::")
    print(data)

if __name__ == "__main__":
    main()