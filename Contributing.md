# Contributing

## Stories/Issues
Head over to the Jira instance and create a user story. Ensure that it follows the format:

> As a **type**, I want **feature/implementation**, so that **result**.

Typically, stories are either feature requests or bug requests.

### Bug Requests
For bugs, please include system information, relevant logs, and recreation steps. This ensures a smooth diagnosis of the bug.

### Features
For features, please be very specific on what you want and value proposition (what it brings to the application).

## Pull Requests
Github Pull Requests are the defacto way to make a code contribution. For internal branches, they must have a name of HSA-XXX, where XXX is the Jira story issue number. This keeps our branches organized for housekeeping.

### Basic Requirements
Creation:
- This PR **specifically** targets an issue mentioned in Jira. If not, create a story beforehand.
- If you changed the instructions to run the code (the old way doesn't work), there is a new step of instructions for a human to test your implementation.
- You have tagged this PR with as specific tags as possible.

Coding Style:
- Pull Requests **should** be of a reasonable size. If it changes many files or contains a large number of modifications, it is either justified in the description (e.g, some boilerplate installation) or split into smaller PRs.
- Code **ideally** should follow style guidelines and maintain high readability. This will speed up code review process.

Non-Feature Updates:
- Documentation should be updated if this PR invalidates previous documentation.
- Rigourous tests are be implemented for the changes or an explanation is provided on why they are not relevant.

Formatting:
- The title of the PR **must** be formatted as ```HSA-XXX description```.
- All commits should **ideally** be formatted as ```HSA-XXX description```.
- If the commit log is messy, the commits will be squashed.

### Additional information
- For frontend changes, we **highly recommend** including screenshots of what you have visually changed.
- For any database changes, we **require** information on what has changed in the schema as well as the "requires | migrations" tag.
- For any running/test command changes, we **require** information on how this has changed as well as the "requires | CICD" tag.

