from Levenshtein import distance as levenshtein_distance

class PlagiarismComparator:
    """Motore di confronto con edit distance e trasposizioni"""
    
    def __init__(self, melody1_repr, melody2_repr):
        """
        melody1_repr, melody2_repr: dizionari con le 5 rappresentazioni
        """
        self.m1 = melody1_repr
        self.m2 = melody2_repr
        self.representations = ['note', 'interval', 'duration', 'pitch_da', 'pitch_nd']
        self.weights = {
            'interval': 0.35,
            'pitch_da': 0.30,
            'pitch_nd': 0.20,
            'duration': 0.10,
            'note': 0.05
        }
    
    def find_best_match(self):
        """
        Prova tutte le 12 trasposizioni e calcola edit distance
        per ogni rappresentazione
        """
        results = {}
        
        for transposition in range(-12, 13):
            for repr_type in self.representations:
                str1 = self.m1[repr_type]
                str2 = self.m2[repr_type]
                
                if not str1 or not str2:
                    continue
                
                # Calcola edit distance
                ed = levenshtein_distance(str1, str2)
                max_len = max(len(str1), len(str2))
                normalized = ed / max_len if max_len > 0 else 1.0
                
                key = f"{repr_type}_transp_{transposition}"
                results[key] = {
                    'edit_distance': ed,
                    'normalized': normalized,
                    'transposition': transposition,
                    'similarity': (1 - normalized) * 100
                }
        
        return self.analyze_results(results)
    
    def analyze_results(self, results):
        """Aggrega i risultati per ogni rappresentazione"""
        best_by_repr = {}
        
        for key, val in results.items():
            repr_type = key.split('_')[0]
            
            if repr_type not in best_by_repr or \
               val['normalized'] < best_by_repr[repr_type]['normalized']:
                best_by_repr[repr_type] = val
        
        # Calcola score pesato
        weighted_score = 0
        total_weight = 0
        
        for repr_type in self.representations:
            if repr_type in best_by_repr:
                weight = self.weights[repr_type]
                similarity = best_by_repr[repr_type]['similarity'] / 100
                weighted_score += weight * similarity
                total_weight += weight
        
        overall_similarity = (weighted_score / total_weight * 100) if total_weight > 0 else 0
        
        # Trova la trasposizione più comune tra le migliori
        best_transpositions = [best_by_repr[r]['transposition'] for r in best_by_repr]
        most_common_transp = max(set(best_transpositions), key=best_transpositions.count)
        
        return {
            'overall_similarity': overall_similarity,
            'best_match_transposition': most_common_transp,
            'results_by_representation': best_by_repr,
            'verdict': self.get_verdict(overall_similarity),
            'confidence': self.calculate_confidence(best_by_repr)
        }
    
    def get_verdict(self, score):
        """Ritorna il verdetto basato sullo score"""
        if score > 75:
            return "🚨 ALTAMENTE SOSPETTO - Probabilissimo plagio"
        elif score > 60:
            return "⚠️  SOSPETTO - Forte similarità rilevata"
        elif score > 45:
            return "🟡 MODERATO - Similarità significativa"
        else:
            return "✅ DIVERSO - Nessuna evidenza di plagio"
    
    def calculate_confidence(self, best_by_repr):
        """Calcola il livello di confidenza dell'analisi"""
        if not best_by_repr:
            return 0
        
        # Confidenza basata sulla convergenza delle rappresentazioni
        similarities = [v['similarity'] for v in best_by_repr.values()]
        
        if not similarities:
            return 0
        
        avg_similarity = sum(similarities) / len(similarities)
        variance = sum((s - avg_similarity) ** 2 for s in similarities) / len(similarities)
        
        # Confidenza più alta se c'è accordo tra rappresentazioni
        confidence = 100 - min(variance, 50)
        return round(confidence, 1)
    
    def get_detailed_report(self):
        """Genera un report dettagliato"""
        results = self.find_best_match()
        
        report = {
            'summary': {
                'similarity_score': round(results['overall_similarity'], 1),
                'verdict': results['verdict'],
                'confidence': results['confidence'],
                'detected_transposition': results['best_match_transposition']
            },
            'by_representation': {}
        }
        
        for repr_type, data in results['results_by_representation'].items():
            report['by_representation'][repr_type] = {
                'similarity': round(data['similarity'], 1),
                'normalized_distance': round(data['normalized'], 3),
                'best_transposition': data['transposition'],
                'strength': self._get_strength(data['similarity'])
            }
        
        return report
    
    @staticmethod
    def _get_strength(similarity):
        """Classifica la forza della similarità"""
        if similarity > 80:
            return "MOLTO FORTE ⭐⭐⭐⭐⭐"
        elif similarity > 60:
            return "FORTE ⭐⭐⭐⭐"
        elif similarity > 40:
            return "MODERATO ⭐⭐⭐"
        elif similarity > 20:
            return "DEBOLE ⭐⭐"
        else:
            return "MOLTO DEBOLE ⭐"
