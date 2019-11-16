#!/usr/bin/env bash

git clone https://github.com/StackExchange/blackbox.git
cd blackbox
cd ..
echo "Importing key"
echo -e "$PGP_PRIVATE_KEY_HEROKU" | gpg --import
./blackbox/bin/blackbox_postdeploy