import logging
from logging.handlers import TimedRotatingFileHandler
from multiprocessing import Process, Queue
from queue import Empty

class MultiProcessingTimedRotatingFileHandler(logging.Handler):
    def __init__(self, log_file_name, when="midnight", interval=1, backupCount=31):
        super().__init__()
        self.queue = Queue(-1)
        self.log_file_name = log_file_name
        self.when = when
        self.interval = interval
        self.backupCount = backupCount
        self.listener_process = Process(target=self.listener)
        self.listener_process.start()

    def listener(self):
        while True:
            try:
                record = self.queue.get(timeout=0.1)
                if record is None:
                    break
                logger = logging.getLogger(record.name)
                if not logger.handlers:
                    handler = TimedRotatingFileHandler(
                        self.log_file_name, when=self.when, 
                        interval=self.interval, backupCount=self.backupCount
                    )
                    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
                    logger.addHandler(handler)
                if record:
                    logger.handle(record)
            except Empty:
                continue

    def emit(self, record):
        self.queue.put(record)

    def close(self):
        self.queue.put(None)
        self.listener_process.join()
        super().close()

def create_logger(name, log_file_name):
    handler = MultiProcessingTimedRotatingFileHandler(log_file_name)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


# 创建日志记录器，可创建多个
logger = create_logger("secure_logger", "logs/secure.log")
# logger_secure = create_logger("llm_logger", "./logs/llm.log")
# logger_api = create_logger("api_logger", "./logs/chat_api.log")

logger.info(f"【start】secuer日志记录器创建成功")
# logger.info(f"request_id:request_id_er; 【start】请求数据错误信息")
# logger_api.info(f"request_id:request_id; 【start】进入逻辑")

print('日志创建启动完成。')