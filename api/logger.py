import logging
import json
from datetime import datetime
import os

os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/openai_{datetime.now().strftime("%Y%m%d")}.log'),
    ]
)

logger = logging.getLogger('openai_api')

def log_api_call(endpoint, request_data, response, error=None):
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'endpoint': endpoint,
        'request': request_data,
        'response': str(response) if response else None,
        'error': str(error) if error else None
    }
    
    if error:
        logger.error(json.dumps(log_entry, indent=2))
    else:
        logger.info(json.dumps(log_entry, indent=2))
        