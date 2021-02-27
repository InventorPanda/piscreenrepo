
cd /home/pi/piscreenrepo
echo Checking local repository
git status
echo Refreshing Git
git fetch
echo Downloading changes
git merge --no-verify
