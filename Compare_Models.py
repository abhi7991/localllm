# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 15:06:01 2024

@author: abhis
"""


import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Set the style of the visualization
sns.set(style="whitegrid")



'''
This function is used to run a particular Llama model and generate the metrics
''' 
def getInsights(model, question):
    url = 'http://localhost:11434/api/generate'
    
    data = {
        "model": model,
        "prompt": question,
        "stream": False
    }
    
    data_json = json.dumps(data)
    
    try:
        r = requests.post(url, data=data_json, headers={'Content-Type': 'application/json'})
        r.raise_for_status() 
        df = r.json() 
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

    return df

'''
This function plots the metrics obtained upon running each question
''' 
def plot_metrics(df, metric):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x="Question", y=metric, hue="Model", marker="o")
    plt.title(f"Comparison of {metric} Across Questions")
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Question")
    plt.ylabel(f"{metric} (s)")
    plt.legend(title="Model")
    
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.getcwd()+"/"+metric.replace('(s)',"").replace(" ","_")+".jpg")
    plt.show()


'''
Converting nanoseconds to seconds for better understanding
'''
def nanoseconds_to_seconds(nanoseconds):
    return nanoseconds / 1_000_000_000

questions = [
    "Who are you and what is the capital of India?",
    "What is the largest mammal in the world?",
    "How do you make an apple pie?",
    "What are the benefits of exercise?",
    "Explain the theory of relativity.",
]

metrics_data = {
    "Model": [],
    "Question": [],
    "Eval Duration (s)": [],
    "Prompt Eval Duration (s)": []
}

'''
Collect metrics for both models

mymistral - This is the custom Mistral model I made using the modelfile 

myllama3 - This is the custom Llama3 model I made using the modelfile 

'''
for model in ["mymistral", "myllama3"]:
    for question in questions:
        response = getInsights(model, question)
        if response:
            metrics_data["Model"].append(model)
            metrics_data["Question"].append(question)
            metrics_data["Eval Duration (s)"].append(nanoseconds_to_seconds(response['eval_duration']))
            metrics_data["Prompt Eval Duration (s)"].append(nanoseconds_to_seconds(response['prompt_eval_duration']))

a = metrics_data
df_metrics = pd.DataFrame(metrics_data)
print(df_metrics)

# Plot each metric
for metric in ["Eval Duration (s)", "Prompt Eval Duration (s)"]:
    plot_metrics(df_metrics, metric)

