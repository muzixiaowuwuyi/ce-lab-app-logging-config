import logging
import os
import time
import uuid
from flask import Flask, request
import structlog

# 1. 确保日志目录存在
LOG_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_PATH = os.path.join(LOG_DIR, "application.log")

# 2. 配置 Python 标准 logging 作为底层输出管道（同时输出到控制台和文件）
# 生产环境中，通常会配置 RotatingFileHandler 以防止单文件过大
file_handler = logging.FileHandler(LOG_FILE_PATH, encoding="utf-8")
console_handler = logging.StreamHandler()

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",  # structlog 会负责整行日志的格式化，这里只需要输出 message 即可
    handlers=[file_handler, console_handler],
)

# 3. 配置 structlog 处理器链
structlog.configure(
    processors=[
        # 添加时间戳，并指定为标准 ISO-8601 格式
        structlog.processors.TimeStamper(fmt="iso"),
        # 自动添加日志级别（info, warn, error 等）
        structlog.stdlib.add_log_level,
        # 核心：将所有参数渲染为标准的 JSON 字符串
        structlog.processors.JSONRenderer(),
    ],
    # 绑定到底层标准的 logging 模块
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()
app = Flask(__name__)


@app.route("/")
def index():
    # 获取或生成 Correlation ID（相关性 ID）
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))

    logger.info(
        "request_received",
        correlation_id=correlation_id,
        path="/",
        method=request.method,
        ip=request.remote_addr,
    )

    return {"message": "Hello World", "correlation_id": correlation_id}


@app.route("/health")
def health():
    logger.info("health_check", status="healthy")
    return {"status": "healthy"}


@app.route("/order", methods=["POST"])
def create_order():
    correlation_id = str(uuid.uuid4())
    # 容错处理：防止请求体为空导致报错
    data = request.get_json() or {}

    logger.info(
        "order_created",
        correlation_id=correlation_id,
        order_id=f"ord-{uuid.uuid4().hex[:8]}",
        amount=data.get("amount", 0),
        items=data.get("items", 0),
        user_id=data.get("user_id"),
    )

    return {"status": "created", "correlation_id": correlation_id}


if __name__ == "__main__":
    logger.info("application_started", port=5000)
    # 提醒：实际生成的日志路径，方便你在本地测试时 tail -f 查看
    print(f"[*] App running. Logs are being written to: {LOG_FILE_PATH}")
    app.run(host="0.0.0.0", port=5000)