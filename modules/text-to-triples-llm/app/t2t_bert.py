import torch
from transformers import BertTokenizerFast
import json
from app import model



# Initialize the tokenizer for processing inputs
tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')

# Define the label map according to the training labels
label_map = {
    'LABEL_0': 'Subject',
    'LABEL_1': 'Predicate',
    'LABEL_2': 'Object',
    'LABEL_3': 'other'
}

def predict_and_form_triples(input_data, model, tokenizer, label_map):
    """ 
    Extract and form S-P-O triples (Subject, Predicate, Object) from a sentence.
    This function tokenizes the sentence, uses a model to predict SPO labels for each token, and aggregates 
    these tokens into coherent phrases. It handles subwords by merging them with preceding tokens and forms 
    triples even if some components are implied. If all components are missing, it returns an empty triple.

    Args:
        input_data (dict): Contains the sentence to be processed.
        model (torch.nn.Module): Pre-trained model for S-P-O prediction.
        tokenizer (BertTokenizerFast): Tokenizer for processing the input sentence.
        label_map (dict): Maps label IDs to their descriptive labels (e.g., Subject, Predicate, Object, other).

    Returns:
        dict: Contains formed triples or an empty structure if no explicit S-P-O components are found.
    """

    sentence = input_data['sentence']
    inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predictions = torch.argmax(logits, dim=-1)[0]
    tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])

    subjects, predicates, objects = [], [], []
    aggregated_subjects, aggregated_predicates, aggregated_objects = '', '', ''
    for token, pred in zip(tokens, predictions):
        label = label_map[model.config.id2label[pred.item()]] 
        
        # Handle subwords and aggregate them into the previous token if necessary
        if token.startswith("##"):
            if label == 'Subject' and subjects:
                subjects[-1] += token[2:]  # Remove '##' and concatenate
            elif label == 'Predicate' and predicates:
                predicates[-1] += token[2:]
            elif label == 'Object' and objects:
                objects[-1] += token[2:]
        else:
            if label == 'Subject':
                subjects.append(token)
            elif label == 'Predicate':
                predicates.append(token)
            elif label == 'Object':
                objects.append(token)

    # Join tokens to form the phrases for subjects, predicates, and objects
    aggregated_subjects = " ".join(subjects)
    aggregated_predicates = " ".join(predicates)
    aggregated_objects = " ".join(objects)

    triples = []
    # Form a triple only if there's at least one non-implied component
    if subjects or predicates or objects:
        triples.append({
            "subject": aggregated_subjects,
            "predicate": aggregated_predicates,
            "object": aggregated_objects
        })
    # If no components are available (all implied), then return an empty triple structure
    else:
        triples.append({
            "subject": "",
            "predicate": "",
            "object": ""
        })

    return triples


def process_input_output(input_data):
    """ 
    Processes input dict to extract S-P-O triples using the 'predict_and_form_triples' function, 
    applying the S-P-O prediction and aggregation logic, returning a dict with triples.
    Args:
        input_data: A dict containing the input data.

    Returns:
        triples: A dict with a list of S-P-O triples extracted from the input.
    """
    triples = predict_and_form_triples(input_data, model.get_model(), tokenizer, label_map)
    return {"triples": triples}
