#!/usr/bin/env bash
# ============================================================================
# install-openclaw-nvidia.sh
# Install OpenClaw with NVIDIA NemoClaw safety guardrails
#
# Based on NVIDIA's official safety guide:
#   https://github.com/NVIDIA/NemoClaw
#   https://github.com/NVIDIA/OpenShell/blob/main/examples/openclaw.md
#
# SAFETY WARNING:
#   OpenClaw is an AI agent that can access files, execute commands, and
#   connect to external services. NVIDIA strongly recommends:
#     - Run on an isolated system or VM
#     - Use dedicated accounts (not your main accounts)
#     - Never expose the dashboard to the public internet without auth
# ============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info()  { echo -e "${GREEN}[INFO]${NC}  $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

# ---------------------------------------------------------------------------
# Safety disclaimer
# ---------------------------------------------------------------------------
echo ""
echo "============================================================"
echo "  NVIDIA NemoClaw + OpenClaw Installation"
echo "  Safety-First Setup for Roofers AI"
echo "============================================================"
echo ""
echo "IMPORTANT SAFETY NOTICE (from NVIDIA's guide):"
echo "  - OpenClaw agents can access files, run commands, and"
echo "    connect to external services."
echo "  - Data exposure and malicious code execution are real risks."
echo "  - Run on an isolated system or VM when possible."
echo "  - Use dedicated accounts, not your main accounts."
echo "  - Never expose the dashboard publicly without authentication."
echo ""
read -rp "Do you understand the risks and want to proceed? [y/N] " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    log_info "Installation cancelled."
    exit 0
fi

# ---------------------------------------------------------------------------
# Step 1: Check prerequisites
# ---------------------------------------------------------------------------
log_info "Checking prerequisites..."

# Check OS
if [[ "$(uname -s)" != "Linux" ]]; then
    log_warn "This script is optimized for Linux (Ubuntu 22.04+)."
    log_warn "For macOS/Windows WSL, see: https://github.com/NVIDIA/NemoClaw"
fi

# Check Docker
if ! command -v docker &>/dev/null; then
    log_error "Docker is required but not installed."
    log_info "Install Docker: https://docs.docker.com/engine/install/"
    exit 1
fi
log_info "Docker found: $(docker --version)"

# Check Node.js (v20+)
if command -v node &>/dev/null; then
    NODE_VERSION=$(node -v | sed 's/v//' | cut -d. -f1)
    if (( NODE_VERSION < 20 )); then
        log_warn "Node.js v20+ required, found v$(node -v). NemoClaw installer will upgrade."
    else
        log_info "Node.js found: $(node -v)"
    fi
else
    log_warn "Node.js not found. NemoClaw installer will install it."
fi

# Check available disk space (need 20GB minimum)
AVAILABLE_GB=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
if (( AVAILABLE_GB < 20 )); then
    log_error "At least 20 GB free disk space required (found ${AVAILABLE_GB}G)."
    log_error "40 GB recommended (sandbox image is ~2.4 GB compressed)."
    exit 1
fi
log_info "Disk space: ${AVAILABLE_GB}G available (20G min, 40G recommended)"

# Check RAM
TOTAL_RAM_KB=$(grep MemTotal /proc/meminfo 2>/dev/null | awk '{print $2}' || echo 0)
TOTAL_RAM_GB=$(( TOTAL_RAM_KB / 1024 / 1024 ))
if (( TOTAL_RAM_GB < 8 )); then
    log_warn "8 GB RAM minimum (16 GB recommended). Found ~${TOTAL_RAM_GB}G."
    log_warn "Systems with <8 GB RAM may need 8 GB swap to avoid OOM."
fi

# ---------------------------------------------------------------------------
# Step 2: Install NemoClaw (includes OpenShell + OpenClaw sandbox)
# ---------------------------------------------------------------------------
log_info "Installing NVIDIA NemoClaw..."
log_info "This runs NVIDIA's official installer which will:"
log_info "  1. Install Node.js if absent"
log_info "  2. Launch an interactive onboarding wizard"
log_info "  3. Create a sandboxed OpenClaw environment"
log_info "  4. Configure inference settings"
log_info "  5. Apply security policies"
echo ""

curl -fsSL https://www.nvidia.com/nemoclaw.sh | bash

# ---------------------------------------------------------------------------
# Step 3: Ensure PATH is updated
# ---------------------------------------------------------------------------
log_info "Updating shell PATH..."
if [[ -f "$HOME/.bashrc" ]]; then
    # shellcheck disable=SC1091
    source "$HOME/.bashrc" 2>/dev/null || true
fi
if [[ -f "$HOME/.zshrc" ]]; then
    # shellcheck disable=SC1091
    source "$HOME/.zshrc" 2>/dev/null || true
fi

# ---------------------------------------------------------------------------
# Step 4: Verify installation
# ---------------------------------------------------------------------------
log_info "Verifying installation..."

if command -v nemoclaw &>/dev/null; then
    log_info "NemoClaw installed successfully."
else
    log_warn "nemoclaw command not found in PATH."
    log_warn "Try opening a new terminal or run: source ~/.bashrc"
fi

if command -v openshell &>/dev/null; then
    log_info "OpenShell installed successfully."
else
    log_warn "openshell command not found in PATH."
fi

# ---------------------------------------------------------------------------
# Step 5: Print post-install safety guide
# ---------------------------------------------------------------------------
echo ""
echo "============================================================"
echo "  Installation Complete - Safety Quick Reference"
echo "============================================================"
echo ""
echo "NVIDIA NemoClaw applies 4 layers of protection:"
echo "  1. Network   - Blocks unauthorized outbound connections"
echo "  2. Filesystem - Restricts access to /sandbox and /tmp only"
echo "  3. Process   - Prevents privilege escalation & dangerous syscalls"
echo "  4. Inference - Routes model calls through controlled backends"
echo ""
echo "Essential commands:"
echo "  nemoclaw my-assistant connect   # Open sandbox shell"
echo "  nemoclaw my-assistant status    # Check sandbox health"
echo "  nemoclaw my-assistant logs -f   # Stream live logs"
echo "  openshell term                  # Monitor & approve requests"
echo ""
echo "Inside the sandbox:"
echo "  openclaw tui                    # Interactive chat (TUI)"
echo "  openclaw health                 # Check health status"
echo ""
echo "Network policies: nemoclaw-blueprint/policies/openclaw-sandbox.yaml"
echo "Credentials:      ~/.nemoclaw/credentials.json"
echo ""
echo "Dashboard (local only): http://127.0.0.1:18789/"
echo ""
echo "Docs: https://github.com/NVIDIA/NemoClaw"
echo "============================================================"
