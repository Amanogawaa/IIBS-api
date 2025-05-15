from datasets import load_dataset

ds = load_dataset("mginoben/tagalog-profanity-dataset")

print(ds['train'])

profanity_list = []

for example in ds['train']:
    word = example['text']
    profanity_list.append(word)

print(profanity_list)   