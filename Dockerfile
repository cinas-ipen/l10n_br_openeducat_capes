FROM odoo:19.0

USER root

# Instalação de dependências de sistema e compiladores para pacotes criptográficos/MEC
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    python3-dev \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    qpdf \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Instalação de dependências Python para PIDs, Criptografia XAdES, QWeb e APIs REST
RUN pip install --no-cache-dir --break-system-packages \
    cryptography \
    pyjwt \
    requests \
    qrcode \
    pillow \
    lxml \
    xmltodict

# Criação dos diretórios de addons e permissões
RUN mkdir -p /mnt/extra-addons /mnt/external-addons \
    && chown -R odoo:odoo /mnt/extra-addons /mnt/external-addons

USER odoo

EXPOSE 8069 8072
