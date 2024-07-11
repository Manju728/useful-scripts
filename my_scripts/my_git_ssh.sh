eval "$(ssh-agent -s)"
ssh-add /home/mareedu/my_git_ssh
ssh -T git@github.com
