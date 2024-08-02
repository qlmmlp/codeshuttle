class Logger:
    @staticmethod
    def log(message: str, level: str = "INFO"):
        print(f"{level}: {message}")