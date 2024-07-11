mkdir -p ~/.ssh/
rm -f ~/.ssh/config
echo "Host github.com" >> ~/.ssh/config
echo "    HostName github.com" >> ~/.ssh/config
echo "    StrictHostKeyChecking no" >> ~/.ssh/config
echo "    IdentityFile ~/.ssh/id_rsa" >> ~/.ssh/config
chmod 600 ~/.ssh/config
eval $(ssh-agent)
ssh-add ~/path_to_private_key
ssh -T git@atc-github.azure.cloud.bmw
