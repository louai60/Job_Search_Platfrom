from django.core.cache import cache
from collections import defaultdict

class SkillsStandardizer:
    def __init__(self):
        self.skills_mapping = self._load_skills_mapping()

    def _load_skills_mapping(self):
        # Load from cache first
        mapping = cache.get('skills_mapping')
        if mapping:
            return mapping

        # If not in cache, load from database or file
        mapping = {
            # Example mappings
            "python": "Python",
            "py": "Python",
            "javascript": "JavaScript",
            "js": "JavaScript",
            "react": "React.js",
            "reactjs": "React.js",
            # Add more mappings
        }
        
        # Cache the mapping
        cache.set('skills_mapping', mapping, timeout=86400)  # 24 hours
        return mapping

    def standardize(self, skills_dict):
        standardized = defaultdict(list)
        
        for category, skills in skills_dict.items():
            for skill in skills:
                skill_lower = skill.lower()
                standardized_skill = self.skills_mapping.get(skill_lower, skill)
                standardized[category].append(standardized_skill)
        
        return dict(standardized)

standardizer = SkillsStandardizer()

def standardize_skills(skills_dict):
    return standardizer.standardize(skills_dict) 