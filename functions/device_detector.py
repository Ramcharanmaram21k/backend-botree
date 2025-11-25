class DeviceDetector:
    @staticmethod
    def detect_device(user_agent: str) -> str:
        ua = user_agent.lower()

        if "okhttp" in ua or "dalvik" in ua:
            return "Android App"
        if "android" in ua and "mobile" in ua:
            return "Android Mobile"
        if "android" in ua and "mobile" not in ua:
            return "Android Tablet"
        if "iphone" in ua:
            return "iPhone"
        if "ipad" in ua:
            return "iPad"
        if "wv" in ua or "; wv" in ua:
            return "Mobile WebView"
        if "windows nt" in ua or "macintosh" in ua or "linux x86_64" in ua:
            return "Desktop"
        if "mobile" in ua:
            return "Mobile Web"

        return "Unknown"
