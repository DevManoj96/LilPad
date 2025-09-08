#!/bin/bash

echo "Setting up directories..."
sudo mkdir -p /usr/local/bin/lilpad
sudo mkdir -p /usr/share/applications
sudo mkdir -p /usr/share/icons/hicolor/48x48/apps

echo "Copying application files..."
sudo cp lilpad.py /usr/local/bin/lilpad/lilpad.py
sudo cp logo.png /usr/local/bin/lilpad/

echo "Creating executable command..."
echo '#!/bin/bash' | sudo tee /usr/bin/lilpad
echo 'python3 /usr/local/bin/lilpad/lilpad.py' | sudo tee -a /usr/bin/lilpad
sudo chmod +x /usr/bin/lilpad

echo "Creating desktop entry..."
cat <<EOL | sudo tee /usr/share/applications/lilpad.desktop
[Desktop Entry]
Version=1.0
Name=Lilpad
Exec=lilpad
Icon=/usr/local/bin/lilpad/logo.png
Type=Application
Categories=TextEditor;
Terminal=false
EOL

echo "Copying application icon..."
sudo cp logo.png /usr/share/icons/hicolor/48x48/apps/logo.png

echo "Lilpad has been installed!, Run by typing lilpad in the terminal.