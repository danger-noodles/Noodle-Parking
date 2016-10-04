# gitflow

## Branches
### Master
This branche contains the latest working (stable) code and is the branche that will be submitted.

### Dev
This branche is for development and contains the latest working development code,
since this is a school project and we do not really have a production environment
this branche will probably be the same as the master branche.

### Feature
These branches are named after the feature that is being developed. We should have
the following branches (names might change):
 + Licence_plate
 + Database
 + RDW_api
 + GUI
 + Extra

## cheat sheet

| Git command                    | Function                | Example                        |
| ------------------------------ | ----------------------- | ------------------------------ |
| git status                     | Get status              | git status                     |
| git add path + filename        | Add file to commit      | git add RDW/apiclient.py       |
| git commit -m""                | Commit files            | git commit -m"Added apiclient  |
| git checkout brancheName       | Switch to branch        | git checkout -b RDW_api        |
| git push origin brancheName    | Push commits to github  | git commit push origin RDW_api |
