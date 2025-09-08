import argparse
import os
from urllib.parse import urlparse

# Nginx configuration template using the relative path substitution strategy.
NGINX_TEMPLATE = """
server {{
    listen {port};

    # Logs for this specific proxy for easier debugging
    access_log /var/log/nginx/{name}-proxy-access.log;
    error_log /var/log/nginx/{name}-proxy-error.log;

    location / {{
        # --- Backend Service ---
        proxy_pass {target_url};

        # --- Standard Proxy Headers ---
        proxy_set_header Host {target_host};
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Accept-Encoding ""; # Let Nginx handle compression

        # --- Content & Redirect Rewriting (to Relative Paths) ---
        # Replaces "https://www.example.com" with "" to make links relative
        sub_filter '{target_url_base}' '';
        # Replaces "//www.example.com" with "" for protocol-relative URLs
        sub_filter '//{target_host}' '';
        sub_filter_once off; # Apply filter to all occurrences
        sub_filter_types text/html text/css application/javascript; # Apply to these content types

        # Rewrites 3xx redirect headers to be relative
        proxy_redirect {target_url_base}/ /;
    }}
}}
"""

def main():
    """Main function to parse arguments and generate the config file."""
    parser = argparse.ArgumentParser(
        description="Nginx Reverse Proxy Config Generator",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--name", 
        required=True, 
        help="A short, file-safe name for the service (e.g., peanutbase)"
    )
    parser.add_argument(
        "--url", 
        required=True, 
        help="The full target URL to proxy (e.g., https://www.peanutbase.org)"
    )
    parser.add_argument(
        "--port", 
        required=True, 
        type=int, 
        help="The local port for Nginx to listen on (e.g., 2027)"
    )
    parser.add_argument(
        "--output-dir", 
        default="./confs", 
        help="Directory to save the config file (defaults to current directory)"
    )

    args = parser.parse_args()

    # Extract components from the target URL
    try:
        parsed_url = urlparse(args.url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid URL format. Please include scheme (http/https) and hostname.")
        target_host = parsed_url.netloc
        target_url_base = f"{parsed_url.scheme}://{target_host}"
    except ValueError as e:
        print(f"Error parsing URL: {e}")
        return

    # Populate the template with the provided arguments
    config_content = NGINX_TEMPLATE.format(
        port=args.port,
        name=args.name,
        target_url=args.url,
        target_host=target_host,
        target_url_base=target_url_base,
    ).strip()

    # Define the output file path
    output_filename = f"{args.name}.conf"

    # Check if the output path existed
    if not os.path.exists(args.output_dir):
        print("-" * 60)
        print(f"Output path not exists. Creating: '{args.output_dir}':")
        print("-" * 60)
        os.mkdir(args.output_dir)
    output_path = os.path.join(args.output_dir, output_filename)

    # --- Output and File Writing ---
    print("-" * 60)
    print(f"Generated Nginx config for '{args.name}':")
    print("-" * 60)
    print(config_content)
    print("-" * 60)

    try:
        with open(output_path, "w") as f:
            f.write(config_content)
        print(f"\nSuccessfully wrote configuration to: {output_path}")
        print("\nTo use this configuration:")
        print(f"1. Move it to your Nginx configuration directory:")
        print(f"   sudo mv {output_path} /etc/nginx/conf.d/{output_filename}")
        print("\n2. Test and reload Nginx:")
        print("   sudo nginx -t && sudo systemctl reload nginx")

    except PermissionError:
        print(f"\nError: Permission denied to write to {output_path}.")
        print("Try running the script with sudo or specify a different --output-dir.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
