# READ ME (or don't I'm not a cop)

## Merge changes from a branch

```
(make sure you're in your branch first. If not then run: git checkout < your-branch >)

git status [make sure you see a message like "Your branch is up to date with 'origin/< your-branch >' ". If it doesn't then run 'git pull']

git merge origin/< branch-to-merge-with > (it may open a file asking you to add a message explaining the merge. Just add whatever then save and exit. It might also say 'use git commit' to complete merge, in which case run: git commit -m '<your message here> )

(you should see some kind of message saying you've merged with the branch)

git add .

git commit -m "your message here"

git push


```
