# The clean-room environment for smoke-testing the agent library.
# The image is only the environment spec: the library and the test
# script mount in at run time — nothing library-specific is baked in,
# so the image never needs rebuilding when the library changes.
FROM python:3.12-slim

# curl and ca-certificates for the Vibe installer, git for optional
# fixture clones, libicu76 for pwsh (.NET aborts without ICU; Debian
# trixie's build — pin the package with the base image's Debian).
# Everything else the CLI brings itself.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates curl git libicu76 \
    && rm -rf /var/lib/apt/lists/*

# PowerShell, for the Windows-installer parity test (smoke/parity.sh):
# install.ps1's composition runs under the cross-platform pwsh, so
# byte-identity with install.py is testable without a Windows kernel
# — a Linux host cannot run Windows containers. Pinned version; the
# build fails loudly if the release asset moves.
ARG POWERSHELL_VERSION=7.6.6
RUN mkdir -p /opt/microsoft/powershell/7 \
    && curl -LsS "https://github.com/PowerShell/PowerShell/releases/download/v${POWERSHELL_VERSION}/powershell-${POWERSHELL_VERSION}-linux-x64.tar.gz" \
    | tar -xz -C /opt/microsoft/powershell/7 \
    && ln -s /opt/microsoft/powershell/7/pwsh /usr/local/bin/pwsh \
    && pwsh --version

# Never root inside the clean room: a write outside HOME must fail
# for the right reason, not because permissions were missing.
RUN useradd --create-home --shell /bin/bash vibe
USER vibe
WORKDIR /home/vibe

# The official one-line installer (docs.mistral.ai, Vibe Code > CLI >
# Install and setup): installs uv if needed, then mistral-vibe as a uv
# tool, exposing `vibe` and `vibe-acp` under ~/.local/bin. PATH must
# be exported first — the installer exits non-zero when its own
# installed command is not on PATH.
ENV PATH="/home/vibe/.local/bin:${PATH}"
RUN curl -LsSf https://mistral.ai/vibe/install.sh | bash

# A broken CLI install must fail the image build, not the smoke run.
RUN vibe --version

# The smoke script arrives with the read-only library mount:
#   docker run --rm -e MISTRAL_API_KEY \
#     -v "$(pwd)":/library:ro mistral-agents-smoke /library/smoke/smoke.sh
ENTRYPOINT ["/bin/bash"]
