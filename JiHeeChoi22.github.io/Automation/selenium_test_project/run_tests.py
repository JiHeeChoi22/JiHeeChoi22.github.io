import pytest
import argparse
import logging
from datetime import datetime
import os

def setup_logging():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 로그 디렉토리 생성
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        filename=f'logs/test_run_{timestamp}.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # 콘솔에도 로그 출력
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def main():
    parser = argparse.ArgumentParser(description='테스트 실행 스크립트')
    parser.add_argument('--type', choices=['all', 'security', 'performance', 'functional'],
                       default='all', help='실행할 테스트 유형')
    parser.add_argument('--browser', choices=['chrome', 'firefox', 'edge'],
                       default='chrome', help='사용할 브라우저')
    parser.add_argument('--parallel', action='store_true',
                       help='병렬 실행 여부')
    parser.add_argument('--grid', action='store_true',
                        help='Selenium Grid 사용')
    
    args = parser.parse_args()
    setup_logging()
    
    pytest_args = ['-v']
    
    if args.parallel:
        try:
            import pytest_xdist
            pytest_args.extend(['-n', 'auto'])
        except ImportError:
            logging.warning("pytest-xdist가 설치되어 있지 않아 병렬 실행이 불가능합니다.")
    
    if args.type != 'all':
        pytest_args.extend(['-m', args.type])
    
    pytest_args.extend(['--browser', args.browser])
    if args.grid:
        pytest_args.append('--grid')
    
    logging.info(f'테스트 실행 시작: {args.type} tests')
    pytest.main(pytest_args)

if __name__ == '__main__':
    main() 