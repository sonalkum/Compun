import os
import openai
import json
from tqdm import tqdm

import itertools

openai.api_key = '' #FILL IN YOUR OWN HERE


def generate_prompt(category_name: str):
    # you can replace the examples with whatever you want; these were random and worked, could be improved
    return f"""Return a list of 5  diverse captions with a "{category_name}" in a photo. The captions should be a maximum of 10 words and one-liners. All 5 captions should describe "{category_name}" in diverse settings with different verbs and actions being performed with the "{category_name}". An example output for "chicken burger": ['Sizzling chicken burger grilling at a lively backyard BBQ.', 'Chef expertly flipping a juicy chicken burger in a diner.','Family enjoying homemade chicken burgers on a sunny picnic.','Athlete fueling up with a protein-packed chicken burger post-workout.','Friends sharing a chicken burger at a vibrant street festival.']. Only return a list of strings and nothing else."""

def stringtolist(description):
    return [descriptor[2:] for descriptor in description.split('\n') if (descriptor != '') and (descriptor.startswith('- '))]


def partition(lst, size):
    for i in range(0, len(lst), size):
        yield list(itertools.islice(lst, i, i + size))
        
def obtain_descriptors_and_save(filename, class_list):
    responses = {}
    descriptors = {}

    
    
    
    prompts = [generate_prompt(category.replace('_', ' ')) for category in class_list]
    
    
    # most efficient way is to partition all prompts into the max size that can be concurrently queried from the OpenAI API
    responses = [openai.Completion.create(model="gpt-4-turbo",
                                            prompt=prompt_partition,
                                            temperature=0.,
                                            max_tokens=100,
                                            ) for prompt_partition in partition(prompts, 20)]
    response_texts = [r["text"] for resp in responses for r in resp['choices']]
    descriptors_list = [stringtolist(response_text) for response_text in response_texts]
    descriptors = {cat: descr for cat, descr in zip(class_list, descriptors_list)}

    # save descriptors to json file
    if not filename.endswith('.json'):
        filename += '.json'
    with open(filename, 'w') as fp:
        json.dump(descriptors, fp)

classes = ['cricket bat'] #update the classes here
obtain_descriptors_and_save('cricket', classes)