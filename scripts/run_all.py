#!/usr/bin/env python3
"""
Batch runner for all active clients in the automatic email application.
This script processes all active clients and sends their scheduled emails.
"""

import sys
import os
import logging
from pathlib import Path

# Add src to Python path so we can import modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.main import run_client_campaign

def main():
    """Run email campaigns for all active clients."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('automatic_emails.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    logger.info("Starting batch processing for all active clients")
    
    # Get the clients directory
    clients_dir = Path("clients")
    
    if not clients_dir.exists():
        logger.error(f"Clients directory {clients_dir} does not exist")
        return 1
    
    # Find all client directories
    client_dirs = [d for d in clients_dir.iterdir() if d.is_dir()]
    
    if not client_dirs:
        logger.warning("No client directories found")
        return 0
    
    logger.info(f"Found {len(client_dirs)} client directories")
    
    success_count = 0
    failed_count = 0
    
    # Process each client directory
    for client_dir in client_dirs:
        client_name = client_dir.name
        
        try:
            logger.info(f"Processing client: {client_name}")
            
            # Run the campaign for this client
            result = run_client_campaign(client_name)
            
            if result:
                logger.info(f"Successfully processed client: {client_name}")
                success_count += 1
            else:
                logger.error(f"Failed to process client: {client_name}")
                failed_count += 1
                
        except Exception as e:
            logger.error(f"Error processing client {client_name}: {str(e)}")
            failed_count += 1
    
    logger.info(f"Batch processing complete. Successful: {success_count}, Failed: {failed_count}")
    
    return 0 if failed_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())