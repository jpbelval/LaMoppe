import random

def get_mock_data():
    """Génère les données de simulation pour le chargement initial."""
    
    # Données pour le Pie Chart
    risk_counts = {
        'high': random.randint(5, 20),
        'medium': random.randint(20, 40),
        'low': random.randint(50, 100),
        'none': random.randint(200, 300)
    }
    
    # Données pour le Line Chart (note sur 10)
    all_ratings = [random.uniform(3.0, 9.5) for _ in range(30)]
    
    # Calcul de la moyenne progressive (moving average)
    moving_avg_data = []
    current_sum = 0
    for i, r in enumerate(all_ratings, 1):
        current_sum += r
        moving_avg_data.append(round(current_sum / i, 2))
    
    # Données pour la note moyenne globale
    overall_avg = round(sum(all_ratings) / len(all_ratings), 1)
    
    # Données pour les 5 plus récents
    recent_prompts = [
        {'id': 1, 'rating': 9.2, 'risk': 'low', 'problem': 'Aucun risque détecté.'},
        {'id': 2, 'rating': 3.1, 'risk': 'high', 'problem': 'Fuite de données (PII)'},
        {'id': 3, 'rating': 5.5, 'risk': 'medium', 'problem': 'Injection de prompt (Jailbreak)'},
        {'id': 4, 'rating': 8.0, 'risk': 'low', 'problem': 'Aucun risque détecté.'},
        {'id': 5, 'rating': 4.2, 'risk': 'high', 'problem': 'Fuite de données (Clé API)'},
    ]
    
    # Données pour les sujets problématiques
    top_topics = [
        {'topic': 'Fuite de données (PII)', 'count': 18},
        {'topic': 'Injection de prompt', 'count': 12},
        {'topic': 'Demande de code malveillant', 'count': 5},
    ]
    
    return {
        'risk_counts': risk_counts,
        'moving_avg_data': moving_avg_data,
        'rating_labels': [f"Req {i+1}" for i in range(len(moving_avg_data))],
        'overall_avg': overall_avg,
        'recent_prompts': recent_prompts,
        'top_topics': top_topics
    }

def get_new_recent_ratings():
    """Simule une nouvelle liste de 5 évaluations pour l'API."""
    all_risks = ['low', 'medium', 'high']
    
    # On prend la liste de base pour la mélanger
    base_prompts = [
        {'id': 1, 'rating': 9.2, 'risk': 'low', 'problem': 'Aucun risque détecté.'},
        {'id': 2, 'rating': 3.1, 'risk': 'high', 'problem': 'Fuite de données (PII)'},
        {'id': 3, 'rating': 5.5, 'risk': 'medium', 'problem': 'Injection de prompt (Jailbreak)'},
        {'id': 4, 'rating': 8.0, 'risk': 'low', 'problem': 'Aucun risque détecté.'},
        {'id': 5, 'rating': 4.2, 'risk': 'high', 'problem': 'Fuite de données (Clé API)'},
    ]
    random.shuffle(base_prompts)
    
    # On génère une "vraie" nouvelle entrée pour la mettre en haut
    new_entry = {
        'id': random.randint(100, 200), 
        'rating': round(random.uniform(2.0, 9.8), 1), 
        'risk': random.choice(all_risks), 
        'problem': f'Problème live simulé #{random.randint(1,100)}'
    }
    
    # Retourne la nouvelle entrée + 4 de la liste mélangée
    return [new_entry] + base_prompts[:4]


def get_rating_color_class(rating):
    """Retourne une classe CSS basée sur la note."""
    if rating >= 8:
        return 'text-green'
    if rating >= 4:
        return 'text-yellow'
    return 'text-red'

def get_risk_color_class(risk_level):
    """Retourne une classe CSS basée sur le niveau de risque."""
    return f"risk-{risk_level.lower()}"