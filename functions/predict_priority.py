from gs_properties import GSProperties

class Priority:
    @staticmethod
    def compute_priority_score(category, sentiment, has_image=False, has_video=False, has_audio=False, rec_loc=False,
                               rec_dept=False):
        base = GSProperties.category_base.get(category, 30)
        cat_contrib = 0.40 * base
        s_raw = GSProperties.sentiment_score.get(sentiment, 0)
        s_clamped = max(-20, min(30, s_raw))
        s_norm = (s_clamped + 20) / 50.0
        sent_contrib = 0.20 * (s_norm * 100)
        evidence_raw = 0
        if has_image: evidence_raw += 10
        if has_video: evidence_raw += 10
        if has_audio: evidence_raw += 5
        evidence_raw = min(25, evidence_raw)
        evidence_contrib = 0.20 * (evidence_raw / 25.0 * 100)
        recurrence_raw = 0
        if rec_loc: recurrence_raw += 20
        if rec_dept: recurrence_raw += 10
        recurrence_raw = min(30, recurrence_raw)
        recurrence_contrib = 0.20 * (recurrence_raw / 30.0 * 100)
        final_priority = cat_contrib + sent_contrib + evidence_contrib + recurrence_contrib
        final_priority = round(max(0.0, min(100.0, final_priority)), 2)
        if final_priority >= 80: return final_priority, "Priority A"
        if final_priority >= 50: return final_priority, "Priority B"
        if final_priority >= 20: return final_priority, "Priority C"
        return final_priority, "Priority D"