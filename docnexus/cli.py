#!/usr/bin/env python
"""
Command-line interface for Markdown Documentation Viewer
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path to import docnexus
sys.path.insert(0, str(Path(__file__).parent.parent))

from docnexus import __version__, __description__


def print_version():
    """Print version information."""
    print(f"Markdown Documentation Viewer v{__version__}")
    print(f"{__description__}")


def start_server(args):
    """Start the Flask server."""
    from docnexus.app import app
    
    host = args.host or 'localhost'
    port = args.port or 8000
    debug = args.debug
    
    print(f"Starting DocNexus v{__version__}")
    print(f"Server: http://{host}:{port}")
    print(f"Documentation: http://{host}:{port}/docs")
    print("Press Ctrl+C to stop")
    print()
    
    app.run(host=host, port=port, debug=debug)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description=f'DocNexus v{__version__}',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  docnexus --version              Show version information
  docnexus start                  Start server on localhost:8000
  docnexus start --port 8080      Start server on port 8080
  docnexus start --debug          Start server in debug mode
        """
    )
    
    parser.add_argument(
        '--version', '-v',
        action='store_true',
        help='Show version information'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Start command
    start_parser = subparsers.add_parser('start', help='Start the documentation server')
    start_parser.add_argument(
        '--host',
        type=str,
        default='localhost',
        help='Host to bind to (default: localhost)'
    )
    start_parser.add_argument(
        '--port', '-p',
        type=int,
        default=8000,
        help='Port to bind to (default: 8000)'
    )
    start_parser.add_argument(
        '--debug', '-d',
        action='store_true',
        help='Run in debug mode'
    )
    
    args = parser.parse_args()
    
    if args.version:
        print_version()
        return 0
    
    if args.command == 'start':
        try:
            start_server(args)
            return 0
        except KeyboardInterrupt:
            print("\nServer stopped.")
            return 0
        except Exception as e:
            print(f"Error starting server: {e}", file=sys.stderr)
            return 1
    
    # If no command specified, show version and help
    if not args.command:
        print_version()
        print()
        parser.print_help()
        return 0
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
