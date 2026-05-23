import random

class Misc:

    @staticmethod
    def loaderx():
        loader = [
            "🔄 Loading... Hold on tight!",
            "⏳ AI is brewing your content potion...",
            "🌟 The AI is working its magic...",
            "🤖 Processing your request... AI at work!",
        ]
        # BUG FIX: random range was 0-2 but list has 4 items (indices 0-3)
        n = random.randint(0, len(loader) - 1)
        return n, loader

    @staticmethod
    def footer():
        ft = """
        <style>
        a:link, a:visited {
            color: #BFBFBF;
            background-color: transparent;
            text-decoration: none;
        }
        a:hover, a:active {
            color: #0283C3;
            background-color: transparent;
            text-decoration: underline;
        }
        footer { visibility: hidden; }
        .footer {
            position: relative;
            left: 0;
            top: -20px;
            bottom: 0;
            width: 100%;
            background-color: transparent;
            color: #808080;
            text-align: center;
        }
        </style>
        
        """
        return ft