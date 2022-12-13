# File organization and Git configuration of this project

![Hierarchy of git repos for this project](https://github.com/aldatubio/opentrons/blob/main/dev/git_setup.jpg?raw=true)

- Bare remote hub exists at on Github - use as cloud storage
- Local for edits exists on OP13 LL's PC - use for script development (push/pull from here)
- Local for file viewing exists in L drive - use for locally running Opentrons scripts (pull from here)
  - L drive repository supports push requests, but this is not advised to reduce conflicts between repositories

Accessing each of these repositories in Git Bash:
- Github: `https://github.com/aldatubio/opentrons.git`
- OP13 LL Local: `c/Users/lucy/opentrons/opentrons`
- L drive: `//10.225.40.23/lab/OPENTRONS/codedump/opentrons`

After major updates, ensure that all repositories are "caught up" with each other.
- Local edits: `git push` to Github
- Github edits: `git fetch` followed by `git pull` on *both* local repos
