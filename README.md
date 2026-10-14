# LotLens — Quality Drift Investigator

LotLens is a prototype for detecting sustained quality drift in manufacturing inspection data. It compares a defect-rate series with a stable baseline, identifies an affected batch when the change persists, and supports a human-led investigation with evidence and synthetic operating-procedure excerpts.

## Run locally

Requires Python 3.11 or newer.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

## Run in a container

```powershell
docker build -t lotlens .
docker run --rm -p 8501:8501 lotlens
```

The application can start without `.env` or AMD credentials; the deterministic sample-data workflow remains available. To use the local AMD settings after the API key is available:

```powershell
docker run --rm -p 8501:8501 --env-file .env lotlens
```

For a hosted deployment, configure the AMD endpoint, model name, and API key through the host's environment/secret settings rather than adding `.env` to the image. See the [deployment guide](docs/Deployment%20Guide.md) for the container contract, host requirements, and release sequence.

The selected hosting target is Streamlit Community Cloud. Its deployment uses the GitHub repository directly; add the AMD settings as Streamlit app secrets rather than uploading `.env`. See the Streamlit section in the deployment guide.

The app opens with a clearly labeled synthetic sample scenario. Choose either **Seeded drift** or **Stable process** to view both alert and no-alert cases, or select **Upload CSV** to use another dataset; the required schema is described below.

The sample fields, units, generation pattern, and limits of interpretation are documented in [the synthetic data dictionary](data/DATA_DICTIONARY.md).

## AMD-backed AI brief

The detector and charts remain available while credentials are absent, but the final hackathon demo includes the AMD-backed investigation brief. To enable it locally:

1. For a fresh local checkout, copy `.env.example` to `.env`. If `.env` already exists, keep it and preserve its endpoint/model settings.
2. Add the API key shown in AMD Token Factory to `AMD_API_KEY` in `.env`. The adapter uses AMD's documented OpenAI-compatible Chat Completions request and response shape.
3. If the app is already open, select **Reload AMD settings from .env** in the sidebar. Otherwise, launch or rerun the app. With all three settings present, **Generate investigation brief** becomes available automatically.

Never commit `.env` or real credentials. The model receives calculated findings and synthetic procedure excerpts; it does not determine the alert or take an operational action.

## CSV schema

Required columns:

```text
timestamp,line_id,batch_id,shift,temperature_c,vibration_mm_s,pressure_bar,units_inspected,defect_count,operator_note
```

Timestamps must parse, numeric readings must be finite, `units_inspected` must be a positive whole-number count, and `defect_count` must be a whole number between zero and `units_inspected`. Each uploaded analysis must contain one `line_id` and at least 12 rows so the app can form a baseline and monitored period. Use synthetic or non-sensitive data in the hackathon demo.

## Detection rule

The first 60% of timestamp-sorted readings form the baseline. LotLens computes the mean defect rate and population standard deviation for that interval. The threshold is:

```text
baseline mean + max(3 × baseline standard deviation, 2 percentage points)
```

The app raises a drift alert after three consecutive monitored readings exceed that threshold. It records the first crossing as the onset and the third reading as the confirmation time. This is a transparent demo rule, not an industrially validated quality-control method.

## Project documentation

- [Project brief and phased build plan](docs/LotLens%20--%20Project%20Brief%20and%20Build%20Plan.md)
- [Phase completion checklist and required user inputs](docs/LotLens%20--%20Completion%20Checklist.md)
- [Manual verification steps and results log](docs/LotLens%20--%20Manual%20Verification%20Guide.md)
- [Deployment guide and host requirements](docs/Deployment%20Guide.md)
- [Submission copy and pitch outline draft](docs/LotLens%20--%20Submission%20and%20Pitch%20Draft.md)
- [Visual identity and color system](docs/LotLens%20--%20Visual%20Identity%20%26%20Color%20System.md)
- [Logo identity and creative direction](docs/LotLens%20--%20Logo%20Identity%20%26%20Creative%20Direction.md)
- [AMD ACT III event page](https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-iii)

