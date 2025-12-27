# ft_onion - Hidden Service Setup

A Docker-based hidden service deployment with SSH access and web interface through the Tor network.

## Description

ft_onion creates a hidden service (.onion site) running nginx web server and SSH server accessible only through the Tor network. The service provides both a web interface and secure SSH access.

## Architecture

Single Docker container running:
- **nginx** - Web server serving static content
- **SSH service** - Remote access on port 4242
- **Tor** - Creates hidden service with .onion address

## Installation

### 1. Start the service

```bash
docker compose up --build
```

### 2. Get your .onion address

```bash
docker compose exec ft_onion cat /var/lib/tor/hidden_service/hostname
```

This will output your unique `.onion` address (e.g., `abc123xyz456.onion`).

## SSH Key Setup

The SSH authentication uses a pre-generated key pair:

### Key Generation

```bash
ssh-keygen -t rsa -b 4096 -f onion_key -N ""
```

This creates:
- **`onion_key.pub`** - Public key (stored in repository)
- **`onion_key`** - Private key (stored on USB drive)

### Key Deployment

- **Public key**: Embedded in Docker image via `Dockerfile:8`
  ```dockerfile
  COPY onion_key.pub /home/onion/.ssh/authorized_keys
  ```
- **Private key**: Stored on **USB flash drive** for security
  - NOT committed to repository
  - Required for SSH connection
  - Keep on physical media for evaluation

## Usage

### Accessing the Web Interface

```bash
# Download Tor Browser
wget https://www.torproject.org/dist/torbrowser/15.0.3/tor-browser-linux-x86_64-15.0.3.tar.xz

# Extract
tar -xvf tor-browser-linux-x86_64-15.0.3.tar.xz

# Run
cd tor-browser
./start-tor-browser.desktop
```

Once Tor Browser is running, navigate to your `.onion` address.

### SSH Access

Connect to the hidden service via SSH using the private key from USB drive:

```bash
torsocks ssh -i /path/to/usb/onion_key -p 4242 onion@<onion_address>
```

## Important Notes for School Evaluation

### Tor Browser Installation
- Tor Browser **can be installed** on school machines using `wget` (see instructions above)
- No special permissions required
- Download and run from user directory

### SSH Connection Requirements
- **SSH access requires `torsocks`** utility
- `torsocks` is **NOT available** on school machines by default
- **For SSH demonstration, you must bring:**
  - **Personal laptop** with `torsocks` installed, OR
  - **Virtual machine** with `torsocks` installed
  - **USB flash drive** with private key (`onion_key`)

### Installing torsocks (on personal machine/VM)

```bash
# Debian/Ubuntu
sudo apt-get install torsocks

# macOS
brew install torsocks
```

## Bonus

### Interactive Dark Web Marketplace (Demo)

The web interface features an **interactive Single Page Application (SPA)** styled as a dark web marketplace for demonstration purposes.

**Important:**
- This is a **fake/demo marketplace** for educational purposes only
- Product images powered by Unsplash API

### Unsplash API Setup

To display product images, you need to configure your Unsplash API key:

1. **Get API key** from [Unsplash Developers](https://unsplash.com/developers)
2. **Configure in your environment** or source code
3. Replace the placeholder with your actual key
