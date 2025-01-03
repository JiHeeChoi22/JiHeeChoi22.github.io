import pytest
import sys
import os

def run_tests():
    # 테스트 결과 디렉토리 생성
    os.makedirs('reports', exist_ok=True)
    
    # pytest 실행 인자
    args = [
        '-v',
        '--html=reports/report.html',
        '--self-contained-html',
        'tests'
    ]
    
    # 테스트 실행
    return pytest.main(args)

if __name__ == '__main__':
    sys.exit(run_tests()) 