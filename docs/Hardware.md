# Hardware

## Raspberry Pi 3 Model B+

[Product link](https://www.pi-shop.ch/raspberry-pi-3-model-b)

### 1. Install Raspberry Pi OS

Use `Raspberry Pi Imager` to install Raspberry Pi OS onto a microSD card. During OS customisation, configure:

- A hostname
- Wifi network
- Username and password
- SSH enabled

### 2. Connect from your computer

Test connection to Raspberry Pi using command line:

```bash
ping <hostname>.local
```

Connect to the host using command line:

```bash
ssh <username>@<hostname>.local
```

_Note_: If `local` does not resolve, use its IP address.

Update the system:

```bash
sudo apt update
sudo apt full-upgrade -y
sudo reboot
```

### 3. Install development tools

Reconnect after reboot, then install Python toolchain:

```bash
sudo apt install -y \
  git \
  python3 \
  python3-venv \
  python3-pip \
  python3-gpiozero
```

### 4. Generate an SSH key

Create an SSH key for the Raspberry Pi:

```bash
ssh-keygen -t ed25519
```

Display and copy the public key to your GitHub account:

```bash
cat ~/.ssh/id_ed25519.pub
```

Test the SSH connection:

```bash
ssh -T git@github.com
```

### 5. Clone the project

Clone the existing project repository:

```bash
git clone git@github.com:USERNAME/AutonomousLegoTechnicCar.git
```

Replace `USERNAME` with your GitHub username.

## 6. Install project dependencies

From the project directory, create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install project dependencies from `requirements.txt`:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Raspberry Pi Camera Module 3 Wide

[Product link](https://www.pi-shop.ch/raspberry-pi-camera-3-wide)
