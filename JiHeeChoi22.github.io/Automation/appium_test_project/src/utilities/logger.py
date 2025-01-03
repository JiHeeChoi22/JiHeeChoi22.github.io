import logging
import json
from datetime import datetime
from logging.handlers import RotatingFileHandler
import os

class Logger:
    _logger = None
    
    @staticmethod
    def get_logger():
        """싱글톤 로거 인스턴스 반환"""
        if Logger._logger is None:
            Logger._logger = Logger._setup_logger()
        return Logger._logger
    
    @staticmethod
    def _setup_logger():
        """로거 설정"""
        logger = logging.getLogger('AppiumTest')
        logger.setLevel(logging.DEBUG)
        
        # 로그 포맷 설정
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # 파일 핸들러 설정
        log_dir = os.path.join('reports', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(
            log_dir, 
            f'test_run_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        )
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # 콘솔 핸들러 설정
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # 핸들러 추가
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    @staticmethod
    def log_test_step(description):
        """테스트 단계 로깅 데코레이터"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                logger = Logger.get_logger()
                logger.info(f"테스트 단계 시작: {description}")
                try:
                    result = func(*args, **kwargs)
                    logger.info(f"테스트 단계 완료: {description}")
                    return result
                except Exception as e:
                    logger.error(f"테스트 단계 실패: {description}, 에러: {str(e)}")
                    raise
            return wrapper
        return decorator
    
    @staticmethod
    def log_performance(threshold_ms=1000):
        """성능 로깅 데코레이터"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                logger = Logger.get_logger()
                start_time = datetime.now()
                try:
                    result = func(*args, **kwargs)
                    execution_time = (datetime.now() - start_time).total_seconds() * 1000
                    
                    if execution_time > threshold_ms:
                        logger.warning(
                            f"성능 경고: {func.__name__} 실행 시간 {execution_time:.2f}ms"
                            f" (임계값: {threshold_ms}ms)"
                        )
                    else:
                        logger.debug(
                            f"성능 측정: {func.__name__} 실행 시간 {execution_time:.2f}ms"
                        )
                    return result
                except Exception as e:
                    logger.error(f"함수 실행 실패: {func.__name__}, 에러: {str(e)}")
                    raise
            return wrapper
        return decorator 