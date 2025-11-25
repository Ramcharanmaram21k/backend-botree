class Sentiment:
    @staticmethod
    def predict_sentiment(text):
        t = (text or "").lower()
        urgent = ["urgent", "immediately", "danger", "accident", "help", "injury", "bleeding", "fire"]
        negative = ["not working", "no water", "no electricity", "delay", "complain", "complaint"]
        positive = ["thanks", "resolved", "good"]
        if any(w in t for w in urgent): return "Very Negative"
        if any(w in t for w in negative): return "Negative"
        if any(w in t for w in positive): return "Positive"
        return "Neutral"