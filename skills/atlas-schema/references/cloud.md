# Atlas-Schema - Cloud

**Pages:** 2

---

## Set Up CI for Your Database with Atlas

**URL:** https://atlasgo.io/cloud/setup-ci

**Contents:**
- Set Up CI for Your Database with Atlas
- Prerequisites​
- GitHub Action Workflow​
  - Step 1: Create a Bot Token for Atlas Cloud​
  - Step 2: Install the Atlas GitHub CLI Extension​
  - Step 3: Configure the GitHub Action​
  - Step 4: Test the Action​
- Summary​

As your application evolves, so does your database schema. If you're not careful with schema changes (migrations), you can end up introducing all sorts of issues that are painful and expensive to fix.

To mitigate the risk of deploying dangerous changes to database schemas, many teams apply CI/CD practices to their database. This means that every change to the database schema is automatically reviewed and tested before it is deployed to production.

In this guide, we'll show you how to set up CI for your database using Atlas Cloud and GitHub Actions.

A similar workflow is supported on other CI platforms as well. To learn more, see the Azure DevOps with GitHub, Azure DevOps with Azure Repos, GitLab CI, CircleCI, and Bitbucket Pipes guides.

Push your migration directory to Atlas Cloud. This is used by the CI process to detect which migration files are new and if linear history is maintained:

In order to report the results of your CI runs to Atlas Cloud, you will need to create a bot token for Atlas Cloud to use. Follow these instructions to create a token and save it somewhere safe.

To streamline the process of configuring the GitHub Action, we've created a GitHub CLI extension that will do most of the work for you:

Make sure you have the GitHub CLI installed.

See here for more installation options.

Install the Atlas GitHub CLI extension:

Atlas will scan your repository (locally) for directories containing Atlas migrations and ask you which one you would like to use for CI. Select the desired directory and press "Enter":

Atlas will then ask you which database driver this directory contains migrations for. Select the desired driver and press "Enter":

Next, the GitHub extension will save your bot token to a GitHub secret and create a pull request with the necessary configuration for the GitHub Action.

The PR contains a GitHub Actions workflow similar to this:

After reviewing the changes, merge the pull request to enable the GitHub Action.

After merging the pull request, the GitHub Action will run atlas migrate lint on every pull request and sync the migrations to Atlas Cloud on every push to master.

(Notice that we're missing the TABLE keyword in the CREATE TABLE statement.)

Our changes are pushed to GitHub:

The linting run failed because of the syntax error we introduced in the migration file.

In this guide, we've shown how to configure Atlas Cloud to apply continuous integration for our database schema changes. With this setup, whenever a developer proposes a change to the database schema, Atlas Cloud will verify the safety of the change using various checks and report back the results.

**Examples:**

Example 1 (shell):
```shell
$ atlas loginYou are now connected to "a8m" on Atlas Cloud.
```

Example 2 (bash):
```bash
atlas migrate push app \  --dev-url "docker://postgres/15/dev?search_path=public"
```

Example 3 (bash):
```bash
atlas migrate push app \  --dev-url "docker://mysql/8/dev"
```

Example 4 (bash):
```bash
atlas migrate push app \  --dev-url "docker://mariadb/latest/dev"
```

---

## Reporting schema migrations to Atlas Cloud

**URL:** https://atlasgo.io/cloud/deployment

**Contents:**
- Reporting schema migrations to Atlas Cloud
  - Deploying without Atlas Cloud​
  - Why deploy from Atlas Cloud?​
  - Report Migrations to Atlas Cloud​
  - Visualizing Migration Runs​

A common way to deploy migrations using Atlas (or any other migration tool) is similar to this:

This process is a common practice, but it requires setting up a CI/CD pipeline (including storage, permissions, and other glue) for each service, adding another layer of complexity.

Atlas Cloud streamlines deploying migrations by providing a single place to manage migrations for all your services. After connecting your migration directory to Atlas Cloud, it is automatically synced to a central location on every commit to your main branch. Once this setup (which takes less than one minute) is complete, you can deploy migrations from Atlas Cloud to any environment with a single command (or using popular CD tools such as Kubernetes and Terraform).

To read the migration directory from the Atlas Registry, use the atlas:// scheme in the migration URL as follows:

Now you can execute schema migrations and report their result to Atlas Cloud using the following command:

If you set up CI for your project to push the migration directory to Atlas Cloud, you can deploy a specific migration tag by setting the tag query string in the directory URL. For example:

Schema migrations are an integral part of application deployments, yet the setup might vary between different applications and teams. Some teams may prefer using init-containers, while others run migrations from a structured CD pipeline. There are also those who opt for Helm upgrade hooks or use our Kubernetes operator. The differences also apply to databases. Some applications work with one database, while others manage multiple databases, often seen in multi-tenant applications.

However, across all these scenarios, there's a shared need for a single place to view and track the progress of executed schema migrations. This includes triggering alerts and providing the means to troubleshoot and manage recovery if problems arise.

When you use the configuration above with a valid token, Atlas will log migration runs in your cloud account. Here's a demonstration of how it looks in action:

**Examples:**

Example 1 (unknown):
```unknown
env {  // Set environment name dynamically based on --env value.  name = atlas.env  migration {    // In this example, the directory is named "myapp".    dir = "atlas://myapp"  }}
```

Example 2 (shell):
```shell
export ATLAS_TOKEN="<ATLAS_TOKEN>"atlas migrate apply \  --url "<DATABASE_URL>" \  --config file://path/to/atlas.hcl \  --env prod
```

Example 3 (shell):
```shell
# Short SHA-1 hash.--dir "atlas://myapp?tag=267b9d1"# Full tag.--dir "atlas://myapp?tag=267b9d1799a3f37ccc0c4112d33f6b3455b62de8"
```

---
