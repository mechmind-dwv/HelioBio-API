#!/bin/bash
echo "========================================="
echo "  Construyendo APK de HelioBio-API v3.0"
echo "========================================="

# Requisitos: Java JDK 17+, Android SDK, Python 3.10+

# Instalar Briefcase
pip install briefcase

# Crear proyecto Android
briefcase create android

# Construir APK
briefcase build android

# La APK estará en:
echo "APK generada en: android/gradle/app/build/outputs/apk/debug/"
