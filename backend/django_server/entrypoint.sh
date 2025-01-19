# Run Django server and some bash magic for OpenVPN
bash -c 'openvpn --config ./UTH_Network.ovpn --auth-user-pass <(echo -e "'"$UTH_USERNAME"'\n'"$UTH_PASSWORD"'")' --auth-nocache &
python3 manage.py runserver 0.0.0.0:9000
