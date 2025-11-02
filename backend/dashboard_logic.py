import json
from routes import read_collection


def get_real_data():
    """Récupère les vraies données depuis JP_la_collection."""
    try:
        # Récupère toutes les données de la collection
        result = read_collection("JP_la_collection")

        if not result.get("success"):
            # Si pas de données, retourner des données vides
            return {
                'risk_counts': {'high': 0, 'medium': 0, 'low': 0, 'none': 0},
                'moving_avg_data': [],
                'rating_labels': [],
                'overall_avg': 0,
                'recent_prompts': [],
                'top_topics': []
            }

        ratings_data = result.get("results", [])

        # Initialiser les compteurs de risques
        risk_counts = {'high': 0, 'medium': 0, 'low': 0, 'none': 0}
        all_ratings = []
        recent_prompts = []
        problems_count = {}

        # Traiter chaque rating
        for item in ratings_data:
            metadata = item.get("metadata", {})

            # Compter les niveaux de risque
            risk_level = metadata.get("risk_level", "none").lower()
            if risk_level in risk_counts:
                risk_counts[risk_level] += 1

            # Extraire la note (review)
            review = metadata.get("review", 0)
            try:
                rating_value = float(review)
            except (ValueError, TypeError):
                rating_value = 0

            all_ratings.append(rating_value)

            # Extraire les données privées (déjà parsées par format_json)
            # private_data est toujours une liste après format_json
            private_data = metadata.get("private_data", [])

            # Joindre les éléments de la liste pour former le problème
            problem = ", ".join(str(p) for p in private_data) if private_data else "Aucun risque détecté."

            # Compter les problèmes
            if problem in problems_count:
                problems_count[problem] += 1
            else:
                problems_count[problem] = 1

            # Ajouter aux récents
            recent_prompts.append({
                'id': item.get("id"),
                'rating': rating_value,
                'risk': risk_level,
                'problem': problem
            })

        # Calcul de la moyenne progressive (moving average)
        moving_avg_data = []
        current_sum = 0
        for i, r in enumerate(all_ratings, 1):
            current_sum += r
            moving_avg_data.append(round(current_sum / i, 2))

        # Calcul de la moyenne globale
        overall_avg = round(sum(all_ratings) / len(all_ratings), 1) if all_ratings else 0

        # Prendre les 5 plus récents
        recent_prompts = recent_prompts[-5:] if len(recent_prompts) >= 5 else recent_prompts
        recent_prompts.reverse()  # Les plus récents en premier

        # Top 3 des problèmes
        top_topics = [
            {'topic': topic, 'count': count}
            for topic, count in sorted(problems_count.items(), key=lambda x: x[1], reverse=True)[:3]
        ]

        return {
            'risk_counts': risk_counts,
            'moving_avg_data': moving_avg_data,
            'rating_labels': [f"Req {i+1}" for i in range(len(moving_avg_data))],
            'overall_avg': overall_avg,
            'recent_prompts': recent_prompts,
            'top_topics': top_topics
        }

    except Exception as e:
        print(f"Erreur lors de la récupération des données: {e}")
        # Retourner des données vides en cas d'erreur
        return {
            'risk_counts': {'high': 0, 'medium': 0, 'low': 0, 'none': 0},
            'moving_avg_data': [],
            'rating_labels': [],
            'overall_avg': 0,
            'recent_prompts': [],
            'top_topics': []
        }

def get_new_recent_ratings():
        """Récupère les 5 évaluations les plus récentes depuis JP_la_collection."""
        try:
                result = read_collection("JP_la_collection")

                if not result.get("success"):
                        return []

                ratings_data = result.get("results", [])
                recent_prompts = []

                # Traiter chaque rating
                for item in ratings_data:
                        metadata = item.get("metadata", {})

                # Extraire la note (review)
                review = metadata.get("review", 0)
                try:
                        rating_value = float(review)
                except (ValueError, TypeError):
                        rating_value = 0

                # Extraire le niveau de risque
                risk_level = metadata.get("risk_level", "none").lower()

                # Extraire les données privées (déjà parsées par format_json)
                # private_data est toujours une liste après format_json
                private_data = metadata.get("private_data", [])

                # Joindre les éléments de la liste pour former le problème
                problem = ", ".join(str(p) for p in private_data) if private_data else "Aucun risque détecté."

                recent_prompts.append({
                        'id': item.get("id"),
                        'rating': rating_value,
                        'risk': risk_level,
                        'problem': problem
                })

                # Retourner les 5 plus récents
                recent_prompts = recent_prompts[-5:] if len(recent_prompts) >= 5 else recent_prompts
                recent_prompts.reverse()  # Les plus récents en premier

                return recent_prompts

        except Exception as e:
                print(f"Erreur lors de la récupération des nouvelles évaluations: {e}")
                return []


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
