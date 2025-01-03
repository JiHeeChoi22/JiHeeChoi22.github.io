# Appium 모바일 테스트 자동화 프로젝트

## 1. 프로젝트 개요
### 목적
- 모바일 앱 자동화 테스트 역량 강화
- Appium을 활용한 실제 앱 테스트 자동화 구현
- 체계적인 테스트 프레임워크 구축

### 대상 애플리케이션
- 안드로이드/iOS 기본 계산기 앱

### 개발 환경
- Language: Python 3.8+
- Framework: 
  - Appium 2.0
  - pytest

## 2. 프로젝트 구조
```
appium-test-project/
├── src/
│   ├── page_objects/
│   │   ├── base/
│   │   │   └── base_page.py      # 기본 페이지 객체
│   │   ├── android/
│   │   │   └── calculator_page.py # 안드로이드 계산기
│   │   └── ios/
│   │       └── calculator_page.py # iOS 계산기
│   └── utilities/
│       ├── driver_manager.py      # Appium 드라이버 관리
│       └── logger.py             # 로깅 유틸리티
├── tests/
│   ├── calculator/
│   │   ├── test_basic_operations.py
│   │   ├── test_complex_operations.py
│   │   ├── test_boundary_cases.py
│   │   ├── test_negative_numbers.py
│   │   ├── test_memory_functions.py
│   │   └── test_error_handling.py
│   └── conftest.py
├── configs/
│   ├── android_config.json       # 안드로이드 설정
│   ├── ios_config.json          # iOS 설정
│   └── logging_config.yaml      # 로깅 설정
└── reports/
    ├── screenshots/             # 실패 스크린샷
    ├── logs/                    # 실행 로그
    └── test_results/           # HTML 테스트 리포트
```

## 3. 주요 구현 기능

### 3.1 로깅 시스템
```python
class Logger:
    @staticmethod
    def _setup_logger():
        """로거 설정"""
        logger = logging.getLogger('AppiumTest')
        logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # 파일 핸들러 설정 (10MB 단위로 로테이션)
        file_handler = RotatingFileHandler(
            f'reports/logs/test_run_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
            maxBytes=10*1024*1024,
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # 콘솔 출력 설정
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        return logger
```

### 3.2 Page Object Pattern
```python
class CalculatorPage(BasePage):
    """안드로이드 계산기 페이지 객체"""
    
    # 요소 식별자
    DIGIT_IDS = {
        '0': 'com.android.calculator2:id/digit_0',
        '1': 'com.android.calculator2:id/digit_1',
        # ...
    }
    
    def calculate(self, expression):
        """수식 계산 (예: "5+3")"""
        self.logger.info(f"수식 계산 시작: {expression}")
        try:
            self.clear()
            current_number = ''
            
            for char in expression:
                if char.isdigit():
                    current_number += char
                elif char in self.OPERATION_IDS.keys():
                    if current_number:
                        for digit in current_number:
                            self.click_number(digit)
                        current_number = ''
                    self.click_operation(char)
            
            self.click_equals()
            result = self.get_result()
            self.logger.info(f"계산 결과: {result}")
            return result
        except Exception as e:
            self.logger.error(f"계산 실패: {expression}, 에러: {str(e)}")
            raise
```

### 3.3 테스트 데코레이터
```python
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
                return result
            except Exception as e:
                logger.error(f"함수 실행 실패: {func.__name__}, 에러: {str(e)}")
                raise
        return wrapper
    return decorator
```

### 3.4 테스트 케이스 구현
```python
@pytest.mark.basic
class TestBasicOperations:
    """기본 계산기 기능 테스트"""
    
    @Logger.log_test_step("기본 덧셈 연산")
    def test_addition(self, setup):
        """덧셈 테스트"""
        result = self.calculator.calculate("5+3")
        assert result == "8"

@pytest.mark.error
class TestErrorHandling:
    """에러 처리 테스트"""
    
    def test_division_by_zero(self, setup):
        """0으로 나누기 테스트"""
        result = self.calculator.calculate("5/0")
        assert "Error" in result or "∞" in result
```

## 4. 품질 관리
- 구조화된 로깅 시스템
  - 파일 및 콘솔 동시 출력
  - 로그 파일 자동 로테이션
  - 로그 레벨별 필터링
- 성능 모니터링
  - 테스트 실행 시간 측정
  - 임계값 초과 시 경고
- 테스트 실행 추적
  - 단계별 로깅
  - 예외 상황 자동 기록

## 5. 향후 계획
- 병렬 테스트 실행 구현
- 테스트 데이터 확장
- 성능 테스트 추가
- iOS 지원 추가
