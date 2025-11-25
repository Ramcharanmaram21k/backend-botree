from gs_properties import GSProperties

class Category:
    @staticmethod
    def predict_category_from_text(text):
        t = (text or "").lower()
        for cat, kws in GSProperties.category_keywords.items():
            for kw in kws:
                if kw in t: return cat
        return "General Complaint"