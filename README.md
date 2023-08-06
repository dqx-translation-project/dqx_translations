# dqx_translations

Files in this repository are hosted and maintained in Weblate.

An attempt is made to avoid doing anything directly in the UI and instead, accessing Weblate with its management commands for ease of administration.

## How is this set up?

Instance is hosted in Docker. You will need a general understanding of how Docker works to stand up this installation.

Not discussed in this documentation is the configuration of a reverse proxy in front of the Docker container for secure access to the web UI. I'm hosting it this way, but you are free to present the web UI in whatever fashion you desire. As a reference, the proxy is configured to process requests as documented in the [Weblate documentation](https://docs.weblate.org/en/latest/admin/install/docker.html#docker-container-with-https-support).

Create a local `.env` file that references all of the environment variables in the `docker-compose.override.yml` file and fill in the appropriate values for each section. You can also create this file from the `.env_example` and fill in the values. You can reference [the Weblate documentation](https://docs.weblate.orgest/admin/install/docker.html) for details on what each of these environment variables does. Once finished, stand up the Weblate instance:

```
docker-compose up -d 
```

Watch the logs with:

```
docker logs weblate -f
```

## Providing Weblate access to GitHub

You will need to add the Weblate public key to the GitHub repository to allow Weblate to push commits to the repo. Only the owner of the repository can configure deployment keys.

Logged in as an admin in the Weblate UI:

- Go to the home page
- Click the wrench in the top right
- Click on "SSH keys"
- Copy the `ssh-rsa` SSH key

In the GitHub repository:

- Click on "Settings"
- Under Security, click on "Deploy keys"
- Give the key a name and paste the public key into the "key" field
- Check "Allow write access" and save

## Getting admin's API token

As we want this installation to be as scriptable as possible, we want to stick to CLI commands wherever we can. Some of the commands run below will use requests to Weblate's REST API. You will need to grab an authorization token for the Admin account configured for your instance that will be used periodically throughout this documentation.

While logged into the Admin account:

- Click on your avatar in the top-right
- Click "Settings"
- Click on the "API access" tab
- Copy your personal API key

## Setting environment variables for below commands

I recommend exporting the below variables (and configuring them) as some of the below commands will be using these throughout the documentation:

```bash
# `WEBLATE_HOST` is the HTTP/HTTPS URL of your Weblate instance. This will be different depending on how you have hosted it
# Example: "http://10.10.10.150" or "https://weblate.mydomain.com"

export WEBLATE_API_KEY="your_api_key"
export WEBLATE_HOST="your_weblate_host"
```

## Adding a new project

```bash
curl -XPOST ${WEBLATE_HOST}/api/projects/ \
   --header "Content-Type: application/json" \
   --header "Authorization: Token ${WEBLATE_API_KEY}" \
   --data '{"name": "dqx", "slug": "dqx", "web": "https://github.com/dqxtranslationproject/dqx_translations"}'
```

## Adding the management component

You will want a single component called "dummy" that will be used as the management component. Addons will be installed on this component and will traverse to all child components.

```bash
curl -XPOST ${WEBLATE_HOST}/api/projects/dqx/components/ \
    --header "Content-Type: application/json" \
    --header "Authorization: Token ${WEBLATE_API_KEY}" \
    --data-binary '{
        "name": "dummy",
        "slug": "dummy",
        "vcs": "git-force-push",
        "repo": "https://github.com/dqxtranslationproject/dqx_translations",
        "branch": "main",
        "push_branch": "main",
        "filemask": "json/_lang/*/.dummy.json",
        "template": "json/_lang/ja/.dummy.json",
        "edit_template": "no",
        "file_format": "json-nested",
        "new_lang": "none",
        "source_language": "ja",
        "push": "git@github.com:dqxtranslationproject/dqx_translations.git",
        "merge_style": "rebase",
        "commit_message": "Translation",
        "add_message": "Added new translation",
        "delete_message": "Deleted translation",
        "merge_message": "Merging branch {{ component_remote_branch }}",
        "addon_message": "{{ addon_name }} has made an update",
        "allow_translation_propagation": "yes",
        "enable_suggestions": "no",
        "suggestion_voting": "no",
        "suggestion_autoaccept": "0",
        "push_on_commit": "yes",
        "commit_pending_age": "1",
        "auto_lock_error": "no",
        "language_regex": "^(en)$"
    }'
```

## Configuring JSON indenting

The translation files use an indent of 2. We need to tell Weblate this so it doesn't try to reformat the existing translation files. Install the add-on on the dummy component:

```bash
docker-compose exec --user weblate weblate \
   weblate \
   install_addon \
   dqx/dummy \
   --addon weblate.json.customize \
   --update \
   --configuration '{"indent": 2, "style": "spaces"}'
```

## Squashing git commits

By default, each change to a file is a "commit", which can flood the git history very quickly. Install the "Squash Git commits" addon to fix this. We use "by author" to make sure we can still see who's making the change, but their changes are consolidated.

```bash
docker-compose exec --user weblate weblate \
   weblate \
   install_addon \
   dqx/dummy \
   --addon weblate.git.squash \
   --update \
   --configuration '{"squash": "author"}'
```

## How do you add new components?

This is done with an add-on called `Component discovery`, configured on the main `dummy` component. This add-on will automatically create a new component when a new file is detected in the translation directories. For our use case, we only want to pull in English files of `json` type. If a file has been removed from the repository, component discovery will automatically remove the component from Weblate on its next check of the VCS.

```bash
docker-compose exec --user weblate weblate \
   weblate \
   install_addon \
   dqx/dummy \
   --addon weblate.discovery.discovery \
   --update \
   --configuration '{"match": "json/_lang/(?P<language>[^/.]*)/(?P<component>[^/]*)\\.json", "file_format": "json-nested", "base_file_template": "json/_lang/ja/{{component}}.json", "new_base_template": "", "intermediate_template": "", "name_template": "{{component}}.json", "language_regex": "^(en)$", "copy_addons": "on", "remove": "on", "confirm": ""}'
```

## Creating users

You can choose to do this in the UI, or make a request for each new user.

Fill out the username, full_name and email fields.

```bash
curl -XPOST ${WEBLATE_HOST}/api/users/ \
    --header "Content-Type: application/json" \
    --header "Authorization: Token ${WEBLATE_API_KEY}" \
    --data-binary '{
       "username": "",
       "full_name": "",
       "email": ""
    }'
```

## Completion

As the number of components being created is large, it will take an hour or two for the Weblate instance to process through all of the tasks in the celery queue. Be patient and let Weblate complete this work before making any changes.

From here, you should have a functioning Weblate instance. Add users and let them contribute to your project.
