import json

def format_json(old_obj):
        new_obj = {
                "success": old_obj['success'],
                "results": []
        }
        result = old_obj['results']
        for i in range(check_elements(old_obj)):
        
                temp = {
                        "collection": result['collection'],
                        "document": result['content']['documents'][i],
                        "id": result['content']['ids'][i],
                        "metadata": result['content']['metadatas'][i]
                }
                temp['metadata']['private_data'] = json.loads(temp['metadata']['private_data'])
                new_obj['results'].append(temp)
        return new_obj

def check_elements(old_obj):
        amount = len(old_obj['results']['content']['ids'])
        return amount

