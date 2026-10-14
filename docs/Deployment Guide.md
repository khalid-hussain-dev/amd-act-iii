# LotLens — Deployment Guide

This guide documents the Streamlit app deployment. Streamlit Community Cloud is the current host; the Docker container instructions remain available for local use or a later host. The user reports that the public app and AMD-generated brief were manually reviewed successfully on 14 October 2026. See the [Manual Verification Guide](LotLens%20--%20Manual%20Verification%20Guide.md) for the hosted review record.

## Container contract

- Build context: project root.
- Build command: `docker build -t lotlens .`
- Start command: the `Dockerfile` starts Streamlit on `0.0.0.0` and reads the port from `PORT`, defaulting to `8501`.
- Required runtime: Python 3.11 container support and outbound HTTPS access to the configured AMD chat-completions endpoint.
- Persistent storage: none. Uploaded CSVs and analysis state are held for the active Streamlit session; they are not saved as a durable dataset.
- Credentials: configure all three runtime variables in the host's environment or secret manager:

  | Variable | Value |
  | --- | --- |
  | `AMD_CHAT_COMPLETIONS_URL` | The team's AMD Token Factory Chat Completions endpoint. |
  | `AMD_MODEL_NAME` | The exact model identifier enabled for the team. |
  | `AMD_API_KEY` | The secret key for that model. |

Do not bake credentials into the image, Dockerfile, repository, or build arguments. Keep `.env` out of the deployment artifact. `.dockerignore` already excludes it.

## Local container with AMD access

To run the container locally with AMD settings after the API key has been added to the ignored `.env` file:

```powershell
docker build -t lotlens .
docker run --rm -p 8501:8501 --env-file .env lotlens
```

This command is for local use only. On a public host, set the same variables through its runtime environment or secret manager. Do not upload `.env` as a source file or image layer.

## Streamlit Community Cloud

Streamlit Community Cloud is the selected free hosting option for the current Streamlit app. It deploys from the public GitHub repository and does not use this project's Dockerfile. In the app's advanced settings, select Python 3.11 or a supported version and set the AMD values in the **Secrets** field as flat TOML entries:

```toml
AMD_CHAT_COMPLETIONS_URL = "https://your-amd-chat-completions-endpoint"
AMD_MODEL_NAME = "your-enabled-model-name"
AMD_API_KEY = "your-secret-key"
```

Use the exact URL and model name from the team's AMD account. Never commit `.streamlit/secrets.toml` or paste the API key into project documentation. The app reads these values from `st.secrets` on Community Cloud; explicit host environment variables take precedence, and local `.env` remains supported for development.

Community Cloud may hibernate an app after inactivity. Open the public app before the demo and allow time for it to wake. After deployment, review the hosted build and confirm it can make the outbound AMD request. See the official [deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy) and [secrets guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management).

## Host requirements

Before choosing a provider, confirm that it:

1. Runs the project Dockerfile and honors the assigned `PORT` environment variable.
2. Provides HTTPS to judges and keeps the app available for the event's judging period.
3. Allows outbound HTTPS requests to the AMD endpoint from the running container.
4. Supports runtime secrets or protected environment variables.
5. Provides enough memory and request time for Streamlit plus a model call that can take up to 45 seconds.
6. Allows unauthenticated judge access if the submission requires a public demo URL.

## Release sequence

1. Select the hosting provider and create the public service from the project root.
2. Configure the runtime secrets above and the host-provided port setting. Keep credentials out of build logs and deployment notes.
3. Deploy the container and open the public URL in a clean browser session.
4. After deployment, manually review both sample scenarios, the CSV path, and the investigation brief on the hosted build. The user reports completing the hosted review successfully; repeat relevant checks after material changes and confirm that errors preserve the calculated analysis.
5. Confirm that uploaded data is synthetic or non-sensitive, and that the demo makes its synthetic procedure excerpts clear.
6. Record the public URL, deployment revision, and manual review outcome in the completion checklist. Current public URL: [https://lotlens.streamlit.app/](https://lotlens.streamlit.app/).
7. Publish the source repository only after reviewing the staged files for credentials and private data.

## Deployment handoff

The public repository has been pushed and the app is live at [https://lotlens.streamlit.app/](https://lotlens.streamlit.app/). The user reports a successful hosted review, including generation of an AMD investigation brief. Codex has not independently checked the account settings or repeated the hosted review.
