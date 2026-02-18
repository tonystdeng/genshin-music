# git init
# git branch -M main
# git remote add origin <link>
# git remote -v

# git fetch origin
# git checkout origin/main -- .


git rm --cached -r .
git add .
git commit -m "${*:-auto commit idk why i\'m just a script named git.bash trying to do my job bruh}"

git push -u origin main