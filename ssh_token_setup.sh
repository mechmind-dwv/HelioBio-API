#!/bin/bash
# =================================================================
# HelioBio-API - Script de Configuración de Credenciales
# Configuración de SSH y tokens de autenticación
# Autor: mechmind-dwv (ia.mechmind@gmail.com)
# =================================================================

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Funciones de utilidad
print_header() {
    echo -e "${BLUE}"
    echo "============================================================"
    echo "$1"
    echo "============================================================"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

# Banner
clear
print_header "HelioBio-API - Configuración de Credenciales y SSH"
echo -e "${BLUE}Autor: mechmind-dwv (ia.mechmind@gmail.com)${NC}\n"

# Variables
USER_EMAIL="ia.mechmind@gmail.com"
USER_NAME="mechmind-dwv"
SSH_KEY_NAME="heliobio_rsa"
SSH_DIR="$HOME/.ssh"
CREDENTIALS_DIR="$HOME/.heliobio/credentials"
TOKEN_FILE="$CREDENTIALS_DIR/tokens.json"
ENV_FILE=".env"

# Menú principal
show_menu() {
    echo -e "\n${CYAN}Seleccione una opción:${NC}"
    echo "1) Configurar SSH Keys para GitHub"
    echo "2) Generar tokens de autenticación"
    echo "3) Configurar credenciales de la aplicación"
    echo "4) Verificar configuración existente"
    echo "5) Backup de credenciales"
    echo "6) Configuración completa (todo lo anterior)"
    echo "0) Salir"
    echo -n "Opción: "
}

# =================================================================
# 1. CONFIGURACIÓN DE SSH KEYS
# =================================================================

configure_ssh_keys() {
    print_header "Configuración de SSH Keys para GitHub"
    
    # Crear directorio SSH si no existe
    mkdir -p "$SSH_DIR"
    chmod 700 "$SSH_DIR"
    
    # Verificar si ya existe una clave
    if [ -f "$SSH_DIR/$SSH_KEY_NAME" ]; then
        print_warning "Ya existe una clave SSH: $SSH_DIR/$SSH_KEY_NAME"
        read -p "¿Desea crear una nueva clave? (s/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Ss]$ ]]; then
            print_info "Usando clave existente"
            return 0
        fi
    fi
    
    # Solicitar email si no está definido
    read -p "Email para la clave SSH [$USER_EMAIL]: " input_email
    USER_EMAIL="${input_email:-$USER_EMAIL}"
    
    # Generar clave SSH
    print_info "Generando clave SSH..."
    ssh-keygen -t rsa -b 4096 -C "$USER_EMAIL" -f "$SSH_DIR/$SSH_KEY_NAME" -N ""
    
    if [ $? -eq 0 ]; then
        print_success "Clave SSH generada exitosamente"
        
        # Iniciar ssh-agent
        eval "$(ssh-agent -s)"
        ssh-add "$SSH_DIR/$SSH_KEY_NAME"
        
        # Crear o actualizar config de SSH
        SSH_CONFIG="$SSH_DIR/config"
        
        if ! grep -q "Host github.com" "$SSH_CONFIG" 2>/dev/null; then
            cat >> "$SSH_CONFIG" << EOF

# HelioBio-API GitHub Configuration
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/$SSH_KEY_NAME
    IdentitiesOnly yes
EOF
            print_success "Configuración SSH actualizada"
        fi
        
        # Mostrar clave pública
        echo ""
        print_info "Tu clave pública SSH (cópiala en GitHub):"
        echo -e "${GREEN}========================================${NC}"
        cat "$SSH_DIR/$SSH_KEY_NAME.pub"
        echo -e "${GREEN}========================================${NC}"
        echo ""
        
        print_info "Pasos para agregar la clave a GitHub:"
        echo "1. Ve a: https://github.com/settings/ssh/new"
        echo "2. Copia la clave pública mostrada arriba"
        echo "3. Dale un nombre descriptivo (ej: 'HelioBio-API Linux Mint')"
        echo "4. Pega la clave y guarda"
        echo ""
        
        read -p "Presiona Enter cuando hayas agregado la clave a GitHub..."
        
        # Probar conexión
        print_info "Probando conexión con GitHub..."
        if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
            print_success "Conexión SSH con GitHub configurada correctamente"
        else
            print_warning "No se pudo verificar la conexión. Verifica que agregaste la clave."
        fi
        
    else
        print_error "Error al generar clave SSH"
        return 1
    fi
}

# =================================================================
# 2. GENERAR TOKENS DE AUTENTICACIÓN
# =================================================================

generate_tokens() {
    print_header "Generación de Tokens de Autenticación"
    
    # Crear directorio de credenciales
    mkdir -p "$CREDENTIALS_DIR"
    chmod 700 "$CREDENTIALS_DIR"
    
    # Generar tokens
    print_info "Generando tokens seguros..."
    
    # Secret key para JWT
    SECRET_KEY=$(openssl rand -hex 32)
    
    # API Key
    API_KEY=$(openssl rand -hex 24)
    
    # Refresh token
    REFRESH_TOKEN=$(openssl rand -hex 32)
    
    # Database encryption key
    DB_ENCRYPTION_KEY=$(openssl rand -hex 16)
    
    # Crear archivo de tokens
    cat > "$TOKEN_FILE" << EOF
{
  "generated_at": "$(date -Iseconds)",
  "generated_by": "$USER_NAME",
  "tokens": {
    "jwt_secret_key": "$SECRET_KEY",
    "api_key": "$API_KEY",
    "refresh_token": "$REFRESH_TOKEN",
    "db_encryption_key": "$DB_ENCRYPTION_KEY"
  },
  "github": {
    "username": "$USER_NAME",
    "email": "$USER_EMAIL",
    "ssh_key_path": "$SSH_DIR/$SSH_KEY_NAME"
  }
}
EOF
    
    chmod 600 "$TOKEN_FILE"
    print_success "Tokens generados y guardados en: $TOKEN_FILE"
    
    # Actualizar .env
    if [ -f "$ENV_FILE" ]; then
        print_info "Actualizando archivo .env..."
        
        # Backup del .env actual
        cp "$ENV_FILE" "${ENV_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
        
        # Actualizar o agregar variables
        if grep -q "^SECRET_KEY=" "$ENV_FILE"; then
            sed -i "s|^SECRET_KEY=.*|SECRET_KEY=$SECRET_KEY|" "$ENV_FILE"
        else
            echo "SECRET_KEY=$SECRET_KEY" >> "$ENV_FILE"
        fi
        
        if grep -q "^API_KEY=" "$ENV_FILE"; then
            sed -i "s|^API_KEY=.*|API_KEY=$API_KEY|" "$ENV_FILE"
        else
            echo "API_KEY=$API_KEY" >> "$ENV_FILE"
        fi
        
        if grep -q "^DB_ENCRYPTION_KEY=" "$ENV_FILE"; then
            sed -i "s|^DB_ENCRYPTION_KEY=.*|DB_ENCRYPTION_KEY=$DB_ENCRYPTION_KEY|" "$ENV_FILE"
        else
            echo "DB_ENCRYPTION_KEY=$DB_ENCRYPTION_KEY" >> "$ENV_FILE"
        fi
        
        print_success "Archivo .env actualizado"
    else
        print_warning "Archivo .env no encontrado, creando uno nuevo..."
        cat > "$ENV_FILE" << EOF
# HelioBio-API Environment Variables
# Generated: $(date)

# Security
SECRET_KEY=$SECRET_KEY
API_KEY=$API_KEY
DB_ENCRYPTION_KEY=$DB_ENCRYPTION_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Author Info
AUTHOR_NAME=$USER_NAME
AUTHOR_EMAIL=$USER_EMAIL

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True
RELOAD=True

# Database
DATABASE_URL=sqlite:///./data/heliobio_database.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=./data/logs/heliobio.log
EOF
        chmod 600 "$ENV_FILE"
        print_success "Archivo .env creado"
    fi
    
    echo ""
    print_success "Tokens generados exitosamente:"
    echo -e "${CYAN}JWT Secret Key:${NC} $SECRET_KEY"
    echo -e "${CYAN}API Key:${NC} $API_KEY"
    echo ""
    print_warning "IMPORTANTE: Guarda estos tokens de forma segura"
}

# =================================================================
# 3. CONFIGURAR CREDENCIALES DE LA APLICACIÓN
# =================================================================

configure_app_credentials() {
    print_header "Configuración de Credenciales de la Aplicación"
    
    # Solicitar información
    read -p "Nombre de usuario GitHub [$USER_NAME]: " input_name
    USER_NAME="${input_name:-$USER_NAME}"
    
    read -p "Email [$USER_EMAIL]: " input_email
    USER_EMAIL="${input_email:-$USER_EMAIL}"
    
    # Configurar Git
    print_info "Configurando Git..."
    git config --global user.name "$USER_NAME"
    git config --global user.email "$USER_EMAIL"
    
    # Configurar credenciales de Git
    git config --global credential.helper store
    
    print_success "Git configurado para $USER_NAME ($USER_EMAIL)"
    
    # Verificar si existe repositorio remoto
    if [ -d .git ]; then
        print_info "Verificando repositorio remoto..."
        
        CURRENT_REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
        
        if [ -z "$CURRENT_REMOTE" ]; then
            read -p "URL del repositorio GitHub: " repo_url
            git remote add origin "$repo_url"
            print_success "Remoto configurado: $repo_url"
        else
            print_info "Remoto actual: $CURRENT_REMOTE"
            read -p "¿Desea cambiar el remoto? (s/n): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Ss]$ ]]; then
                read -p "Nueva URL del repositorio: " repo_url
                git remote set-url origin "$repo_url"
                print_success "Remoto actualizado: $repo_url"
            fi
        fi
    fi
    
    # Crear archivo de credenciales de aplicación
    APP_CREDS_FILE="$CREDENTIALS_DIR/app_credentials.json"
    cat > "$APP_CREDS_FILE" << EOF
{
  "updated_at": "$(date -Iseconds)",
  "application": {
    "name": "HelioBio-API",
    "version": "3.0.0",
    "author": "$USER_NAME",
    "email": "$USER_EMAIL"
  },
  "git": {
    "username": "$USER_NAME",
    "email": "$USER_EMAIL",
    "configured": true
  },
  "paths": {
    "ssh_dir": "$SSH_DIR",
    "credentials_dir": "$CREDENTIALS_DIR",
    "project_dir": "$(pwd)"
  }
}
EOF
    
    chmod 600 "$APP_CREDS_FILE"
    print_success "Credenciales de aplicación guardadas"
}

# =================================================================
# 4. VERIFICAR CONFIGURACIÓN
# =================================================================

verify_configuration() {
    print_header "Verificación de Configuración"
    
    echo -e "${CYAN}1. Verificando SSH...${NC}"
    if [ -f "$SSH_DIR/$SSH_KEY_NAME" ]; then
        print_success "Clave SSH encontrada: $SSH_DIR/$SSH_KEY_NAME"
        
        # Verificar permisos
        PERMS=$(stat -c %a "$SSH_DIR/$SSH_KEY_NAME")
        if [ "$PERMS" = "600" ]; then
            print_success "Permisos correctos (600)"
        else
            print_warning "Permisos incorrectos: $PERMS (debería ser 600)"
            chmod 600 "$SSH_DIR/$SSH_KEY_NAME"
            print_success "Permisos corregidos"
        fi
        
        # Probar conexión GitHub
        print_info "Probando conexión con GitHub..."
        if timeout 5 ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
            print_success "Conexión SSH con GitHub OK"
        else
            print_warning "No se pudo verificar conexión con GitHub"
        fi
    else
        print_warning "Clave SSH no encontrada"
    fi
    
    echo -e "\n${CYAN}2. Verificando Git...${NC}"
    GIT_NAME=$(git config --global user.name)
    GIT_EMAIL=$(git config --global user.email)
    
    if [ -n "$GIT_NAME" ] && [ -n "$GIT_EMAIL" ]; then
        print_success "Git configurado:"
        echo "   Nombre: $GIT_NAME"
        echo "   Email: $GIT_EMAIL"
    else
        print_warning "Git no está completamente configurado"
    fi
    
    echo -e "\n${CYAN}3. Verificando tokens...${NC}"
    if [ -f "$TOKEN_FILE" ]; then
        print_success "Archivo de tokens encontrado"
        echo "   Ubicación: $TOKEN_FILE"
        
        # Verificar permisos
        PERMS=$(stat -c %a "$TOKEN_FILE")
        if [ "$PERMS" = "600" ]; then
            print_success "Permisos correctos (600)"
        else
            print_warning "Permisos incorrectos: $PERMS"
        fi
    else
        print_warning "Archivo de tokens no encontrado"
    fi
    
    echo -e "\n${CYAN}4. Verificando .env...${NC}"
    if [ -f "$ENV_FILE" ]; then
        print_success "Archivo .env encontrado"
        
        # Verificar variables críticas
        if grep -q "^SECRET_KEY=" "$ENV_FILE"; then
            print_success "SECRET_KEY configurada"
        else
            print_warning "SECRET_KEY no encontrada"
        fi
        
        if grep -q "^API_KEY=" "$ENV_FILE"; then
            print_success "API_KEY configurada"
        else
            print_warning "API_KEY no encontrada"
        fi
    else
        print_warning "Archivo .env no encontrado"
    fi
    
    echo -e "\n${CYAN}5. Verificando repositorio...${NC}"
    if [ -d .git ]; then
        print_success "Repositorio Git inicializado"
        
        REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
        if [ -n "$REMOTE" ]; then
            print_success "Remoto configurado: $REMOTE"
        else
            print_warning "No hay remoto configurado"
        fi
        
        BRANCH=$(git branch --show-current)
        print_info "Rama actual: $BRANCH"
    else
        print_warning "No es un repositorio Git"
    fi
    
    echo ""
    print_success "Verificación completada"
}

# =================================================================
# 5. BACKUP DE CREDENCIALES
# =================================================================

backup_credentials() {
    print_header "Backup de Credenciales"
    
    BACKUP_DIR="$HOME/.heliobio/backups"
    mkdir -p "$BACKUP_DIR"
    chmod 700 "$BACKUP_DIR"
    
    BACKUP_FILE="$BACKUP_DIR/credentials_backup_$(date +%Y%m%d_%H%M%S).tar.gz"
    
    print_info "Creando backup..."
    
    tar -czf "$BACKUP_FILE" \
        -C "$HOME" \
        ".ssh/$SSH_KEY_NAME" \
        ".ssh/$SSH_KEY_NAME.pub" \
        ".ssh/config" \
        ".heliobio/credentials" \
        2>/dev/null
    
    if [ -f "$(pwd)/$ENV_FILE" ]; then
        tar -rzf "$BACKUP_FILE" -C "$(pwd)" "$ENV_FILE" 2>/dev/null
    fi
    
    chmod 600 "$BACKUP_FILE"
    
    print_success "Backup creado: $BACKUP_FILE"
    echo "   Tamaño: $(du -h "$BACKUP_FILE" | cut -f1)"
    
    # Limpiar backups antiguos (mantener últimos 5)
    print_info "Limpiando backups antiguos..."
    ls -t "$BACKUP_DIR"/credentials_backup_*.tar.gz | tail -n +6 | xargs -r rm
    
    print_success "Backup completado"
}

# =================================================================
# 6. CONFIGURACIÓN COMPLETA
# =================================================================

full_configuration() {
    print_header "Configuración Completa"
    
    echo "Esta opción ejecutará todas las configuraciones:"
    echo "1. SSH Keys"
    echo "2. Tokens"
    echo "3. Credenciales de aplicación"
    echo "4. Verificación"
    echo "5. Backup"
    echo ""
    read -p "¿Desea continuar? (s/n): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        return 0
    fi
    
    configure_ssh_keys
    echo ""
    generate_tokens
    echo ""
    configure_app_credentials
    echo ""
    verify_configuration
    echo ""
    backup_credentials
    
    print_header "Configuración Completa Finalizada"
    print_success "Todas las configuraciones han sido aplicadas"
}

# =================================================================
# MENÚ PRINCIPAL
# =================================================================

while true; do
    show_menu
    read option
    
    case $option in
        1)
            configure_ssh_keys
            ;;
        2)
            generate_tokens
            ;;
        3)
            configure_app_credentials
            ;;
        4)
            verify_configuration
            ;;
        5)
            backup_credentials
            ;;
        6)
            full_configuration
            ;;
        0)
            echo ""
            print_success "¡Hasta pronto!"
            exit 0
            ;;
        *)
            print_error "Opción inválida"
            ;;
    esac
    
    echo ""
    read -p "Presiona Enter para continuar..."
done
