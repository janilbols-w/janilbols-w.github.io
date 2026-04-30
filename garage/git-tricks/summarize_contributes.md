# HOW TO SUMMARIZE YOUR CONTRIBUTION IN A GIT PROJECT
```bash
git log --author="<contributor-name>" --pretty=tformat: --numstat | \
    awk '{ add += $1; subs += $2; loc += $1 + $2 } END { printf "increase lines: %s\ndelete lines: %s\ntotal lines: %s\n", add, subs, loc }'
```


```
# e.g. output
increase lines: 4015
delete lines: 2015
total lines: 6030
```