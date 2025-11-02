

def format_json(json):
        new_obj = {
                "success": json['success'],
                "results": []
        }
        result = json['results']
        for i in range(check_elements(json)):
        
                temp = {
                        "collection": result['collection'],
                        "document": result['content']['documents'][i],
                        "id": result['content']['ids'][i],
                        "metadata": result['content']['metadatas'][i]
                }
                new_obj['results'].append(temp)
        return new_obj

def check_elements(json):
        amount = len(json['results']['content']['ids'])
        return amount

